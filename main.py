import glob
from helpers.sql_manager import SQLManager
from helpers.util import *
from io import StringIO
import logging
import pandas as pd
from ro.parser import Parser
from ro.event import Event as RO
from typing import Dict, List
import xml.dom.minidom


def read_files_from_dir(dir: str) -> List[str]:
    """
    Reads files from a directory and returns their contents in a list.
    :param dir: directory to read files from
    :return: Contents of the file
    """

    log = logging.getLogger("read_files_from_dir")
    xml_data = []

    for file_name in sorted(glob.glob(f"{dir}/*.xml")):
        log.info(f"Reading {file_name}")
        with open(file_name) as f:
            contents = f.read()

            try:
                # Add in the file name for debugging
                contents = contents.replace("</event>", f"\t<file_name>{file_name}</file_name>\n</event>")

                # Simple way to validate that the XML was well-formed.
                # Improvement Idea: Validate that the expected elements are present
                xml.dom.minidom.parseString(contents)
                xml_data.append(contents)
            except Exception as ex:
                log.error(f"Error parsing {file_name}\n\t{ex}")

    return xml_data


def parse_xml(files: List[str]) -> pd.DataFrame:
    """
    Parses the XML contents into a flattened Pandas DataFrame.
    Note: we didn't do any special logic for the parts, so I probably didn't need
    to flatten the files.
    :param files: List of XML strings read from files
    :return: Flattened Pandas Dataframe
    """

    log = logging.getLogger("parse_xml")

    # XML template
    xslt = """
        <xsl:stylesheet version="1.0" 
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:edgar="http://www.sec.gov/edgar/nport">
        <xsl:output method="xml" indent="yes" />
        <xsl:strip-space elements="*"/>
        <xsl:template match="/">
            <xsl:for-each select="event">
                <xsl:variable name="file_name" select="file_name"/>
                <xsl:variable name="order_id" select="order_id"/>
                <xsl:variable name="date_time" select="date_time"/>
                <xsl:variable name="status" select="status"/>
                <xsl:variable name="cost" select="cost"/>
                <xsl:for-each select="repair_details">
                    <xsl:variable name="technician" select="technician"/>
                    <xsl:for-each select="repair_parts/part">
                        <event>
                        <file_name><xsl:value-of select="$file_name"/></file_name>
                        <order_id><xsl:value-of select="$order_id"/></order_id>
                        <date_time><xsl:value-of select="$date_time"/></date_time>
                        <status><xsl:value-of select="$status"/></status>
                        <cost><xsl:value-of select="$cost"/></cost>
                        <technician><xsl:value-of select="$technician"/></technician>
                        <part_name><xsl:value-of select="@name"/></part_name>
                        <part_quantity><xsl:value-of select="@quantity"/></part_quantity>
                        </event>
                    </xsl:for-each>
                </xsl:for-each>
        </xsl:for-each>
      </xsl:template>
    </xsl:stylesheet>
    """

    dfs = []
    for file in files:
        dfs.append(pd.read_xml(StringIO(file), stylesheet=xslt, xpath="//event"))

    df = pd.concat(dfs)
    df["date_time"] = pd.to_datetime(df["date_time"])

    # When resetting the index, the old index becomes a column named "index"
    # since we appended a bunch of data01 frames together, the index is the same as
    # line number for the file that was read.
    df = df.reset_index()
    df.rename(columns={"index": "part_row"}, inplace=True)
    df = df.sort_values(["date_time", "order_id", "part_row"])

    log.info(f"Events flattened to {len(df['order_id'])} rows")
    return df


def window_by_datetime(data: pd.DataFrame, window: str) -> Dict[str, pd.DataFrame]:
    """
    Groups the data01 by the specified window.
    This function will calculate the beginning of the time window, for example if the
    window is "1Y" then the start of th time window will be "2024-01-01 00:00:00" and the
    end will be one year from there, "2025-01-01 00:00:00". Only ROs from between
    "2024-01-01 00:00:00" and "2025-01-01 00:00:00" will be in the grouping of
    "2024-01-01 00:00:00".
    :param data: Flattened Pandas Dataframe containing RO events
    :param window: Format is like 5D or 1W
        Valid partitions are:
        H: Hour
        D: Day
        W: Week
        M: Month
        Y: Year
    :return: Dictionary with the key being the beginning time part.
        For example, if the window is "1Y", the key will be "2024-01-01 00:00:00"
        or if window is "1D", the key will be "2024-05-25 00:00:00"
    """
    log = logging.getLogger("window_by_datetime")
    windows = {}
    if not data.items:
        return windows

    # set the time partition upper bound
    upper_relative_date = parse_window(window)
    key_end = datetime.fromtimestamp(0)
    prev_key = ""

    # Group data01 based on selected window
    # IRL, would split out the steps into separate functions to support unit testing and
    # follow the principle of "do one thing, and do it well"
    for i, (_, row) in enumerate(data.iterrows()):
        # check to see if we need to reset the keys
        if row["date_time"] >= key_end:
            # round down
            key_start = get_window_start(window, row["date_time"])
            key_end = key_start + upper_relative_date

            if prev_key:
                windows[str(prev_key)]["end"] = i

            windows[str(key_start)] = {"start": i, "end": len(data["order_id"])}
            prev_key = key_start

    log.info(f"Set the following windows: {str(list(windows.keys()))}")

    # select the latest values for selected window
    for key, value in windows.items():
        log.info(f"Parsing: {key} {value}")

        df: pd.DataFrame = data.iloc[value["start"]: value["end"]]

        # get the latest date_time for each order_id
        # we are assuming that 1) date_time is an unique identifier (two updates to an order
        # won't share the same date_time and 2) latest date_time wins
        df_latest = df[['order_id', 'date_time']].copy()
        df_latest = df_latest.drop_duplicates(["order_id"], keep='last')
        log.info(f"De-dupped keys:\n {df_latest}")

        # select only those rows that match the latest values
        df = df.merge(df_latest, on=['order_id', 'date_time'])

        windows[key] = df

    return windows


def process_to_RO(data: Dict[str, pd.DataFrame]) -> List[RO]:
    """
    Convert Pandas Dataframes to RO objects
    :param data: Pandas dataframe of RO
    :return: List of RO objects
    """
    log = logging.getLogger("process_to_RO")
    ro = []

    for window, rows in data.items():
        if ros := Parser.parse(rows):
            ro.extend(ros)

    log.info(f"ROs returned: {len(ro)}")

    return ro


def main() -> None:
    """
    Executes the script
    """

    # Setup logging
    # For the demo version, the log file is re-used and wipes the prior run.
    # In production, I would create a log folder and have the log file name be
    # the timestamp
    logging.basicConfig(filename="log.txt", level=logging.INFO, filemode="w")
    logging.info(f"Running {str(datetime.now())}")

    # "data" and "1D" should be configurable somehow such as a config file or execution params
    xml_data = read_files_from_dir("data")
    data = parse_xml(xml_data)
    data = window_by_datetime(data, '1D')
    data = process_to_RO(data)

    SQLManager.setup_db()
    SQLManager.write_db(data)


if __name__ == "__main__":
    main()
import pandas as pd
from ro.event import Event
from ro.repair_details import RepairDetails
from ro.repair_parts import RepairParts
from typing import List


class Parser:
    """
    Converts Pandas Dataframe to RO objects
    """

    @staticmethod
    def parse(data: pd.DataFrame) -> List[Event]:
        """
        Converts Pandas Dataframe to RO objects.
        :param data:
        :return: List of RO objects
        """

        ro = Event(None, None, None, None)
        repair_details = RepairDetails(None)
        events = []

        for i, row in data.iterrows():
            # Check to see if this is the same order or a new order
            if ro.order_id != row["order_id"] and ro.date_time != row["date_time"]:
                # cheating a bit here, IRL would validate keys exist in DataFrame
                # and explicity assign them
                ro = Event(**dict(row))
                events.append(ro)
                repair_details = RepairDetails(**dict(row))
                ro.repair_details.append(repair_details)

            repair_details.repair_parts.append(RepairParts(**dict(row)))

        return events

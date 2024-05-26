import sqlite3
from ro.event import Event as RO
from typing import List


class SQLManager:

    @staticmethod
    def setup_db():
        """
        Checks to see if database and table exists, if not it will create them
        :return: None
        """
        conn = sqlite3.connect("../ro.db")
        cur = conn.cursor()

        res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ro';")

        if not res.fetchone():
            cur.executescript("""
                CREATE TABLE ro (
                    order_id varchar(10),
                    date_time datetime,
                    status varchar(10),
                    cost decimal(10,2)
                );
                
                CREATE TABLE repair_details (
                    order_id varchar(10),
                    date_time datetime,
                    technician varchar(10)
                );               
                
                CREATE TABLE repair_parts (
                    order_id varchar(10),
                    date_time datetime,
                    name varchar(100),
                    quantity int,
                    row_num int
                );               
            """)

    @staticmethod
    def write_db(data: List[RO]):
        """
        Send RO values to the database
        :param data: List of RO objects
        :return:
        """
        conn = sqlite3.connect("../ro.db")
        cur = conn.cursor()

        # IRL, should make the string SQL insert safe (check for quotes within the strings
        # If it;'s going into a relational database, then I would setup referential integrity
        # and write data01 in transactions.
        # If it's going into a columnar database, then I would write out as larger files
        # and ingest those
        for ro in data:
            sql = "insert into ro(order_id, date_time, status, cost)\n"
            sql += f"values('{ro.order_id}', '{ro.date_time}', '{ro.status}', {ro.cost});\n\n"

            for rd in ro.repair_details:
                sql += "insert into repair_details(order_id, date_time, technician)\n"
                sql += f"values('{ro.order_id}', '{ro.date_time}', '{rd.technician}');\n\n"

                for rp in rd.repair_parts:
                    sql += "insert into repair_parts(order_id, date_time, name, quantity, row_num)\n"
                    sql += f"values('{ro.order_id}', '{ro.date_time}', '{rp.name}', {rp.quantity}, {rp.row_num});\n\n"


            cur.executescript(sql)

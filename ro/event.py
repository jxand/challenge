import datetime
from decimal import Decimal
from typing import Any, Dict, Tuple


class Event:
    """
    Repair Order Event
    The unique key is (order_id, date_time)
    """

    order_id = None
    date_time = None
    status = None
    cost = None
    repair_details = []

    def __init__(self,
                 order_id: int,
                 date_time: datetime,
                 status: str,
                 cost: Decimal,
                 *args: Tuple,
                 **kwargs: Dict[Any, Any]
                 ):
        self.order_id = order_id
        self.date_time = date_time
        self.status = status
        self.cost = cost
        self.repair_details = []

    def __str__(self):
        return str(
            {**self.__dict__, **{"repair_parts_qty": len(self.repair_details[0].repair_parts)}}
        )

    def __repr__(self):
        return self.__str__()
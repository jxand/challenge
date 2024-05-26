from typing import Any, Dict, Tuple


class RepairParts:
    """
    Repair Order Parts
    Each Repair Order Event may have one or more parts
    """
    row_num = None
    name = None
    quantity = None

    def __init__(self,
                 part_row: int,
                 part_name: str,
                 part_quantity: int,
                 *args: Tuple,
                 **kwargs: Dict[Any, Any]
                 ):
        self.row_num = part_row
        self.name = part_name
        self.quantity = part_quantity

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
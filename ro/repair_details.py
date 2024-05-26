from typing import Any, Dict, Tuple


class RepairDetails:
    """
    Repair Order Details
    """

    technician = None
    repair_parts = []

    def __init__(self, technician: str, *args: Tuple, **kwargs: Dict[Any, Any]):
        self.technician = technician
        self.repair_parts = []

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
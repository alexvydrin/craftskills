"""прототипы"""


import copy


class PrototypeMixin:  # pylint: disable=too-few-public-methods
    """прототип"""

    def clone(self):
        """Clone a registered object and update inner attributes dictionary"""
        return copy.deepcopy(self)

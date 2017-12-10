"""

.. module:: delay_function
    :synopsis: Contains all delay defined by user functions

.. moduleauthor: Israr Mahmood <im278@cornell.edu>

:Module: delay_function
:Author: Israr Mahmood <im278@cornell.edu>

"""


def delay(records):
    """Sample Delay Function

    :param records: Completed Evaluation Record
    :type records: EvalRecord

    :return: int
    """

    return 5 + 5 * (records.params[0] > 0.25)
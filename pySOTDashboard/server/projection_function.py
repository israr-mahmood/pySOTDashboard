"""

.. module:: projection_function
    :synopsis: Contains all projection defined by user functions

.. moduleauthor: Israr Mahmood <im278@cornell.edu>

:Module: projection_function
:Author: Israr Mahmood <im278@cornell.edu>

"""


import numpy as np


def projection(x):
	"""Sample Projection Function

	:param x: Input list
    :type x: int

    :return: Norm form of input list
    """

	return x / np.linalg.norm(x)
		
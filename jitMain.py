import numpy as np
from numba import njit
from numba.core import config

config.DISABLE_JIT = False


@njit
def multiply_matrices(matrix1, matrix2):
    result = np.dot(matrix1, matrix2)
    return result


@njit
def add_matrices(matrix1, matrix2):
    result = np.add(matrix1, matrix2)
    return result


@njit
def square_matrices(matrix1):
    result = np.square(matrix1)
    return result

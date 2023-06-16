import numpy as np

from helpers import measure_execution_time
measureTime = True


@measure_execution_time("multiply_matrices_timing.csv", measureTime)
def multiply_matrices(matrix1, matrix2):
    result = np.dot(matrix1, matrix2)
    return result


@measure_execution_time("add_matrices_timing.csv", measureTime)
def add_matrices(matrix1, matrix2):
    result = np.add(matrix1, matrix2)
    return result

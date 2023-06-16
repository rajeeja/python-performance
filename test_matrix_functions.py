import numpy as np
import matrix_functions as maf


def test_matrix_functions():
    # Test matrices
    matrix1 = np.random.rand(1000, 1000)
    matrix2 = np.random.rand(1000, 1000)

    # Test multiplication and addition functions
    result_multiply = maf.multiply_matrices(matrix1, matrix2)
    result_add = maf.add_matrices(matrix1, matrix2)

    # Find the expected results
    expected_result_multiply = np.matmul(matrix1, matrix2)
    expected_result_add = np.add(matrix1, matrix2)

    # Assert the results
    assert np.array_equal(result_multiply, expected_result_multiply)
    assert np.array_equal(result_add, expected_result_add)

import csv
import timeit
import os

from functools import wraps


def measure_execution_time(filename, measureTime):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not measureTime:
                return func(*args, **kwargs)

            # Get the average time function takes to run
            timing_data = timeit.repeat(lambda: func(*args, **kwargs), number=1, repeat=7)
            execution_time = sum(timing_data) / len(timing_data)

            # Check to see if the file exists
            is_file_exists = os.path.exists(filename)

            # Open a CSV file to record timing data
            with open(filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                # If the file doesn't exist, write the column names
                if not is_file_exists:
                    writer.writerow(["Function Name", "Execution Time (s)"])
                # Write to the CSV file
                writer.writerow([func.__name__, execution_time])

            return func(*args, **kwargs)

        return wrapper

    return decorator

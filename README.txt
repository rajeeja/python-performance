Simple example of how we might implement a timing feature for functions in UXarray.

The use of timeit allows an average run time of each function to be found. You can change how many times timeit runs
by changing the repeat variable. It takes the average time from that and prints it to a formatted CSV file for
convenient viewing and saving purposes. (taking the average time won't work actually because it adds time, which messes
up the other functions that called it previously, if you are timing multiple interconnected functions)

To time a function, just add the decorator @measure_execution_time("fileNameHere", measureTime). If measure time is set
to true, it will run the decorator and time the function. If it is false, operation will continue as normal and no
timing will be done.

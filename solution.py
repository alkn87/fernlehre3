#!/usr/bin/python3

"""
Author: A. Knapp // 2019

This script reads multiple .csv files, which consist of integer values.

Every value is multiplied by 2 by using the calc.sh file.

The result is appended to a new list, which will be sorted by using slowsort algorithm.

The slow sorted list will then be outputted to a new file with file name: min-max.csv

The script uses multithreading for speeding things up. The calc.sh file is a limited ressource
which cannot be used by more than 2 threads at once. This is handled by the use of a
bounded semaphore.
"""

import os
import threading

# Create global variable SEM to store semaphore object -> bounded semaphore, max 2 threads
SEM = threading.BoundedSemaphore(2)

def write_to_file(var_in_array):
    """
    This function takes an input list(array) and writes its content to a new file.
    It has the following naming convention: min-max.csv
    """

    # Get the minimum and maximum of the list:
    minimum = min(var_in_array)
    maximum = max(var_in_array)

    # Create the file name:
    name = str(int(minimum)) + "-" + str(int(maximum)) + ".csv"

    # Open a new file, write the content and close the file:
    output_file = open(name, "w+")
    for array_element in var_in_array:
        output_file.write(str(array_element) + "\n")
    output_file.close()

    # Change file permissions to owner rw only (0600):
    os.chmod(name, 0o600)


def calc(var_in_value):
    """
    This function uses the calc.sh script to change the input value.
    It is a shared ressource and must no be used by more than 2 threads at once.
    """

    # Acquire semaphore (increment):
    SEM.acquire()

    # Calculate the result:
    result = os.popen("./calc.sh " + str(var_in_value)).read()

    # Release semaphore (decrement):
    SEM.release()

    # Return the result:
    return result

def start_slowsort(var_in_array):
    """
    This function prepares and starts the slowsort algorithm.
    """

    # Create a new local array(list)
    ary = []

    # Loop through the input array and append the value to new array:
    for in_element in var_in_array:
        ary.append(int(calc(int(in_element))))

    # Call the slowsort algorithm // args: array, start index, end index
    slowsort(ary, 0, len(ary)-1)

    # Write the results of the slowsort algorithm to a new file
    write_to_file(ary)

def slowsort(var_in_array, i, j):
    """
    This function provides the slowsort algorithm. Details about it can be found
    within several scientific papers.
    """
    if i >= j:
        return
    mid = (i+j)//2
    slowsort(var_in_array, i, mid)
    slowsort(var_in_array, mid+1, j)
    if var_in_array[mid] > var_in_array[j]:
        var_in_array[mid], var_in_array[j] = var_in_array[j], var_in_array[mid]
    slowsort(var_in_array, i, j-1)


# Load all Files with .csv extension:
FILE_LIST = [f for f in os.listdir() if ".csv" in f]

# Print all the files to double check if they are right (Debugging only):
print(FILE_LIST)

# Create global list variable to store all the threads as objects:
THREADS = []

# Create global list variable to store all the input values from the files, becomes a list of lists:
VALUES = []

# global index variable for looping and indexing
CNT = 0

# Loop through every file in the file list, get each line and store it in a list
for element in FILE_LIST:
    arr = []
    with open(element, "r") as file:
        for line in file:
            value = line.strip() # remove special characters
            arr.append(int(value)) # make sure it is an integer
        file.close()
        #print(len(arr))
    VALUES.append(arr) # append list of file values to VALUES

    # Create new thread for each file and store the thread object in THREADS
    # use CNT for list indexing
    THREADS.append(threading.Thread(target=start_slowsort, args=(VALUES[CNT],)))
    CNT += 1

# Start all the threads
for thread in THREADS:
    thread.start()

# Join all the threads (optional)
CNT = 0
for thread in THREADS:
    thread.join()
    CNT += 1

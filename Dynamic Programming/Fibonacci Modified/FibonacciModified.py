import math
import os
import random
import re
import sys
import bisect
import requests
import filecmp
import threading

def fibonacciModified(t1, t2, n):
    # use some function for hackerrank
    # solved with tabulation bc it's dp
    '''
    # tabulation array init
    arr = [0] * n
    arr[0] = t1
    arr[1] = t2

    for i in range(2, n):
        arr[i] = arr[i - 2] + (arr[i - 1])**2
    return arr[n - 1]
    '''

    # reduced to space complexity of (O(1))
    for _ in range(2, n):
        t3 = t1 + t2**2
        t1 = t2
        t2 = t3

    return t3

def main():
	# use at least one function to solve problem
	# important for reading from stdin
	# input():	reads line as string
	# split():	seperates into list
	# rstrip():	removes whitespace from input

	# get input into data structures
	# pass data structure into foo(), do not declare global vars

	# print to stdout with print() if function returns a value
    # be careful with whitespace!

    data = input().split()
    t1 = int(data[0])
    t2 = int(data[1])
    n = int(data[2])
    print(fibonacciModified(t1, t2, n))

    return None

# returns a list of files in the test directory for the problem
def getFilePaths(relativeDirectory: str):
    # get full path 
    currentDirectory = os.path.dirname(__file__)
    fullPath = os.path.join(currentDirectory, relativeDirectory)

    # exit if the directory doesn't exist
    if os.path.isdir(fullPath) == False:
        print("Directory '" + relativeDirectory + "' does not exist. Closing", file = sys.stderr)
        sys.exit(-1)

    # get all the files in the folder
    filePaths = list()
    for filename in os.listdir(fullPath):
        # add files paths to a list
        filePath = os.path.join(fullPath, filename)
        if os.path.isfile(filePath):
            filePaths.append(filePath)

    return filePaths

def runLocalTests():
    # run test cases from test cases
    # requires ./test/input and ./test/output to exist with the same number of files
    # since we're downloading them directly from HackerRank, this is a safe assumption
    inputFiles = getFilePaths("tests/input")
    expectedOutputFiles = getFilePaths("tests/output")

    # save original stdout
    commandLine = sys.stdout
    
    for i in range(len(inputFiles)):
        # open file for input/output from hackerank
        inputFile = open(inputFiles[i], mode="r")
        expectedOutputFile = open(expectedOutputFiles[i], mode="r")

        # create a file to replace stdout
        outputFile = open(os.path.join(os.path.dirname(__file__), os.path.basename(expectedOutputFile.name)), mode="w")

        # redirect stdin/stdout
        sys.stdin = inputFile
        sys.stdout = outputFile
        
        # run test on new thread
        threading.Thread(target=runTest(inputFile, outputFile, expectedOutputFile, commandLine)).start()

# accepts an open file parameter
def runTest(inputFile, outputFile, expectedOutputFile, commandLine):
    main()

    # close files
    expectedOutputFile.close()
    inputFile.close()
    outputFile.close()

    # compare files and print result to command line
    print("Test Case " + os.path.basename(inputFile.name) + ": ", end="", file=commandLine)
    if filecmp.cmp(expectedOutputFile.name, outputFile.name, shallow=True):
        print("PASSED", file=commandLine)
    else:
        print("FAILED", file=commandLine)

if __name__ == "__main__":
    # if in my vscode enviornment
    if len(sys.argv) > 1 and sys.argv[1] == "--jorgDebug":
        runLocalTests()

    # if not
    else:
        main()
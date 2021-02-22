import math
import os
import random
import re
import sys
import bisect
import requests
import filecmp
import threading

LIMITER = 10 ** 9 + 5

def construct(n, k, x):
    # use some function for hackerrank
    
    # for most cases:
    # combinations scaled by (k - 1) because we can't choose the
    # previous number

    # for the n - 2 case, we have to worry about previous and next case
        # scale by (k - 1)
        # subtract number of cases where a combination == x

    # goal: keep track of number of combinations and how many of them
    # end with x

    # dp tabulation array style approach
    # space complexity = O(2n)
    # time complexity = O(n)
    # initialize

    '''
    # this method does not handle large numbers well but this logic is actually sound
    combinations = [0] * n
    xs = [0] * n
    combinations[0] = 1
    if x == 1:
        xs[0] = 1
    else:
        xs[0] = 0 

    for i in range(1, n):
        combinations[i] =  combinations[i - 1] * (k - 1)
        xs[i] = combinations[i - 1] - xs[i - 1]

    return combinations[n - 2] - xs[n - 2]
    '''

    # this does not yield the correct answer, it yields a better and more precise answer
    # than the test cases on hackerrank

    # the time constraints actually come from continuously reallocating memory
    # to avoid this, we can make two built in python big ints with the power function
    prevNumXs = k ** n
    currNumXs = k ** n
    prevNumCombinations = k ** n
    prevNumXs = k ** n

    # initializes
    prevNumCombinations = 1
    if x == 1:
        prevNumXs = 1
    else:
        prevNumXs = 0

    for i in range(1, n):
        currNumCombinations = prevNumCombinations * (k - 1)
        currNumXs = prevNumCombinations - prevNumXs

        if i == n - 1:
            break

        prevNumXs = currNumXs
        prevNumCombinations = currNumCombinations

    return (prevNumCombinations - prevNumXs) % LIMITER


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

    data = list(map(int, input().split()))
    n = data[0]
    k = data[1]
    x = data[2]

    result = construct(n, k, x)
    print(result)

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
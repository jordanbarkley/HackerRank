import math
import os
import random
import re
import sys
import bisect
import requests
import filecmp
import threading

def mino(n, arr):
    # not solved with dp, uses greedy algorithm
    # can be solved in O(nlogn)
    # arr must be sorted at this point

    # get numbers to work with
    operationsMin = math.inf

    low = arr[0]

    for i in range(4):
        # test different start values!
        low = arr[0] - i

        # don't test negative values
        if low < 0:
            continue

        # add operations if i !- 0
        if i == 1 or i == 2:
            operations = 1
        elif i == 3 or i == 4:
            operations = 2
        else:
            operations = 0

        for j in range(1, n):
            x = arr[j]

            # calculate difference and min operation for this difference
            difference = x - low
            
            # get difference down to 5 max
            operations += difference // 5
            difference = difference % 5

            # base cases
            if difference == 1 or difference == 2:
                operations += 1
            elif difference == 0:
                operations += 0
            else:
                operations += 2 

        if operations < operationsMin:
            operationsMin = operations   

    return int(operationsMin)

def main():
	# use at least one function to solve problem
	# important for reading from stdin
	# input():	reads line as string
	# split():	seperates into list
	# rstrip():	removes whitespace from input
    t = int(input())

    for i in range(t):
        n = int(input())
        # arr = input().rstrip().split()
        arr = list(map(int, input().rstrip().split()))
        arr.sort()

        result = mino(n, arr)

        if i != t - 1:
            print(result)
        else:
            print(result, end="")

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
        outputFile = open(os.path.join(os.path.dirname(__file__), "out" + str(i) + ".txt"), mode="w")

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
    print("Test Case " + os.path.basename(expectedOutputFile.name) + ": ", end="", file=commandLine)
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
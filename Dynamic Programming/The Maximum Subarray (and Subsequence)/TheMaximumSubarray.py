import math
import os
import random
import re
import sys
import bisect
import requests
import filecmp
import threading

def maxes(arr, n):
    # use some function for hackerrank

    '''
    # no longer used.
    # nlogn + n solution for only this problem

    # max subsequence
    # use a greedy algorithm. add all positives or take largest negative
    sortedArr = sorted(arr)
    index = bisect.bisect_left(sortedArr, 0)

    # if it's not max index, there are positives
    maxSubsequence = 0
    if index != n:
        for i in range(index, n):
            maxSubsequence += sortedArr[i]
    
    # otherwise, we get the largest negative
    else:
        maxSubsequence = sortedArr[n - 1]
    '''

    '''
    # no longer used, honestly terrible solution lol
    # space complexity n^2
    # time complexity n^2/2

    # 2d array filled out with tabulation where dp[i][j] represents sum of arr[i] through arr[j]
    dp = [[0 for _ in range(n)] for _ in range(n)]
    maxSubarray = arr[0]
    for i in range(n):
        for j in range(i, n):
            if i != j:
                dp[i][j] = arr[j] + dp[i][j - 1]
            else:
                dp[i][j] = arr[i]
            if dp[i][j] > maxSubarray:
                maxSubarray = dp[i][j]
    '''
    
    # same algorithm but without dp array
    # also inlcudes maxSubsequence
    maxSubarray = arr[0]
    maxSubsequence = arr[0]
    maxLocal = arr[0]
    for i in range(1, n):
        # maxSubbarray
        maxLocal = max(arr[i], maxLocal + arr[i])
        maxSubarray = max(maxSubarray, maxLocal)

        # max Subsequence
        maxSubsequence = max(max(maxSubsequence, maxSubsequence + arr[i]), arr[i])

    return [maxSubarray, maxSubsequence]

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

    t = int(input())

    for i in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        result = maxes(arr, n)
        
        print(str(result[0]) + " " + str(result[1]), end="")
        if i != t - 1:
            print()

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
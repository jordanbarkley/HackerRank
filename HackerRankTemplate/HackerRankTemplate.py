import math
import os
import random
import re
import sys
import bisect
import requests
import filecmp
import threading

def foo():
    return

def main(inputFile, outputFile):
    # do not use input() as this reads from sys.stdin directly
    # we can't change sys.stdin across threads, sadly
    # use the below instead

        # reading
            # for line in inputFile:
            # inputFile.readLine()

	        # split():	seperates into list
	        # rstrip():	removes whitespace from input

        # writing
            # outputFile.write(<str> + '\n')
            # be careful with whitespace!

    return


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

    threads = list()
    
    for i in range(len(inputFiles)):
        # open file for input/output from hackerank
        inputFileName = inputFiles[i] 
        expectedOutputFileName = expectedOutputFiles[i]
        outputFileName = os.path.join(os.path.dirname(__file__), os.path.basename(expectedOutputFileName))
        
        # run in a new subprocess
        t = threading.Thread(target=runTest, args=[inputFileName, expectedOutputFileName, outputFileName])
        threads.append(t)

    # run threads
    for t in threads:
        t.start()

    # avoids closing stdin
    for t in threads:
        t.join()

# accepts an open file parameter
def runTest(inputFileName, expectedOutputFileName, outputFileName):
    # open files
    inputFile = open(inputFileName, mode="r")
    outputFile = open(outputFileName, mode="w+")

    # run main with a given stdin
    main(inputFile, outputFile)

    # close files
    inputFile.close()
    outputFile.close()

    # compare files and print result to command line
    printStr = "Test Case " + os.path.basename(inputFile.name) + ": "
    if filecmp.cmp(expectedOutputFileName, outputFileName, shallow=True):
        print(printStr + "PASSED")
    else:
        print(printStr + "FAILED")

if __name__ == "__main__":
    # if in my vscode enviornment
    if len(sys.argv) > 1 and sys.argv[1] == "--jorgDebug":
        runLocalTests()

    # if not
    else:
        main(sys.stdin, sys.stdout)
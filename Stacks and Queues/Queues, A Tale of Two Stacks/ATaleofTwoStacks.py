import math
import os
import random
import re
import sys
import bisect
import requests
import filecmp
import threading

class DumbQueue(object):
    def __init__(self):
        # init stacks
        self.fifo = list()
        self.lifo = list()

    # Adds element to end of queue
    def enqueue(self, value):
        self.fifo.append(value)

    # Removes and returns element from the "queue" (first element added)
    def dequeue(self):
        self.transfer()
        return self.lifo.pop()
    
    # Returns element from the "queue" (first element added)
    def peep(self):
        self.transfer()
        value = self.lifo.pop()
        self.lifo.append(value)
        return value

    # Move all elements to self.lifo iff the lifo is empty. If the queue is not
    # empty, there is no reason to transfer because our next dequeue()/peep()
    # value is already there.
    def transfer(self):
        if len(self.lifo) == 0:
            while len(self.fifo) > 0:
                value = self.fifo.pop()
                self.lifo.append(value)


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
    
    n = int(inputFile.readline())
    dq = DumbQueue()
    hasWritten = False
    for _ in range(n):
        # get query
        data = list(map(int, inputFile.readline().rstrip().split()))
        
        if data[0] == 1:
            value = data[1]
            dq.enqueue(value)

        elif data[0] == 2:
            dq.dequeue()

        elif data[0] == 3:
            if hasWritten == True:
                outputFile.write('\n')
            outputFile.write(str(dq.peep()))
            hasWritten = True

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
#!/usr/bin/python3

import sys

import xml.etree.cElementTree as ET
import re

import datetime

class XMLWriter:
    def __init__(self, outputFilePath = ''):
        try:
            self.fh_ = open(outputFilePath, 'w')
            print("Writing to {outputFilePath}...".format(outputFilePath = outputFilePath))
        except FileNotFoundError:
            print("No outputfile specified, writing to stdout...")
            self.fh_ = sys.stdout
        print('<?xml version="1.0" encoding="UTF-8"?>', file=self.fh_)
        print('<root>', file=self.fh_)
       
    def __del__(self):
        print('</root>', file=self.fh_)
        if self.fh_ is not sys.stdout:
            self.fh_.close()

    def writeMeasurementHeader(self, name, writeList):
        print('<measurements name="{measurementsName}" size="{size}">'.format(measurementsName = name, size=len(writeList)), file=self.fh_)

    def writeEndMeasurementHeader(self):
        print('</measurements>', file=self.fh_)

    def writeMeasurement(self, key, value):
        print('    <measurement name="{name}" value="{value}"/>'.format(name = key, value = value), file=self.fh_)

    # expects key -> value pairs
    def write(self, name, write):
        self.writeMeasurementHeader(name, write)
        for key,value in write.items():
            self.writeMeasurement(key, value)
        self.writeEndMeasurementHeader()

class SconsTimeOutputReader:
    def __init__(self, inputFilePath):
        try:
            with open(inputFilePath, 'r') as self.fh_:
                print("Interpreting {inputFilePath}...".format(inputFilePath = inputFilePath))
                self.lines = self.fh_.readlines()
        except FileNotFoundError:
            print("Input file not found")
            raise
    @staticmethod
    def getModule(path):
        pathList = path.split('/')
        for i in range(len(pathList)):
            if pathList[i] == "modules" or pathList[i] == "3rdparty":
                return pathList[i+1]
    @staticmethod
    def getTime(line):
        lineList = line.split(':')
        for line in lineList:
            if 'seconds' in line:
                return float(line.split(' ')[1])

    def getModuleTimeLines(self):
        result = dict()
        for line in self.lines:
            pattern = re.search("Command execution time:.*opencv", line) 
            if pattern:
                module = self.getModule(line)
                time = self.getTime(line)
                if module in result:
                    result[module] += time
                else:
                    result[module] = time
        return result
    def getTotalBuildTime(self):
        for line in self.lines:
            pattern = re.search("Total build time:", line)
            if pattern:
                return self.getTime(line)

def extractBuildTimeInformation(inputFile, fh):
    totalBuildtime = inputFile.getTotalBuildTime()
    fh.write('total-build-time', {'total-build-time' : totalBuildtime})
    moduleList = inputFile.getModuleTimeLines()
    fh.write('modules', moduleList)

def main():
    if len(sys.argv) < 1:
        print('Error in format. Format: [script] inputFile [outputFile]')
        return 1

    # Create reader
    reader = SconsTimeOutputReader(sys.argv[1])

    # Create output writer
    try:
        outputFile = sys.argv[2]
    except IndexError:
        outputFile = ''
    outputHandler = XMLWriter(outputFile)
    extractBuildTimeInformation(reader, outputHandler)
    return 0

if __name__ == "__main__":
        main()

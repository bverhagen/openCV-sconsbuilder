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
            self.fh_ = open(inputFilePath, 'r')
            print("Interpreting {inputFilePath}...".format(inputFilePath = inputFilePath))
        except FileNotFoundError:
            print("Input file not found")
            raise
    def __del__(self):
        self.fh_.close()
    @staticmethod
    def getModule(path):
        pathList = path.split('/')
        for i in range(len(pathList)):
            if pathList[i] == "modules" or pathList[i] == "3rdparty":
                return pathList[i+1]
    @staticmethod
    def getTime(line):
        lineList = line.split(':')
        return float(lineList[2].split(' ')[1])

    def getModuleTimeLines(self):
        content = self.fh_.readlines()
        result = dict()

        for line in content:
            pattern = re.search("Command execution time:.*opencv", line) 
            if pattern:
                module = self.getModule(line)
                time = self.getTime(line)
                if module in result:
                    result[module] += time
                else:
                    result[module] = time
        return result


def extractBuildTimeInformation(inputFile, fh):
    moduleList = inputFile.getModuleTimeLines();
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

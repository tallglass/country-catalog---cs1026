'''Oren Joffe - CS1026A - Assignment 4 - Program utilizes a CountryCatalogue class to update a country catalogue.'''

from os.path import exists as file_exists
from catalogue import CountryCatalogue

def lineFormat(line):
    original_countryList = line.split(";")
    countryList = []
    for i in original_countryList:
        countryList.append(i.strip())
    while '' in countryList:
        countryList.remove('')
    return countryList

def nameCheck(name):
    invalid_chars = "1234567890!@#$%^&*()-+=[]\\|}{;:/?.>,<~`"
    for char in name:
        if char in invalid_chars:
            return False
    if len(name) > 0 and (name[0].isupper()):
        return True
    else:
        return False

def listLengthCheck(list):
    if len(list) < 5:  # up to 3 semi-colons/4 list objects

        if len(list) == 1:  # just name on line
            return '1'

        elif len(list) > 1: # more info on line
            return '>1'
    else:
        return False

def labelCheck(list):
    info_list = list[1:]  # not checking name, only info

    correct_label = False
    Pcounter = 0 # info type has not been updated
    Acounter = 0
    Ccounter = 0
    for i in info_list:
        if (i[:2] == "P=") or (i[:2] == "A=") or (i[:2] == "C="):
            if (i[:1] == 'P') and (Pcounter == 0):
                Pcounter += 1
                correct_label = True
            elif (i[:1] == 'A') and (Acounter == 0):
                Acounter += 1
                correct_label = True
            elif (i[:1] == 'C') and (Ccounter == 0):
                Ccounter += 1
                correct_label = True
            else:
                return False
        else:
            return False
    return correct_label

def commaCheck(number_string):
    checkingNumber = number_string

    for char in checkingNumber:
        if not char.isnumeric():
            checkingNumber = checkingNumber.replace(char, '', 1)
    int_checkingNumber = int(checkingNumber)
    checkingNumber = "{:,}".format(int_checkingNumber)

    return checkingNumber == number_string

def typeCheck(list, continents):
    info_list = list[1:]  # not checking name, only info

    correct_info = False
    for i in info_list:
        if len(i) != 2:
            if (i[:2] == "P=") or (i[:2] == "A="):
                if commaCheck(i[2:]) == True:
                    correct_info = True
                else:
                    return False
            elif (i[:2] == "C="):
                if i[2:] in continents:
                    correct_info = True
                else:
                    return False
        else:
            return False
    return correct_info

def detectSemicolons(line):
    counter = 0
    for char in line:
        if char == ';':
            counter += 1
    return counter

def checkLine(line):
    '''Checks if line is formatted correctly.'''
    continent_list = ["Africa", "Antarctica", "Arctic", "Asia", "Europe", "North_America",
                      "South_America"]
    line_is_valid = True
    if line != "\n":
        if detectSemicolons(line) <= 3:
            countryList = lineFormat(line)

            name = countryList[0]
            if nameCheck(name) == True:
                if listLengthCheck(countryList) == '1':
                    return (True, name)
                elif listLengthCheck(countryList) == '>1':
                    if labelCheck(countryList) == True:
                        if typeCheck(countryList, continent_list) == True:
                            return (True, name)
                        else:
                            line_is_valid = False
                    else:
                        line_is_valid = False
                else:
                    line_is_valid = False
            else:
                line_is_valid = False
        else:
            line_is_valid = False

    if line_is_valid == False:
        return False

def updateCatalogue(line, catalogue_class, valid_tuple):
    lineList = lineFormat(line)
    catlog = catalogue_class
    line_valid = valid_tuple
    if catlog.findCountry(line_valid[1]) == None:  # country not in catalogue
        name = lineList[0]
        pop = ''
        area = ''
        continent = ''
        for i in range(1, len(lineList)):
            if lineList[i][0] == 'P':
                pop = lineList[i][2:]
            elif lineList[i][0] == 'A':
                area = lineList[i][2:]
            elif lineList[i][0] == 'C':
                continent = lineList[i][2:]
        catlog.addCountry(name, pop, area, continent)
    else: # country in catalogue
        for i in range(1, len(lineList)):
            if lineList[i][0] == 'P':
                catlog.setPopulationofCountry(lineList[0], lineList[i][2:])
                continue
            if lineList[i][0] == 'A':
                catlog.setAreaofCountry(lineList[0], lineList[i][2:])
                continue
            if lineList[i][0] == 'C':
                catlog.setContinentofCountry(lineList[0], lineList[i][2:])
                continue


def processUpdates(cntryFileName, updateFileName, badUpdateFile):
    unsuccessful = (False, None)
    countryFile = cntryFileName

    while True:
        if file_exists(countryFile):
            updateFile = updateFileName
            while True:
                if file_exists(updateFile):
                    catlog = CountryCatalogue(countryFile)

                    with open(badUpdateFile, 'w') as badFile:

                        with open(updateFile, 'r') as infile:
                            for line in infile:
                                original_line = line
                                line = line.rstrip("\n")
                                line = line.replace(' ', '')

                                line_valid = checkLine(line)
                                if line_valid != False:  # line is valid
                                    updateCatalogue(line, catlog, line_valid)
                                else: # invalid line
                                    badFile.write(original_line)

                        catlog.saveCountryCatalogue('output.txt')
                        return(True, catlog) # update successful

                else: # update file check
                    quitInput = input("Update File does not exist! Quit? (Y,N): ")
                    if quitInput == "N":
                        updateFile = input("Please enter a new update file: ")
                    else:
                        with open('output.txt', 'w') as outputFile:
                            outputFile.write("Update Unsuccessful\n")
                            return unsuccessful
        else: # country file check
            quitInput = input("Country File does not exist! Quit? (Y,N): ")
            if quitInput == "N":
                countryFile = input("Please enter a new country file: ")
            else:
                with open('output.txt', 'w') as outputFile:
                    outputFile.write("Update Unsuccessful\n")
                    return unsuccessful
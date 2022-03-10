'''Oren Joffe - CS1026A - Assignment 4 - This program contains the Country class.'''

class Country:
    '''Models a country with name, population, area, and continent.'''
    def __init__(self, name, pop, area, continent=""):
        self._name = str(name)
        self._pop = str(pop)
        self._area = str(area)
        self._continent = str(continent)

    # getter methods
    def getName(self):
        return self._name
    def getPopulation(self):
        return self._pop
    def getArea(self):
        return self._area
    def getContinent(self):
        return self._continent

    # setter methods
    def setPopulation(self, pop):
        self._pop = pop
    def setArea(self, area):
        self._area = area
    def setContinent(self, continent):
        self._continent = continent

    def __repr__(self):
        return self._name + " (pop: " + str(self._pop) + ", size: " + str(self._area) + ") in " + self._continent
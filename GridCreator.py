from Map import Map
from Pedestrian import Pedestrian
from Constant import *
import numpy as np
import math
import matplotlib.pyplot as plt


class GridCreator:


    def __init__(self, data, scale_var):
        self.data = data
        self.rows = np.size(self.data, 0)
        self.columns = np.size(self.data, 1)
        self.scale_var = scale_var
        self.grid = self.createEmptyGrid()
        self.corners = []

        self.emptyGridfiller()

    def createEmptyGrid(self):
        return np.zeros((self.rows * self.scale_var, self.columns * self.scale_var))

    def emptyGridfiller(self):
        #create an empty grid scaled with the scale_var
        for row in range(self.rows):
            for column in range(self.columns):
                if self.data[row][column] == S_EMPTY:
                    continue
                else:
                    cell_value = self.data[row][column]
                    if cell_value == S_TARGET:
                        self.targetCreator(row * self.scale_var, column * self.scale_var)
                    else:
                        self.blockCreater(row * self.scale_var, column * self.scale_var, cell_value)
                
                

    def blockCreater(self, row, column, value):
        #This function will take a type of block(such as pedestrian, obstacle) and will resize them into multiple blocks according to the scale_var
        #The main logic is the left corner cell of the new enlarged cell will be the old cell
        for r in range(self.scale_var):
            for c in range(self.scale_var):
                self.grid[row+r][column+c] = value
        if value == S_PEDESTRIAN:
            self.pedestrianListAdder(row,column)
    
    def pedestrianListAdder(self, row, col):
        self.corners.append([(row, col),(row, col + (self.scale_var - 1)),(row + (self.scale_var - 1), col),(row + (self.scale_var - 1), col + (self.scale_var - 1))])
        

    def targetCreator(self, scaled_row, scaled_column):
        ##now we have a cell here which is self.data[row][column]
        #boundaries of the new multi block is:
        #(row*scale, column*scale)     (row*scale, column*scale + scale-1)
        #(row*scale + scale-1, column*scale ) (row*scale + scale-1, column*scale + scale-1)
        #from left-top to right top
        #scaled_row = row * self.scale_var
        #scaled_column = column * self.scale_var
        for i in range(self.scale_var):
            self.grid[scaled_row][scaled_column + i] = S_TARGET
            self.grid[scaled_row + i][scaled_column] = S_TARGET
            self.grid[scaled_row + (self.scale_var - 1)][scaled_column + i] = S_TARGET
            self.grid[scaled_row + i][scaled_column + (self.scale_var - 1)] = S_TARGET
            #from left top to left down

    def gridChecker(self):
        plt.imshow(self.grid, cmap='Blues', interpolation='none')
        plt.show()
        plt.pause(10)
        plt.cla() 
import sys
import re
import numpy as np
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from pyqtgraph import *

from PySide2 import QtGui


class My_GUI(QWidget):   # making the class of the GUI

    def __init__(self):  # define of the constructor of the class
        super().__init__()
        self.setWindowTitle("Function Plotter")  #making the window
        # window size
        self.setGeometry(500, 500, 500, 500)
        self.setMinimumHeight(620)
        self.setMinimumWidth(680)
        self.setMaximumHeight(620)
        self.setMaximumWidth(680)
        # layout
        widget = QWidget(self)
        layout = QFormLayout(widget)


        # add text box for x minimum and maximum and the function entered by the user
        self.text1 = QLineEdit()
        self.text2 = QLineEdit()
        self.text3 = QLineEdit()
        # make push button
        self.b = QPushButton("click to plot")
        # adding the rows to the window
        layout.addRow("Function", self.text1)
        layout.addRow("Minimum Value", self.text2)
        layout.addRow("Maximum Value", self.text3)


        # execute the function main when the button is pushed
        self.b.clicked.connect(self.main)

        # add the button to the window
        layout.addRow(self.b)
        # graph desgin
        self.graphWidget = PlotWidget()
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLabel('left', "<span style=\"color:red;font-size:20px\">F(X)</span>")
        self.graphWidget.setLabel('bottom', "<span style=\"color:red;font-size:20px\">X</span>")
        self.graphWidget.setBackground('k')

        layout.addRow(self.graphWidget)

    def error_box(self,message): # show message box include the error
        QMessageBox.critical(self, "ERROR !!!!", message)


    def error(self, function): # function that detect the error
        error_occured = False
        error_message="\n"
        if function[len(function)-1]=="^" or function[len(function)-1]=="*" or function[len(function)-1]=="+" or function[len(function)-1]=="-" or function[len(function)-1]=="^":
            error_message=error_message+("Error in the las operator"+function[len(function)-1]+"you can't end the function with operation"+"\n")
            error_occured = True

        if function.count("(") != function.count(")"):  # check the number of opened and closed brackets
            error_message=error_message+("Error in brackets the number of opened brackets must be equal to the closed"+"\n")
            error_occured = True

        for i in range(len(function) - 1): # check if there is number followed by x

            if (function[i] == "0" or function[i] == "1" or function[i] == "2" or function[i] == "3" or
                    function[i] == "4" or function[i] == "5" or function[i] == "6" or function[i] == "7" or
                    function[i] == "8" or function[i] == "9"):
                if function[i + 1] == "x":
                    error_message=error_message+(" Error you can't use number followed by x "+"\n")
                    error_occured = True
                    break

        for i in range(len(function) - 1): #check if there is x followed by number

            if (function[i + 1] == "0" or function[i + 1] == "1" or function[i + 1] == "2" or function[i + 1] == "3" or
                    function[i + 1] == "4" or function[i + 1] == "5" or function[i + 1] == "6" or function[ i + 1] == "7" or function[i + 1] == "8" or
                    function[i + 1] == "9"):
                if function[i] == "x":
                    error_message=error_message+("Error you can't use x followed by number"+"\n")
                    error_occured = True
                    break

        for i in range(len(function)): # check if there is any unknown character

            if (function[i] != "x" and function[i] != "*" and function[i] != "/" and function[i] != "+" and
                    function[i] != "^" and
                    function[i] != "-" and function[i] != "0" and function[i] != "1" and function[i] != "2" and
                    function[i] != "3" and
                    function[i] != "4" and function[i] != "5" and function[i] != "6" and function[i] != "7" and
                    function[i] != "8" and
                    function[i] != "9" and function[i] != "(" and function[i] != ")"):

                 error_message=error_message+("Error you can't write " + function[i]+" you can only write numbers,+,-,/,*,^,symbol x \n")

                 error_occured = True


        for i in range(len(function) - 1): # check if there is repeated character
            if (function[i] == "x" or function[i] == "*" or function[i] == "/" or function[i] == "+" or function[i] == "^" or
                    function[i] == "-"):
                if function[i] == function[i + 1]:
                    error_message=error_message+("Error in " + function[i] + function[i + 1] + " you can't repeat " + function[i]+"\n")
                    error_occured = True

         # check if there is empty bracket
            if (function[i] == "(" and function[i + 1] == ")"):
                error_message=error_message+("Error in " + function[i] + function[i + 1] + " you can't use empty brackets \n")
                error_occured = True

        # check if there is x followed by bracket and vise versa
            if (function[i] == "x" and function[i + 1] == "("):
                error_message=error_message+("Error in " + function[i] + function[i + 1] + " use x*( instead\n")

            if (function[i] == ")" and function[i + 1] == "x"):
                error_message=error_message+("Error in " + function[i] + function[i + 1] + " use )*x instead \n")
        # check if there is number followed by bracket and vise versa
            if (function[i] == "0" or function[i] == "1" or function[i] == "2" or function[i] == "3" or
                    function[i] == "4" or function[i] == "5" or function[i] == "6" or function[i] == "7" or function[i] == "8" or
                    function[i] == "9"):
                if function[i + 1] == "(":
                    error_message=error_message+("Error in " + function[i] + function[i + 1] + " use instead " + function[i] + "*" + function[i + 1]+"\n")

                    error_occured = True

            if (function[i + 1] == "0" or function[i + 1] == "1" or function[i + 1] == "2" or function[i + 1] == "3" or
                    function[i + 1] == "4" or function[i + 1] == "5" or function[i + 1] == "6" or function[i + 1] == "7" or function[i + 1] == "8" or
                    function[i + 1] == "9"):
                if function[i] == ")":
                    error_message=error_message+( "Error in " + function[i] + function[i + 1] + " use instead " + function[i] + "*" + function[i + 1]+"\n")

                    error_occured = True

        # check the followed operators

            if (function[i] + function[i + 1] == "*/" or function[i] + function[i + 1] == "/*" or function[i] +
                    function[i + 1] == "/+" or
                    function[i] + function[i + 1] == "+/" or function[i] + function[i + 1] == "+*" or function[i] +
                    function[i + 1] == "*+" or function[i] +function[i + 1] == "(*" or function[i] + function[i + 1] == "*)"or function[i] +
                    function[i + 1] == ")("or function[i] +function[i + 1] == "(+" or function[i] + function[i + 1] == "+)"or function[i] +function[i + 1] == "-)" or
                    function[i] +function[i + 1] == "^*"or function[i] +function[i + 1] == "*^"or function[i] +function[i + 1] == "^)"or function[i] +function[i + 1] == "+^"):
                error_message=error_message+("Wrong input in " + function[i] + function[i + 1]+"\n")
                error_occured = True

        if error_occured==True :
           self.error_box(str(error_message))

        self.graphWidget.clear()
        return error_occured

    # this is the function that evaluates the function entered by the user at certain value of x
    def function_evaluation(self, function, x_value):


        function = function.replace("^", "**")
        x_str = str(x_value)
        function = function.replace("x", "(" + x_str + ")")
        return eval(function)

    def main(self): # the main function executed when the button is pushed
        error_detected= False
        # inputs the user entered
        function_x = self.text1.text()
        function_x = function_x.replace(" ", "")
        function_x = function_x.replace("X", "x") # change all x to small letters
        min_value = self.text2.text()
        max_value = self.text3.text()

        if function_x =="" or min_value=="" or max_value=="": #check if there is missing input
            self.error_box("Missing input")
            self.graphWidget.clear()
            error_detected = True
        if min_value.isalpha() == False and max_value.isalpha() == False:
           if int(min_value) > int(max_value): # check if the max value is smaller than min value

               self.error_box("you can't enter a maximum value smaller than the minimum value")
               self.graphWidget.clear()
               error_detected = True
        if min_value.isalpha()==True or max_value.isalpha()==True: # check if the max value and min are numbers
            self.error_box("The Maximum and Minimum value must be numbers")
            self.graphWidget.clear()
            error_detected = True
        if error_detected==False:
            error_detected = self.error(function_x)

        if error_detected == False:
            x = np.linspace(int(min_value),int(max_value), num=500)  # construct the array of the x axis
            y = []
            for i in range(len(x)):
                y.append((self.function_evaluation(function_x, x[i])))  # construct the array of the y axis
            self.graphWidget.clear()

            pen=mkPen('r',width=2)
            self.graphWidget.plot(x, y,pen=pen)
            if min_value==max_value:
                QMessageBox.warning(self, "Warnning !!!!", "you plotted only one point")



me = QApplication(sys.argv)
my_GUI =My_GUI()
my_GUI.show()
me.exec_()
sys.exit(0)

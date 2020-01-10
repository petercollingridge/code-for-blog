import os
import sys
import numpy as np


def readFile(filename, delimiter='\t'):
    """ Read file and assign first column to X and second to Y. """
    
    x = []
    y = []
    
    for line in open(filename):
        temp = line.rstrip().split(delimiter)
        x.append(float(temp[0]))
        y.append(float(temp[1]))
    
    print("\nLoaded file: %s" % filename)
    print("Items found: %d" % len(x))
    return x, y


def summariseData(x, y):   
    print("Mean x: %.3f" % (sum(x) * 1.0/len(x)))
    print("Mean y: %.3f" % (sum(y) * 1.0/len(y)))


def plotData(x, y):
    import pylab
    
    pylab.scatter(x, y, marker='x')
    pylab.xlabel('x')
    pylab.ylabel('y')
    pylab.grid(True)
    pylab.show()


def getSign(value):
    return '-' if value < 0 else '+'


def solveRegression(list_x, list_y):
    """ Convert two lists of the same size to matrixs and solve linear regression using normal equation """
    
    from numpy.linalg import lstsq
    
    X = np.matrix(list_x)    
    X = np.row_stack((np.ones(X.shape[1]), X)).T    # Add column of 1s
    y = np.matrix(list_y).T
    
    #p = (X.T * X).I * X.T * y
    (p, residuals, rank, s) = lstsq(X, y)
    
    print("y = %.2fx %s %.2f" % (p[1,0], getSign(p[0,0]), abs(p[0,0])))


def fitPolynomial(x, y):
    degree = input("What degree polynomial? ")
    
    p = np.polyfit(x, y, degree)
    equation = "y = "
    for i, v in enumerate(p):
        if i > 0:
            equation += " %s %.3f" % (getSign(v), abs(v))
        else:    
            equation += "%.3f" % v
        if degree - i > 0:
            equation += "x"
        if degree - i > 1:
            equation += "^%d" % (degree - i)
    
    print(equation)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1]:
            f = sys.argv[1]
    else:
        f = raw_input("Enter filename: ")
    
    x, y = readFile(f)    
    
    print "\nChoose an option:"
    print " 1. Simple summary"
    print " 2. Plot data"
    print " 3. Find linear regression"
    print " 4. Find polynomial fit"
    print " 5. Exit"
    
    choice_dict = {1:summariseData, 2: plotData, 3: solveRegression, 4:fitPolynomial}
    makingChoice = True
    
    while makingChoice:
        print
        choice = input("> ")
        
        f = choice_dict.get(choice)
        if f:
            f(x, y)
        else:
            makingChoice = False

import numpy as np
from scipy.optimize import linprog
import pandas as pd

'''
Two-player zero-sum matrix games.


There are two players (row and column one) playing zero-sum game and an 2-D numpy array stands for a payoff
matrix passed as an argument in all functions. The script checks the payoff matrix for dominated strategies 
and removes them. Additionally it checks for a saddle point and prints it out unless it does not exist. 
One can easily prove all saddle points have the same value (in a game theory sense). The final output is 
the initial payoff matrix, a statement about saddle points, a simplified payoff matrix in case there are
dominated options, the expected value of the win (game value) for the row player and optimal strategies 
for each player which are probability vectors. The game value and optimal strategies are obtained by using
a simplex algorithm for linear maximization problem.


'''


def domoptions(matrix):
    '''

    Checks for dominated strategies for both players and removes them


    :return: simplified matrix without both players' dominated strategies
    '''


    collist = []
    rowlist = []
    nrows, ncols = matrix.shape[0], matrix.shape[1]
    for i in range(0, nrows-1):
        if i not in rowlist:
            for j in range(i+1, nrows):
                 if j not in rowlist:
                     if (matrix[i,:] > matrix[j,:]).all():
                         rowlist.append(j)
                     elif (matrix[i,:]<=matrix[j,:]).all():
                         rowlist.append(i)
                         break
                 continue
        continue


    for i in range(0, ncols-1):
        if i not in collist:
            for j in range(i+1, ncols):
                 if j not in collist:
                     if (matrix[:,i] < matrix[:,j]).all():
                         collist.append(j)
                     elif (matrix[:,i] >= matrix[:,j]).all():
                         collist.append(i)
                         break
                 continue
        continue
    return np.delete(np.delete(matrix, rowlist, axis=0), collist, axis=1)


def saddlepoint(matrix):
    ''' returns a saddle point and its indices in case it exists'''

    matrix2 = matrix.T
    for i, row in enumerate(matrix2):
        M = max(row)
        for j, x in enumerate(row):
            if x==M and min(matrix2[:,j]) == M:
                return (j,i), matrix2[i,j]



def simplex(matrix):
    '''uses simplex algorithm from SciPy library for linear maximization problem and returns the game value
    and optimal strategies'''

    rows, cols = matrix.shape[0], matrix.shape[1]
    A_ub = np.zeros((cols,rows+1))
    A_ub[:,-1] = np.ones(cols)
    A_ub[:,:-1] = -matrix.T
    b_ub = np.zeros(cols)
    c = np.zeros((rows+1,1))
    c[-1,0] = -1
    A_eq = np.ones((1,rows+1))
    A_eq[0,-1] = 0
    b_eq = 1
    bounds = [(0, None)]*(rows+1)
    bounds[-1] = (None, None)
    result = linprog(c, A_ub, b_ub, A_eq, b_eq, bounds, method='simplex')
    return result.x[0:-1], -1*result.fun


def solve(matrix):
    '''prints out the initial payoff matrix and the final result'''

    print(np.matrix(matrix))
    if not np.array_equal(matrix, domoptions(matrix)):
        print('The game has dominated options, the simplified matrix is ')
        print(np.matrix(domoptions(matrix)))

    try:
        int(saddlepoint(matrix)[1])
        print('The game has a saddle point at ', end='')
        print(saddlepoint(matrix)[0])
        print('The game value is ', end=' ')
        print(saddlepoint(matrix)[1])
        print('The optimal strategies for the row and column player are')
        df = pd.DataFrame([[np.around(simplex(matrix)[0], decimals=4), np.around(simplex(-matrix.T)[0], decimals=4)]],columns=['Row Player', 'Column Player'])
        df.index = ['']
        print(df)

    except TypeError:
        print('The game has no saddle points')
        print('The game value is ', end=' ')
        print(round(simplex(matrix)[1], 4))
        print('The optimal strategies for the row and column player are')
        df = pd.DataFrame([[np.around(simplex(matrix)[0], decimals=4), np.around(simplex(-matrix.T)[0], decimals=4)]],columns=['Row Player', 'Column Player'])
        df.index = ['']
        print(df)


















































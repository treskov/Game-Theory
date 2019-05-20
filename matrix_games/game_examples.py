import gamesolver
import numpy as np

'''3 examples of Matrix Games'''
def main():
    ex_1 = np.array([[-3,2],[2,-1]])
    gamesolver.solve(ex_1)
#---------------------------------------------
    ex_2 = np.array([[-3,4,5,7,8],[-5,0,4,6,-1],[-12,5,-7,8,2]])
    gamesolver.solve(ex_2)
#---------------------------------------------
    ex_3 = np.array([[-1,2,7,-8],[-2,1,1,4],[3,1,2,-2]])
    gamesolver.solve(ex_3)


if __name__ == '__main__':
    main()

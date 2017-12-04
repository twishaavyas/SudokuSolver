"""
Created on Sat Nov 25 15:34:57 2017

@author: Twisha
"""
def solve(question):
    for i in range(0, 9):
        for j in range(0, 9):
            if question[i][j] == 0:
                for digit in range(1,10):
                    valid = digitIsValid(i, j, digit, question)
                    if valid:
                        question[i][j] = digit

                        if solve(question):
                            return True
                        else:
                            question[i][j] = 0
                return False
    return True


def digitIsValid(row, column, digit, question):
    # checking if the digit is present in the row or column
    for i in range(0,9):
        if question[i][column] == digit:
            return False

        if question[row][i] == digit:
            return False

    # checking if the digit is present in the small square
    for i in range(0,3):
        for j in range(0,3):
            if question[(row / 3) * 3 + i][(column / 3) * 3 + j] == digit:
                return False

    return True


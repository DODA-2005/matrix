# Pranav Anil and Krishna Saini
#*COMPUTER SCIENCE SCHOOL PROJECT ON MATRICES AND DETERMINANTS *#

import random
import mysql.connector

file = open("matrices.txt", "a")

conn = mysql.connector.connect(host="localhost", user="root", password="1234", database="practical")
myc = conn.cursor()

myc.execute("create table matrices(Sno int primary key auto_increment, Matrix varchar(50))")
conn.commit()

# -----x-----x-----x--START OF USER-DEFINED FUNCTIONS--x-----x-----x----- #


# MYSQL CONNECTIVITY AND FILE SHARING
def connect(matrix):
    file.write(f"{matrix}\n")
    file.flush()
    sql = "insert into matrices (Matrix) values('{}')".format(matrix)
    myc.execute(sql)
    conn.commit()


# FOR CREATING A MATRIX BASED ON THE INPUTTED ROWS AND COLUMNS
def create_matrix(rows, columns, form="normal"):
    matrix = []
    for i in range(1, rows+1):
        temp_row = []
        for j in range(1, columns+1):
            if form == "random":
                element = random.randint(0, 30)
            else:
                element = int(input(f"Element in row {i} and column {j}: "))

            temp_row.append(element)
        matrix.append(temp_row)

    return matrix


# FOR PROMPTING THE USER FOR NO. OF ROWS AND COLUMNS
def matrix_rowcolumn():
    rows = int(input("Enter the no. of rows for matrix: "))
    columns = int(input("Enter the no. of columns for matrix: "))

    return rows, columns


# FOR PRETTY PRINTING A MATRIX
def matrix_print(matrix, msg=None):
    if msg == "original":
        print("The Original Matrix: ")
    else:
        print("The Resultant Matrix: ")
    for i in range(len(matrix)):
        print("\t|", end="  ")
        for j in range(len(matrix[i])):
            if j == len(matrix[i]) - 1:
                print(f"{matrix[i][j]}  |")
            else:
                print(matrix[i][j], end="  ")
    print()








# FOR THE FUNCTIONS AND ITS DECLARED MESSAGE
def declaration():
    operation = input("""Which matrix function would you like to execute: 
    1: Generate a Random Matrix
    2: Addition
    3: Subtraction
    4: Multiplication by a Scalar
    5: Multiplication by a Matrix
    6: Calculate Determinant
    7: Calculate Minor
    8: Calculate Cofactor
    9: Calculate Adjoint
    10: Transpose
    11: Inversion

    Enter the respective
    serial number to choose: """)
    print()
    return operation


# FOR THE FUNCTION OF ADDITION AND SUBTRACTION
def mat_addorsub(mat_1, mat_2, operation):
    matrix = []
    for i in range(len(mat_1)):
        temp_row = []
        for j in range(len(mat_1[i])):
            temp_row.append(eval(f"{mat_1[i][j]}{operation}{mat_2[i][j]}"))
        matrix.append(temp_row)

    return matrix


# FOR THE FUNCTION OF MULTIPLICATION BY A SCALAR
def mat_scalarmultiply(matrix, scalar):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = round(matrix[i][j] * scalar, 2)

    return matrix


# FOR THE FUNCTION OF MULTIPLICATION BY A MATRIX
def mat_matrixmultiply(mat_1, mat_2):
    matrix = []
    for i in range(len(mat_1)):
        temp_row = []
        for k in range(len(mat_2[0])):
            temp_element = []
            for j in range(len(mat_1[i])):
                temp_element.append(round(mat_1[i][j] * mat_2[j][k], 2))
            temp_row.append(sum(temp_element))
        matrix.append(temp_row)
    return matrix


# FOR TRANSPOSING A MATRIX
def mat_transpose(matrix):
    j = 0
    temp_matrix = []
    while j < len(matrix[0]):
        i = 0
        temp_row = []
        while i < len(matrix):
            temp_row.append(matrix[i][j])
            i += 1
        temp_matrix.append(temp_row)
        j += 1

    return temp_matrix


# FOR GENERATION A 2X2 MATRIX OF MINORS
def mat_minor(matrix):
    two_two = {1: [2, 2], 2: [2, 1], 3: [1, 2], 4: [1, 1]}

    f_matrix = []
    for k in range(1, len(matrix)**2 + 1):
        temp_row = []
        for a in range(1, len(matrix) + 1):
            for b in range(1, len(matrix) + 1):
                if [a, b] == two_two[k]:
                    temp_row.append(matrix[a-1][b-1])
        f_matrix.append(temp_row)
    temp_matrix = [[], []]

    for i in range(len(f_matrix)):
        if i < 2:
            temp_matrix[0].append(f_matrix[i][0])
        else:
            temp_matrix[1].append(f_matrix[i][0])

    f_matrix = temp_matrix
    return f_matrix


# FOR GENERATING A 3X3 MATRIX OF MINORS
def mat2_minor(matrix):
    pos = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    f_matrix = []
    for k in pos:
        x, y = k
        temp_row = []
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if x != i and y != j:
                    temp_row.append(matrix[i][j])
        temp_matrix = [[], []]
        for i in range(len(temp_row)):
            if i < 2:
                temp_matrix[0].append(temp_row[i])
            else:
                temp_matrix[1].append(temp_row[i])

        f_matrix.append(determinant(temp_matrix))
    temp_matrix = [[], [], []]
    col = 0
    for i in range(1, len(f_matrix) + 1):
        if i / 3 in [1.0, 2.0, 3.0]:
            temp_matrix[col].append(f_matrix[i - 1])
            col += 1
        else:
            temp_matrix[col].append(f_matrix[i - 1])
    f_matrix = temp_matrix
    return f_matrix


# FOR THE GENERATION OF A MATRIX OF COFACTORS
def mat_cofactor(matrix):
    if len(matrix) == 2:
        matrix = mat_minor(matrix)
    else:
        matrix = mat2_minor(matrix)

    for i in range(1, len(matrix) + 1):
        for j in range(1, len(matrix) + 1):
            matrix[i-1][j-1] = (-1)**(i+j)*(matrix[i-1][j-1])

    return matrix

# FOR CALCULATING THE DETERMINANT OF A MATRIX
def determinant(matrix):
    det = 0
    column = 0
    for l in range(len(matrix)):
        det += matrix[l][column]*mat_cofactor(matrix)[l][column]

    return det

# FOR GENERATING THE ADJOINT OF A MATRIX
def mat_adjoint(matrix):
    matrix = mat_transpose(mat_cofactor(matrix))

    return matrix

# FOR GENERATING THE INVERSE OF A MATRIX
def mat_invert(matrix):
    matrix = mat_scalarmultiply(mat_adjoint(matrix), 1/determinant(matrix))

    return matrix
# -----x-----x--END OF USER-DEFINED FUNCTIONS------- x-----x-----x----- #

use = True


print("\n!! WELCOME TO THE MATRICES AND DETERMINANT CALCULATOR ☆*: .｡. o(≧▽≦)o .｡.:*☆\n")


while use:
    operator = declaration()

    if operator == "1":
        # RANDOM MATRIX
        r1, c1 = matrix_rowcolumn()

        result = create_matrix(r1, c1, form="random")
        connect(result)
        matrix_print(result)

    elif operator in ["2", "3"]:
        # ADDITION OR SUBTRACTION
        sign = {"2": "+", "3": "-"}
        print("For Matrices:")
        r1, c1 = matrix_rowcolumn()

        print("Matrix 1:")
        m1 = create_matrix(r1, c1)
        print("Matrix 2:")
        m2 = create_matrix(r1, c1)

        result = mat_addorsub(m1, m2, sign[operator])
        matrix_print(m1, "original")
        matrix_print(m2, "original")
        connect(result)
        matrix_print(result)

    elif operator == "4":
        # SCALAR MULTIPLICATION
        r1, c1 = matrix_rowcolumn()
        m1 = create_matrix(r1, c1)
        num = int(input("Enter the multiplicative scalar: "))

        result = mat_scalarmultiply(m1, num)
        matrix_print(m1, "original")
        connect(result)
        matrix_print(result)

    elif operator == "5":
        # MATRIX MULTIPLICATION
        while True:
            print("Matrix 1:")
            r1, c1 = matrix_rowcolumn()
            print("Matrix 2:")
            r2, c2 = matrix_rowcolumn()

            if c1 == r2:
                print("Matrix 1:")
                m1 = create_matrix(r1, c1)
                print("Matrix 2:")
                m2 = create_matrix(r2, c2)

                result = mat_matrixmultiply(m1, m2)
                matrix_print(m1, "original")
                matrix_print(m2, "original")
                connect(result)
                matrix_print(result)
                break

            else:
                print("Error! Columns of Matrix 1 should be equal to Rows of Matrix 2.\n")
                continue

    elif operator == "6":
        # DETERMINANT
        while True:
            r1, c1 = matrix_rowcolumn()

            if r1 == c1:
                m1 = create_matrix(r1, c1)
                matrix_print(m1, "original")
                print(f"Determinant: {determinant(m1)}")
                break
            else:
                print("Error! Operation can be used only on Square Matrices.\n")
                continue

    elif operator == "7":
        # MINOR
        while True:
            r1, c1 = matrix_rowcolumn()

            if r1 == c1:
                m1 = create_matrix(r1, c1)
                matrix_print(m1, "original")
                if r1 == 2:
                    result = mat_minor(m1)
                    connect(result)
                    matrix_print(result)
                    break
                else:
                    result = mat2_minor(m1)
                    connect(result)
                    matrix_print(result)
                    break
            else:
                print("Error! Operation can be used only on Square Matrices.\n")
                continue

    elif operator == "8":
        # COFACTOR
        while True:
            r1, c1 = matrix_rowcolumn()

            if r1 == c1:
                m1 = create_matrix(r1, c1)
                result = mat_cofactor(m1)
                matrix_print(m1, "original")
                connect(result)
                matrix_print(result)
                break
            else:
                print("Error! Operation can be used only on Square Matrices.\n")
                continue

    elif operator == "9":
        # ADJOINT
        while True:
            r1, c1 = matrix_rowcolumn()

            if r1 == c1:
                m1 = create_matrix(r1, c1)
                result = mat_adjoint(m1)
                matrix_print(m1, "original")
                connect(result)
                matrix_print(result)
                break
            else:
                print("Error! Operation can be used only on Square Matrices.\n")
                continue

    elif operator == "10":
        # TRANSPOSE
        r1, c1 = matrix_rowcolumn()
        m1 = create_matrix(r1, c1)

        result = mat_transpose(m1)
        matrix_print(m1, "original")
        connect(result)
        matrix_print(result)

    elif operator == "11":
        # INVERT
        while True:
            m1 = []
            r1, c1 = matrix_rowcolumn()

            if r1 == c1:
                m1 = create_matrix(r1, c1)
                if determinant(m1) != 0:
                    result = mat_invert(m1)
                    matrix_print(m1, "original")
                    connect(result)
                    matrix_print(result)
                    break
                else:
                    print("Error! Inverse is not defined for Determinant = 0\n")
                    continue
            else:
                print("Error! Operation can be used only on Square Matrices.\n")
                continue

    else:
        print("Error! Enter from the given serial numbers.\n")
        continue

    while True:
        restart = input("Do you want to restart the program? (Yes/No): ").lower()

        if restart == "yes":
            print("alright.\n")
            break

        elif restart == "no":
            print("Bye...")
            use = False
            file.close()
            conn.close()
            break

        else:
            print("Enter only Yes/No!!")
            continue


'''

@author : Shweta Oak

Animation of robot 'ninja' writing the solution to the sudoku problem
'''

import turtle


ninja = turtle.Turtle()
ninja.speed(1) #modify the speed 



sudoku = "075000096030100075020970004740000308089000460306000017200063080590008020860000540"


def draw(num,initial_x,initial_y):
    if num == "1":
        ninja.penup()
        ninja.setposition(initial_x + 10,initial_y + 15)
        ninja.pendown()
        ninja.right(90)
        ninja.forward(10)
        ninja.left(90)
        ninja.penup()

    elif num == "2":
        ninja.penup()
        ninja.setposition(initial_x + 5,initial_y + 15)
        ninja.pendown()
        ninja.forward(10)
        ninja.right(90)
        ninja.forward(5)
        ninja.right(90)
        ninja.forward(10)
        ninja.left(90)
        ninja.forward(5)
        ninja.left(90)
        ninja.forward(10)
        ninja.penup()

    elif num == "3":
        ninja.penup()
        ninja.setposition(initial_x + 5,initial_y + 15)
        ninja.pendown()
        ninja.forward(10)
        ninja.right(90)
        ninja.forward(5)
        ninja.right(90)
        ninja.forward(10)
        ninja.backward(10)
        ninja.left(90)
        ninja.forward(5)
        ninja.right(90)
        ninja.forward(10)
        ninja.right(180)
        ninja.penup()

    elif num == "4":
        ninja.penup()
        ninja.setposition(initial_x + 15,initial_y + 15)
        ninja.pendown()
        ninja.left(45)
        ninja.backward(10)
        ninja.right(45)
        ninja.forward(13)
        ninja.penup()
        ninja.setposition(initial_x + 15,initial_y + 15)
        ninja.pendown()
        ninja.right(90)
        ninja.forward(15)
        ninja.left(90)
        ninja.penup()

    elif num == "5":
        ninja.penup()
        ninja.setposition(initial_x + 15,initial_y + 15)
        ninja.pendown()
        ninja.backward(10)
        ninja.right(90)
        ninja.forward(5)
        ninja.left(90)
        ninja.forward(10)
        ninja.right(90)
        ninja.forward(5)
        ninja.right(90)
        ninja.forward(10)
        ninja.right(180)
        ninja.penup()

    elif num == "6":
        ninja.penup()
        ninja.setposition(initial_x + 15,initial_y + 15)
        ninja.pendown()
        ninja.backward(10)
        ninja.right(90)
        ninja.forward(10)
        ninja.left(90)
        ninja.forward(10)
        ninja.left(90)
        ninja.forward(5)
        ninja.left(90)
        ninja.forward(10)
        ninja.right(180)
        ninja.penup()

    elif num == "7":
        ninja.penup()
        ninja.setposition(initial_x + 5,initial_y + 15)
        ninja.pendown()
        ninja.forward(10)
        ninja.left(45)
        ninja.backward(14)
        ninja.right(45)
        ninja.penup()

    elif num == "8":
        ninja.penup()
        ninja.setposition(initial_x + 15,initial_y + 15)
        ninja.pendown()
        ninja.backward(10)
        ninja.right(90)
        ninja.forward(5)
        ninja.left(90)
        ninja.forward(10)
        ninja.right(90)
        ninja.forward(5)
        ninja.right(90)
        ninja.forward(10)
        ninja.right(90)
        ninja.forward(5)
        ninja.right(90)
        ninja.forward(10)
        ninja.left(90)
        ninja.forward(5)
        ninja.right(90)
        ninja.penup()

    elif num == "9":
        ninja.penup()
        ninja.setposition(initial_x + 5,initial_y + 5)
        ninja.pendown()
        ninja.forward(10)
        ninja.left(90)
        ninja.forward(10)
        ninja.left(90)
        ninja.forward(10)
        ninja.left(90)
        ninja.forward(5)
        ninja.left(90)
        ninja.forward(10)


    else:
        ninja.penup()
        ninja.setposition(initial_x+5, initial_y+10)
        ninja.pendown()

        ninja.forward(10)
        ninja.penup()


j = 90
index = 0

while j > -90:
    i = -90
    while i < 90:

        initial_x= i;
        initial_y = j;

        number = sudoku[index]


        draw(number, initial_x, initial_y)

        index = index + 1
        i = i+ 20
    j = j - 20


ninja.setposition(200,200)


turtle.done()

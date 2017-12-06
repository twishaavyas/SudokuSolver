import cv2
import sudokuLines

cv2.namedWindow("SUDOKU Solver")
vc = cv2.VideoCapture(0)
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

flag = True
while True:
    print cv2.imshow("frame", frame)
    print not (flag)
    if((flag)):
        print "in"
        output = sudokuLines.Sudoku.solveSudoku(frame)
        print output, "lalalal"
        if(output):
             flag = False
    cv2.imshow("SUDOKU Solver", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(30)
    if key == 27:  # exit on ESC
        break
vc.release()
cv2.destroyAllWindows()

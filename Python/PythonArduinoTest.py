from __future__ import print_function
import serial
import time
import sunfish_with_undo as ai
import copy
import sys
import playerMove
import QRCodeRecognition.recognitionColor as recognition

BAUDRATE = 9600

# Protocol used to communicate with the arduino
NO_DATA = b''
MOVE_MADE = b'1'
MOVE_UNDO = b'2'
INVALID_MOVE = b'3'
MOVE_DONE = b'4'
DOING_MOVE = b'5'

positionListPrec = []

arduino = serial.Serial("/dev/tty.usbmodem1411",BAUDRATE,timeout=1)
time.sleep(2)
arduino.flushInput()

# Python 2 compatability
if sys.version_info[0] == 2:
    input = raw_input
    
def printMatrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))
    
def convert(move):
    """ converts the move in chess notation to the move understandable
    by the arduino

    eg : [0,2]=convert(e2e4)"""

    return [ord(move[2])-ord(move[0]),ord(move[3])-ord(move[1])]

def main():
    
    positionListPrec = recognition.parse('test1') #precedent positions in list format. Will take a picture and recognize the QR codes
    print (positionListPrec)
    
    if len(positionListPrec) != 8:
        print('error')
    
    #initialization of the chessboard
    pos = ai.Position(ai.initial,0,(True,True),(True,True),0,0)
    prevPos = copy.deepcopy(pos)
    
    print('Make a move, then press button')
    
    while True:
        data=arduino.readline()
        #moveMade = input('move made ?')
        #data = MOVE_MADE
        if (data == MOVE_MADE):
            # We add some spaces to the board before we print it.
            # That makes it more readable and pleasing.
            print(' '.join(pos.board))
            # we got the command that the player has done his move take picture
            # extract the data and send the move to the chess engine
            
            positionList = recognition.parse('test1')
            printMatrix(positionListPrec)
            print (' ')
            printMatrix(positionList)
            crdn = playerMove.getMove(positionListPrec, positionList)
            print (crdn)
            
            # for now we just ask the user to input the move by hand since the
            # webcam code is not done yet
            #crdn = input("Your move: ")

            # ctlvar    = '0' => destination case is empty (default)
            #           = '1' => destination case is not empty
            #           = '2' => invalid move
            ctrlvar = '0'
            
            try:
                move = ai.parse(crdn[0:2]), ai.parse(crdn[2:4])
            except ValueError:
                print("Invalid Move !")
            # if the move is not allowed then send a flag to the arduino
            # to notify the user
            if move not in pos.genMoves():
                crtlvar = '2'
                arduino.write((ctrlvar+'0000').encode())
                print("Invalid Move")
                positionListPrec = copy.copy(positionList)
            else:
                
                print("You moved  a: ",pos.board[move[0]])
                
                #check if there is a piece on the place where the new piece is
                #being moved
                if (pos.board[move[1]] != '.'):
                    print("you just destroyed my :" + pos.board[move[1]])
                    
                prevPos = copy.deepcopy(pos)  
                pos = pos.move(move)
                # After our move we rotate the board and print it again.
                # This allows us to see the effect of our move.
                print(' '.join(pos.rotate().board))

                # Fire up the engine to look for a move.
                move, score = ai.search(pos)
                if score <= -ai.MATE_VALUE:
                    #play song
                    print("You won")
                    break
                if score >= ai.MATE_VALUE:
                    #play song
                    print("You lost")
                    break

                # The black player moves from a rotated position, so we have to
                # 'back rotate' the move before printing it.
                print("My move:", ai.render(119-move[0]) + ai.render(119-move[1]))

                #play sound here when the player has moved, the piece that is going
                #to be moved is given by pos.board[move[0]]
                print("Ai moved a: ",pos.board[move[0]])
                lastMovedPiece = pos.board[move[0]]
                if (pos.board[move[1]] != '.'):
                    print("I just destroyed your :" + pos.board[move[1]])
                    ctrlvar = '1'
                pos = pos.move(move)
                print(' '.join(pos.board))
                #send the move to the arduino
                movement = ai.render(119-move[0]) + ai.render(119-move[1])
                arduino.write((ctrlvar + makeArduinoConversion(movement)).encode())
                
                del positionListPrec[:]
                printMatrix(positionListPrec)
                positionListPrec = moveAI(makeArduinoConversion(movement), positionList)
                printMatrix(positionListPrec)
        
        elif (data == MOVE_UNDO):
            #player used undo
            pos = copy.deepcopy(prevPos)
            print(' '.join(pos.board))

        elif (data == DOING_MOVE):
            #here is where we play the sound when the arduino is moving a chess
            #for which we have a sound
            # for now we just print it
            print(lastMovedPiece,"is moving")

def moveAI(move, liste):
    ret = copy.copy(liste)
    print (move)
    ret[7-(int(move[1])-1)][(int(move[0])-1)] = 0
    ret[7-(int(move[3])-1)][(int(move[2])-1)] = 1
    return ret

def makeArduinoConversion(movement):

    result = '';
    for i in range(len(movement)):
        if i in range(0,4,2):
            result += chr(ord(movement[i]) - 48)
        else:
            result += movement[i]
    return result

            
main()

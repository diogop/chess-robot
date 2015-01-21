from copy import deepcopy
import random
import decode as d

liste = [[None]*8 for _ in range(8)]
lettres = ['A', 'B']

def printMatrix(matrix):
	s = [[str(e) for e in row] for row in matrix]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table = [fmt.format(*row) for row in s]
	print '\n'.join(table)

def getMove(list1, list2):
    differences = []

    for k in range(8):
        for l in range(8):
            if list1[k][l] != list2[k][l]:
                differences.append([k,l])

    if len(differences)==2:
        if list2[differences[0][0]][differences[0][1]] == 0:
            #print str(list2[differences[1][0]][differences[1][1]])+' from '+str(differences[0])+' to '+str(differences[1])
            return d.decode(differences[0],differences[1])
        else :
            #print str(list2[differences[0][0]][differences[0][1]])+' from '+str(differences[1])+' to '+str(differences[0])
            return d.decode(differences[1],differences[0])        

def generate():

    ## GENERATE FIRST LIST

    for i in range(8):
        for j in range(8):
            if random.randint(0,1)>0:
                player = lettres[random.randint(0,1)]
                piece = random.randint(1,6)
                liste[i][j] = str(player)+str(piece)
            else:
                liste[i][j] = 0

    ## GENERATE SECOND LIST

    liste2 = deepcopy(liste)
    for i in range(7):
        if liste2[0][i] == 0 and liste2[0][i+1] != 0:
            liste2[0][i], liste2[0][i+1] = liste2[0][i+1], liste2[0][i]
            break
    return liste, liste2

## DIFFERENCES

#print(getMove(liste,liste2))

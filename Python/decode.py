def decode(posFrom,posTo):
    """ returns the move from posFrom to posTo in chess notations
        (list) posFrom = origin of the move (eg.[0,1])
        (list) posTo   = destination of the move (eg.[0,2])
    """
    ASCII_a = 97
    ASCII_0 = 48
    result = ''
    result = result + chr(posFrom[1]+ ASCII_a)
    result = result + chr(convert_numbers(posFrom[0]) + ASCII_0)
    result = result + chr(posTo[1]+ ASCII_a)
    result = result + chr(convert_numbers(posTo[0]) + ASCII_0)
    return result


def convert_numbers(num):
    """ in lists numbers are increasing from top to bottom while for the chess
        engine it is increasing. lowest row is 1 while top row is 8. With lists
        it's top row 0 and lowest row 7

    """
    return 8- (num%8)

    

def multiply(m1, m2):
    result = []
    
    for x in range(len(m1)):
        row = []
        for y in range(len(m1[0])):
            value = ''
            for n in range(len(m1)):
                a = "%s" % m1[x][n]
                b = "%s" % m2[n][y]
                
                if a != "0" and b != "0":
                    a = '%s' % a
                    b = '%s' % b
                    sign = 1
                
                    if a.startswith('-'):
                        sign *= -1
                        a = a[1:]
                    if b.startswith('-'):
                        sign *= -1
                        b = b[1:]
                    
                    if sign == 1:
                        if value: value += " + "
                    else:
                        value += " - " if value else "-"
                    
                    if a == '1':
                        value += "%s" % b
                    elif b == '1':
                        value += "%s" % a
                    else:
                        if ' + ' in a or ' - ' in a: a = "(%s)" % a
                        if ' + ' in b or ' - ' in b: b = "(%s)" % b
                        value += "%s.%s" % (a, b)

            if not value: value = 0
            row.append(value)
        result.append(row)
        
    return result

def print_matrix(matrix):
    for row in matrix:
        print()"\t".join("%s" % s for s in row))

if __name__ == '__main__':
    rotate = [
        ['c', '-s', 0, 0],
        ['s', 'c',  0, 0],
        [0,    0,   1, 0],
        [0,    0,   0, 1]]

    translate1 = [
        [1, 0, 0, '-dx'],
        [0, 1, 0, '-dy'],
        [0, 0, 1, '-dz'],
        [0, 0, 0, 1]]

    translate2 = [
        [1, 0, 0, 'dx'],
        [0, 1, 0, 'dy'],
        [0, 0, 1, 'dz'],
        [0, 0, 0, 1]]

    coords = [
        ['x'],
        ['y'],
        ['z'],
        [1]]

    result = multiply(rotate, translate1)
    result = multiply(translate2, result)
    result = multiply(result, coords)
    print_matrix(result)
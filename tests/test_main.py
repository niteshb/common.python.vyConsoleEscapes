import vyConsoleEscapes as vce

headerLength = 120
tableHeaderColor = '404040'
def printHeader(txt, startChar='\n'):
    print(startChar, end='')
    print(vce.format(('{0:<'+f'{headerLength}'+'}').format(': ' + txt), fgColor='white', bgColor='b146c2', flags=vce.BOLD), end='')
    print('')

def printSubHeader(txt, startChar=''):
    print(startChar, end='')
    print(vce.format(('{0:<'+f'{headerLength}'+'}').format(':: ' + txt), fgColor='white', bgColor='ca5010', flags=vce.BOLD) + '\n', end='')

def testBasicCodes():
    printHeader('Basic ANSI Color Codes: 8 colors * 2 variants = 16 Codes', startChar='')
    print(vce.format('       | SB | S  | N  | SU | S  | N  |', bgColor=tableHeaderColor, flags=vce.BOLD), end='')
    print('')
    for color in vce.VyConsoleEscapeColorDiffs:
        txt  = vce.format(f'{color:>7}' + vce.esc.reset + '|', bgColor=tableHeaderColor, flags=vce.BOLD)
        txt += vce.format(' AA ' + vce.esc.reset + '|', fgColor=color, flags=vce.BOLD)
        txt += vce.format(' AA ' + vce.esc.reset + '|', fgColor=color)
        txt += vce.format(' AA ' + vce.esc.reset + '|', fgColor=color + '-normal')
        txt += vce.format(' AA ' + vce.esc.reset + '|', fgColor=color, flags=vce.UNDERLINE)
        txt += vce.format('    ' + vce.esc.reset + '|', bgColor=color)
        txt += vce.format('    ' + vce.esc.reset + '|', bgColor=color + '-normal')
        print(txt)

def testExtendedCodes():
    printHeader('08 Bit Extended Codes: 256 Codes')
    printSubHeader('000-015: Base Colors')
    print(vce.esc.bold + vce.esc.underline + ' '*6 + '|', end='')
    for color, diff in vce.VyConsoleEscapeColorDiffs.items():
        print(f'{color:^9}' + '|', end='')
    print(vce.esc.reset)
    for i, variant in enumerate(['normal', 'strong']):
        print(vce.format(f'{variant}', flags=vce.BOLD) + '|', end='')
        for color, diff in vce.VyConsoleEscapeColorDiffs.items():
            key = f'{color}-{variant}-256'
            print(vce.esc.fg[key] + '  AAAAA  |', end='')
        print(vce.esc.resetFg)
    for i, variant in enumerate(['normal', 'strong']):
        print(vce.format(f'{variant}|', flags=vce.BOLD), end='')
        for color, diff in vce.VyConsoleEscapeColorDiffs.items():
            key = f'{color}-{variant}-256'
            print(vce.esc.bg[key] + '         ' + vce.esc.reset + '|', end='')
        print(vce.esc.resetBg)

    printSubHeader('016-231: 6*6*6=216 RGB Colors', startChar='\n')
    print(' ' + (vce.format('   0 1 2 3 4 5', fgColor='00c0ff', bgColor='404040', flags=vce.BOLD) + ' ')*6)
    for g in range(0, 6):
        for r in range(0, 6):
            print(vce.esc.reset + vce.esc.bold + ' ' + vce.esc.bg['404040'], end='')
            print(vce.esc.fg['ff2070'] + f'{r}' + vce.esc.fg['80ff80'] + f'{g}' + vce.esc.reset, end='')
            for b in range(0, 6):
                rgb = r * 100 + g * 10 + b
                print(vce.esc.fg[rgb] + 'AA', end='')
        print(vce.esc.reset)

    for g in range(0, 6):
        for r in range(0, 6):
            print(vce.esc.reset + vce.esc.bold + ' ' + vce.esc.bg['404040'], end='')
            print(vce.esc.fg['ff2070'] + f'{r}' + vce.esc.fg['80ff80'] + f'{g}' + vce.esc.reset, end='')
            for b in range(0, 6):
                rgb = r * 100 + g * 10 + b
                print(vce.esc.bg[rgb] + f'  ', end='')
        print(vce.esc.reset)

    printSubHeader('232-255: 24 Shades of Grey', startChar='\n')
    for i in range(24):
        print(f'{i:2}|', end='')
    print(vce.esc.reset)
    for i in range(24):
        print(vce.esc.fg['grey-'+str(i)] + 'AA' + vce.esc.reset + '|', end='')
    print(vce.esc.reset)
    for i in range(24):
        print(vce.esc.bg['grey-'+str(i)] + '  ' + vce.esc.reset + '|', end='')
    print(vce.esc.reset)

    printHeader('24 Bit Extended Codes: 2^24 colors for text and background each')
    printSubHeader('Showcase: 256 Shades of Red')
    cols = 32
    print(vce.esc.underline + '  |' + ''.join([f'{i:02}|' for i in range(cols)]) + vce.esc.reset)
    for row in range(256//cols):
        print(vce.esc.underline + f'{row:02}|' + vce.esc.reset, end='')
        for col in range(cols):
            red = row * cols + col
            print(vce.esc.bg[f'{red:02x}0000'] + '  ' + vce.esc.resetBg + ' ', end='')
        print(vce.esc.reset)

def testMixed():
    printHeader('Mixed Colors Test')
    txt  = vce.format(' I love my India ', fgColor='white', bgColor='red', flags=vce.UNDERLINE|vce.INVERSE|vce.NO_UNDERLINE|vce.BOLD)
    txt += vce.format(' I love my India ', fgColor='blue', bgColor='white', flags=vce.INVERSE|vce.NO_INVERSE|vce.BOLD)
    txt += vce.format(' I love my India ', fgColor='white', bgColor='green', flags=vce.BOLD)
    print(txt, end='')

if __name__ == '__main__':
    testBasicCodes()
    testExtendedCodes()
    testMixed()

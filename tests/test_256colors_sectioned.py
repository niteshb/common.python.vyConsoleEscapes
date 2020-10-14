import sys
from collections import namedtuple, Counter
RGB_HSL = namedtuple('RGB_HSL', 'rgb hsl')

def hsl(r, g, b): # 0.0 <= r,g,b <= 1.0
    if r == g and g == b:
        hue = -60
    if r >= g and g >= b and r != b:
        hue = 60 * (g-b)/(r-b)
    if g > r and r >= b:
        hue = 60 * (2 - (r-b)/(g-b))
    if g >= b and b > r:
        hue = 60 * (2 + (b-r)/(g-r))
    if b > g and g > r:
        hue = 60 * (4 - (g-r)/(b-r))
    if b > r and r >= g:
        hue = 60 * (4 + (r-g)/(b-g))
    if r >= b and b > g:
        hue = 60 * (6 - (b-g)/(r-g))
    # luminosity
    luminosity = (max(r, g, b) + min(r, g, b)) / 2
    # saturation
    if 0 < luminosity and luminosity < 1:
        saturation = (max(r, g, b) - min(r, g, b)) / (1 - abs(2 * luminosity - 1))
    elif luminosity in [0, 1]:
        saturation = 0
    return (int(hue), int(saturation*100), int(luminosity*100))

for i in range(0, 2):
    for j in range(0, 8):
        code = str(i * 8 + j)
        sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
    print(u"\u001b[0m")

colors = {}
for r in range(0, 6):
    for g in range(0, 6):
        for b in range(0, 6):
            code = 16 + 36 * r + 6 * g + b
            colors[code] = RGB_HSL(rgb=(r, g, b), hsl=hsl(r/5, g/5, b/5))

for r in range(0, 6):
    for g in range(0, 6):
        for b in range(0, 6):
            code = 16 + 36 * r + 6 * g + b
            code = str(code)
            sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        print(u"\u001b[0m")

for i in range(0, 3):
    for j in range(0, 8):
        code = str(232 + i * 8 + j)
        sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
    print(u"\u001b[0m")


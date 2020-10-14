
# https://en.wikipedia.org/wiki/ANSI_escape_code
# ==============================================================================
# 8 BIT CODES: 256 codes
# ==============================================================================
# ESC[38;5;⟨n⟩ m Select foreground color
# ESC[48;5;⟨n⟩ m Select background color
#   0-  7:  standard colors (as in ESC [ 30–37 m)
#   8- 15:  high intensity colors (as in ESC [ 90–97 m)
#  16-231:  6 × 6 × 6 cube (216 colors): 16 + 36 × r + 6 × g + b (0 ≤ r, g, b ≤ 5)
# 232-255:  grayscale from black to white in 24 steps

# https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences#screen-colors
# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#16-colors

strEscape = '\033'
unicodeEscape = u'\u001b'
# on windows cmd.exe press 'CTRL+[' for 'Escape'. Normal keybord escape input will clear the command

class VyConsoleEscapes:
    colorDiffs = {
        'black': 0,
        'red': 1,
        'green': 2,
        'yellow': 3,
        'blue': 4,
        'magenta': 5,
        'cyan': 6,
        'white': 7,
    }
    reset = 0           # Returns all attributes to the default state prior to modification
    bold = 1            # Applies brightness/intensity flag to foreground color
    underline = 4       # Adds underline
    inverse = 7         # Swaps foreground and background colors
    noUnderline = 24    # Removes underline
    positive = 27       # No negative/inverse, returns foreground/background to normal
    foreground8bit = 38     # Foreground Extended, applies extended color value to the foreground
    background8bit = 48     # Background Extended, applies extended color value to the background
    foregroundDefault = 39  # Foreground Default	Applies only the foreground portion of the defaults (see 0)
    backgroundDefault = 49  # Background Default	Applies only the background portion of the defaults (see 0)

    foreground = {}
    background = {}

vce = VyConsoleEscapes
reset = '\033[0m'

for color, diff in VyConsoleEscapes.colorDiffs.items():
    vce.foreground['normal-' + color] = 30 + diff
    vce.background['normal-' + color] = 40 + diff
    vce.foreground['strong-' + color] = 90 + diff
    vce.background['strong-' + color] = 100 + diff

NO_FLAGS = 0
UNDERLINE = 1
BOLD = 2
INVERSE = 4
NO_UNDERLINE = 2 ^ 30
NO_INVERSE = 2 ^ 31

def format(text, fgColor=None, fgVariant='strong', bgColor=None, bgVariant='strong', flags=NO_FLAGS):
    escapedStr = ''
    if fgColor:
        fgCode = vce.foreground[f'{fgVariant}-{fgColor}']
        escapedStr += f'\033[{fgCode}m'
    if bgColor:
        bgCode = vce.background[f'{bgVariant}-{bgColor}']
        escapedStr += f'\033[{bgCode}m'
    if flags & UNDERLINE:
        escapedStr += f'\033[{vce.underline}m'
    if flags & BOLD:
        escapedStr += f'\033[{vce.bold}m'
    if flags & INVERSE:
        escapedStr += f'\033[{vce.inverse}m'
    if flags & NO_INVERSE:
        escapedStr += f'\033[{vce.positive}m'
    if flags & NO_UNDERLINE:
        escapedStr += f'\033[{vce.noUnderline}m'
    escapedStr += text + reset
    return escapedStr

def fgColor256(text, color):
    pass


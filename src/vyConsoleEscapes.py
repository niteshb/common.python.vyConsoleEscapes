
import re
# https://en.wikipedia.org/wiki/ANSI_escape_code
# https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences#screen-colors
# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#16-colors

strEscape = '\033'
unicodeEscape = u'\u001b'
# on windows cmd.exe press 'CTRL+[' for 'Escape'. Normal keybord escape input will clear the command

VyConsoleEscapeColorDiffs = {
    'black': 0,
    'red': 1,
    'green': 2,
    'yellow': 3,
    'blue': 4,
    'magenta': 5,
    'cyan': 6,
    'white': 7,
}

class vyColorDict():
    def __init__(self, normalColorsOffset, strongColorsOffset, extendedColorsOffset):
        self._dict = {}
        self.extendedColorsOffset = extendedColorsOffset
        for color, diff in VyConsoleEscapeColorDiffs.items():
            # foreground normal colors e.g. esc.fg.red0 = esc.fg.red_normal
            # background normal colors e.g. esc.bg.red0 = esc.bg.red_normal
            self[color+'-normal'] = self[color+'0'] = f'\033[{normalColorsOffset+diff}m'
            # foreground strong colors e.g. esc.fg.red = esc.fg.red1 = esc.fg.red_strong
            # background strong colors e.g. esc.bg.red = esc.bg.red1 = esc.bg.red_strong
            self[color+'-strong'] = self[color+'1'] = self[color] = f'\033[{strongColorsOffset+diff}m'
        
        self['grey'] = self['gray'] = self['black-strong']
        # ==============================================================================
        # Extended Codes: 8 bits, 256 codes
        # ==============================================================================
        # ESC[38;5;⟨n⟩m : Foreground colors
        # ESC[48;5;⟨n⟩m : Background colors
        #   0-  7: Normal colors
        #          key: e.g. 'white-normal-256'
        #   8- 15: Strong colors
        #          key: e.g. 'white-strong-256'
        #  16-231: 216 RGB colors : 16+ 36R + 6G + B : 0 ≤ R, G, B ≤ 5
        #          key: e.g. 0, 500, 231
        # 232-255: Grayscale in 24 steps, from black to white
        #          key: e.g. grey-0, grey-11, grey-23

        for i, variant in enumerate(['normal', 'strong']):
            for color, diff in VyConsoleEscapeColorDiffs.items():
                code = i * 8 + diff
                key = f'{color}-{variant}-256'
                self[key] = f'\033[{extendedColorsOffset};5;{code}m'

        for r in range(0, 6):
            for g in range(0, 6):
                for b in range(0, 6):
                    key = r * 100 + g * 10 + b
                    code = 16 + 36 * r + 6 * g + b
                    self[key] = f'\033[{extendedColorsOffset};5;{code}m'

        for shade in range(24):
            self['grey-'+str(shade)] = self['gray-'+str(shade)] = f'\033[{extendedColorsOffset};5;{232+shade}m'
        # ==============================================================================
        # Extended Codes: 24 bit RGB colors
        # ==============================================================================
        # this we will handle through getitem, storing it is very memory intensive
        # key: e.g. 'ffffff', 'ff0011', '000000'

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        if key in self._dict:
            return self._dict[key]
        if type(key) is str:
            mo = re.match('[0-9a-fA-F]{6}', key)
            if mo:
                r, g, b = tuple(int(key[i:i+2], 16) for i in (0, 2, 4))
                return f'\033[{self.extendedColorsOffset};2;{r};{g};{b}m'
        raise KeyError

class VyConsoleEscapes:
    reset       = '\033[0m'     # Returns all attributes to the default state prior to modification
    bold        = '\033[1m'     # Applies brightness/intensity flag to foreground color
    underline   = '\033[4m'     # Adds underline
    inverse     = '\033[7m'     # Swaps foreground and background colors
    noUnderline = '\033[24m'    # Removes underline
    positive    = '\033[27m'    # No negative/inverse, returns foreground/background to normal
    resetFg     = '\033[39m'    # Foreground Default, applies only the foreground portion of the defaults
    resetBg     = '\033[49m'    # Background Default, applies only the background portion of the defaults
    fg = vyColorDict(30, 90, 38)
    bg = vyColorDict(40, 100, 48)

esc = VyConsoleEscapes

# ==============================================================================
# Quick utility string format function
# ==============================================================================
NO_FLAGS = 0
UNDERLINE = 1
BOLD = 2
INVERSE = 4
NO_UNDERLINE = 2 ^ 30
NO_INVERSE = 2 ^ 31

def format(text, fgColor=None, bgColor=None, flags=NO_FLAGS):
    escapedStr = ''
    if fgColor:
        escapedStr += esc.fg[fgColor]
    if bgColor:
        escapedStr += esc.bg[bgColor]
    if flags & UNDERLINE:
        escapedStr += esc.underline
    if flags & BOLD:
        escapedStr += esc.bold
    if flags & INVERSE:
        escapedStr += esc.inverse
    if flags & NO_INVERSE:
        escapedStr += esc.positive
    if flags & NO_UNDERLINE:
        escapedStr += esc.noUnderline
    escapedStr += text + esc.reset
    return escapedStr

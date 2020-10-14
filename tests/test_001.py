import pytest
import vyConsoleEscapes as vce

def test_001():
    txt = vce.format(' I am the best ', fgColor='white', bgColor='red', flags=vce.UNDERLINE|vce.INVERSE|vce.NO_UNDERLINE|vce.BOLD)
    txt += vce.format(' I am the best ', fgColor='blue', bgColor='white', flags=vce.INVERSE|vce.NO_INVERSE|vce.BOLD)
    txt += vce.format(' I am the best ', fgColor='white', bgColor='green', flags=vce.BOLD)
    print(txt)

if __name__ == '__main__':
    test_001()
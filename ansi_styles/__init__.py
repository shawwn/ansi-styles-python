__version__ = '0.2.2'

from argparse import Namespace
import re
import math

ANSI_BACKGROUND_OFFSET = 10


def wrapAnsi16(offset=0):
    def wrapAnsi16_wrapper(code):
        return '\u001B[{}m'.format(code + offset)
    return wrapAnsi16_wrapper


def wrapAnsi256(offset=0):
    def wrapAnsi256_wrapper(code):
        return '\u001B[{};5;{}m'.format(38 + offset, code)
    return wrapAnsi256_wrapper


def wrapAnsi16m(offset=0):
    def wrapAnsi16m_wrapper(red, green, blue):
        return '\u001B[{};2;{};{};{}m'.format(38 + offset, red, green, blue)
    return wrapAnsi16m_wrapper


def assembleStyles():
    codes = {}
    styles = Namespace(
        modifier=Namespace(
            reset=[0, 0],
            # 21 isn't widely supported and 22 does the same thing
            bold=[1, 22],
            dim=[2, 22],
            italic=[3, 23],
            underline=[4, 24],
            overline=[53, 55],
            inverse=[7, 27],
            hidden=[8, 28],
            strikethrough=[9, 29]
        ),
        color=Namespace(
            black=[30, 39],
            red=[31, 39],
            green=[32, 39],
            yellow=[33, 39],
            blue=[34, 39],
            magenta=[35, 39],
            cyan=[36, 39],
            white=[37, 39],

            # Bright color
            blackBright=[90, 39],
            redBright=[91, 39],
            greenBright=[92, 39],
            yellowBright=[93, 39],
            blueBright=[94, 39],
            magentaBright=[95, 39],
            cyanBright=[96, 39],
            whiteBright=[97, 39]
        ),
        bgColor=Namespace(
            bgBlack=[40, 49],
            bgRed=[41, 49],
            bgGreen=[42, 49],
            bgYellow=[43, 49],
            bgBlue=[44, 49],
            bgMagenta=[45, 49],
            bgCyan=[46, 49],
            bgWhite=[47, 49],

            # Bright color
            bgBlackBright=[100, 49],
            bgRedBright=[101, 49],
            bgGreenBright=[102, 49],
            bgYellowBright=[103, 49],
            bgBlueBright=[104, 49],
            bgMagentaBright=[105, 49],
            bgCyanBright=[106, 49],
            bgWhiteBright=[107, 49]
        )
    )

    # Alias bright black as gray (and grey)
    styles.color.gray = styles.color.blackBright
    styles.bgColor.bgGray = styles.bgColor.bgBlackBright
    styles.color.grey = styles.color.blackBright
    styles.bgColor.bgGrey = styles.bgColor.bgBlackBright


    for groupName, group in dict(styles.__dict__).items():
        for styleName, style in group.__dict__.items():
            styles.__dict__[styleName] = Namespace(
                open = '\u001B[{}m'.format(style[0]),
                close = '\u001B[{}m'.format(style[1])
            )

            group.__dict__[styleName] = styles.__dict__[styleName]

            codes[style[0]] = style[1]

        styles.__dict__[groupName] = group

    styles.codes = codes

    styles.color.close = '\u001B[39m'
    styles.bgColor.close = '\u001B[49m'

    styles.color.ansi = wrapAnsi16()
    styles.color.ansi256 = wrapAnsi256()
    styles.color.ansi16m = wrapAnsi16m()
    styles.bgColor.ansi = wrapAnsi16(ANSI_BACKGROUND_OFFSET)
    styles.bgColor.ansi256 = wrapAnsi256(ANSI_BACKGROUND_OFFSET)
    styles.bgColor.ansi16m = wrapAnsi16m(ANSI_BACKGROUND_OFFSET)

    # From https://github.com/Qix-/color-convert/blob/3f0e0d4e92e235796ccb17f6e85c72094a651f49/conversions.js
    def rgbToAnsi256(red, green, blue):
        # We use the extended greyscale palette here, with the exception of
        # black and white. normal palette only has 4 greyscale shades.
        if red == green and green == blue:
            if red < 8:
                return 16

            if red > 248:
                return 231

            return round(((red - 8) / 247) * 24) + 232

        return 16 + \
            (36 * round(red / 255 * 5)) + \
            (6 * round(green / 255 * 5)) + \
            round(blue / 255 * 5)

    def hexToRgb(hex):
        match = re.search(r'(?P<colorString>[a-f\d]{6}|[a-f\d]{3})', hex, re.IGNORECASE)
        if match is None:
            return [0, 0, 0]
        colorString = match.groupdict()['colorString']
        if len(colorString) == 3:
            colorString = ''.join([c + c for c in colorString])
        integer = int(colorString, 16)
        return [
            (integer >> 16) & 0xFF,
            (integer >> 8) & 0xFF,
            integer & 0xFF
        ]

    def hexToAnsi256(hex):
        return styles.rgbToAnsi256(*styles.hexToRgb(hex))

    def ansi256ToAnsi(code):
        if code < 8:
            return 30 + code

        if code < 16:
            return 90 + (code - 8)

        if code >= 232:
            red = (((code - 232) * 10) + 8) / 255
            green = red
            blue = red
        else:
            code -= 16

            remainder = code % 36

            red = math.floor(code / 36) / 5
            green = math.floor(remainder / 6) / 5
            blue = (remainder % 6) / 5

        value = max(red, green, blue) * 2

        if value == 0:
            return 30

        result = 30 + ((round(blue) << 2) | (round(green) << 1) | round(red))

        if value == 2:
            result += 60

        return result

    def rgbToAnsi(red, green, blue):
        return styles.ansi256ToAnsi(styles.rgbToAnsi256(red, green, blue))

    def hexToAnsi(hex):
        return styles.ansi256ToAnsi(styles.hexToAnsi256(hex))

    styles.rgbToAnsi256 = rgbToAnsi256
    styles.hexToRgb = hexToRgb
    styles.hexToAnsi256 = hexToAnsi256
    styles.ansi256ToAnsi = ansi256ToAnsi
    styles.rgbToAnsi = rgbToAnsi
    styles.hexToAnsi = hexToAnsi

    return styles


ansiStyles = assembleStyles()

# ansi-styles

> [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors_and_Styles) for styling strings in the terminal

A port of the Node.js package [`ansi-styles`](https://github.com/chalk/ansi-styles) to Python.

## Install

```
python3 -m pip install -U ansi-styles
```

## Usage

```py
from ansi_styles import ansiStyles as styles

print(f'{styles.green.open}Hello world!{styles.green.close}')

# Color conversion between 256/truecolor
# NOTE: When converting from truecolor to 256 colors, the original color
#       may be degraded to fit the new color palette. This means terminals
#       that do not support 16 million colors will best-match the
#       original color.
print(f'{styles.color.ansi(styles.rgbToAnsi(199, 20, 250))}Hello World{styles.color.close}')
print(f'{styles.color.ansi256(styles.rgbToAnsi256(199, 20, 250))}Hello World{styles.color.close}')
print(f'{styles.color.ansi16m(*styles.hexToRgb("#abcdef"))}Hello World{styles.color.close}')
```

## License

MIT

## Contact

A library by [Shawn Presser](https://www.shawwn.com). If you found it useful, please consider [joining my patreon](https://www.patreon.com/shawwn)!

My Twitter DMs are always open; you should [send me one](https://twitter.com/theshawwn)! It's the best way to reach me, and I'm always happy to hear from you.

- Twitter: [@theshawwn](https://twitter.com/theshawwn)
- Patreon: [https://www.patreon.com/shawwn](https://www.patreon.com/shawwn)
- HN: [sillysaurusx](https://news.ycombinator.com/threads?id=sillysaurusx)
- Website: [shawwn.com](https://www.shawwn.com)


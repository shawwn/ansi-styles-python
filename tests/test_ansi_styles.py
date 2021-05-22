from ansi_styles import ansiStyles


def eq(a, b):
    assert a == b


def test_return_ansi_escape_codes():
    assert ansiStyles.green.open == '\u001B[32m'
    assert ansiStyles.bgGreen.open == '\u001B[42m'
    assert ansiStyles.green.close == '\u001B[39m'
    assert ansiStyles.gray.open == ansiStyles.grey.open


def test_group_related_codes_into_categories():
    assert ansiStyles.color.magenta == ansiStyles.magenta
    assert ansiStyles.bgColor.bgYellow == ansiStyles.bgYellow
    assert ansiStyles.modifier.bold == ansiStyles.bold


# test('groups should not be enumerable', t => {
# 	t.not(Object.getOwnPropertyDescriptor(ansiStyles, 'modifier'), undefined);
# 	t.false(Object.keys(ansiStyles).includes('modifier'));
# });


def test_support_conversion_to_ansi_16_colors():
    assert ansiStyles.color.ansi(ansiStyles.rgbToAnsi(255, 255, 255)) == '\u001B[97m'
    assert ansiStyles.color.ansi(ansiStyles.hexToAnsi('#990099')) == '\u001B[35m'
    assert ansiStyles.color.ansi(ansiStyles.hexToAnsi('#FF00FF')) == '\u001B[95m'

    assert ansiStyles.bgColor.ansi(ansiStyles.rgbToAnsi(255, 255, 255)) == '\u001B[107m'
    assert ansiStyles.bgColor.ansi(ansiStyles.hexToAnsi('#990099')) == '\u001B[45m'
    assert ansiStyles.bgColor.ansi(ansiStyles.hexToAnsi('#FF00FF')) == '\u001B[105m'


def test_support_conversion_to_ansi_256_colors():
    assert ansiStyles.color.ansi256(ansiStyles.rgbToAnsi256(255, 255, 255)) == '\u001B[38;5;231m'
    assert ansiStyles.color.ansi256(ansiStyles.hexToAnsi256('#990099')) == '\u001B[38;5;127m'
    assert ansiStyles.color.ansi256(ansiStyles.hexToAnsi256('#FF00FF')) == '\u001B[38;5;201m'

    assert ansiStyles.bgColor.ansi256(ansiStyles.rgbToAnsi256(255, 255, 255)) == '\u001B[48;5;231m'
    assert ansiStyles.bgColor.ansi256(ansiStyles.hexToAnsi256('#990099')) == '\u001B[48;5;127m'
    assert ansiStyles.bgColor.ansi256(ansiStyles.hexToAnsi256('#FF00FF')) == '\u001B[48;5;201m'


def test_support_conversion_to_ansi_16_million_colors():
    assert ansiStyles.color.ansi16m(255, 255, 255) == '\u001B[38;2;255;255;255m'
    assert ansiStyles.color.ansi16m(*ansiStyles.hexToRgb('#990099')) == '\u001B[38;2;153;0;153m'
    assert ansiStyles.color.ansi16m(*ansiStyles.hexToRgb('#FF00FF')) == '\u001B[38;2;255;0;255m'

    assert ansiStyles.bgColor.ansi16m(255, 255, 255) == '\u001B[48;2;255;255;255m'
    assert ansiStyles.bgColor.ansi16m(*ansiStyles.hexToRgb('#990099')) == '\u001B[48;2;153;0;153m'
    assert ansiStyles.bgColor.ansi16m(*ansiStyles.hexToRgb('#FF00FF')) == '\u001B[48;2;255;0;255m'


def test_16_256_16m_color_close_escapes():
    assert ansiStyles.color.close == '\u001B[39m'
    assert ansiStyles.bgColor.close == '\u001B[49m'


def test_export_raw_ansi_escape_codes():
    assert ansiStyles.codes.get(0) == 0
    assert ansiStyles.codes.get(1) == 22
    assert ansiStyles.codes.get(91) == 39
    assert ansiStyles.codes.get(40) == 49
    assert ansiStyles.codes.get(100) == 49


def test_rgb_to_truecolor_is_stubbed():
    assert ansiStyles.color.ansi16m(123, 45, 67) == '\u001B[38;2;123;45;67m'

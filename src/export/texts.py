import configparser

import utils


def _decodeText(text_data):
    ask = None

    if text_data.endswith(b'\xff'):
        text_data = text_data[:-1]
    elif text_data.endswith(b'\xfe'):
        text_data = text_data[:-1]
        ask = text_data[(len(text_data) - 1) & ~15:].decode("ascii").replace("^", "'")
        ask = ask.strip()
        text_data = text_data[:(len(text_data) - 1) & ~15]
    else:
        raise RuntimeError("Bad ROM?")

    text = ""
    for n in range(0, len(text_data), 16):
        line = text_data[n:n + 16]
        for k, v in utils.TEXT_SYMBOLS.items():
            line = line.replace(bytes([v]), k)
        text = text + " " + line.decode("ascii").replace("^", "'")
        text = text.strip()
    return text, ask


def exportTexts(rom, filename):
    cp = configparser.ConfigParser()
    for index, text_data in enumerate(rom.texts):
        if isinstance(text_data, int):
            continue
        section = "dialog_%03x" % (index)
        cp.add_section(section)

        text, ask = _decodeText(text_data)

        cp.set(section, "text", text)
        if ask:
            cp.set(section, "ask", ask)
    cp.write(open(filename, "wt"))


def importTexts(rom, filename):
    cp = configparser.ConfigParser()
    cp.read(filename)

    for index, text_data in enumerate(rom.texts):
        if isinstance(text_data, int):
            continue
        section = "dialog_%03x" % (index)
        text = cp.get(section, "text")
        ask = cp.get(section, "ask") if cp.has_option(section, "ask") else None

        old_text, old_ask = _decodeText(text_data)
        if old_text == text and old_ask == ask:
            continue

        rom.texts[index] = utils.formatText(text, ask=ask)

import configparser

import utils


def exportTexts(rom, filename):
    cp = configparser.ConfigParser()
    for index, text_data in enumerate(rom.texts):
        if isinstance(text_data, int):
            break
        section = "dialog_%03x" % (index)
        cp.add_section(section)

        if text_data.endswith(b'\xff'):
            text_data = text_data[:-1]
        elif text_data.endswith(b'\xfe'):
            text_data = text_data[:-1]
            ask = text_data[(len(text_data) - 1) & ~15:].decode("ascii").replace("^", "'")
            ask = ask.strip()
            text_data = text_data[:(len(text_data) - 1) & ~15]
            cp.set(section, "ask", ask)
        else:
            raise RuntimeError("Bad ROM?")

        for k, v in utils.TEXT_SYMBOLS.items():
            text_data = text_data.replace(bytes([v]), k)
        text = ""
        for n in range(0, len(text_data), 16):
            line = text_data[n:n + 16]
            text = text + " " + line.decode("ascii").replace("^", "'")
            text = text.strip()

        cp.set(section, "text", text)
    cp.write(open(filename, "wt"))


def importTexts(rom, filename):
    cp = configparser.ConfigParser()
    cp.read(filename)

    for index, text_data in enumerate(rom.texts):
        if isinstance(text_data, int):
            break
        section = "dialog_%03x" % (index)
        text = cp.get(section, "text")
        ask = cp.get(section, "ask") if cp.has_option(section, "ask") else None

        rom.texts[index] = utils.formatText(text, ask=ask)

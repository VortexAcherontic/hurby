from flask import render_template, request


def exec_charlist(hurby):
    hasChars = False
    offset = 0
    page_size = 25
    all_chars = []
    all = 0
    range = 0
    if request.args.get("offset") is not None:
        offset = int(request.args.get("offset"))
    if request.args.get("pagesize") is not None:
        page_size = int(request.args.get("pagesize"))
    if hurby.char_manager.get_characters() is not None:
        for c in hurby.char_manager.get_characters():
            if c is not None:
                all_chars.append(c.convert_to_json())
        all = len(all_chars)
        all_chars = all_chars[offset:offset + page_size]
        range = str(offset) + "-" + str(offset + page_size)
        if len(all_chars) > 0:
            hasChars = True

    return render_template("restricted/charlist.html", botname=hurby.botConfig.botname, characters=all_chars,
                           hasChars=hasChars, range=range, all=all)

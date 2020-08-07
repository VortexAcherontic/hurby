from flask import render_template


def exec_charview(hurby, uuid):
    ch = hurby.char_manager.get_character_by_uuid(uuid)
    c = None
    invalid = True
    if ch is not None:
        c = ch.convert_to_json()
        invalid = False
    return render_template("character_view.html", botname=hurby.botConfig.botname, c=c, invalid=invalid)

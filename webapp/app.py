from flask import Flask, render_template


def run_flask(hurby):
    hurby = hurby
    app = Flask(__name__)

    @app.route("/")
    @app.route("/index")
    def index():
        return render_template("index.html", botname=hurby.botConfig.botname)

    @app.route("/characters")
    def characters():
        hasChars=False
        if hurby.char_manager.get_characters() is not None:
            all_chars = []
            for c in hurby.char_manager.get_characters():
                if c is not None:
                    all_chars.append(c.convert_to_json())
            if len(all_chars) > 0:
                hasChars=True

        return render_template("charlist.html", botname=hurby.botConfig.botname, characters=all_chars, hasChars=hasChars)

    app.run(debug=True, host="0.0.0.0")

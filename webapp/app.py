from flask import Flask, render_template

from webapp.controller.index import exec_index


def run_flask(hurby):
    hurby = hurby
    app = Flask(__name__)

    @app.route("/")
    @app.route("/index")
    def index():
        return exec_index(hurby)

    @app.route("/characters")
    def characters():
        return exec_charlist(hurby)

    @app.route("/characters/view/<uuid>")
    def characters_view(uuid):
        return exec_charview(hurby, uuid)

    @app.route("/restricted")
    def restricted():
        return render_template("abstract/restricted.html", botname=hurby.botConfig.botname)

    app.run(debug=True, host="0.0.0.0")


from webapp.controller.charlist import exec_charlist
from webapp.controller.charview import exec_charview

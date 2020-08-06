from flask import Flask, render_template


def run_flask():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/characters")
    def characters():
        return render_template("charlist.html")

    app.run(debug=True, host="0.0.0.0")

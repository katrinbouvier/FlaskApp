from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/document')
def document():
    return render_template("document.html")


@app.route('/favorites')
def favorites():
    return render_template("favorites.html")


if __name__ == "__main__":
    app.run(debug=True)

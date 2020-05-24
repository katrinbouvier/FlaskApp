from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.util import NoneType

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translator.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = create_app()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))
    favorites = db.relationship("Favorites", backref=db.backref("parents", uselist=False))

    def __repr__(self):
        return '<Users %r>' % self.id


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fav_path = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.id


# @app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        input_text = request.form['en_text']
        print(input_text)
        return render_template("app/index.html")
    else:
        return render_template("app/index.html")


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        user_email = request.form['user']

        if user_email == '':
            return "В поле ничего нет"
        else:
            cur_user = Users.query.filter_by(email=user_email).first()
            if cur_user is not None:
                # return render_template("app/index.html", email=user_email)
                return redirect('/home')
            else:
                try:
                    new_user = Users(email=user_email)
                    db.session.add(new_user)
                    db.session.commit()
                    # return render_template("app/index.html", email=user_email)
                    return redirect('/home')
                except:
                    return "При добавлении email произошла ошибка"
    else:
        return render_template("app/auth.html")


@app.route('/document')
def document():
    return render_template("app/document.html")


@app.route('/favorites')
def favorites():
    return render_template("app/favorites.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

db = SQLAlchemy()
UPLOAD_FOLDER = './/file-storage'
ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx'])


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translator.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)
    return app


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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


@app.route('/home', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        input_text = request.form['en_text']
        print(input_text)
        return render_template("app/index.html")
    else:
        return render_template("app/index.html")


@app.route('/', methods=['POST', 'GET'])
def auth():
    message = ''
    if request.method == 'POST':
        user_email = request.form['user']

        if user_email == '':
            message = 'В поле ничего нет'
            return render_template("app/auth.html", message=message)
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
                    message = 'При добавлении email произошла ошибка'
    else:
        return render_template("app/auth.html", message=message)


@app.route('/document', methods=['POST', 'GET'])
def document():
    if request.method == "POST":
        file = request.files['file2upload']
        filename = secure_filename(file.filename)
        # save_path = "{}/{}".format(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "successful_upload"
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('uploaded_file', filename=filename))
    return render_template("app/document.html")


@app.route('/uploaded_file')
def uploaded_file(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    lines = []
    with open(path) as file:
        for line in file:
            lines.append(line)
            print(lines)
    return render_template("app/uploaded_file.html", lines)


@app.route('/favorites')
def favorites():
    return render_template("app/favorites.html")


if __name__ == "__main__":
    app.run(debug=True)

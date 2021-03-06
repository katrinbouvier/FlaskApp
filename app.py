from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
import glob
from neuralnet import netinterface

db = SQLAlchemy()
UPLOAD_FOLDER = './/file-storage//temp'
IN_DATA = ''
CUR_EMAIL = ''
CUR_ID = 1
# ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx'])


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translator.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['CUR_ID'] = CUR_ID
    app.config['IN_DATA'] = IN_DATA
    app.config['CUR_EMAIL'] = CUR_EMAIL
    db.init_app(app)

    return app


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#

app = create_app()


# Класс Пользователи для БД
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))
    favorites = db.relationship("Favorites", backref=db.backref("parents", uselist=False))

    def __repr__(self):
        return '<Users %r>' % self.id


# Класс Избранное для БД
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fav_path = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.id


# Домашняя страница приложения
@app.route('/home', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        # получаем строку для перевода
        app.config['IN_DATA'] = request.form['en_text']
        if len(app.config['IN_DATA']) != 0:
            return redirect('/home/translate')
        return render_template("app/index.html", email=app.config['CUR_EMAIL'])
    return render_template("app/index.html", email=app.config['CUR_EMAIL'])


# Страница перевода
@app.route('/home/translate', methods=['POST', 'GET'])
def translate():
    data = netinterface.pass_to_encoder(app.config['IN_DATA'])
    print("IN_DATA", app.config['IN_DATA'])
    # print("data", data)

    # if request.method == "POST":
        # получаем строку для перевода
        # input_text = request.form['en_text']

        # print(input_text)
    return render_template("app/mod_index.html", data=data, email=app.config['CUR_EMAIL'])


# TODO: валидация почты

# Страница авторизации
@app.route('/', methods=['POST', 'GET'])
def auth():
    message = ''
    if request.method == 'POST':
        user_email = request.form['user']

        if user_email == '':
            message = 'В поле ничего нет'
            return render_template("app/auth.html", email=app.config['CUR_EMAIL'], message=message)

        else:
            cur_user = Users.query.filter_by(email=user_email).first()
            if cur_user is not None:
                app.config['CUR_ID'] = cur_user.id
                app.config['CUR_EMAIL'] = cur_user.email
                return redirect('/home')
            else:
                try:
                    db.create_all()
                    new_user = Users(email=user_email)
                    db.session.add(new_user)
                    db.session.commit()
                    app.config['CUR_ID'] = new_user.id
                    app.config['CUR_EMAIL'] = new_user.email
                except:
                    message = 'При добавлении email произошла ошибка'
                    return render_template("app/auth.html", email=app.config['CUR_EMAIL'], message=message)

                return redirect('/home')

    return render_template("app/auth.html", email=app.config['CUR_EMAIL'], message=message)


# Страница загрузки документа
@app.route('/document', methods=['POST', 'GET'])
def document():
    message = "Перетащите файл в эту область"
    return render_template("app/document.html", email=app.config['CUR_EMAIL'], message=message)


# Загрузка документа на сервер для обработки
@app.route('/document/upload_file', methods=['POST'])
def upload_file():
    print("called upload_file")
    # if request.method == 'POST':
    message = "Перетащите файлы в эту область"
    file = request.files['file2upload']
    # TODO: Заменить имя папки на UPLOAD_FOLDER
    filename = secure_filename(file.filename)
    dir = os.listdir("./file-storage/temp")
    if len(dir) == 0:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        message = file.filename
    else:
        old_files = glob.glob('./file-storage/temp/*')
        print(old_files)
        for f in old_files:
            os.remove(f)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        message = file.filename

    return message


# Страница избранных переводов
@app.route('/favorites', methods=['POST', 'GET'])
def favorites():
    cur_id = app.config['CUR_ID']
    cur_user = Users.query.filter_by(id=cur_id).first()
    fav_id = cur_user.favorites_id
    fav = Favorites.query.filter_by(id=fav_id).first()
    fav_list = read_files(fav.fav_path)
    new_list = [x.split('<>')for x in fav_list]
    left_list = []
    right_list = []
    for x in range(len(new_list)):
        left_list.append(new_list[x][0])
        right_list.append(new_list[x][1])

    return render_template("app/favorites.html", email=app.config['CUR_EMAIL'], left=left_list, right=right_list)


# Чтение файлов
def read_files(file_path):
    with open(file_path) as file:
        lines = file.read()
        new_lines = lines.strip().split("\n")
        return new_lines


# Запуск программы
if __name__ == "__main__":
    app.run(debug=True)

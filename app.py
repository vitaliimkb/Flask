from flask import Flask

app = Flask(__name__)  # створюється об'єкт фласка в ДАНОМУ файлі


@app.route('/') # прописується роут(шлях) адреса
def hello_world():
    return '<h1><i>Hello World!</i></h1>'
# i(italic), b(bold), u(underline), s


@app.route('/about') # прописується роут(шлях) адреса
def about():
    return '<h3>About us!</h3>'


@app.route('/contacts') # прописується роут(шлях) адреса
def about():
    return '<h3>Contacts</h3>'


if __name__ == '__main__':
    app.run(debug=True)

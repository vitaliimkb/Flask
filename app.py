from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    is_login = False
    array = ["task1", "task2", "task3", "task4"]
    return render_template("index.html", object={"name": "Vitalii", "age": 24},
                           array=array, is_login=is_login)


@app.route('/about', methods=['POST', 'GET'])
def about():
    if request.method == "POST":
        title = request.form["title"]
        return render_template("about.html", title=title)
    elif request.method == "GET":
        title = request.args.get("title")
        return render_template("about.html", title=title)

    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)

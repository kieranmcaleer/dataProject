from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        query = request.form.get("search")
    else:
        return render_template("search.html", search=search)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

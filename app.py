from flask import Flask, escape, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    keyword = request.args.get('keyword')
    return render_template("search.html", keyword = escape(keyword))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("missing.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

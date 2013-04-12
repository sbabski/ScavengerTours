from flask import Flask
from flask import render_template

app = Flask(__name__)
app.secret_key = "tom_waits_is_grits"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home")
def homepage():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.debug=True
    app.run()

from flask import Flask, render_template, request, redirect, url_for
import os
import osu
import flask_limiter as limit
import flask_limiter.util as limit_util
from dotenv import load_dotenv

# Load .env
load_dotenv()

# https://pytutorial.com/how-to-use-render_template-in-flask/
app = Flask(__name__)
client_id = int(os.environ.get('CLIENT_ID'))
client_secret = os.environ.get('CLIENT_SECRET')

# Setup limit
limit_rate = limit.Limiter(limit_util.get_remote_address, app=app)
    
# https://www.geeksforgeeks.org/using-request-args-for-a-variable-url-in-flask/
# https://www.geeksforgeeks.org/retrieve-text-from-textarea-in-flask/
# https://www.geeksforgeeks.org/redirecting-to-url-in-flask/
@app.route("/", methods = ['GET', 'POST'])
#@limit_rate.limit("1/second")
def home():
    if request.method == "POST":
        name = request.form.get("name_input")
        return redirect(url_for('profile',name=name))
    return render_template("index.html")

# "Very safe" 5-ish API accesses per minute per person
@app.route("/profile")
@limit_rate.limit("5/minute")
def profile():
    name = request.args.get('name')
    return name

if __name__ == "__main__":
    app.run()

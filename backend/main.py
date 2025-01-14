from flask import Flask, request, render_template, make_response
from model.auth import JWTAuthManager

app = Flask(__name__)


JWTManager = JWTAuthManager()
Creds = {"username": "admin", "password": "admin"}

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        JWToken = request.cookies.get('auth_token')

        if JWTManager.CheckToken(JWToken):
            return render_template("protected.html")

    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if Creds["username"] == username and Creds["password"] == password:
            JWToken = JWTManager.CreateToken(request.remote_addr)
            response = make_response(render_template('protected.html'))
            response.set_cookie('auth_token', JWToken)
            return response

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=80)

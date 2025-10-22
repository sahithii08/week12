from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('pwd')

    if not username:
        return "<script>alert('Username cannot be empty.');window.history.back();</script>"
    elif not password:
        return "<script>alert('Password cannot be empty.');window.history.back();</script>"
    elif len(password) < 6:
        return "<script>alert('Password must be at least 6 characters long.');window.history.back();</script>"
    else:
        return redirect(url_for('result', username=username))

@app.route('/result')
def result():
    username = request.args.get('username')
    return render_template('result.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)

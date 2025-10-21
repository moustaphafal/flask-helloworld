from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = []

@app.route('/')
def hello():
    return render_template('index.html', users=users, enumerate=enumerate)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    if name:
        users.append(name)
    return redirect(url_for('hello'))

@app.route('/delete_user/<int:index>', methods=['POST'])
def delete_user(index):
    if 0 <= index < len(users):
        users.pop(index)
    return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
DATABASE_URL = f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
print(DATABASE_URL)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        text_area = request.form['message']
        message = Message(name=name, message=text_area)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('index'))
    messages = Message.query.all()
    return render_template('index.html', messages=[{'name': message.name, 'message': message.message} for message in messages])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
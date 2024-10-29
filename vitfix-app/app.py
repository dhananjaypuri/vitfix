from flask import Flask , render_template , request , jsonify, flash , redirect , url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash , check_password_hash
import os

app = Flask(__name__);

app.secret_key = "hdjhjhdj88300303";
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db = SQLAlchemy(app);

def create_db():
    print(os.listdir());
    if(os.path.exists(f"instance/users.db")):
        print("db already created");
    else:
        print("Creating db");
        with app.app_context():
            db.create_all()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True);
    email = db.Column(db.String(100), nullable = False);
    username = db.Column(db.String(100), unique = True, nullable = False);
    password = db.Column(db.String(100), nullable = False);

    def __repr__(self):
        return f"Id : {self.id} - Username : {self.username}"


@app.route('/', methods = ['GET', 'POST'])
def home():

    if('user' in session):

        return render_template('dashboard.html');
    else:
        return render_template('login.html');
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if(request.method == 'POST'):

        username = request.form.get('username');
        password = request.form.get('password');

        if(username == ''):
            flash("Username is required !!!!", category="error");
        elif(password == ""):
            flash("Password is required !!!!", category="error");
        else:

            user = Users.query.filter_by(username=username).first();
            if user:

                if(check_password_hash(user.password, password)):
                    print("Password matched");
                    session['user'] = username;
                    flash("Logged In Successfully !!!!!" , category= "success");
                    return redirect(url_for('home'));
                    print(user.email);
                else:
                    flash("Incorrect Password !!!!", category="error");
                    return redirect(url_for('login'))
            else:
                print("No user found");
    return render_template('login.html');

@app.route('/logout')
def logout():

    if('user' in session):
        session.clear();
        return redirect(url_for('login'));
    else:
        return redirect(url_for('login'));

@app.route('/sign-up', methods = ['GET', 'POST'])
def signup():

    if(request.method == 'POST'):

        email = request.form.get('email');
        username = request.form.get('username');
        password = request.form.get('password');
    
        if(email == ""):
            flash("Email is required !!!!", category="error");
        elif(username == ""):
            flash("Username is required !!!!", category="error");
        elif(password == ""):
            flash("Password is required !!!!", category="error");
        else:

            user = Users(email=email, username=username, password = generate_password_hash(password, method='scrypt'));
            db.session.add(user);
            db.session.commit();
            flash("Account Created !!!!!" , category= "success");
            return redirect('/');
            


    return render_template('signup.html');

if __name__ == "__main__":

    create_db();
    app.run(debug=True, host='0.0.0.0', port=5001);
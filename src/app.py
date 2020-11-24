from flask import Flask, render_template, request, flash, url_for, redirect, session
import mysql.connector

#inicializar variable
app = Flask(__name__)
app.secret_key = 'mysupersecretkey'

mydb = mysql.connector.connect(  user="root", passwd="", host="localhost", database="login")

#crear rutas
@app.route('/')
def index():
    if 'username' in session:        
        return render_template('home.html')
    else:
        return render_template('index.html')

@app.route('/verifyLogin', methods=['POST'])
def verifyLogin():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        cur = mydb.cursor()

        sql = """
        SELECT id, username, role FROM users WHERE username = %s AND password = SHA2(%s, 512)
        """
        val = (username, password)
        
        cur.execute(sql, val)
        
        rs= cur.fetchone()

        if rs == None:
            flash('No coincide con nuestra Base de Datos', 'error')
            return redirect('/')
        else:
        
            session['id']=rs[0]
            session['username']=rs[1]
                
            return redirect('/home')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('username', None)
    return render_template('index.html')

@app.route('/add_user_view')
def add_user_view():
    return render_template('add_user.html')

#Procesa datos desde la vista
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        cur = mydb.cursor()

        sql = """
        INSERT INTO users (username, password, role) VALUES
        (%s,  SHA2(%s, 512), %s)
        """

        val = (username, password, role)

        cur.execute(sql, val)

        mydb.commit()

        flash('El Usuario fue creado exitosamente')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
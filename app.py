from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'gwapoko'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'midact1' 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM personal")
    data = cur.fetchall()
    cur.close()
    return render_template('Users/index.html', personal=data)
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        bday = request.form['bday']
        address = request.form['address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO personal (fname, lname, age, bday, address) VALUES (%s, %s, %s, %s, %s)",
                    (fname, lname, age, bday, address))
        mysql.connection.commit()
        cur.close()
        flash('Record added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('Users/add.html')

@app.route('/edit/<string:fname>', methods=['POST', 'GET'])
def edit(fname):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM personal WHERE fname = %s", [fname])
    data = cur.fetchone()
    cur.close()
    return render_template('Users/edit.html', personal=data)

@app.route('/update/<string:fname>', methods=['POST'])
def update(fname):
    if request.method == 'POST':
        lname = request.form['lname']
        age = request.form['age']
        bday = request.form['bday']
        address = request.form['address']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE personal SET lname=%s, age=%s, bday=%s, address=%s WHERE fname=%s",
                    (lname, age, bday, address, fname))
        mysql.connection.commit()
        cur.close()
        flash('Record Updated Successfully!', 'success')
        return redirect(url_for('index'))

@app.route('/delete/<string:fname>', methods=['POST', 'GET'])
def delete(fname):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM personal WHERE fname = %s", [fname])
    mysql.connection.commit()
    cur.close()
    flash('Record Deleted Successfully!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)

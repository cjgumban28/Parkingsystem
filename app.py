from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL 
from datetime import datetime
import pymysql

import yaml
app = Flask(__name__)
db = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'flaskapp',
}

app.config['MYSQL_USER'] = db['user']
app.config['MYSQL_PASSWORD'] = db['password']
app.config['MYSQL_DB'] = db['database']
app.config['MYSQL_HOST'] = db['host']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 
mysql = MySQL(app)

@app.route("/")
def HomePage():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers")
    vehicles = cur.fetchall()
    cur.close()
    
    return render_template("index.html", vehicles=vehicles)


@app.route("/entry", methods=['GET', 'POST'])
def Entry():
    if request.method == "GET":
        return render_template("entry.html", entry_data=None)
    
    if request.method == 'POST':
        carDetails = request.form
        Reg_num = carDetails['Reg_num']
        Customer_Name = carDetails['Customer_Name']
        Age = carDetails['Age']
        Bill_Amount = carDetails['Bill_Amount']
        Model_name = carDetails['Model_name']
        Color = carDetails['Color']
        Entry_time = datetime.now()

    try:
        cur_customer = mysql.connection.cursor()
        cur_customer.execute("INSERT INTO Customers(Reg_Num, Name, Age, Bill_Amount, Model_name, Color, Entry_time) VALUES( %s, %s, %s, %s, %s, %s, %s)", (Reg_num, Customer_Name, Age, Bill_Amount, Model_name, Color, Entry_time))
        mysql.connection.commit()


        entry_data = {
            'Reg_num': Reg_num,
            'Customer_Name': Customer_Name,
            'Age': Age,
            'Bill_Amount': Bill_Amount,
            'Model_name': Model_name,
            'Color': Color,
            'Entry_time': Entry_time
        }

        return render_template("entry.html", entry_data=entry_data)

    except pymysql.Error as err:
        print(f"Error: {err}")
        mysql.connection.rollback()  


    except pymysql.Error as err:
        print(f"Error: {err}")
        mysql.connection.rollback()  
        return "Error"

def BillCalculator(entry_time):
    exit_time = datetime.now()
    diff_year =  (exit_time.date().year - entry_time.date().year)*365
    diff_month = (exit_time.date().month - entry_time.date().month)*30
    diff_day = (exit_time.date().day - entry_time.date().day)
    total_date = diff_year + diff_month + diff_day
    
    diff_hour =  (exit_time.time().hour - entry_time.time().hour)*60
    diff_min = (exit_time.time().minute - entry_time.time().minute)*1/60
    total_min = total_date*24*60 + diff_hour + diff_min
    total_bill = 1/6 * total_min
    return total_min


def BillHandler(Reg_Num):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, Entry_time FROM customers WHERE Reg_Num = %s", [Reg_Num])
    car = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    entry_time = car[0][1]
    total_amount = BillCalculator(entry_time)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Customers SET Bill_Amount = Bill_Amount + %s WHERE Customer_ID = %s", (total_amount))
    mysql.connection.commit()
    cur.close()


@app.route("/delete/<string:id>", methods=["GET", "POST"])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers WHERE id = %s", [id])
    mysql.connection.commit()
    
    cur.close()
    return redirect(url_for('HomePage'))

@app.route("/edit/<string:id>", methods=['GET', 'POST'])
def edit(id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customers WHERE id = %s", [id])
        vehicle = cur.fetchall()
        cur.close()
        return render_template("edit.html", vehicle=vehicle[0])

    if request.method == 'POST':
        carDetails = request.form
        Reg_num = carDetails['Reg_num']
        Customer_Name = carDetails['Customer_Name']
        Age = carDetails['Age']
        Bill_Amount = carDetails['Bill_Amount']
        Model_name = carDetails['Model_name']
        Color = carDetails['Color']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE Customers SET Reg_Num = %s, Name = %s, Age = %s, Bill_Amount = %s, Model_name = %s, Color = %s WHERE id = %s", (Reg_num, Customer_Name, Age, Bill_Amount, Model_name, Color, id))
        mysql.connection.commit()

        return redirect(url_for('HomePage'))
    
@app.route('/view/<string:id>', methods=['GET'])
def view(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers WHERE id = %s", [id])
    car_data = cur.fetchall()
    cur.close()
    return render_template("view.html", car_data=car_data)
    

if __name__ == '__main__':
    app.run(debug=True)

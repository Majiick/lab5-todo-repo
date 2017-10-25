import os
from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
from flask_prometheus import monitor
#from slackclient import SlackClient

#slack_token = os.environ["SLACK_API_TOKEN"]
#sc = SlackClient(slack_token)

mysql = MySQL()
app = Flask(__name__)

# My SQL Instance configurations 
# Change the HOST IP and Password to match your instance configurations
 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'todotask'
app.config['MYSQL_HOST'] = '35.187.85.20'
mysql.init_app(app)

@app.route('/')
@app.route('/<name>')
def statichtml(name=None):
    
    return render_template('index.html', name=name)


@app.route("/list")
def list(): # Name of the method
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    cur.execute('''SELECT * FROM TASKTABLE''') # execute an SQL statment
    rv = cur.fetchall() #Retreive all rows returend by the SQL statment
    
    return render_template('index.html', name=str(rv))     #Return the data in a string format

  
@app.route("/add/<taskname>")
def add(name=None, email=None):
    cur= mysql.connection.cursor()
    insert_stmt = ("INSERT INTO TASKTABLE (tName) VALUES (%s)")
    data=(taskname)
    cur.execute(insert_stmt, data)
    mysql.connection.commit()
    
    return render_template('index.html', name = "New task added to the database")
  
  
@app.route("/delete/<tno>")
def delete(tno=None):
    cur=mysql.connection.cursor()
    delstatmt = "DELETE FROM TASKTABLE WHERE tno = ' {} ' ".format(tno)
    print(delstatmt)
    cur.execute(delstatmt)
    mysql.connection.commit()
    
    return render_template('index.html', name="Task record has been deleted")      #Return the data in a string format


@app.route("/update/<taskname>/<tno>")
def update(taskname=None, tno=None):
    cur=mysql.connection.cursor()
    update_stmt = ("UPDATE TASKTABLE SET tName = %s WHERE tNo = %s")
    data=(taskname,tno)
    cur.execute(update_stmt, data)
    mysql.connection.commit()

    return render_template('index.html', name="Task record has been updated")      #Return the data in a string format


if __name__ == "__main__":
        monitor(app, port=8000)
        app.run(host='0.0.0.0', port='5000')

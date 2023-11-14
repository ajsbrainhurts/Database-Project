from flask import Flask, render_template
import mysql.connector, os, json

# 
secrets = os.path.abspath('/home/aj/secrets/secrets.json')
with open(secrets, 'r') as secretFile:
    creds = json.load(secretFile)['mysqlcredentials']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def showCustomer():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    mycursor.execute("""SELECT * FROM Customer""")
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('customer.html', customers=myresult)
if __name__ == '__main__':
    app.run(port=8001, debug=True, host="0.0.0.0")
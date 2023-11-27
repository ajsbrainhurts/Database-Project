from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json


with open('/home/aj/secrets/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlcredentials']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def showOrders():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    orderID = request.args.get('OrderID')
    if orderID is not None:
        mycursor.execute("""SELECT OrderID, TotalCost, DateOfOrder, CustomerID, ProductID, ProductType, ProductPrice
                         FROM _Order_
                         JOIN OrderProduct ON _Order_.OrderID = OrderProduct.OrderID
                         JOIN Product ON Product.ProductID = OrderProduct.ProductID
                         WHERE _Order_.OrderID = %s""", (orderID,))              
        myresult = mycursor.fetchall()
        if len(myresult) >= 1:
            totalCost = myresult[0][1]
            dateofOrder = str(myresult[0][3])
            print(totalCost,dateofOrder)
        else:
            totalCost = dateofOrder = 'Unknown'
    else:
        mycursor.execute("SELECT * FROM _Order_")
        myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('order.html', orders=myresult)

@app.route('/product', methods=['GET'])
def showProducts():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    productID = request.args.get('ProductID')
    if productID is not None:
        mycursor.execute("""SELECT Product.ProductID, ProductType, ProductPrice 
                         FROM Product
                         JOIN OrderProduct ON Product.ProductID = OrderProduct.ProductID
                         JOIN _Order_ ON _Order_.OrderID = OrderProduct.OrderID
                         WHERE _Order_.OrderID=%s""", (productID,))
        myresult = mycursor.fetchall()
        if len(myresult) >= 1:
            productType = myresult[0][1]
            productPrice = myresult[0][2]
            print(productType, productPrice)
        else:
            productType = productPrice = 'Unknown'
    else:
        mycursor.execute("SELECT ProductID, ProductType, ProductPrice FROM Product")
        myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('product.html', products=myresult)

@app.route('/orders_for_product', methods=['GET'])
def showOrdersForProduct():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    productID = request.args.get('ProductID')
    if productID is not None:
        mycursor.execute("""SELECT _Order_.OrderID, TotalCost, DateOfOrder, CustomerID
                         FROM _Order_
                         JOIN OrderProduct ON _Order_.OrderID = OrderProduct.OrderID
                         WHERE OrderProduct.ProductID=%s""", (productID,))
        myresult = mycursor.fetchall()
    else:
        myresult = []
    mycursor.close()
    connection.close()
    return render_template('orders_for_product.html', orders=myresult)

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
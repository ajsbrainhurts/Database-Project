from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, json



with open('/home/aj/secrets/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlcredentials']

app = Flask(__name__)

# Home page. Renders the Order table. 
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

# Renders the product table.
@app.route('/product', methods=['GET'])
def showProducts():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    productID = request.args.get('ProductID')
    if productID is not None:
        mycursor.execute("""SELECT ProductID, ProductType, ProductPrice 
                         FROM Product WHERE ProductID=%s""", (productID,))
        myresult = mycursor.fetchall()
        if len(myresult) >= 1:
            productType = myresult[0][1]
            productPrice = myresult[0][2]
            print(productType, productPrice)
        elif len(myresult) == 0:
            myresult = []
        else:
            productType = productPrice = 'Unknown'
    else:
        mycursor.execute("SELECT ProductID, ProductType, ProductPrice FROM Product")
        myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('product.html', products=myresult)

# Shows products within a specified order. 
@app.route('/products_in_order/<orderID>', methods=['GET'])
def showProductsForOrder(orderID):
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    if orderID is not None:
        mycursor.execute("""SELECT Product.ProductID, ProductType, ProductPrice 
                         FROM Product
                         JOIN OrderProduct ON Product.ProductID = OrderProduct.ProductID
                         JOIN _Order_ ON _Order_.OrderID = OrderProduct.OrderID
                         WHERE _Order_.OrderID=%s""", (orderID,))
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
    return render_template('products_in_order.html', products=myresult)

# Shows orders that contain a specific product.
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

# Adds order to order table. 
@app.route('/add_order', methods=['GET', 'POST'])
def addOrder():
    if request.method == 'POST':
        connection = mysql.connector.connect(**creds)
        mycursor = connection.cursor()
        orderID = request.form['orderID']
        customerID = request.form['customerID']
        totalCost = request.form['totalCost']
        dateOfOrder = request.form['dateOfOrder']
        productID = request.args.get('ProductID')
        if orderID is not None:
            connection.start_transaction()
            mycursor.execute("""
                INSERT INTO _Order_ (OrderID, CustomerID, TotalCost, DateOfOrder)
                VALUES (%s, %s, %s, %s)""", (orderID, customerID, totalCost, dateOfOrder))
            mycursor.execute("""
                INSERT INTO OrderProduct (OrderID, ProductID) 
                VALUES (%s, %s)""", (orderID, productID))
            connection.commit()
            mycursor.execute("""SELECT * FROM _Order_""")
            myresult = mycursor.fetchall()
            return redirect(url_for('showOrders', orders=myresult))
        mycursor.close()
        connection.close()
    return render_template('add_order.html')
# Adds product to product table. 
@app.route('/add_product', methods=['GET', 'POST']) 
def addProduct():
    if request.method == 'POST':
        connection = mysql.connector.connect(**creds)
        mycursor = connection.cursor()
        productID = request.form['productID']
        productType = request.form['productType']
        productPrice = request.form['productPrice']
        if productID is not None:
            connection.start_transaction()
            mycursor.execute("""
                INSERT INTO Product (ProductID, ProductType, ProductPrice)
                VALUES (%s, %s, %s)""", (productID, productType, productPrice))
            connection.commit()
            mycursor.execute("""SELECT * FROM Product""")
            myresult = mycursor.fetchall()
            return redirect(url_for('showProducts', products=myresult))
    return render_template("add_product.html")

# Inserts new record into bridge table to associate a product w/ an order
@app.route('/add_product_to_order/<orderID>', methods=['GET','POST'])
def addProductToOrder(orderID):
    if request.method == 'POST':
        connection = mysql.connector.connect(**creds)
        mycursor = connection.cursor()
        productID = request.form['productID']
        if productID is not None:
            connection.start_transaction()
            mycursor.execute("""
                INSERT INTO OrderProduct (OrderID, ProductID)
                VALUES (%s, %s)""", (orderID, productID))
            connection.commit()
            mycursor.execute("""SELECT ProductID from OrderProduct WHERE OrderID=%s""", (orderID,))
            myresult = mycursor.fetchall()
            print(myresult)
            return redirect(url_for('showOrders'))
    else:
        connection = mysql.connector.connect(**creds)
        mycursor = connection.cursor()
        mycursor.execute("""SELECT * FROM _Order_ WHERE OrderID=%s""", (orderID,))
        myorder = mycursor.fetchone()
        mycursor.close()
        connection.close()
        return render_template('add_product_to_order.html', order=myorder)
    
# Deletes selected entry from order table. 
@app.route('/delete_order/<orderID>', methods=['POST'])
def deleteOrder(orderID):
    if request.method == 'POST':
        connection = mysql.connector.connect(**creds)
        mycursor = connection.cursor()
        connection.start_transaction()
        mycursor.execute("""DELETE FROM OrderProduct WHERE OrderID = %s""", (orderID,))
        mycursor.execute("""DELETE FROM _Order_ WHERE OrderID = %s""", (orderID,))
        connection.commit()
        mycursor.close()
        connection.close()
        return redirect(url_for('showOrders'))
    
# Deletes selected entry from product table.
@app.route('/delete_product/<productID>', methods=['POST'])
def deleteProduct(productID):
    pass
    if request.method == 'POST':
        connection = mysql.connector.connect(**creds)
        mycursor = connection.cursor()
        connection.start_transaction()
        mycursor.execute("""DELETE FROM OrderProduct WHERE ProductID=%s""",(productID,))
        mycursor.execute("""DELETE FROM Product WHERE ProductID=%s""", (productID,))
        connection.commit()
        mycursor.close()
        connection.close()
        return redirect(url_for('showProducts'))
    
# Updates entries in the order table    
@app.route('/update_order/<orderID>', methods=['GET','POST'])
def updateOrder(orderID):
    if request.method == 'POST':
        connection = mysql.connector.connect(**creds)
        mycursor = connection.cursor()
        totalCost = request.form['totalCost']
        dateOfOrder = request.form['dateOfOrder']
        mycursor.execute("""UPDATE _Order_ SET TotalCost=%s, DateOfOrder=%s 
                    WHERE OrderID=%s""", (totalCost, dateOfOrder, orderID))
        connection.commit()
        mycursor.close()
        connection.close()
        return redirect(url_for('showOrders'))
    else:
        connection = mysql.connector.connect(**creds)
        mycursor = connection.cursor()
        mycursor.execute("""SELECT OrderID, TotalCost, DateOfOrder, CustomerID FROM _Order_ 
                    WHERE OrderID=%s""", (orderID,))
        order = mycursor.fetchone()
        mycursor.close()
        connection.close()
        return render_template('update_order.html', order=order)
    
# Updates entries in the product table, same methods as the route above. 
@app.route('/update_product/<productID>', methods=['GET','POST'])
def updateProduct(productID):
    if request.method == 'POST':
        connection = mysql.connector.connect(**creds)
        mycursor = connection.cursor()
        productType = request.form['productType']
        productPrice = request.form['productPrice']
        mycursor.execute("""UPDATE Product SET ProductType=%s, ProductPrice=%s 
                    WHERE ProductID=%s""", (productType,productPrice, productID) )
        connection.commit()
        mycursor.close()
        connection.close()
        return redirect(url_for('showProducts'))
    else:
        connection = mysql.connector.connect(**creds)
        mycursor = connection.cursor()
        mycursor.execute("""SELECT ProductID, ProductType, ProductPrice FROM Product
                    WHERE ProductID=%s""", (productID,))
        product = mycursor.fetchone()
        mycursor.close()
        connection.close()
        return render_template('update_product.html', product=product)

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
    
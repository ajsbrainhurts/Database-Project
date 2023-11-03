from flask import Flask, render_template, request, redirect

app = Flask(__name__)
customers = 
@app.route('/')
def form():
    return render_template('form.html', customers=customers)

@app.route('/add_customer', methods=['POST','GET'])
def add_customer():
    customer_id = request.form['customer_id']
    customer_name = request.form['customer_name']
    payment_method = request.form['payment_method']

    new_customer = {
        "CustomerID": customer_id,
        "CustomerName": customer_name,
        "PaymentMethod": payment_method
    }
    customers.append(new_customer)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
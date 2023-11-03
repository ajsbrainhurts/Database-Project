# Current Schema:


# _Product:_
ProductID(PK), ProductType, ProductPrice
# _Customer:_
CustomerID(PK), CustomerName, PaymentMethod
# _CustomerInfo(Plural attribute):_
CustomerID(PK), PhoneNumber, EmailAddress
# _Order(make sure to put underscores around order to bring the table up):_ 
OrderID(PK), CustomerID(FK), TotalCost, DateOfOrder
# _Discount:_
DiscountID(PK), OrderID(FK), AmountDeducted, DateOfDiscount


# Questions / Use cases
1. I want to be able to place an order with this system and calculate the total price of said order.
2. Keep track of inventory within store and be able to restock when needed.
3. Apply discounts to items and calculate the price of an order after a discount has been applied.

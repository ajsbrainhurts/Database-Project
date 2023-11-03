# Grocery Store Database Project


## Current Schema:


# _Product:_
ProductID(PK), ProductType, ProductPrice
# _Customer:_
CustomerID(PK), CustomerName, PaymentMethod
# _CustomerInfo(Plural attribute):_
CustomerID(PK), PhoneNumber, EmailAddress
# _Order:_ (IMPORTANT: YOU NEED TO PUT UNDERSCORES AROUND ORDER TO BRING THE TABLE UP)
OrderID(PK), CustomerID(FK), TotalCost, DateOfOrder
# _Discount:_
DiscountID(PK), OrderID(FK), AmountDeducted, DateOfDiscount
# Questions / Use cases
1. I want to be able to place an order with this system and calculate the total price of said order.
2. Keep track of inventory within store and be able to restock when needed.
3. Apply discounts to items and calculate the price of an order after a discount has been applied.

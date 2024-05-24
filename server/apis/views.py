from django.shortcuts import render
from .models import users_collection, transactions_collection, stocks_collection, orders_collection
from django.http import HttpResponse
import json
import bson
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Create your views here.

@csrf_exempt
def register(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    usertype = data.get('usertype')
    balance = 0
    
    data = {
        'username': username,
        'email': email,
        'password': password,
        'usertype': usertype,
        'balance': balance
    }
    print(data)
    try:
        result = users_collection.insert_one(data)
        data = {
            '_id': str(result.inserted_id),
            'username': username,
            'email': email,
            'password': password,
            'usertype': usertype,
            'balance': balance
        }
        return HttpResponse(status=201, content=bson.json_util.dumps(data))
   
    except Exception as e:
        print(f"Error saving data to MongoDB: {e}")  # Log the error
        return HttpResponse(status=400, content="An error occurred while saving data.")

@csrf_exempt
def login(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    email = data.get('email')
    password = data.get('password')
    print(email, password)
    try:
        user = users_collection.find_one({"email": email})
        if user.get('password') == password:
            user['_id'] = str(user['_id'])
            return HttpResponse(status=200, content=bson.json_util.dumps(user))
        else:
            return HttpResponse(status=401, content="Invalid login credentials.")
    except Exception as e:
        print(f"Error fetching data from MongoDB: {e}")  # Log the error
        return HttpResponse(status=400, content="An error occurred while fetching data.")

@csrf_exempt
def deposit(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    userId = data.get('userId')
    depositAmount = data.get('depositAmount')
    depositMode = data.get('depositMode')
    
    currentDateAndTime = datetime.now()
    try:
        object_id = bson.ObjectId(userId)
        user = users_collection.find_one({"_id": object_id})
        balance = user.get('balance')
        new_balance = balance + float(depositAmount)
        users_collection.update_one({"_id": object_id}, {"$set": {"balance": new_balance}})
        
        transaction = {
            "user": userId,
            "type": "deposit",
            "amount": depositAmount,
            "mode": depositMode,
            "time": str(currentDateAndTime)
        }
        
        transactions_collection.insert_one(transaction)
        
        return HttpResponse(status=200, content=bson.json_util.dumps({"balance": new_balance}))
    except Exception as e:
        print(f"Error fetching data from MongoDB: {e}")  # Log the error
        return HttpResponse(status=400, content="An error occurred while fetching data.")

@csrf_exempt
def withdraw(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    userId = data.get('userId')
    withdrawAmount = data.get('withdrawAmount')
    withdrawMode = data.get('withdrawMode')
     
    currentDateAndTime = datetime.now()
    try:
        object_id = bson.ObjectId(userId)
        user = users_collection.find_one({"_id": object_id})
        balance = user.get('balance')
        new_balance = balance - float(withdrawAmount)
        users_collection.update_one({"_id": object_id}, {"$set": {"balance": new_balance}})
        
        transaction = {
            "user": userId,
            "type": "Withdraw",
            "amount": withdrawAmount,
            "mode": withdrawMode,
            "time": str(currentDateAndTime)
        }
        
        transactions_collection.insert_one(transaction)
        
        return HttpResponse(status=200, content=bson.json_util.dumps({"balance": new_balance}))
    except Exception as e:
        print(f"Error fetching data from MongoDB: {e}")  # Log the error
        return HttpResponse(status=400, content="An error occurred while fetching data.")

@csrf_exempt
def buyStock(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    userId = data.get('userId')
    symbol = data.get('symbol')
    name = data.get('name')
    stockType = data.get('stockType')
    stockExchange = data.get('stockExchange')
    price = data.get('price')
    count = data.get('count')
    totalPrice = data.get('totalPrice')
    
    stock = stocks_collection.find_one({"user": userId, symbol: symbol})
    
    object_id = bson.ObjectId(userId)
    user = users_collection.find_one({"_id": object_id})
    
    if(user['balance'] < totalPrice):
        return HttpResponse(status=400, content="Insufficient balance")
    else:
        
        if(stock):
            stock['price'] = (int(stock['price']) + int(price)) / (int(stock['count']) + int(count))
            stock['count'] = int(stock['count']) + int(count)
            stock['totalPrice'] = int(stock['totalPrice']) + int(totalPrice)
            stocks_collection.update_one({"_id": userId, "symbol": symbol}, {"$set": stock})
        else:
            stock = {
                "user": userId,
                "symbol": symbol,
                "name": name,
                "stockType": stockType,
                "stockExchange": stockExchange,
                "price": price,
                "count": count,
                "totalPrice": totalPrice
            }
            stocks_collection.insert_one(stock)
            
        new_order = {
            "user": userId,
            "symbol": symbol,
            "name": name,
            "stockType": stockType,
            # "stockExchange": stockExchange,
            "price": price,
            "count": count,
            "totalPrice": totalPrice,
            "orderType": "Buy",
            "orderStatus": "completed"
        }
        orders_collection.insert_one(new_order)
        
        new_balance = user.get('balance') - totalPrice
        users_collection.update_one({"_id": object_id}, {"$set": {"balance": new_balance}})

        return HttpResponse(status=200, content="success")
            
    
@csrf_exempt        
def sellStock(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    userId = data.get('userId')
    symbol = data.get('symbol')
    name = data.get('name')
    stockType = data.get('stockType')
    price = data.get('price')
    count = data.get('count')
    totalPrice = data.get('totalPrice')
    
    try:
        
        stock = stocks_collection.find_one({"user": userId, "symbol": symbol})
        
        object_id = bson.ObjectId(userId)
        user = users_collection.find_one({"_id": object_id})
        
        if(stock['count'] > count):
            stock['totalPrice'] = int(stock['totalPrice']) - int(totalPrice)
            stock['count'] = int(stock['count']) - int(count)
            
            users_collection.update_one({"_id": object_id}, {"$set": {"balance": user['balance'] + totalPrice}})
            
            stocks_collection.update_one({"user": userId, "symbol": symbol}, {"$set": stock})
        else:
            stocks_collection.delete_one({"user": userId, "symbol": symbol})
            users_collection.update_one({"_id": object_id}, {"$set": {"balance": user['balance'] + totalPrice}})
        
        new_order = {
            "user": userId,
            "symbol": symbol,
            "name": name,
            "stockType": stockType,
            "price": price,
            "count": count,
            "totalPrice": totalPrice,
            "orderType": "Sell",
            "orderStatus": "completed"
        }
        orders_collection.insert_one(new_order)
        
        return HttpResponse(status=200, content="success")
        
    except:
        return HttpResponse(status=400, content="An error occurred while fetching data.")
    
    
        
    

def FetchUser(request, id):
    object_id = bson.ObjectId(id)
    document = users_collection.find_one({"_id": object_id})
    if document:
        # Return the entire document, not just the field names
        return HttpResponse(bson.json_util.dumps(document))
    else:
        return HttpResponse(status=404)

def Transactions(request):
    transactions = transactions_collection.find()
    transactions = [transaction for transaction in transactions_collection.find()]
    
    for transaction in transactions:
        transaction['_id'] = str(transaction['_id'])
        
    return HttpResponse(bson.json_util.dumps(transactions))    


def fetchOrders(request):
    orders = orders_collection.find()
    orders = [order for order in orders_collection.find()]

    for order in orders:
        order['_id'] = str(order['_id'])
    print(orders)
    return HttpResponse(bson.json_util.dumps(orders))


def fetchStocks(request):
    stocks = stocks_collection.find()
    stocks = [stock for stock in stocks_collection.find()]

    for stock in stocks:
        stock['_id'] = str(stock['_id'])
    print(stocks)
    return HttpResponse(bson.json_util.dumps(stocks))    

    
def fetchUsers(request):
    users = users_collection.find()
    users = [user for user in users_collection.find()]

    for user in users:
        user['_id'] = str(user['_id'])
    print(users)
    return HttpResponse(bson.json_util.dumps(users))
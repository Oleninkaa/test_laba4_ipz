from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import random
from pymongo import MongoClient
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId

id_counter = 0

DATABASE_URL = "postgresql://user:password@db:5432/car_sales"

app = Flask(__name__)
CORS(app)

# Read environment variable to determine the database type
USE_MONGO = os.getenv("USE_MONGO")
print(f"Using MongoDB: {USE_MONGO == 'true'}")
# Ensure DATABASE_URL is set correctly, fallback to environment variables if not
DATABASE_URL = os.getenv('DATABASE_URL') or f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Configure SQLAlchemy with PostgreSQL URI
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MongoDB configuration with PyMongo
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongodb:27017/car_sales")  # Default MongoDB URI
mongo = PyMongo(app)
print("USING NOSQL")
"""
# Перемикання між SQL та MongoDB
USE_MONGO = os.getenv("USE_MONGO")
print(USE_MONGO)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:  {os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if USE_MONGO == "true":
    # Налаштування для MongoDB
    app.config["MONGO_URI"] = "mongodb://mongodb:27017/car_sales"  # Задайте правильний URI для MongoDB
    mongo = PyMongo(app)
    print("USING NOSQL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:  {os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    print("USING SQL")
    
"""

# Модель клієнта
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column('clientid', db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    car_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', backref='client', lazy=True, cascade='all, delete, delete-orphan')

class Car(db.Model):
    __tablename__ = 'cars'
    
    id = db.Column('carid', db.Integer, primary_key=True)
    car_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    technical_condition = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Car {self.car_type}, ${self.price}>"


class Seller(db.Model):
    __tablename__ = 'sellers'
    
    id = db.Column('sellerid', db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    additional_info = db.Column(db.Text)

    def __repr__(self):
        return f"<Seller {self.full_name}, {self.age}>"


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column('orderid', db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.clientid'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.carid'), nullable=False)
    order_date = db.Column(db.Date, default=db.func.current_date)

    def __repr__(self):
        return f"<Order {self.id}: Client {self.client_id}, Car {self.car_id}>"

"""
def create_tables_and_seed():
    with app.app_context():
        if USE_MONGO == "true":
            return
            mongo.db.clients.insert_one(
              { "FullName": "Іван Іванов", "Age": 35, "Gender": "Чоловік", "CarType": "Седан", "Price": 15000 }
            )
            
            mongo.db.clients.insert_one( { "FullName": "Олена Петрова", "Age": 28, "Gender": "Жінка", "CarType": "Хетчбек", "Price": 12000 })

            mongo.db.cars.insert_many([
              { "CarType": "Седан", "Price": 15000, "Mileage": 80000, "TechnicalCondition": "Гарний" },
              { "CarType": "Хетчбек", "Price": 12000, "Mileage": 60000, "TechnicalCondition": "Середній" }
            ])


            mongo.db.sellers.insert_many([
              { "FullName": "Сергій Сергієнко", "Age": 40, "Gender": "Чоловік", "AdditionalInfo": "Досвідчений продавець" }
            ])


            mongo.db.orders.insert_one({
              "ClientID": db.clients.findOne({ "FullName": "Іван Іванов" })._id,
              "CarID": db.cars.findOne({ "CarType": "Седан" })._id,
              "OrderDate": date.today()
            })
            return
        # Створення таблиць
        db.create_all()

        # Додавання початкових записів у таблицю Clients
        if Client.query.count() == 0:
            initial_clients = [
                Client(full_name="Іван Іванов", age=30, gender="Чоловік", car_type="Седан", price=15000),
                Client(full_name="Марія Петренко", age=25, gender="Жінка", car_type="Хетчбек", price=12000),
                Client(full_name="Олег Сидоров", age=40, gender="Чоловік", car_type="Позашляховик", price=30000),
            ]
            db.session.bulk_save_objects(initial_clients)
            db.session.commit()

        # Додавання початкових записів у таблицю Cars
        if Car.query.count() == 0:
            initial_cars = [
                Car(car_type="Седан", price=15000, mileage=50000, technical_condition="Добрий"),
                Car(car_type="Хетчбек", price=12000, mileage=30000, technical_condition="Відмінний"),
                Car(car_type="Позашляховик", price=30000, mileage=100000, technical_condition="Задовільний"),
            ]
            db.session.bulk_save_objects(initial_cars)
            db.session.commit()

        # Додавання початкових записів у таблицю Sellers
        if Seller.query.count() == 0:
            initial_sellers = [
                Seller(full_name="Анна Смирнова", age=35, gender="Жінка", additional_info="10 років досвіду продажу"),
                Seller(full_name="Петро Коваленко", age=45, gender="Чоловік", additional_info="Експерт у сфері автомобілів"),
            ]
            db.session.bulk_save_objects(initial_sellers)
            db.session.commit()

        # Додавання початкових записів у таблицю Orders
        if Order.query.count() == 0:
            initial_orders = [
                Order(client_id=1, car_id=1, order_date="2024-01-15"),
                Order(client_id=2, car_id=2, order_date="2024-01-20"),
                Order(client_id=3, car_id=3, order_date="2024-01-25"),
            ]
            db.session.bulk_save_objects(initial_orders)
            db.session.commit()


# --- REST-методи ---

# Отримати всіх клієнтів
@app.route("/clients", methods=["GET"])
def get_clients():
    if USE_MONGO:
        print("USING NOSQL")
        clients = mongo.db.clients.find()  # Зчитуємо всі документи з колекції "clients"
        print(clients)
        return jsonify([client for client in clients])  # Повертаємо результат у форматі JSON
    else:
        clients = Client.query.all()
        return jsonify([
            {
                "id": client.id,
                "full_name": client.full_name,
                "age": client.age,
                "gender": client.gender,
                "car_type": client.car_type,
                "price": client.price
            }
            for client in clients
    ])

# Додати нового клієнта
@app.route("/clients", methods=["POST"])
def add_client():
    if USE_MONGO:
        print("USING NOSQL")
        client_data = request.get_json()
        # Вставляємо новий документ в колекцію "clients"
        mongo.db.clients.insert_one(client_data)
        return jsonify({"message": "Client added to MongoDB"}), 201
    else:
        data = request.get_json()
        new_client = Client(
            full_name=data["full_name"],
            age=data["age"],
            gender=data["gender"],
            car_type=data["car_type"],
            price=data["price"]
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({"message": "Клієнта додано", "id": new_client.id}), 201

# Редагувати клієнта
@app.route("/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    if USE_MONGO:
        print("USING NOSQL")
        updated_data = request.get_json()
        result = mongo.db.clients.update_one(
            {"_id": client_id},  # Пошук по ID
            {"$set": updated_data}  # Оновлення документа
        )
        if result.matched_count > 0:
            return jsonify({"message": "Client updated successfully"})
        else:
            return jsonify({"message": "Client not found"}), 404
    
    else:
        data = request.get_json()
        client = Client.query.get_or_404(client_id)
        client.full_name = data.get("full_name", client.full_name)
        client.age = data.get("age", client.age)
        client.gender = data.get("gender", client.gender)
        client.car_type = data.get("car_type", client.car_type)
        client.price = data.get("price", client.price)
        db.session.commit()
        return jsonify({"message": "Клієнта оновлено"})

# Видалити клієнта
@app.route("/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    if USE_MONGO:
        print("USING NOSQL")
        result = mongo.db.clients.delete_one({"_id": client_id})  # Видалення документа за ID
        if result.deleted_count > 0:
            return jsonify({"message": "Client deleted successfully"})
        else:
            return jsonify({"message": "Client not found"}), 404
    else:
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": "Клієнта видалено"})

@app.route('/cars', methods=['GET'])
def get_cars():
    if USE_MONGO:
        cars = mongo.db.cars.find()
        return jsonify([car for car in cars])
    else:
        cars = Car.query.all()
        return jsonify([{
            'id': car.id,
            'car_type': car.car_type,
            'price': str(car.price),
            'mileage': car.mileage,
            'technical_condition': car.technical_condition
        } for car in cars])


@app.route('/cars', methods=['POST'])
def add_car():
    if USE_MONGO:
        print("USING NOSQL")
        car_data = request.get_json()
        mongo.db.cars.insert_one(car_data)
        return jsonify({"message": "Car added to MongoDB"}), 201
    else:
        data = request.json
        new_car = Car(
            car_type=data['car_type'],
            price=data['price'],
            mileage=data['mileage'],
            technical_condition=data['technical_condition']
        )
        db.session.add(new_car)
        db.session.commit()
        return jsonify({'message': 'Car added successfully', 'car_id': new_car.id}), 201

@app.route('/sellers', methods=['GET'])
def get_sellers():
    if USE_MONGO:
        print("USING NOSQL")
        sellers = mongo.db.sellers.find()
        return jsonify([seller for seller in sellers])
    else:
        sellers = Seller.query.all()
        return jsonify([{
            'id': seller.id,
            'full_name': seller.full_name,
            'age': seller.age,
            'gender': seller.gender,
            'additional_info': seller.additional_info
        } for seller in sellers])


@app.route('/sellers', methods=['POST'])
def add_seller():
    if USE_MONGO:
        print("USING NOSQL")
        seller_data = request.get_json()
        mongo.db.sellers.insert_one(seller_data)
        return jsonify({"message": "Seller added to MongoDB"}), 201
    else:
        data = request.json
        new_seller = Seller(
            full_name=data['full_name'],
            age=data['age'],
            gender=data['gender'],
            additional_info=data.get('additional_info', '')
        )
        db.session.add(new_seller)
        db.session.commit()
        return jsonify({'message': 'Seller added successfully', 'seller_id': new_seller.id}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    if USE_MONGO:
        print("USING NOSQL")
        orders = mongo.db.orders.find()
        return jsonify([order for order in orders])
    else:
        orders = Order.query.all()
        return jsonify([{
            'id': order.id,
            'client_id': order.client_id,
            'car_id': order.car_id,
            'order_date': order.order_date
        } for order in orders])


@app.route('/orders', methods=['POST'])
def add_order():
    if USE_MONGO:
        print("USING NOSQL")
        order_data = request.get_json()
        mongo.db.orders.insert_one(order_data)
        return jsonify({"message": "Order added to MongoDB"}), 201
    else:
        data = request.json
        new_order = Order(
            client_id=data['client_id'],
            car_id=data['car_id'],
            order_date=date.today()
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order added successfully', 'order_id': new_order.id}), 201
"""
def serialize_mongo_document(doc):
    """
    Recursively convert non-serializable fields in MongoDB documents to JSON-serializable ones.
    """
    if isinstance(doc, ObjectId):
        return str(doc)
    if isinstance(doc, datetime):
        return doc.isoformat()
    if isinstance(doc, dict):
        return {key: serialize_mongo_document(value) for key, value in doc.items()}
    if isinstance(doc, list):
        return [serialize_mongo_document(item) for item in doc]
    return doc

def clear_all_data():
    with app.app_context():
        if USE_MONGO == "true":
            # Clear MongoDB collections
            mongo.db.clients.delete_many({})
            mongo.db.cars.delete_many({})
            mongo.db.sellers.delete_many({})
            mongo.db.orders.delete_many({})
            print("All MongoDB collections cleared.")
        else:
            # Clear SQLAlchemy tables
            try:
                db.session.execute("DELETE FROM orders")  # Clear orders
                db.session.execute("DELETE FROM sellers")  # Clear sellers
                db.session.execute("DELETE FROM cars")  # Clear cars
                db.session.execute("DELETE FROM clients")  # Clear clients
                db.session.commit()
                print("All SQLAlchemy tables cleared.")
            except Exception as e:
                db.session.rollback()
                print(f"Error clearing SQLAlchemy tables: {e}")
                return jsonify({"error": str(e)}), 500

        return jsonify({"message": "All data cleared successfully."}), 200

# Create tables and seed data based on the selected database
def create_tables_and_seed():
    clear_all_data()
    with app.app_context():
        if USE_MONGO == "true":
            # MongoDB seeding
            mongo.db.clients.insert_many([
                { "FullName": "John Doe", "Age": 35, "Gender": "Male", "CarType": "Sedan", "Price": 15000 },
                { "FullName": "Олена Петрова", "Age": 28, "Gender": "Жінка", "CarType": "Хетчбек", "Price": 12000 }
            ])
            print("Seeding clients data...")
            print([
                { "FullName": "John Doe", "Age": 35, "Gender": "Male", "CarType": "Sedan", "Price": 15000 },
                { "FullName": "Олена Петрова", "Age": 28, "Gender": "Жінка", "CarType": "Хетчбек", "Price": 12000 }
            ])
            mongo.db.cars.insert_many([
                { "CarType": "Седан", "Price": 15000, "Mileage": 80000, "TechnicalCondition": "Гарний" },
                { "CarType": "Хетчбек", "Price": 12000, "Mileage": 60000, "TechnicalCondition": "Середній" }
            ])
        
            mongo.db.sellers.insert_many([
                { "FullName": "Сергій Сергієнко", "Age": 40, "Gender": "Чоловік", "AdditionalInfo": "Досвідчений продавець" }
            ])

            # Find client and car by valid criteria
            client = mongo.db.clients.find_one({ "FullName": "John Doe" })
            car = mongo.db.cars.find_one({ "CarType": "Седан" })

            print("Client found:", client)  # Debugging print
            print("Car found:", car)  # Debugging print
            if client and car:
                client_id = client['_id']
                car_id = car['_id']

                # Adding an order example with MongoDB
                mongo.db.orders.insert_one({
                    "ClientID": str(client_id),  # Ensure ObjectId is converted to string
                    "CarID": str(car_id),
                    "OrderDate": datetime.today().isoformat()  # Use ISO format for datetime
                })
            else:
                print("Client or Car not found. Seeding failed for orders.")
            clear_all_data()
            return
        
        # SQLAlchemy seeding (PostgreSQL)
        db.create_all()

        if Client.query.count() == 0:
            initial_clients = [
                Client(full_name="Іван Іванов", age=30, gender="Чоловік", car_type="Седан", price=15000),
                Client(full_name="Марія Петренко", age=25, gender="Жінка", car_type="Хетчбек", price=12000),
                Client(full_name="Олег Сидоров", age=40, gender="Чоловік", car_type="Позашляховик", price=30000)
            ]
            db.session.bulk_save_objects(initial_clients)
            db.session.commit()

        if Car.query.count() == 0:
            initial_cars = [
                Car(car_type="Седан", price=15000, mileage=50000, technical_condition="Добрий"),
                Car(car_type="Хетчбек", price=12000, mileage=30000, technical_condition="Відмінний"),
                Car(car_type="Позашляховик", price=30000, mileage=100000, technical_condition="Задовільний")
            ]
            db.session.bulk_save_objects(initial_cars)
            db.session.commit()

        if Seller.query.count() == 0:
            initial_sellers = [
                Seller(full_name="Анна Смирнова", age=35, gender="Жінка", additional_info="10 років досвіду продажу"),
                Seller(full_name="Петро Коваленко", age=45, gender="Чоловік", additional_info="Експерт у сфері автомобілів")
            ]
            db.session.bulk_save_objects(initial_sellers)
            db.session.commit()

        if Order.query.count() == 0:
            initial_orders = [
                Order(client_id=1, car_id=1, order_date="2024-01-15"),
                Order(client_id=2, car_id=2, order_date="2024-01-20"),
                Order(client_id=3, car_id=3, order_date="2024-01-25")
            ]
            db.session.bulk_save_objects(initial_orders)
            db.session.commit()
        clear_all_data()

# REST Methods for clients
@app.route("/clients", methods=["GET"])
def get_clients():
    if USE_MONGO == "true":
        clients = mongo.db.clients.find()
        clients_list = []
        for client in clients:
            client['_id'] = str(client['_id'])  # Convert ObjectId to string
            clients_list.append(client)
        return jsonify(clients_list)
    else:
        clients = Client.query.all()
        return jsonify([{
            "id": client.id,
            "full_name": client.full_name,
            "age": client.age,
            "gender": client.gender,
            "car_type": client.car_type,
            "price": client.price
        } for client in clients])

@app.route("/clients", methods=["POST"])
def add_client():
    if USE_MONGO == "true":
        client_data = request.get_json()
        mongo.db.clients.insert_one(client_data)
        return jsonify({"message": "Client added to MongoDB"}), 201
    else:
        data = request.get_json()
        new_client = Client(
            full_name=data["full_name"],
            age=data["age"],
            gender=data["gender"],
            car_type=data["car_type"],
            price=data["price"]
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({"message": "Client added", "id": new_client.id}), 201

@app.route("/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    if USE_MONGO == "true":
        updated_data = request.get_json()
        result = mongo.db.clients.update_one({"_id": client_id}, {"$set": updated_data})
        if result.matched_count > 0:
            return jsonify({"message": "Client updated"})
        else:
            return jsonify({"message": "Client not found"}), 404
    else:
        data = request.get_json()
        client = Client.query.get_or_404(client_id)
        client.full_name = data.get("full_name", client.full_name)
        client.age = data.get("age", client.age)
        client.gender = data.get("gender", client.gender)
        client.car_type = data.get("car_type", client.car_type)
        client.price = data.get("price", client.price)
        db.session.commit()
        return jsonify({"message": "Client updated"})

@app.route("/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    if USE_MONGO == "true":
        result = mongo.db.clients.delete_one({"_id": client_id})
        if result.deleted_count > 0:
            return jsonify({"message": "Client deleted"})
        else:
            return jsonify({"message": "Client not found"}), 404
    else:
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": "Client deleted"})

@app.route('/cars', methods=['GET'])
def get_cars():
    if USE_MONGO:
        cars = mongo.db.cars.find()
        cars_list = []
        for car in cars:
            car['_id'] = str(car['_id'])  # Convert ObjectId to string
            cars_list.append(car)
        return jsonify(cars_list)
    else:
        cars = Car.query.all()
        return jsonify([{
            'id': car.id,
            'car_type': car.car_type,
            'price': str(car.price),
            'mileage': car.mileage,
            'technical_condition': car.technical_condition
        } for car in cars])


@app.route('/cars', methods=['POST'])
def add_car():
    if USE_MONGO:
        print("USING NOSQL")
        car_data = request.get_json()
        mongo.db.cars.insert_one(car_data)
        return jsonify({"message": "Car added to MongoDB"}), 201
    else:
        data = request.json
        new_car = Car(
            car_type=data['car_type'],
            price=data['price'],
            mileage=data['mileage'],
            technical_condition=data['technical_condition']
        )
        db.session.add(new_car)
        db.session.commit()
        return jsonify({'message': 'Car added successfully', 'car_id': new_car.id}), 201


@app.route('/sellers', methods=['GET'])
def get_sellers():
    if USE_MONGO:
        print("USING NOSQL")
        sellers = mongo.db.sellers.find()
        sellers_list = []
        for seller in sellers:
            seller['_id'] = str(seller['_id'])  # Convert ObjectId to string
            sellers_list.append(seller)
        return jsonify(sellers_list)
    else:
        sellers = Seller.query.all()
        return jsonify([{
            'id': seller.id,
            'full_name': seller.full_name,
            'age': seller.age,
            'gender': seller.gender,
            'additional_info': seller.additional_info
        } for seller in sellers])


@app.route('/sellers', methods=['POST'])
def add_seller():
    if USE_MONGO:
        print("USING NOSQL")
        seller_data = request.get_json()
        mongo.db.sellers.insert_one(seller_data)
        return jsonify({"message": "Seller added to MongoDB"}), 201
    else:
        data = request.json
        new_seller = Seller(
            full_name=data['full_name'],
            age=data['age'],
            gender=data['gender'],
            additional_info=data.get('additional_info', '')
        )
        db.session.add(new_seller)
        db.session.commit()
        return jsonify({'message': 'Seller added successfully', 'seller_id': new_seller.id}), 201


@app.route('/orders', methods=['GET'])
def get_orders():
    if USE_MONGO:
        print("USING NOSQL")
        orders = mongo.db.orders.find()
        orders_list = [serialize_mongo_document(order) for order in orders]
            #order['ClientID'] = str(order['ClientID'])
            #order['CarID'] = str(order['CarID'])
        return jsonify(orders_list)
    else:
        orders = Order.query.all()
        return jsonify([{
            'id': order.id,
            'client_id': order.client_id,
            'car_id': order.car_id,
            'order_date': order.order_date.isoformat()  # Ensure order_date is serializable
        } for order in orders])


@app.route('/orders', methods=['POST'])
def add_order():
    if USE_MONGO:
        print("USING NOSQL")
        order_data = request.get_json()
        order_data['_id'] = random.randint(0, 10000)
        mongo.db.orders.insert_one(order_data)
        return jsonify({"message": "Order added to MongoDB", 'order_id': order_data['_id']}), 201
    else:
        data = request.json
        new_order = Order(
            id = random.randint(0, 10000),
            client_id=data['client_id'],
            car_id=data['car_id'],
            order_date=date.today()
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order added successfully', 'order_id': new_order.id}), 201

# --- Запуск ---
if __name__ == "__main__":
    #create_tables_and_seed()
    app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# إعدادات MongoDB
app.config["MONGO_URI"] = "mongodb://warshatech:KS9SVRiWUSyDAJnc@cluster0.u78olpb.mongodb.net/raheeq"

mongo = PyMongo(app)


@ app.route('/')
def home():
    return 'Hello, World!'


@ app.route('/about')
def about():
    return 'About'


@ app.route('/jsontest')
def jsontest():
    return jsonify({"message": "Sale not found"}), 404


@ app.route('/get_data', methods=['GET'])
def get_sales():
    sales = []
    for sale in mongo.db.sales.find():
        sales.append({
            "sale_id": str(sale["_id"]),
            "client_id": sale["client_id"],
            "created_at": sale["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
            "name": sale["name"],
            "phone": sale["phone"],
            "chairs_number": sale["chairs_number"],
            "tables_number": sale["tables_number"],
            "other_products": sale["other_products"],
            "discount": sale["discount"],
            "total_amount": sale["total_amount"],
            "installments_number": sale["installments_number"],
            "address": sale["address"],
            "notes": sale["notes"],
            "status": sale["status"],
            "collected_installment_number": sale["collected_installment_number"],
            "future_installments_total": sale["future_installments_total"],
        })
    return jsonify(sales)

    # إضافة بيانات جديدة إلى Collection
    collection = mongo.db.sales
    result = collection.insert_one({"field": "value"})

    # إرجاع النتيجة
    return jsonify({"message": "Data added successfully"})

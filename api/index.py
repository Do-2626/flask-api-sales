from flask import Flask, request, jsonify
from .models import mongo, Sale
from .config import MONGO_URI
from flask_cors import CORS, cross_origin
import random
from bson.objectid import ObjectId

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# إعدادات قاعدة البيانات
app.config["MONGO_URI"] = MONGO_URI
mongo.init_app(app)


# نقاط النهاية لـ API

# ## إدارة المبيعات


@app.route('/sales', methods=['GET'])
@cross_origin()
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


@app.route('/sales/<sale_id>', methods=['GET'])
@cross_origin()
def get_sale(sale_id):
    sale = mongo.db.sales.find_one({"_id": ObjectId(sale_id)})
    if sale:
        return jsonify({
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
    else:
        return jsonify({"message": "Sale not found"}), 404


@app.route('/sales', methods=['POST'])
@cross_origin()
def create_sale():
    data = request.get_json()
    client_id = random.randint(1000, 9999)
    sale = Sale(
        client_id=client_id,
        name=data["name"],
        phone=data.get("phone"),
        chairs_number=data.get("chairs_number"),
        tables_number=data.get("tables_number"),
        other_products=data.get("other_products"),
        discount=data["discount"],
        total_amount=data["total_amount"],
        installments_number=data["installments_number"],
        address=data["address"],
        notes=data.get("notes"),
        status=data.get("status")
    )
    sale.save()
    return jsonify({"message": "Sale created successfully"})


@app.route('/sales/<sale_id>', methods=['DELETE'])
@cross_origin()
def delete_sale(sale_id):
    sale = Sale()
    sale.delete(sale_id)
    return jsonify({"message": "Sale deleted successfully"})


@app.route('/sales/<sale_id>', methods=['PUT'])
@cross_origin()
def update(sale_id):
    data = request.get_json()
    sale = Sale(sale_id, "", "", "", "", "",
                "", "", "", "", "", 0, "", "")

    sale.update(
        sale_id=sale_id,
        name=data.get('name'),
        phone=data.get('phone'),
        chairs_number=data.get('chairs_number'),
        tables_number=data.get('tables_number'),
        other_products=data.get('other_products'),
        discount=data.get('discount'),
        total_amount=data.get('total_amount'),
        installments_number=data.get('installments_number'),
        address=data.get('address'),
        notes=data.get('notes'),
        collected_installment_number=data.get('collected_installment_number'),
        future_installments_total=data.get('future_installments_total'),
        status=data.get('status'),
    )

    return jsonify({"message": "Sale updated successfully"})


@app.route('/sales/<sale_id>', methods=['POST'])
@cross_origin()
def issue_receipt(sale_id):
    sale_data = mongo.db.sales.find_one({"_id": ObjectId(sale_id)})
    sale = Sale(sale_data["_id"],
                sale_data["client_id"],
                sale_data["name"],
                sale_data["phone"],
                sale_data["chairs_number"],
                sale_data["tables_number"],
                sale_data["other_products"],
                sale_data["discount"],
                sale_data["total_amount"],
                sale_data["installments_number"],
                sale_data["address"],
                sale_data["notes"],
                sale_data["collected_installment_number"],
                sale_data["future_installments_total"],
                sale_data["status"],
                sale_data["created_at"]
                )

    if sale.issue_receipt():
        return jsonify({"message": "Receipt issued successfully", "sale": sale.to_json()})
    else:
        return jsonify({"message": "تم تحصيل جميع الأقساط"})

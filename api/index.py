from flask import Flask, request, jsonify 
from flask_cors import CORS, cross_origin
import random
from bson.objectid import ObjectId

# ###############################################
# ###############################################
# ##############[ models.py ]####################
# ###############################################
# ###############################################
from flask_pymongo import PyMongo 
from datetime import datetime
from bson.objectid import ObjectId


# إنشاء كائن PyMongo
mongo = PyMongo()

# تعريف نموذج البيع


class Sale:
    def __init__(self,
                 _id=None,
                 client_id=None,
                 name=None,
                 phone=None,
                 chairs_number=None,
                 tables_number=None,
                 other_products=None,
                 discount=None,
                 total_amount=None,
                 installments_number=None,
                 address=None,
                 notes=None,
                 collected_installment_number=0,
                 future_installments_total=None,
                 status=None,
                 created_at=None) -> None:

        self._id = _id
        self.client_id = client_id
        self.created_at = created_at or datetime.now()
        self.name = name
        self.phone = phone
        self.chairs_number = chairs_number
        self.tables_number = tables_number
        self.other_products = other_products
        self.discount = discount
        self.total_amount = total_amount
        self.installments_number = installments_number or 0  # قيمة افتراضية
        self.address = address
        self.notes = notes
        self.collected_installment_number = collected_installment_number
        self.future_installments_total = future_installments_total
        self.status = status

    # حفظ البيع في قاعدة البيانات
    def save(self):
        # حساب مجموع تحصيل الأشهر القادمة
        self.future_installments_total = (
            int(self.total_amount) * int(self.installments_number)
            - int(self.total_amount) * int(self.collected_installment_number)
        )
        sale_data = {
            "client_id": self.client_id,
            "created_at": self.created_at,
            "name": self.name,
            "phone": self.phone,
            "chairs_number": self.chairs_number,
            "tables_number": self.tables_number,
            "other_products": self.other_products,
            "discount": self.discount,
            "total_amount": self.total_amount,
            "installments_number": self.installments_number,
            "address": self.address,
            "notes": self.notes,
            "collected_installment_number": self.collected_installment_number,  # إضافة هذه السطر
            "future_installments_total": self.future_installments_total,
            "status": self.status,
        }
        mongo.db.sales.insert_one(sale_data)

    # حذف البيع من قاعدة البيانات
    def delete(self, sale_id):
        mongo.db.sales.delete_one({"_id": ObjectId(sale_id)})

    # تحديث معلومات البيع
    def update(self, sale_id, client_id=None, name=None, phone=None, chairs_number=None, tables_number=None, other_products=None,
               discount=None, total_amount=None, installments_number=None, address=None, notes=None,
               collected_installment_number=None, future_installments_total=None, status=None):
        update_data = {}
        if client_id:
            update_data["client_id"] = client_id
        if name:
            update_data["name"] = name
        if phone:
            update_data["phone"] = phone
        if chairs_number:
            update_data["chairs_number"] = chairs_number
        if tables_number:
            update_data["tables_number"] = tables_number
        if other_products:
            update_data["other_products"] = other_products
        if discount:
            update_data["discount"] = discount
        if total_amount:
            update_data["total_amount"] = total_amount
        if installments_number:
            update_data["installments_number"] = installments_number
        if address:
            update_data["address"] = address
        if notes:
            update_data["notes"] = notes
        if collected_installment_number:
            update_data["collected_installment_number"] = collected_installment_number
        if future_installments_total:
            update_data["future_installments_total"] = future_installments_total
        if status:
            update_data["status"] = status
        mongo.db.sales.update_one(
            {"_id": ObjectId(sale_id)}, {"$set": update_data})

    def issue_receipt(self):
        if int(self.collected_installment_number) < int(self.installments_number):
            self.collected_installment_number = int(
                self.collected_installment_number) + 1
            self.update(
                sale_id=self._id,
                collected_installment_number=self.collected_installment_number,
                future_installments_total=int(
                    self.total_amount)*int(self.installments_number)
                - int(self.collected_installment_number) *
                int(self.total_amount),

            )
            return True
        else:
            return False

    def to_json(self):
        return {
            "_id": str(self._id),
            "client_id": self.client_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "name": self.name,
            "phone": self.phone,
            "chairs_number": self.chairs_number,
            "tables_number": self.tables_number,
            "other_products": self.other_products,
            "discount": self.discount,
            "total_amount": self.total_amount,
            "installments_number": self.installments_number,
            "address": self.address,
            "notes": self.notes,
            "collected_installment_number": self.collected_installment_number,
            "future_installments_total": self.future_installments_total,
            "status": self.status,
        }


# ###############################################
# ###############################################
# ##############[ // models.py ]#################
# ###############################################
# ###############################################


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# إعدادات قاعدة البيانات
app.config["MONGO_URI"] = "mongodb+srv://warshatech:KS9SVRiWUSyDAJnc@cluster0.u78olpb.mongodb.net/raheeq"
mongo.init_app(app)


# نقاط النهاية لـ API

# ## إدارة المبيعات


@app.route('/', methods=['GET'])
@cross_origin()
def index():
  return "Hello, World!"



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

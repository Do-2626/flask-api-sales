from flask_pymongo import PyMongo
from config import MONGO_URI
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

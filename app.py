# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///licenses.db'
db = SQLAlchemy(app)

class LicenseKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(100), unique=True, nullable=False)
    machine_signature = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    expire_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

@app.route("/", methods=["GET"])
def home():
    # Tarayıcıdan http://127.0.0.1:5000 adresine girince bu dönecek
    return "Merhaba! Lisans doğrulama endpoint'i için /verify adresine POST isteği atın."

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "JSON body required"}), 400

    license_key = data.get("license_key")
    machine_signature = data.get("machine_signature")

    if not license_key or not machine_signature:
        return jsonify({"status": "error", "message": "Missing license_key or machine_signature"}), 400

    # Lisans kodunu veritabanında ara
    lic = LicenseKey.query.filter_by(license_key=license_key).first()

    if not lic:
        return jsonify({"status": "error", "message": "Invalid license key"}), 400

    if not lic.is_active:
        return jsonify({"status": "error", "message": "License is inactive"}), 403

    # Daha önce machine_signature set edilmemişse bu ilk aktivasyon
    if lic.machine_signature is None:
        # start_date ve expire_date'i burada ayarlıyoruz (ilk aktivasyondan itibaren 15 gün örneği)
        lic.machine_signature = machine_signature
        lic.start_date = datetime.utcnow()
        lic.expire_date = datetime.utcnow() + timedelta(days=15)  # sabit 15 gün
        db.session.commit()
        return jsonify({"status": "success", "message": "License activated"}), 200
    else:
        # Lisans daha önce aktivasyona sahip, makine imzası eşleşmeli
        if lic.machine_signature != machine_signature:
            return jsonify({"status": "error", "message": "License already used on another machine"}), 403

        # Süre kontrolü
        if lic.expire_date and datetime.utcnow() > lic.expire_date:
            return jsonify({"status": "error", "message": "License expired"}), 403

        return jsonify({"status": "success", "message": "License valid"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)

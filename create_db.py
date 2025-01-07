# create_db.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///licenses.db'
db = SQLAlchemy(app)

class LicenseKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(100), unique=True, nullable=False)
    machine_signature = db.Column(db.String(200), nullable=True)  # HWID
    start_date = db.Column(db.DateTime, nullable=True)            # İlk aktivasyon tarihi
    expire_date = db.Column(db.DateTime, nullable=True)           # Lisansın bitiş tarihi
    is_active = db.Column(db.Boolean, default=True)               # Lisans aktif mi?

    def __repr__(self):
        return f"<LicenseKey {self.license_key}>"

if __name__ == "__main__":
    # ÖNEMLİ: Uygulama bağlamı (context) içinde tablo oluşturma
    with app.app_context():
        db.create_all()
        print("Veritabanı ve tablo oluşturuldu.")

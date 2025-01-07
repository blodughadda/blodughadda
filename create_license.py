# create_license.py
import uuid
from datetime import datetime
from app import db, LicenseKey, app

def create_license_key():
    new_key = str(uuid.uuid4()).upper()
    with app.app_context():
        license_obj = LicenseKey(
            license_key=new_key,
            machine_signature=None,
            start_date=None,
            expire_date=None,
            is_active=True
        )
        db.session.add(license_obj)
        db.session.commit()
        print("Created license key:", new_key)

if __name__ == "__main__":
    create_license_key()

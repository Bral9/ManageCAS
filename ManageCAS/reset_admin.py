from website import create_app
from website.database import db
from website.models import Admin
from werkzeug.security import generate_password_hash, check_password_hash

app = create_app()
with app.app_context():
    print([a.email for a in Admin.query.all()])
    admin = Admin.query.filter_by(email="brealtchuimi@gmail.com").first()
    if admin:
        if not check_password_hash(admin.password, "1234567"):
            admin.password = generate_password_hash("1234567")
            db.session.commit()
            print("Password reset for:", admin.email)
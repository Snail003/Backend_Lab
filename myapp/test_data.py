from click import echo
from passlib.hash import pbkdf2_sha256

from myapp import app, db
from myapp.models import UserModel, CategoryModel, RecordModel


@app.cli.command("seed-testdata")
def seed_testdata():
    with app.app_context():
        if UserModel.query.first():
            echo("DB already has data – skipping.")
            return

        u1 = UserModel(
            name="testUser2332",
            password=pbkdf2_sha256.hash("password1"),
        )
        u2 = UserModel(
            name="testUsering2352",
            password=pbkdf2_sha256.hash("password2"),
        )
        db.session.add_all([u1, u2])
        db.session.flush()

        c_g1 = CategoryModel(name="Transport", is_global=True,  owner_user_id=None)
        c_g2 = CategoryModel(name="Food",      is_global=True,  owner_user_id=None)
        c_u1 = CategoryModel(name="Test",      is_global=False, owner_user_id=u1.id)
        c_u2 = CategoryModel(name="Test2",     is_global=False, owner_user_id=u2.id)
        db.session.add_all([c_g1, c_g2, c_u1, c_u2])
        db.session.flush()

        r1 = RecordModel(user_id=u1.id, category_id=c_g1.id, expenses=500.0)
        db.session.add(r1)

        db.session.commit()
        echo("Seed done.")
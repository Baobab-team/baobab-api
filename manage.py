from flask.cli import FlaskGroup

from app import create_app, db
from app.businesses.models import Category, Business, Phone

app = create_app()
cli = FlaskGroup(app)


@cli.command("seed_db")
def seed_db():

    db.drop_all()
    db.create_all()

    db.session.add(Category(name="Restaurant"))
    db.session.add(Business(name="Gracia Afrika",
                            description="description",
                            category_id=1,
                            phones=[
                                Phone(
                                    number="514-555-5555",
                                    extension="",
                                    type="tel",
                                ),
                                Phone(
                                    number="514-232-3456",
                                    extension="",
                                    type="tel",
                                ),
                            ]
                            ))
    db.session.add(Business(name="Mama africa",
                            description="description",
                            category_id=1,
                            ))
    db.session.add(Business(name="Marmite africaine",
                            description="description",
                            category_id=1,
                            ))

    db.session.add(Category(name="Barbershop"))
    db.session.add(Business(name="La ruche",
                            description="description",
                            category_id=2,
                            ))
    db.session.add(Business(name="Famous cut",
                            description="description",
                            category_id=2,
                            ))
    db.session.add(Business(name="Rick's cut",
                            description="description",
                            category_id=2,
                            ))
    db.session.commit()


if __name__ == '__main__':
    cli()

from flask.cli import FlaskGroup

from app import create_app, db
from app.businesses.models import Category, Business, Phone, Plate, Tag, BusinessHour, SocialLink, Address, Restaurant, Menu
from datetime import time, timedelta, date

app = create_app()
cli = FlaskGroup(app)


@cli.command("seed_db")
def seed_db():

    db.drop_all()
    db.create_all()

    db.session.add(Category(name="Restaurant"))
    db.session.add(
        Restaurant(
            menus=[
                Menu(
                    name="menu1",
                    start=time(19, 30),
                    end=time(9, 30),
                    plates=[
                        Plate(
                            name="poulet",
                            price=22.50,
                            description="hello plate"
                        ),
                        Plate(
                            name="couscous",
                            price=20.50,
                            description="hello world"
                        ),
                        Plate(
                            name="foufou",
                            price=10.50,
                            description="hello foufou"
                        )
                    ]
                )
            ]
        ),
    )
    db.session.add(Business(name="Gracia Afrika",
                            description="Lorem Ipsum is simply dummy text of the printing and typesetting industry. "
                                        "Lorem Ipsum has been the industry's standard dummy text ever since the "
                                        "1500s, when an unknown printer took a galley of type and scrambled it to "
                                        "make a type specimen book. It has survived not only five centuries, "
                                        "but also the leap into electronic typesetting, remaining essentially "
                                        "unchanged. It was popularised in the 1960s with the release of Letraset "
                                        "sheets containing Lorem Ipsum passages, and more recently with desktop "
                                        "publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                            notes="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem "
                                  "Ipsum has been the industry's standard dummy text ever since the 1500s, "
                                  "when an unknown printer took a galley of type and scrambled it to make a type "
                                  "specimen book. It has survived not only five centuries, but also the leap into "
                                  "electronic typesetting, remaining essentially unchanged. It was popularised in the "
                                  "1960s with the release of Letraset sheets containing Lorem Ipsum passages, "
                                  "and more recently with desktop publishing software like Aldus PageMaker including "
                                  "versions of Lorem Ipsum.",
                            category_id=1,
                            accepted_at=date.today(),
                            slogan="Hello world",
                            website="www.helloworld.com",
                            email="helloworld@hello.com",
                            created_at=date.today(),
                            restaurant_id=1,
                            capacity=23,
                            addresses=[
                                Address(
                                    street_number="5692",
                                    street_type="rue",
                                    street_name="saint-André",
                                    direction=Address.DirectionEnum.e.value,
                                    city="Montreal",
                                    zip_code="h3s2k1",
                                    province=Address.ProvinceEnum.qc.value,
                                    region="Quebec",
                                    country="Canada"
                                ),
                                Address(
                                    street_number="6325",
                                    street_type="av",
                                    street_name="somerled",
                                    direction=Address.DirectionEnum.w.value,
                                    city="Montreal",
                                    zip_code="h3s2k1",
                                    province=Address.ProvinceEnum.ab.value,
                                    region="Quebec",
                                    country="Canada"
                                )
                            ],
                            payment_types=[
                                Business.PaymentTypeEnum.cash.value,
                                Business.PaymentTypeEnum.credit.value
                            ],
                            status=Business.StatusEnum.accepted.value,
                            social_links=[
                                SocialLink(
                                    link="www.facebook.com/willkoua",
                                    type=SocialLink.TypeEnum.facebook.value,
                                ),
                                SocialLink(
                                    link="www.instagram.com/willkoua",
                                    type=SocialLink.TypeEnum.instragram.value,
                                )
                            ],
                            business_hours=[
                                BusinessHour(
                                    day=BusinessHour.DaysEnum.thursday.value,
                                    closing_time=time(19, 30),
                                    opening_time=time(9, 30)
                                ),
                                BusinessHour(
                                    day=BusinessHour.DaysEnum.wednesday.value,
                                    closing_time=time(19, 30),
                                    opening_time=time(9, 30)
                                ),
                                BusinessHour(
                                    day=BusinessHour.DaysEnum.tuesday.value,
                                    closing_time=time(19, 30),
                                    opening_time=time(9, 30)
                                ),
                                BusinessHour(
                                    day=BusinessHour.DaysEnum.friday.value,
                                    closing_time=time(19, 30),
                                    opening_time=time(9, 30)
                                ),
                                BusinessHour(
                                    day=BusinessHour.DaysEnum.saturday.value,
                                    closing_time=time(19, 30),
                                    opening_time=time(9, 30)
                                ),
                                BusinessHour(
                                    day=BusinessHour.DaysEnum.sunday.value,
                                    closing_time=time(19, 30),
                                    opening_time=time(9, 30)
                                )
                            ],
                            tags=[
                                Tag(
                                    name="tropBon"
                                ),
                                Tag(
                                    name="restaurant"
                                ),
                                Tag(
                                    name="montreal"
                                )
                            ],
                            phones=[
                                Phone(
                                    number="514-555-5555",
                                    extension="+1",
                                    type="telephone",
                                ),
                                Phone(
                                    number="514-232-3456",
                                    extension="+1",
                                    type="telephone",
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

    print("Suuccesfuly seeded the database")

if __name__ == '__main__':
    cli()

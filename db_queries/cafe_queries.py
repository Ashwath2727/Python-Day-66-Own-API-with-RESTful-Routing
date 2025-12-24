import random

from extensions import db
from models.cafe import Cafe

class CafeQueries:

    def add_cafe(self, cafe):
        try:
            print("=================> Adding cafe to database")

            present_cafe = self.get_cafe_by_name(cafe.name)

            print(f"present cafe = {present_cafe}")

            if present_cafe is None:
                # if cafe["name"] != present_cafe["name"]:
                print("adding=====================> ")
                db.session.add(cafe)
                db.session.commit()
            else:
                print(f"cafe {cafe} already exists")

                print("=================> Finished adding cafe to database")
        except Exception as e:
            print(f"Error adding cafe {cafe} to database: {e}")


    def get_cafe_by_name(self, cafe_name):
        try:
            print("=================> Getting cafe by name")
            cafe = Cafe.query.filter_by(name=cafe_name).all()

            if len(cafe) == 0:
                return None
            else:
                print(cafe[0])

                print("=================> Finished getting cafe by name")
                return cafe[0]
        except Exception as e:
            print(f"Error getting cafe by name {cafe_name}: {e}")


    def get_all_cafes(self):
        try:
            print("=================> Getting all cafes")

            cafes = Cafe.query.order_by(Cafe.id).all()
            return cafes

        except Exception as e:
            print(f"Error getting all cafes: {e}")


    def get_random_cafe(self):
        try:
            print("=================> Getting random cafe")

            cafes = self.get_all_cafes()

            return random.choice(cafes)

        except Exception as e:
            print(f"Error getting random cafe: {e}")


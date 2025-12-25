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


    def get_cafe_by_id(self, cafe_id):

        try:
            print("=================> Getting cafe by id")

            cafe = Cafe.query.filter_by(id=cafe_id).all()

            if len(cafe) == 0:
                return None
            else:
                print(cafe[0])

                print("=================> Finished getting cafe by id")
                return cafe[0]
        except Exception as e:
            message = f"Error getting cafe by id: {cafe_id}: {e}"
            print(message)


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


    def get_cafe_by_location(self, location):
        try:
            print("=================> Getting cafe by location")
            cafes = Cafe.query.filter_by(location=location).all()

            return cafes

        except Exception as e:
            print(f"Error getting cafe by location: {location}: {e}")


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


    def update_price(self, cafe_id, new_price):
        try:
            print("================> Updating price")

            cafe = Cafe.query.filter_by(id=cafe_id).all()
            if len(cafe) == 0:
                return {"message": {"error": "cafe not found"}, "code": 404}

            else:
                cafe[1].coffee_price = new_price
                db.session.commit()

                print("===============> Finished updating price")
                return {"message": {"success": "coffee price updated with new price"}, "code": 200}

        except Exception as e:
            error_message = f"Error updating price: {e}"
            print(f"Error updating price: {e}")
            return {"message": {"error": error_message}, "code": 500}



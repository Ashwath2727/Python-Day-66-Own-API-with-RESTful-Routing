import requests

from models.cafe import Cafe


class CafeData:

    def __init__(self):
        self.cafe_api = "https://api.npoint.io/a90756d52d3d17a93886"

    def get_cafes(self):
        response = requests.get(self.cafe_api)
        cafe_dict_list = response.json()
        print(f"cafe_dict_list = {cafe_dict_list}")

        cafes = []

        for cafe in cafe_dict_list:
            c = Cafe(
                name = cafe["name"],
                map_url = cafe["map_url"],
                img_url = cafe["img_url"],
                location = cafe["location"],
                seats = cafe["seats"],
                has_toilet = True if cafe["has_toilet"] == "true" else False,
                has_wifi = True if cafe["has_wifi"] == "true" else False,
                has_sockets = True if cafe["has_sockets"] == "true" else False,
                can_take_calls = True if cafe["can_take_calls"] == "true" else False,
                coffee_price = cafe["coffee_price"]
            )

            cafes.append(c)
        # cafes = []
        # for cafe in cafe_dict_list:
        #     new_cafe_object = Cafe(**cafe)
        #
        #     cafes.append(new_cafe_object)

        print(f"Cafes =======================> {cafes}")
        return cafes

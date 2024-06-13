from flask import Flask
from api.user_manager import user_manager_blueprint
from api.country_city_manager import country_city_manager_blueprint
from api.amenity_manager import amenity_blueprint
from api.place_manager import place_manager_blueprint
from api.review_manager import review_manager_blueprint

app = Flask(__name__)

app.register_blueprint(user_manager_blueprint)
app.register_blueprint(country_city_manager_blueprint)
app.register_blueprint(amenity_blueprint)
app.register_blueprint(place_manager_blueprint)
app.register_blueprint(review_manager_blueprint)

if __name__ == "__main__":
    app.run()
from model.BaseModel import BaseModel


class Place(BaseModel):
    def __init__(self, name, description, address, city_id, latitude, longitude, host_id,
                 number_of_rooms, number_of_bathrooms, price_per_night, max_guests, amenity_ids=[], **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenity_ids = amenity_ids

    def __str__(self):
        return f"[Place] ({self.id}) {self.to_dict()}"
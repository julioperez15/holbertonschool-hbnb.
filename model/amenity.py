from model.BaseModel import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def __str__(self):
        return f"[Amenity] ({self.id}) {self.to_dict()}"
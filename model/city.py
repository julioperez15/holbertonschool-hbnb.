from model.BaseModel import BaseModel


class City(BaseModel):
    def __init__(self, name, country_code, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.country_code = country_code

    def __str__(self):
        return f"[City] ({self.id}) {self.to_dict()}"
from model.BaseModel import BaseModel


class User(BaseModel):
    def __init__(self, email, password, first_name="", last_name="", **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []

    def __str__(self):
        return f"[User] ({self.id}) {self.to_dict()}"
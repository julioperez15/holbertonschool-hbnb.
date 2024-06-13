from model.BaseModel import BaseModel


class Review(BaseModel):
    def __init__(self, place_id, user_id, rating, comment, **kwargs):
        super().__init__(**kwargs)
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    def __str__(self):
        return f"[Review] ({self.id}) {self.to_dict()}"
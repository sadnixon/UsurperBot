class gameBonus:
    def __init__(self, name, card_id, text):
        self.name = name
        self.card_id = card_id
        self.text = text

    def __str__(self):
        return f"{self.name}\n \n{self.text}"

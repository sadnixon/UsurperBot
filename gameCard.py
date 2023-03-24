class gameCard:
    def __init__(self, name, card_id, base_points, color, hands, eyes, bags, placement_grid, instant, text, dummy=False):
        self.name = name
        self.card_id = card_id

        self.og_base_points = base_points
        self.base_points = base_points

        self.og_points = base_points
        self.points = base_points

        self.og_color = color
        self.color = color

        self.og_hands = hands
        self.hands = hands

        self.og_eyes = eyes
        self.eyes = eyes

        self.og_bags = bags
        self.bags = bags

        self.placement_grid = placement_grid
        self.instant = instant
        self.activation = False
        self.placement_indices = []
        for i in range(9):
            if self.placement_grid[i//3][i%3]>0:
                self.placement_indices.append(i)
                if self.placement_grid[i//3][i%3]==2:
                    self.activation = True
        self.text = text
        self.flipped = False
        self.g3_stored_data = {}
        self.dummy = dummy

    def __str__(self):
        if self.flipped:
            return f"FLIPPED\n{self.name}"
        if self.g3_stored_data != {}:
            return f"{self.name}\nCOPYING\n{self.g3_stored_data['copied_name']}"
        grid_string = ""
        for i in range(3):
            for j in range(3):
                if self.placement_grid[i][j] == 0:
                    grid_string = grid_string+"⬛"
                elif self.placement_grid[i][j] == 1:
                    grid_string = grid_string+"⬜"
                else:
                    grid_string = grid_string+"➕"
            grid_string = grid_string+"\n"
        return f"({self.og_base_points}) {self.name} ({self.color})\nHands: {self.hands}\nEyes: {self.eyes}\nBags: {self.bags}\n{grid_string}{self.text}"

    def __copy__(self):
        new_copy = gameCard(self.name, self.card_id, self.og_base_points, self.color, self.hands,
                            self.eyes, self.bags, self.placement_grid, self.instant, self.text, self.dummy)
        new_copy.g3_stored_data = self.g3_stored_data.copy()
        new_copy.base_points = self.base_points
        new_copy.points = self.points
        new_copy.color = self.color
        new_copy.hands = self.hands
        new_copy.eyes = self.eyes
        new_copy.bags = self.bags
        new_copy.flipped = self.flipped
        return new_copy

    def changepoints(self, p):
        self.points += p

    def changeheb(self, p, symbol):
        if symbol == 'hands':
            self.hands += p
        elif symbol == 'eyes':
            self.eyes += p
        else:
            self.bags += p

    def reset(self):
        if self.flipped:
            self.base_points = 0
            self.points = 0
            self.color = ""
            self.hands = 0
            self.eyes = 0
            self.bags = 0
        else:
            self.base_points = self.og_base_points
            self.points = self.og_points
            self.color = self.og_color
            self.hands = self.og_hands
            self.eyes = self.og_eyes
            self.bags = self.og_bags

    def flip(self):
        if self.flipped:
            self.base_points = self.og_base_points
            self.points = self.og_points
            self.color = self.og_color
            self.hands = self.og_hands
            self.eyes = self.og_eyes
            self.bags = self.og_bags
        else:
            self.base_points = 0
            self.points = 0
            self.color = ""
            self.hands = 0
            self.eyes = 0
            self.bags = 0
        self.flipped = not self.flipped

    def g3_copy(self, copied_card):
        if self.g3_stored_data != {}:
            return
        self.g3_stored_data['copied_name'] = copied_card.name
        self.g3_stored_data['card_id'] = self.card_id
        self.card_id = copied_card.card_id
        self.g3_stored_data['og_base_points'] = self.og_base_points
        self.og_base_points = copied_card.og_base_points
        self.base_points = copied_card.og_base_points
        self.og_points = copied_card.og_base_points
        self.points = copied_card.og_base_points
        self.g3_stored_data['og_color'] = self.og_color
        self.og_color = copied_card.color
        self.color = copied_card.color
        self.g3_stored_data['og_hands'] = self.og_hands
        self.og_hands = copied_card.hands
        self.hands = copied_card.hands
        self.g3_stored_data['og_eyes'] = self.og_eyes
        self.og_eyes = copied_card.eyes
        self.eyes = copied_card.eyes
        self.g3_stored_data['og_bags'] = self.og_bags
        self.og_bags = copied_card.bags
        self.bags = copied_card.bags
        self.g3_stored_data['flipped'] = self.flipped
        self.flipped = copied_card.flipped

    def un_copy(self):
        if self.g3_stored_data == {}:
            return
        self.card_id = self.g3_stored_data['card_id']
        self.og_base_points = self.g3_stored_data['og_base_points']
        self.base_points = self.g3_stored_data['og_base_points']
        self.og_points = self.g3_stored_data['og_base_points']
        self.points = self.g3_stored_data['og_base_points']
        self.og_color = self.g3_stored_data['og_color']
        self.color = self.g3_stored_data['og_color']
        self.og_hands = self.g3_stored_data['og_hands']
        self.hands = self.g3_stored_data['og_hands']
        self.og_eyes = self.g3_stored_data['og_eyes']
        self.eyes = self.g3_stored_data['og_eyes']
        self.og_bags = self.g3_stored_data['og_bags']
        self.bags = self.g3_stored_data['og_bags']
        self.flipped = self.g3_stored_data['flipped']
        self.g3_stored_data = {}

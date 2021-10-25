
class Player:
    def __init__(self, user: User, player_num: int):
        if user:
            self.user = user
        # else, create an AI player
        self.player_num = player_num

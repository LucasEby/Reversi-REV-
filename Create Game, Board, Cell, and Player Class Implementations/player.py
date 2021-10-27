
class Player:
    def __init__(self, user: User, player_num: int):
        if user:
            self.user = user
        # else, create an AI player
        if (player_num != 1) & (player_num != 2):
            raise Exception("Player num must be valid (1 or 2)")
        self.player_num = player_num

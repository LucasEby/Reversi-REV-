from typing import Tuple, List


class CalculateNewELOs:
    @classmethod
    def get_new_elos(
        cls, p1_id: int, p1_old_elo: int, p2_id: int, p2_old_elo: int, p1_won: bool
    ) -> List[Tuple[int, int]]:
        """
        Calculate the new ELOs for two players.

        :param p1_id: the id of the first player
        :param p1_old_elo: the old ELO of the first player
        :param p2_id: the id of the second player
        :param p2_old_elo: the old ELO of the second player
        :param p1_won: whether the first player won the game
        :return: the two players IDs with their new ELOs
        """
        expected_1: float = cls.__expected(p1_old_elo, p2_old_elo)
        expected_2: float = cls.__expected(p2_old_elo, p1_old_elo)
        p1_new_elo: int = cls.__calc_elo(p1_old_elo, p1_won, expected_1)
        p2_new_elo: int = cls.__calc_elo(p2_old_elo, not p1_won, expected_2)
        return [(p1_id, p1_new_elo), (p2_id, p2_new_elo)]

    @classmethod
    def __expected(cls, elo_a: int, elo_b: int) -> float:
        """
        Calculate the expected outcome for this player (percentage).
        :param elo_a: the old ELO of the player whose expected outcome is being calculated
        :param elo_b: the old ELO of the opponent
        """
        return 1.0 / (1 + (10 ** ((elo_a - elo_b) / 400)))

    @classmethod
    def __calc_elo(
        cls, old_elo: int, player_won: bool, expected_outcome: float
    ) -> int:
        """
        Calculate the player's new ELO.
        :param old_elo: the player's old ELO
        :param player_won: whether the player won the last game or not
        :param expected_outcome: the expected outcome of the game for this player
        """
        return old_elo + int(32 * (player_won - expected_outcome))

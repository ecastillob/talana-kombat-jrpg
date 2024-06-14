from collections import deque

from django.conf import settings


class Player:
    def __init__(self, name: str, movements: list[str], hits: list[str], special_movements: tuple):
        self.name = name
        self.movements = deque(movements)
        self.special_movements = special_movements
        self.hits = deque(hits)
        self.energy = settings.MAX_PLAYER_ENERGY


class TalanaKombat:
    def __init__(self, player1: dict, player2: dict):
        self.player1 = Player(
            name=settings.PLAYER_1_NAME,
            movements=player1["movimientos"],
            hits=player1["golpes"],
            special_movements=(
                # movement, hit, damage, name
                ("DSD", "P", 3, "Taladoken"),
                ("SD", "K", 2, "Remuyuken"),
                ("", "P", 1, "Puño"),
                ("", "K", 1, "Patada"),
            ),
        )
        self.player2 = Player(
            name=settings.PLAYER_2_NAME,
            movements=player2["movimientos"],
            hits=player2["golpes"],
            special_movements=(
                # movement, hit, damage, name
                ("SA", "K", 3, "Remuyuken"),
                ("ASA", "P", 2, "Taladoken"),
                ("", "P", 1, "Puño"),
                ("", "K", 1, "Patada"),
            ),
        )
        self.starts_player1 = False
        self.starts_player2 = False
        self.movements = []
        self.winner = {}

    def _define_start_player(self):
        player1_moves, player1_hits = self.player1.movements, self.player1.hits
        player2_moves, player2_hits = self.player2.movements, self.player2.hits
        if len(player1_moves) + len(player1_hits) < len(player2_moves) + len(player2_hits):
            self.starts_player1 = True
        elif len(player1_moves) + len(player1_hits) > len(player2_moves) + len(player2_hits):
            self.starts_player2 = True
        else:
            if len(player1_moves) < len(player2_moves):
                self.starts_player1 = True
            elif len(player1_moves) > len(player2_moves):
                self.starts_player2 = True
            else:
                if len(player1_hits) < len(player2_hits):
                    self.starts_player1 = True
                elif len(player1_hits) > len(player2_hits):
                    self.starts_player2 = True
                else:
                    self.starts_player1 = True

    def kombat(self):
        self._define_start_player()
        while True:
            if self.starts_player1:
                self.starts_player2 = True
                if self.player1.movements:
                    finish_game = self._run_player(self.player1, self.player2)
                    if finish_game:
                        break
            else:
                self.starts_player1 = True
            if self.starts_player2:
                self.starts_player1 = True
                if self.player2.movements:
                    finish_game = self._run_player(self.player2, self.player1)
                    if finish_game:
                        break
            else:
                self.starts_player2 = True
        return {
            "movements": self.movements,
            "winner": self.winner,
        }

    def _run_player(self, player1: Player, player2: Player) -> bool:
        finish_game = False
        p1_move = player1.movements.popleft()
        p1_hit = player1.hits.popleft()
        if p1_move and not p1_hit:
            self.movements.append(f"{player1.name} se mueve")
        else:
            for move, hit, damage, name in player1.special_movements:
                if p1_move.endswith(move) and p1_hit == hit:
                    player2.energy -= damage
                    self.movements.append(f"{player1.name} da un {name}")
                    break
        if player2.energy <= 0:
            self.movements.append(f"{player1.name} gana la pelea y aún le queda {player1.energy} de energía")
            self.winner = {
                "name": player1.name,
                "energy": player1.energy,
            }
            finish_game = True
        return finish_game

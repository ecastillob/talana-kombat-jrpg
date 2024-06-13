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
                ("SA", "K", 3, "Remuyuken"),
                ("ASA", "P", 2, "Taladoken"),
                ("", "P", 1, "Puño"),
                ("", "K", 1, "Patada"),
            ),
        )
        self.starts_player1 = False
        self.starts_player2 = False

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
        movements = []
        while True:
            if self.starts_player1:
                self.starts_player2 = True
                if self.player1.movements:
                    p1_move = self.player1.movements.popleft()
                    p1_hit = self.player1.hits.popleft()
                    if p1_move and not p1_hit:
                        movements.append(f"{self.player1.name} se mueve")
                    else:
                        for move, hit, damage, name in self.player1.special_movements:
                            if p1_move.endswith(move) and p1_hit == hit:
                                self.player2.energy -= damage
                                movements.append(f"{self.player1.name} da un {name}")
                                break
                    if self.player2.energy <= 0:
                        movements.append(
                            f"{self.player1.name} gana la pelea y aún le queda {self.player1.energy} de energía"
                        )
                        break
            else:
                self.starts_player1 = True
            if self.starts_player2:
                self.starts_player1 = True
                if self.player2.movements:
                    p2_move = self.player2.movements.popleft()
                    p2_hit = self.player2.hits.popleft()
                    if p2_move and not p2_hit:
                        movements.append(f"{self.player2.name} se mueve")
                    for move, hit, damage, name in self.player2.special_movements:
                        if p2_move.endswith(move) and p2_hit == hit:
                            self.player1.energy -= damage
                            movements.append(f"{self.player2.name} da un {name}")
                            break
                    if self.player1.energy <= 0:
                        movements.append(
                            f"{self.player2.name} gana la pelea y aún le queda {self.player2.energy} de energía"
                        )
                        break
            else:
                self.starts_player2 = True
        return movements

from dataclasses import dataclass

@dataclass
class BotWinrate:
    wins: int = 0
    losses: int = 0
    draws: int = 0

    def on_win(self):
        self.wins += 1

    def on_loss(self):
        self.losses += 1

    def on_draw(self):
        self.draws += 1
    
    def get_winrate(self) -> float:
        return self.wins / (self.get_total() or 1)
    
    def get_total(self) -> int:
        return self.wins + self.losses + self.draws

    def __str__(self):
        return f"[WINRATE] {self.wins}/{self.get_total()} = {100*self.get_winrate()}%"
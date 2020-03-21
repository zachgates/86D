from ...core import gameclass, CardGame


@gameclass
class BlackjackGame(CardGame):

    def play(self):
        super().play()
        self.dealer.insurance()

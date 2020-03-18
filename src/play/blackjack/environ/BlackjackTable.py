from ....core import CardTable


class BlackjackTable(CardTable):

    def __init__(self):
        from .. import BlackjackDealer # Avoid circular import
        super().__init__(BlackjackDealer)

    def play(self):
        super().play()
        self.dealer.insurance()

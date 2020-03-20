if __name__ == '__main__':
    from .core import CardPlayer
    from .play import BlackjackTable
    p1 = CardPlayer(_funds=5000)
    p2 = CardPlayer(_funds=5000)
    t = BlackjackTable()
    t.add_player(p1)
    t.add_player(p2)
    t.play()
    t.remove_player(p1)
    t.remove_player(p2)

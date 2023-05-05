class Poker:
    suits = {'Club': '♣', 'Diamond': '♦', 'Heart': '♥', 'Spade': '♠'}
    points = {1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6',
              7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K'}

    def __init__(self, suit, point: int) -> None:
        self.suit = self.suits[suit]
        self.point = self.points[point]
        if (point == 1):
            self.value = 14
        else:
            self.value = point

    def __repr__(self) -> str:
        return f"[{self.suit}] {self.point}"


a = Poker('Heart', 15)
print(a.value)

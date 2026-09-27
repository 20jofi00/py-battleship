class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def _calc(self, num: int) -> list:
        points = []
        if self.start[num] > self.end[num]:
            for i in range(self.start[num] - self.end[num] + 1):
                poi = self.end[num] + i
                points.append(poi)
        else:
            for i in range(self.end[num] - self.start[num] + 1):
                poi = self.start[num] + i
                points.append(poi)
        return points

    def __init__(
        self,
        start: tuple,
        end: tuple,
        is_drowned: bool = False,
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks: list[Deck] = []

        if start[0] != end[0]:
            points = self._calc(0)
            for point in points:
                self.decks.append(Deck(row=point, column=start[1]))
        elif start[1] != end[1]:
            points = self._calc(1)
            for point in points:
                self.decks.append(Deck(row=start[0], column=point))

        else:
            self.decks.append(Deck(row=start[0], column=start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row=row, column=column)
        if deck:
            deck.is_alive = False

        for deck in self.decks:
            if deck.is_alive:
                self.is_drowned = False
                break
        else:
            self.is_drowned = True


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        self.field = {}
        for boat in ships:
            ship = Ship(start=boat[0], end=boat[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship: Ship = self.field[location]
            ship.fire(row=location[0], column=location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

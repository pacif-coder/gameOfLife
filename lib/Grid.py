import pickle

from . Element import Element

class Grid:
    _elements = None
    _rows = None
    _cols = None
    _type = None

    _neighbour = {
        'square': (
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        )
    }

    def __init__(self, type = None, cols = None, rows = None):
        self._type = type
        self._rows = rows
        self._cols = cols

    def getSize(self):
        return Element.getSize(self._type, self._cols, self._rows)

    def _fill(self):
        if None != self._elements:
            return

        if None == self._type or None == self._cols or None == self._rows:
            raise Exception('fdsfs')

        self._elements = []
        for col in range(self._cols):
            self._elements.insert(col, [Element() for row in range(self._rows)])

    def calcNextState(self):
        self._fill()

        for row in range(self._rows):
            for col in range(self._cols):
                neighbours = []
                for neighbour in self._neighbour[self._type]:
                    neighbourCol = col + neighbour[0]
                    if neighbourCol >= self._cols:
                        neighbourCol -= self._cols
                    elif neighbourCol < 0:
                        neighbourCol += self._cols

                    neighbourRow = row + neighbour[1]
                    if neighbourRow >= self._rows:
                        neighbourRow -= self._rows
                    elif neighbourRow < 0:
                        neighbourRow += self._rows

                    neighbours.append(self._elements[neighbourCol][neighbourRow])

                self._elements[col][row].calcNextState(neighbours)

        for row in range(self._rows):
            for col in range(self._cols):
                self._elements[col][row].relaseNextState()

    def createView(self, scene):
        self._fill()

        for row in range(self._rows):
            for col in range(self._cols):
                self._elements[col][row].createView(scene, self._type, col, row)

    def load(self, file):
        self._fill()

        data = pickle.loads(file.readData(file.size()))

        i = 0
        for row in range(data.rows):
            for col in range(data.cols):
                self._elements[row][col].active = data.active[i]
                self._elements[row][col].calcState()
                i += 1

    def save(self, file):
        self._fill()

        data = GridData()
        data.rows = self._elements.shape[0]
        data.cols = self._elements.shape[1]
        data.active = []

        for row in range(data.rows):
            for col in range(data.cols):
                data.active.append(self._elements[row][col].active)

        file.writeData(pickle.dumps(data))

class GridData:
    rows = None
    cols = None
    active = None
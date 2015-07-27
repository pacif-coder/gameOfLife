from PyQt4 import QtCore, QtGui
import math, random

class Element:
    state = 0
    active = True
    _nextState = None

    _view = None

    # Constant
    _cos = math.sqrt(3) / 2
    _size = 1
    _vectors = (
        (0.5 * _size, -1 * _size * _cos),
        (_size, 0),
        (0.5 * _size, _size * _cos),
        (-0.5 * _size, _size * _cos),
        (-1 * _size, 0),
    )

    _name2colors = {
        'no_active': (247, 247, 247),
        'active': (147, 147, 147),
    }

    _colors = {}
    _pens = {}
    _brushs = {}

    def __init__(self):
        self.state = 0

    def createView(self, scene, elementType, cell, row):
        x, y = self._calcPos(elementType, cell, row)

        if elementType == 'hexagon':
            poly = QtGui.QPolygonF()
            poly.append(QtCore.QPointF(x, y))
            for point in self._vectors:
                x = x + point[0]
                y = y + point[1]
                poly.append(QtCore.QPointF(x, y))

            self._view = HexagonGraphicsPolygonItem(poly)
        elif elementType == 'square':
            self._view = HexagonGraphicsRectItem(x, y, 2 * Element._size, 2 * Element._size)
        else:
            raise Exception('Unsupport type "' + elementType + '"')

        self._view.model = self
        self._setColor(Element._name2colors['no_active'])

        scene.addItem(self._view)

    # инвертируем статус
    def onClick(self):
        self.state = 0 if self.state else 1
        self._state2Color()

    # делаем вычесленный статус текущим, перекрашиваем
    # элемент
    def relaseNextState(self):
        self.state = self._nextState
        self._state2Color()

    def calcNextState(self, neighbours):
        stateSum = 0
        for neighbour in neighbours:
            stateSum += neighbour.state

        self._nextState = 0
        if self.state:
            if stateSum == 2 or stateSum == 3:
                self._nextState = 1
        else:
            if stateSum == 3:
                self._nextState = 1

    # перекрашиваем элемент в зависимости от статуса
    def _state2Color(self):
        colorType = 'active' if self.state else 'no_active'
        self._setColor(Element._name2colors[colorType])

    def _setColor(self, color):
        if not self._view:
            return

        # для экономий пямяти - создаём обьекты цвета, пера и кисти только один раз
        if color not in Element._colors:
            Element._colors[color] = QtGui.QColor(color[0], color[1], color[2])

        if color not in Element._pens:
            Element._pens[color] = QtGui.QPen(Element._colors[color])

        if color not in Element._brushs:
            Element._brushs[color] = QtGui.QBrush(Element._colors[color])

        self._view.setPen(Element._pens[color])
        self._view.setBrush(Element._brushs[color])

    def _calcPos(self, elementType, col, row):
        if elementType == 'hexagon':
            x = 1.5 * Element._size * col
            if col % 2 == 1:
                y = 2 * row * Element._size * Element._cos + 2 * Element._size * Element._cos
            else:
                y = 2 * row * Element._size * Element._cos + Element._size * Element._cos
        elif elementType == 'square':
            x = 2 * Element._size * col
            y = 2 * Element._size * row
        else:
            raise Exception('Unsupport type "' + elementType + '"')

        return (x, y)

    @staticmethod
    def getSize(elementType, col, row):
        height = width = None
        if elementType == 'hexagon':
            if col == 1:
                width = 2 * col * Element._size
            else:
                width = 3 * (col / 2) * Element._size + 0.5 * Element._size
                if row % 2 == 0:
                    height = 2 * Element._size * Element._cos * row
                else:
                    height = 2 * Element._size * Element._cos * row + Element._size * Element._cos
        elif elementType == 'square':
            width = 2 * Element._size * col
            height = 2 * Element._size * row
        else:
            raise Exception('Unsupport type "' + elementType + '"')

        return (width, height)

class HexagonGraphicsPolygonItem(QtGui.QGraphicsPolygonItem):
    model = None

    def mousePressEvent(self, event):
        event.accept()
        self.model.onClick()

class HexagonGraphicsRectItem(QtGui.QGraphicsRectItem):
    model = None

    def mousePressEvent(self, event):
        event.accept()
        self.model.onClick()


"""
Implements mainly the Vector class. See its documentation.
"""


class VectorError(Exception):
    """
    An exception to use with Vector
    """

    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def __str__(self):
        return repr(self.value)


class Vector(tuple):
    """
    A vector.
    """

    def __init__(self, seq):
        tuple.__init__(seq)

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise VectorError("right hand side is not a Vector")
        return Vector(map(lambda x, y: x + y, self, other))

    def __neg__(self):
        return Vector(map(lambda x: -x, self))

    def __pos__(self):
        return self

    def __sub__(self, other):
        return Vector(map(lambda x, y: x - y, self, other))

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise VectorError("right hand side is illegal")
        return Vector(map(lambda x: x * other, self))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise VectorError("right hand side is illegal")
        return Vector(map(lambda x: x / other, self))

    @staticmethod
    def __rdiv__():
        raise VectorError("you can't divide something by a vector")

    def __and__(self, other):
        """
        this is a dot product, done like this: a&b
        must use () around it because of broken operator precedence.
        """
        if not isinstance(other, Vector):
            raise VectorError("you can't do dot product of Vector with a "
                              "non-Vector")
        dimension = self.dim()
        size = 0.
        for i in range(dimension):
            size += self[i] * other[i]
        return size

    def __rand__(self, other):
        return self & other

    def __or__(self, other):
        """
        cross product, defined only for 3D Vectors. goes like this: a|b
        don't try this on non-3d Vectors. must use () around it because of
        fucked up operator precedence.
        """
        a = self
        b = other
        return Vector([a[1] * b[2] - a[2] * b[1],
                       a[2] * b[0] - a[0] * b[2],
                       a[0] * b[1] - a[1] * b[0]])

    def __ror__(self, other):
        return -(self | other)

    def __abs__(self):
        s = 0.
        for x in self:
            s += x ** 2
        return s ** (1.0 / 2)

    def __iadd__(self, other):
        self = self + other
        return self

    def __isub__(self, other):
        self = self - other
        return self

    def __imul__(self, other):
        self = self * other
        return self

    def __idiv__(self, other):
        self = self / other
        return self

    def __iand__(self, other):
        raise VectorError("please don't do &= with my Vectors, it confuses me")

    def __ior__(self, other):
        self = self | other
        return self

    def __repr__(self):
        return "Vector(" + tuple.__repr__(self) + ")"

    def norm(self):
        """
        gives the Vector, normalized
        """
        return self / abs(self)

    def dim(self):
        return len(self)

    def copy(self):
        return Vector(self)


def zeros(length):
    """
    Returns a zero Vector of length n.
    """
    return Vector(map(lambda x: 0., range(length)))


def ones(length):
    """
    Returns a Vector of length n with all ones.
    """
    return Vector(map(lambda x: 1., range(length)))

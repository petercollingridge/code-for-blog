from collections import namedtuple
from enum import IntEnum


Connection = namedtuple('Connection', ['point', 'position'])

def write_connection(connection):
    return "{0}: {1}".format(connection.point, str(connection.position))

class Position(IntEnum):
    ARM1 = 0
    ARM2 = 1
    BASE = 2

class System:
    def __init__(self, num_points=0):
        self.points = []
        self.add_points(num_points)

    def add_points(self, num_points):
        for _ in range(num_points):
            n = len(self.points)
            self.points.append(Point(n))

    def add_track(self, point_index1, position1, point_index2, position2):
        connection1 = self._get_connection(point_index1, position1)
        connection2 = self._get_connection(point_index2, position2)

        # Create connections
        connection1.point.connections[position1] = connection2
        connection2.point.connections[position2] = connection1

    def _get_connection(self, index, position):
        point = self.points[index]
        return Connection(point, position)

    def describe(self):
        for point in self.points:
            point.describe()

    def run(self, point_index, position, n):
        connection = self._get_connection(point_index, position)
        
        for _ in range(n):
            # print(write_connection(connection))
            connection = connection.point.next(connection.position)


class Point:
    def __init__(self, index):
        self.index = index
        self.connections = [None] * 3
        self.switch = 0

    def next(self, position):
        """
        Given a position representing the point at which a train enters, the point,
        return the connection to the next point and position.
        """
        if position == Position.BASE:
            # Entering the point at the base, so leave via an arm
            # determined by the switch
            connection_index = self.switch
        else:
            # Entering the point at an arm, so leave via the base
            # The switch changes the point to this arm
            self.switch = position
            connection_index = Position.BASE
        
        next_connection = self.connections[connection_index]
        print("Point {0}: In {1}, out {2}".format(
            self.index,
            str(position),
            str(Position(connection_index))
        ))
        return next_connection

    def describe(self):
        print(self)
        for i, connection in enumerate(self.connections):
            print("  {0} -> {1}".format(
                str(Position(i)),
                write_connection(connection)
            ))

    def __repr__(self):
        return "Point {}".format(self.index)

if __name__ == '__main__':
    system = System(2)
    system.add_track(0, Position.BASE, 1, Position.BASE)
    system.add_track(0, Position.ARM1, 0, Position.ARM2)
    system.add_track(1, Position.ARM1, 1, Position.ARM2)

    # system.describe()
    system.run(0, Position.BASE, 2)


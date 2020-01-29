from collections import namedtuple


Connection = namedtuple('Connection', ['point', 'position'])
ARM1 = 0
ARM2 = 0
BASE = 2

class System:
    def __init__(self, num_points=0):
        self.points = []
        self.tracks = []
        self.add_points(num_points)

    def add_points(self, num_points):
        for _ in range(num_points):
            self.points.append(Point())

    def add_track(self, point_index1, position1, point_index2, position2):
        point1 = self.points[point_index1]
        point2 = self.points[point_index2]

        # Create connections
        connection1 = Connection(point1, position1)
        connection2 = Connection(point2, position2)

        track_index = len(self.tracks)
        track = Track(connection1, connection2, track_index)
        point1.tracks[position1] = track
        point2.tracks[position2] = track
        self.tracks.append(track)


class Point:
    def __init__(self):
        self.tracks = [None] * 3
        self.switch = 0

    def next(self, position):
        if position == BASE:
            # TODO
            pass
        else:
            outgoing_track = self.tracks[BASE]
            return outgoing_track.next()


class Track:
    def __init__(self, connection1, connection2, index):
        self.connections = [connection1, connection2]
        self.index = index

    def next(self, connection):
        """ Given one connection, return the connection at the other end of the track. """

        index = self.connections.index(connection)
        if index == 0:
            return self.connections[1]
        elif index == 1:
            return self.connections[0]
        else:
            raise IndexError

    def __repr__(self):
        return "Track {0}".format(self.index)


if __name__ == '__main__':
    system = System(2)
    system.add_track(0, BASE, 1, BASE)
    system.add_track(0, ARM1, 0, ARM2)
    system.add_track(1, ARM1, 1, ARM2)

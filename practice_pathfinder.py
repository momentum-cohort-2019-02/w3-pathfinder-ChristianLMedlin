from pillow import Image, ImageDraw, ImageColor


class ElevationMap:

    def __init__(self, filename):
        self.elevations = []
        with open(filename) as file:
            for line in file:
                self.elevations.append([int(e) for e in line.split()])

        self.max_elevation = max(max(row) for row in self.elevations)
        self.min_elevation = min(min(row) for row in self.elevations)


    def ele_print(self, max_elevation, min_elevation):
        print(min_elevation)


    def get_elevation(self, x, y):
        return self.elevations[y][x]


    def get_intensity(self, x, y):
        return (self.get_elevation(x, y) - self.min_elevation) / (self.max_elevation - self.min_elevation) * 255
 


if __name__ == "__main__":
    current_map = Elevation("elevation_small.txt")

    current_map.get_intensity(1, 1)


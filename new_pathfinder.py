from PIL import Image, ImageDraw
from random import randint, randrange, choice
import sys
sys.setrecursionlimit(2000)

class Data:
    def __init__(self, file):
        self.file = file
        self.parent_list = []
        with open(self.file) as data:
            for line in data.readlines():
                self.parent_list.append([int(num) for num in line.split()])
        self.width = len(self.parent_list[0])
        self.height = len(self.parent_list)
        self.min = min([min(row) for row in self.parent_list])
        self.max = max([max(row) for row in self.parent_list])

    def rgb(self, point_x, point_y):
        rgb_value = int(((self.parent_list[point_y][point_x] - self.min) / (self.max - self.min)) * 255)
        return (rgb_value, rgb_value, rgb_value)

    def get_elevation(self, point):
        return self.parent_list[point[1]][point[0]]

    def get_rgb(self, point):
        return self.rgb(point[0], point[1])[0]

class Map:
    def __init__(self, data):
        self.data = data
        self.image = Image.new('RGB', (self.data.width, self.data.height))
        self.draw = ImageDraw.Draw(self.image)

    def draw_map(self):
        for y in range(len(self.data.parent_list)):
            for x in range(len(self.data.parent_list[y])):
                self.draw.point((x, y), self.data.rgb(x, y))
        return self

    def draw_path(self, path, color):
        for point in path[1]:
            self.draw.point(point, color)
        return self

    def display(self):
        return self.image.show()

class Pathfinder:
    def __init__(self, data):
        self.data = data
        self.recursive_results = {}
        self.iterative_results = []

    def greedy_path(self, starting_point):
        current_point = starting_point
        path_cost = 0
        path = []
        path.append(current_point)
        for step in range(self.data.width-1):
            up = (step+1, max(current_point[1]-1, 0))
            straight = (step+1, current_point[1])
            down = (step+1, min(current_point[1]+1, self.data.height-1))
            choices = [up, straight, down]

            up_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(up))
            straight_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(straight))
            down_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(down))
            costs = [up_cost, straight_cost, down_cost]

            choices_costs = dict(zip(choices, costs))
            sorted_choices = sorted(choices_costs, key=choices_costs.__getitem__)

            if up_cost >= straight_cost <= down_cost:
                path_cost += straight_cost
                path.append(straight)
                current_point = straight

            elif up_cost == down_cost:
                    options = [up, down]
                    decision = choice(options)
                    path_cost += choices_costs[decision]
                    path.append(decision)
                    current_point = decision
            
            else:
                path_cost += choices_costs[sorted_choices[0]]
                path.append(sorted_choices[0])
                current_point = sorted_choices[0]

        return (path_cost, path)

    def recursive_best(self, starting_point):
        if starting_point in self.recursive_results:
            return self.recursive_results[starting_point]

        current_point = starting_point
        
        up = (current_point[0]+1, max(current_point[1]-1, 0))
        straight = (current_point[0]+1, current_point[1])
        down = (current_point[0]+1, min(current_point[1]+1, self.data.height-1))
        choices = [up, straight, down]

        up_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(up))
        straight_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(straight))
        down_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(down))
        costs = [up_cost, straight_cost, down_cost]

        choices_costs = dict(zip(choices, costs))
        sorted_choices = sorted(choices_costs, key=choices_costs.__getitem__)

        if current_point[0] == self.data.width - 2:
            self.recursive_results[current_point] = (choices_costs[sorted_choices[0]], [sorted_choices[0]])
            return self.recursive_results[current_point]
        paths = [self.recursive_best(point) for point in choices]
        new_paths = [(paths[0][0]+costs[0], [current_point]+paths[0][1]),
                    (paths[1][0]+costs[1], [current_point]+paths[1][1]),
                    (paths[2][0]+costs[2], [current_point]+paths[2][1])]
        sorted_paths = sorted(new_paths, key=lambda x: x[0])
        self.recursive_results[current_point] = sorted_paths[0]
        return self.recursive_results[current_point]

    def iterative_best(self, starting_point):
        new_data = [row[(abs(column - starting_point[1])):] for column, row in enumerate            (self.data.parent_list)]
        pass


if __name__ == "__main__":
    data = Data('elevation_small.txt')
    a_map = Map(data)
    a_map.draw_map()
    paths = []
    pathfinder = Pathfinder(data)
    pathfinder.recursive_best((0, 300))
    for y in range(data.height - 1):
        path = pathfinder.greedy_path((0, y))
        a_map.draw_path(path, (0, 255, 0))
        paths.append(path)
    sorted_paths = sorted(paths, key=lambda x: x[0])
    a_map.draw_path(sorted_paths[0], (0, 0, 255))
    a_map.display()
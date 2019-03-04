from PIL import Image, ImageDraw, ImageColor

###Project was not completed. Not comfortable with my current understanding of Pillow, going to use other's code for learning purposes and re-do project while using other code as inspiration.



class ElevationMap:
    """Finds and stores the highest and lowest elevations in a dataset, then finds the appropriate level of intensity to represent the data."""
    
    def __init__(self, filename):
        self.elevations = []
        with open(filename) as file:
            for line in file:
                self.elevations.append([int(e) for e in line.split()])

        self.max_elevation = max(max(row) for row in self.elevations)
        self.min_elevation = min(min(row) for row in self.elevations)


    def get_elevation(self, x, y):
        return self.elevations[y][x]


    def get_intensity(self, x, y):
        return int((self.get_elevation(x, y) - self.min_elevation) / (self.max_elevation - self.min_elevation) * 255)

 


class DrawMap:
    

    def __init__(self, the_map):
        self.the_map = the_map
        self.map_img = Image.new('RGB', (len(self.the_map.elevations), len(self.the_map.elevations[0])), (255,255,255))


    def create_image_file(self):
        for y in range(len(self.the_map.elevations)):
            for x in range(len(self.the_map.elevations)):
                rgb_value = self.the_map.get_intensity(x, y)
                self.map_img.putpixel((x, y), (rgb_value, rgb_value, rgb_value))
        self.map_img.save('small_map.jpg', "JPEG")



if __name__ == "__main__":
    main_map = ElevationMap('elevation_small.txt')
    drawing_tool = DrawMap(main_map)
    drawing_tool.create_image_file()
import pygame
from shapely.geometry import Polygon
import copy


class Polygono:

    def __init__(self,vertices,description):
        
        self.vertices = vertices
        self.initialverts=vertices
        self.color=(255,245,230,120)
        self.polygon=Polygon(vertices)
        self.min_x,self.min_y,self.max_x,self.max_y=self.polygon.bounds
        self.bounding_box=self.polygon.minimum_rotated_rectangle
        self.bounding_box_vertices=list(self.bounding_box.exterior.coords)
        self.description=description
        #self.pointsInside=self.getPointsInsidePolygon()
    
    def draw(self,screen):
        
        pygame.draw.polygon(screen, self.color, self.vertices, 0)

    def move(self,x,y):
        
        self.vertices=copy.deepcopy(self.initialverts)
        for vertice in self.vertices:
            vertice[0]+=x
            vertice[1]+=y
        self.polygon=Polygon(self.vertices)
        print('verts')
        print(self.vertices)
        print('initialverts')
        print(self.initialverts)

        
    """ def getPointsInsidePolygon(self):

        points_inside_polygon = []
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                point = Point(x, y)
                if self.polygon.contains(point):
                    points_inside_polygon.append((x, y))

        return points_inside_polygon """

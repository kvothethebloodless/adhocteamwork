import numpy as np
import matplotlib.pyplot as plt

import pygame
import time
import pdb
pygame.init()

#An implementation of the level-based foraging domain.
#10by10 or 15by15 is the right size to go.



#What this code should expect

"""
Initial parameters.
1) mbym array of 'blocks' in the arena with '0's if empty and 'weight' if food is present.
2) The agents and their properties to display
    a)Their capacity
    b)Their viewcone-radius and angle

Time-varying parameters
1) Location and orientation of each agent.
2) Presence/Absence of food

"""



class arena_game():
    def __init__(self,food_matrix,agents_parameters):
        """
        :param food_matrix: mxm numpy array where mxm is the size of the arena. weight if food is present, zero otherwise.
        :param agents_parameters: nby3 array where n is number of agents and each row is [capacity,radius,viewconeangle] of individual agent.
        """
        self.food_matrix = food_matrix
        self.gridsize = np.shape(self.food_matrix)
        self.agents_parameters = agents_parameters

        #Setting up display related parameters.
        self.box_size = 60 #Each of the boxes in the domain is 60px wide
        self.screen = pygame.display.set_mode((self.gridsize[0]*self.box_size,self.gridsize[1]*self.box_size))
        self.clock = pygame.time.Clock()
        self.screen.fill((255,255,255))
        self.done=False
        self.screen_memory = self.screen

        #setting up text related parameters.
        pygame.font.init()
        self.font = pygame.font.SysFont("comicsansms", 25)
        self.wait_on_event()
        return

    def draw(self):
        self.draw_arena()
        self.text_overlay()
        self.draw_agents(dummy_pos,orientations)

    def draw_arena(self):
        for i in range(self.gridsize[0]):
            for j in range(self.gridsize[1]):
                x = j*self.box_size
                y = i*self.box_size
                color = (0,128,255) #Blue borders.
                pygame.draw.rect(self.screen,color,pygame.Rect(x,y,self.box_size,self.box_size),2)
        pygame.display.flip()

    def text_overlay(self):
        """
        The function looks at all non-zero weight values and overalys text of weight-values accordingly.
        :return:
        """
        nonzero_locs = np.where(self.food_matrix!=0)
        for loc in nonzero_locs:
            [x,y] = loc*self.box_size
            text = self.font.render(str('{:02.2f}'.format(self.food_matrix[loc[0],loc[1]])),True,(0,128,0))
            self.screen.blit(text,(x+self.box_size//2 - text.get_width()//2, y+self.box_size//2 -text.get_height()//2 ))
        pygame.display.flip()


    def draw_agents(self,positions,orientations):
        """
        :param positions: Expects position in terms of in which box the agent is in the grid.
        :param orientations: Expects orientation in terms of the radian angle in anti-clockwise direction with respect to x-axis
        :return: Nothing, just draws.
        """

        no_agents = len(positions)
        viewcone_angles = self.agents_parameters[:,2]
        radius = self.agents_parameters[:,1]
        #GET Center pixel loc of each box involved.
        positions_pixels = np.array((positions+.5)*self.box_size).astype('int')

        #GET_starting ending points of all lines we are going to draw
        #the starting points are basically center points. Ending points are to be determined.
        [lines_startpoints1,lines_endpoints1]= self.convertslopepoint_to_pointpoint(positions_pixels,orientations-viewcone_angles/2,radius)
        [lines_startpoints2,lines_endpoints2]= self.convertslopepoint_to_pointpoint(positions_pixels,orientations+viewcone_angles/2,radius)
        [start_angles,end_angles] = self.process_angles(orientations,viewcone_angles)

        for (pos,orien,cap,i) in zip(positions_pixels,orientations,capacities,range(no_agents)):

            #Circular shape
            pygame.draw.circle(self.screen,(255,0,0),[pos[0],pos[1]],int(self.box_size/2),2)
            #ViewConeLines
            pygame.draw.lines(self.screen,(255,0,0),False,[lines_startpoints1[i],lines_endpoints1[i]],5)
            pygame.draw.lines(self.screen,(255,0,0),False,[lines_startpoints2[i],lines_endpoints2[i]],5)
            #ViewConeArc
            rect_arc = pygame.Rect(list(pos-radius[i])+[2*radius[i],2*radius[i]])
            pygame.draw.arc(self.screen,(255,0,0),rect_arc,start_angles[i],end_angles[i],5)
            #Text displaying weight
            text = self.font.render(str('{:02.2f}'.format(cap)), True, (0,128,0))
            #decide to print text above or below.
            if orien>(np.pi):
                self.screen.blit(text,(pos[0]-text.get_width()//2,pos[1]-text.get_width()+self.box_size//5))
            else:
                self.screen.blit(text,(pos[0]-text.get_width()//2,pos[1]+text.get_width()-self.box_size//2))




        pygame.display.flip()


        return




    def convertslopepoint_to_pointpoint(self,start_point,slope,length):
        """
        :param start_point: starting point(array) of the line
        :param slope: slope of the line(array)
        :param length: Length of the line(array)
        :returns: [start_point,end_point] - (array)

        """
        x_diff = length*np.cos(slope)
        y_diff = length*np.sin(slope)
        end_point = start_point + np.array([x_diff,-y_diff]).T

        return np.array([start_point,end_point])

    def process_angles(self,orientation,viewcone_angle):
        """
        :param orientation: Orientation of the center of the viewcone in radians. taken clockwise wrt x-axis
        :param viewcone_angle: Width of the viewcone in radians
        :return: [start_angle,end_angle] in radians suitable for the pygame library to draw.
        """
        orientation = orientation%(2*np.pi)
        beginning_angles = (orientation - viewcone_angle/2)%(2*np.pi)
        ending_angles = (orientation + viewcone_angle/2)%(2*np.pi)
        angles = np.array([beginning_angles,ending_angles])
        return angles


    def wait_on_event(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    pygame.display.quit()
                    pygame.quit()
                else:
                    self.draw()




dummy_params = np.random.random((2,3))
dummy_params[:,1]*=500
dummy_params[:,2]*=2
dummy_food = np.zeros((10,10))
dummy_food [1,1] = .09
dummy_food [1,2] = .1
dummy_pos = np.array([[5,3],[4,4]])
orientations = np.array([4,2])
capacities = np.array([4,4])
a = arena_game(dummy_food,dummy_params)


def demo_vis():
    for i in range(10):
        global dummy_pos
        dummy_pos +=np.random.randint(-2,2,(2,2))
        global orientations
        orientations += np.random.random((2,2))*4 - 2







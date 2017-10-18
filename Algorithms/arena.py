import numpy as np
import matplotlib.pyplot as plt
from Algorithms.Astar import astar as astar_nav
from copy import copy


"""
ITEM should also be an object. with position and capacity.

"""


"""
REFDOC for ARENA Class:

1) Connections.
        
                                                           ->/   Agent1     \->
                                                          ->/    Agent2      \->   
                                                           /                  \ 
     Variables: Grid_matrix,item_list,agent_list          /                    \    Variables: Pos, parameters, orientation. (The passed objects include this)
     Methods: simulation_nextstep()-Make food disappear   \                    /    Methods: Run next_step. -> Should give the next position. 
                                                           \                  /      
                                                          ->\    Agent3      /->
                                                           ->\   MCTSAgent1 /->
                                                        
2) Each simluation step should also update the info in the grid_matrix to make the pygame animation display run well.
3) arena.update()
    This function should be updating the arena after every object has moved.
    It needs to 
      a) Check agents reaching to pick up any object. 
          if they do, make that object disappear by deleting it off the grid_matrix
          else
          let everything be.
      b) Update visualization - through pygame
4) This function

##THE SIM CLASS HAS TO BE SEPERATE - BECAUSE THE MCTS agent has to play often!

Methods:
    1) init()
    2) MCTS - helpers. 
        current_board()
        players_


"""



class item():
    def __init__(self,position,weight):
        self.position = position
        self.weight = weight


class arena()
    def __init__(self,grid_matrix):
        self.grid_matrix = grid_matrix
        self.agents = []
        self.items = []
        self.create_objectitems()


    def get_item_posarray(self):
        posarray = []
        for item in self.items:
            posarray.append(item.position)
        self.item_pos_array = np.array(posarray)

    def get_agent_posarray(self):
        posarray = []
        for agent in self.agents:
            posarray.append(agent.position)
        self.agent_pos_array = np.array(posarray)

    def add_agents(self,agents_list):
        #Add agent objects once they are created.
        self.agents = agents_list
        self.no_agents = len(self.agents)

    def create_objectitems(self):
        items_loc = np.argwhere(self.grid_matrix>0)
        for loc in items_loc:
            item_obj = item(loc,self.grid_matrix[loc[0],loc[1]])
            self.items.append(item_obj)

    def update(self):
        agents_around = []

        #Check how far each agent is from each item by a numpy array manipulation.
        agents_relative_positions  = np.array([self.item_pos_array-agent.curr_position for agent in self.agents]) #Array holding agents' relative positions with respect to each of the objects.
        agents_relative_distances = np.linalg.norm(agents_relative_positions,axis=2)

        #no_of agents surrouding each item
        is_agent_adjacent = agents_relative_distances<=np.sqrt(2)
        no_surrounding_agents = np.sum(is_agent_adjacent,axis=1)
        is_consumable = no_surrounding_agents>2
        potentially_consumable_items = [item if consumable else None for consumable in is_consumable ]
        potentially_consuming_agents = [[agent if is_adjacent else None for (agent,is_adjacent) in zip(self.agents,is_agent_adjacent[i])]for i in range(self.no_items)]












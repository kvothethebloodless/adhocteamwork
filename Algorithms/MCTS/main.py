#Algorithm


#Aim decide next move when you are in state-t

#Algo

#Examine children, if you have best children,

"""
REF DOC
MCTS has to be refactored.
1) State is when you make a move.
2) You have to keep track of all states. - states can be remembered as dictionaries or hashtables

"""

""""""





"""
What should MCTS work on?

1) A 'WORLD' doing this:
    a) You take an action. The world does something too. Now it is your turn to take action again.
    b) Everytime you take some action and (the world does something too) and then you land yourself in a new states,
       the world spits out a reward.
2) Programmatically, what should a 'WORLD' look like.
    a) Given a current state, it should give us all possible actions. S->A func
    b) Given an action on a current state, it should gives us all possible new-states that you pushed the world into. T(S,A)
    c) Given an action on a current state, it should give us rewards(BANDIT context) for that particular transition. R(S,A)
    

3) Overview of the algorithm in the newfound MCTS design.
    a) Each node in the tree is a world-state coupled with MCTS information of UCT related stuff (Expected reward, N_tries).
    b) Expected reward comes from sum(rewards_allpaths)/N_paths simulated starting at that node.
    c) N_tries comes from all the time this particular node has been tried out.
    d) After we start-off at current_state, we do:
        
    
4) Each run of the simulation:
    a) We sample a type. 
    b) We retrieve the best parameter estimate of the type.
    c) We run MCTS for given number of iterations and stop to pick the best action:
        i) Initialize a new gym in the world with the current state of the world in the simulator.
        ii) Create a new node object and add statedef from the world object to this.
        ii) Start building the tree with the starting node as the current state.
        iii) Create a dictionary of state-nodeobj pairs. Add initial state to it.
        iii) While loop until specified iters or time.
            1) Pick a action according to UCT (greatest)
            2) Transition into a new state - retrieve the stateconfig from the gym
            3) Search if the new_state has already been encountered. If it was: 
            2) Collect discounted reward at each state according to time from now. (Absolute discount doesn't matter as we compare)
            3) For each state in the trajectory beginning from the end:
                a) 
"""


#DESIGN: USING GRAPH TOOL NOW BECAUSE
#Design: 1) We need to store stuff
#design 2) We need speed and can't compromise on those intializations and search and loads.


import numpy as np
import random
import matplotlib.pyplot as plt
from operator import attrgetter
import random
from graph_tool.all import *

global C
C = np.sqrt(2)
external_player = 0
internal_agent = 1


UNIVERSE = False
AIAGENT = True


PARENT = False
CHILD = True


#Todo: 1) Change all of these properties as graph-node's internal properties and add those functions as external methods

class mcts_statenode():
    def __init__(self,state,parent,childaction_array):
        self.state = state
        #Each state node is uniquely identified by this state definition. This could be a numpy array of the grid-world or whatever.
        #The only requirement is that this is unique.
        self.parent = parent
        self.childaction_array = childaction_array
        self.avg_reward = 0
        self.cum_reward = 0
        self.reward = 0
        self.ucb = 0
        self.n_sims = 0
        self.turn_whose = AGENT

        #The following two are tricky.
        #First, we need to know how 'good' this position is, which is inferred from the first part of the UCT
        #THis is calculated by a ratio of number of times this node played resulted in a win vs number of times this
        #node is played at all
        #The second part is to know how much this node is exploited. This is calculated by computing the total number of times
        #simulations started at its parent node divided by the number of times this node particular node was traversed in the process.
        self.n_sims = 0 #Number of simulations involving the current node.

    def update_meanreward(self):
        self.avg_reward = self.cum_reward/self.n_sims
    def update_ucb(self):
        self.update_meanreward()
        self.ucb = self.avg_reward + C*np.sqrt(((np.log(self.parent.n_sims))/self.n_sims))
        return


class universe():
    #Could be plug-and-play
    #A game should allow :
    #1) Tell all possible legal states
    #2) Evaluate if a state is terminal or not
    #3) If it is terminal, tell who won.

    def __init__(self):
        #TODO: set this to the beginning state of every-universe
        #design: This state will always give the turn to the AI agent.
        self.state = False

    def create_world(self):
        world = universe()
        return world

    def get_actionsLegal(self,state):
        #First get all moves allowed.
        #Apply them to the game and get the possible states.
        #Always generates a list of new legal next-state's features possible.
        return


    def react(self,action_external,state,Transition=False):
        """
        :param action_external: action taken by the external agent.
        :param state: state from which the agent is taking the action.
        :param Transition: Should the world transition into that state, or just peek and tell us what the state is.
        :return:
        """
        #This function gives the universe's reaction to a particular user action in a state.
        #This could be thought as the transition when the agent acts, pushing the universe into its turn-taking state.
        self.state = self.get_stateNext(self.state,action_external)
        return

    def act(self,state,Transition=False):
        """
        :param state: state from which the world should act
        :param Transition: Should the world transition into that state, or just peek and tell us what the state is.
        :return:
        """
        #This function gives the universe's response to a particular state when the turn is its.
        #This cold be thought of as universe's move.
        return

    def is_terminalstate(self,state):
        return True

    def get_reward(self,state):
        return 0
        #return one if player 1 won #Whose action we are trying to build a tree for
        #return -1 if player 2 won, Whose actions are generated randomly.

    def get_stateNext(self,curr_state,action_curr):
        return self.state #Some dummy


class mcts():
    def __init__(self,universe,number_of_playouts,name='Default'):

        self.universe = universe
        self.number_of_playouts = number_of_playouts
        self.discount = .95


        #Graph properties
        self.graph = Graph()
        self.graph.new_graph_property("string")
        self.graph.properties["config"] = name

        #Vertex Properties
        vp_stateKey = self.graph.new_vertex_property("string")#Key to identify, lookup states
        self.graph.vp.state_key = vp_stateKey

        vp_avgreward = self.graph.new_vertex_property("double")
        self.graph.vp.avg_reward = vp_avgreward

        vp_cumreward = self.graph.new_vertex_property("double")
        self.graph.vp.cum_reward = vp_cumreward

        vp_reward = self.graph.new_vertex_property("double")
        self.graph.vp.reward = vp_reward

        vp_uct = self.graph.new_vertex_property("double")
        self.graph.vp.uct = vp_uct

        vp_nsims = self.graph.new_vertex_property("int")
        self.graph.vp.nsims = vp_nsims

        vp_turn_whose = self.graph.new_vertex_property("boolean")
        self.graph.vp.turn_whose = vp_turn_whose


        #Edge properties
        #True-1-child False-0-Parent
        ep_relationship = self.graph.new_edge_property("boolean")
        self.graph.edge_properties['relationship'] = ep_relationship

        #Dict to remember the conversion between index of the vertex in the graph and stateKey
        self.dict_stateKeyIndex = {}

    def addVertex(self,stateKey):
        v = self.g.add_vertex()
        self.graph.vp.state_key[v] = stateKey
        self.graph.vp.reward = 0
        self.graph.vp.avg_reward = 0
        self.graph.vp.cum_reward = 0
        self.graph.vp.nsims = 0
        self.graph.vp.uct = 0
        self.graph.vp.turn_whose = UNIVERSE


        #Add v to the dictionary of the vertexindex - statekey pairs`
        self.dict_stateKeyIndex[stateKey] = self.graph.vertex_index[v]
        return v

    def hash_state(self,state):
        #Custom hash function for the state.
        #if nothing is mentioned, by default use python's hash function on numpytostring function.

        #design: for our usecase, state is the numpy array of [locofmctsagent,locsofallotheragents,[heading,0]of all otheragents,
        #design: locsoffood].
        self.stateArrayShape = state.shape()
        self.stateArrayType = state.dtype
        return state.tostring()

    def unhash_state(self,hashed_state):
        #design: same as above
        state1Darray = np.fromstring(hashed_state,self.stateArrayType)
        return state1Darray.reshape(self.stateArrayShape)


    def create_graph(self):
        self.vertex_list = []
        self.edge_list = []


    def rollout(self,state):
        self.reward_list = []
        #All rewards are interpreted as beneficial/adversarial for agent.
        #So a reward received in the node where it is the universe's turn, describes how good it is for the agent.

        world = self.universe.create_world()
        #TODO: set the world_gym's starting state to our curr_state of the rollout.

        #design: we always start with our turn. The world is assumed to just have taken its turn, and then it is us.
        begin_state = state
        begin_stateKey = self.hash_state(begin_state)
        world.state = state

        #TODO: replace this with the new graph defintition
        # if not self.dict_stateKeyIndex.has_key(begin_stateKey):
        #     self.statenodes_dict[str(curr_state)] = mcts_statenode(begin_state,None,[])

        if not self.dict_stateKeyIndex.has_key(begin_stateKey):
            self.addVertex(begin_stateKey)

        while not self.world.is_terminalstate(state):
            #design: As we always begin first, we assume our start is after the world's action that resulted in world's curr_state
            curr_state = self.world.curr_state
            curr_stateKey = self.hash_state(curr_state)
            curr_stateIndex = self.dict_stateKeyIndex[curr_stateKey]

            #DESIGN: !!!!! WE DON'T NEED OBJECTS ANYMORE> ALL WE NEEDED IS THE INDEX OF THE VERTEX.


            """
            #todo: replace with appropriate vertex definition
            # curr_state_node = self.statenodes_dict[str(curr_state)]
            currstate_vertex = self.graph.vertex(curr_stateIndex)

            #design: It is our turn
            #curr_state_node.turn = AIAGENT
            #todo: replace this with appropriate vertex definition
            self.graph.vp.turn_whose[currstate_vertex] = AIAGENT
            """
            #replacing the above with the following
            self.graph.vp.turn_whose[curr_stateIndex] = AIAGENT

            actions_legal = self.world.get_actionsLegal(state)

            #todo: replace this with statevertices_legal, but see if there is any similar function offered by graphtools already
            #design: so instead of node objects, we use vertex indices in the graph
            stateIndices_legal = []
            #Now retrieve the resulting state-objects.

            #Now this is a turn-by-turn simulation. We pick one action, obtain reward, store it, and ask the universe to do the same.
            #until we reach a terminal state.
            for actions in actions_legal:
                next_state = self.world.react(curr_state,action,Transition=False) #Peek into a one-step future.

                #todo: convert this to vertex-graph notation
                # next_state_key = str(next_state)
                next_stateKey = self.hash_state(next_state)



                #todo: convert this to vertex-graph notation?
                next_state_node = None


                #See if the next-state has related node-objects already. If the node-objects don't exist, create them
                #otherwise, just assosciate them with our children_array.

                #todo: convert tthis to vertex-grah notation?
                """
                if self.nodes_dict.has_key(next_state_key):
                    next_state_node = self.nodes_dict[next_state_key]
                else:
                    next_state_node = mcts_statenode(next_state,curr_state,[])
                    self.nodes_dict[next_state_key] = next_state_node
                    """
                #replaced the above with the below.

                if not self.dict_stateKeyIndex.has_key(next_stateKey):
                    self.addVertex(next_stateKey)

                next_stateIndex = self.dict_stateKeyIndex[next_stateKey]




                #todo: convert to the graph notation
                #because it is always the case that the children node are universe's turn policy
                # next_state_node.turn = UNIVERSE
                self.graph.vp.turn_whose[next_stateIndex] = UNIVERSE


                #todo: converting to the graph notation
                #Add this node as one of the children of the curr_state node
                # if next_state_node not in curr_state_node.children:
                #     curr_state_node.childaction_array.append([action,next_state_node])
                #Added directed edge from currstate to the child state
                self.graph.add_edge(curr_stateIndex,next_stateIndex)

                    
                #Add this node to the statenodes_legal
                stateIndices_legal.append(next_stateIndex)



            #notes: There is different strategy to be followed while exploring vs while actually playing the game.
            #notes: While exploring, we choose the next node on the following order"
            #notes: 1) If there are unexplored actions, pick one at random and explore it.
            #notes: 2) If there are no unexplored actions, pick the one with highest UCB.
            #notes: 3) If there are nodes with same UCB, resolve ties arbitrarily.

            #todo:CTG -  convert to graph
            #design: Pick the best action to explore.
            action_bestExploration,stateIndex_bestExploration = self.pick_actionBestExploration(actions_legal,stateIndices_legal)

            #todo:CTG
            #design: Chose the action and make it as the successor to this current state node we are in.
            # statenode_bestExploration.parent = curr_state_node



            #design: Remember the reward we gained through taking this action.
            self.reward_list.append(world.reward(statenode_bestExploration))

            #design: Update the n_sims of the curr_node we are in.
            curr_state_node.n_sims+=1

            #design: Make the universe act on this current move of ours.
            self.world.act(statenode_bestExploration,Transition=True)

            #design: Change the currnode and currstate to chosen best exploration node for the next stage of the loop.
            curr_state_node = statenode_best
            curr_state = statenode_best.state


        #backpropagate the rewards.
        #design: After done with the forward simulation, go backwards and

        #start off with the terimanal node, whose reward is given.
        curr_state_node.cum_reward+=self.reward_list[-1]
        curr_state_node.n_sims+=1
        curr_state_node.update_ucb()

        backprop_currstatenode = curr_state_node.parent
        backprop_currchildnode = curr_state_node
        for idx,reward in enumerate(reversed(self.reward_list[0:-1])):
            backprop_currstatenode.cum_reward+=reward+self.discount*backprop_currchildnode.avg_reward
            backprop_currstatenode.n_sims+=1
            backprop_currstatenode.update_ucb()
            backprop_currchildnode = backprop_currstatenode
            backprop_currstatenode = backprop_currstatenode.parent
        return


    def pick_actionBestExploration(self,actions_legal,stateIndices_legal):
        # unexplored_stateIndices = [statenode if statenode.n_sims==0 else None for statenode in statenodes_legal]
        unexplored_stateIndices = [stateIndex if self.graph.vp.nsims[stateIndex] else None for stateIndex in stateIndices_legal]
        if unexplored_stateIndices:
            #design: Means there are unexplored child-states, which is bad for UCB comparision, so go forward and pick them.
            next_statenode = random.choice(unexplored_statenodes)
            next_action = actions_legal[statenodes_legal.index(next_statenode)]
            return(next_action,next_statenode)
        else:
            #design: Means all the child-states are explored all-ready. Pick the highest UCB child state.
            maxUCB_statenode = max(statenodes_legal,key=attrgetter('ucb'))
            maxUCB_action = actions_legal[statenodes_legal.index(maxUCB_statenode)]
            return(maxUCB_action,maxUCB_statenode)

    def pick_actionBestReward(self,actions_legal,statenodes_legal):
        maxreward_statenode = max(statenodes_legal,key=attrgetter('avg_reward'))
        maxreward_action = actions_legal[statenodes_legal.index(maxreward_statenode)]
        return(maxreward_action,maxreward_statenode)

    def play(self):
        curr_state = self.world.curr_state
        self.rewards = []
        self.states = []

        while not self.world.is_terminalstate(curr_state):
            self.states.append(curr_state)
            for i in range(self.number_of_playouts):
                self.rollout(curr_state)
            curr_actions_legal = self.world.get_actionsLegal(curr_state)
            childaction_array = curr_state.childaction_array
            best_action,best_state = self.pick_actionBestReward(childaction_array[:,0],childaction_array[:,1])
            self.world.transition(best_action)
            curr_state = self.world.curr_state
        return self.rewards,self.states



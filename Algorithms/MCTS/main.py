#Algorithm


#Aim decide next move when you are in state-t

#Algo

#Examine children, if you have best children,

import numpy as np
import random
import matplotlib.pyplot as plt

global C
C = np.sqrt(2)
external_player = 0
internal_agent = 1


class gameTree_statenode():
    def __init__(self,player,features,parent,child_array):
        self.features = features
        self.parent = parent
        self.child_array = child_array
        self.n_wins = 0 #Number of wins by starting off this node and executing random policy.
        self.playedby = player
        self.uct


        self.causedby_move

        #The following two are tricky.
        #First, we need to know how 'good' this position is, which is inferred from the first part of the UCT
        #THis is calculated by a ratio of number of times this node played resulted in a win vs number of times this
        #node is played at all
        #The second part is to know how much this node is exploited. This is calculated by computing the total number of times
        #simulations started at its parent node divided by the number of times this node particular node was traversed in the process.
        self.n_sims = 0 #Number of simulations involving the current node.

    def update_UCT(self):
        self.uct = (self.n_wins/self.n_sims) + C*np.sqrt(((np.log(self.parent.n_sims))/self.n_sims))
        return


class game():
    #Could be plug-and-play
    #A game should allow :
    #1) Tell all possible legal states
    #2) Evaluate if a state is terminal or not
    #3) If it is terminal, tell who won.

    def __init__(self):
        self.currentstate = False

    def get_legalplays_next(self,state):
        #First get all moves allowed.
        #Apply them to the game and get the possible states.
        #Always generates a list of new legal next-state's features possible.
        return

    def is_terminalstate(self,state):
        return

    def who_won(self,state):
        return
        #return one if player 1 won #Whose action we are trying to build a tree for
        #return -1 if player 2 won, Whose actions are generated randomly.

class mcts():
    #This class should provide the following defs
    # Should include a function to faciliate external player's movement - get-player2-move(state)
    #1) A game-play(state) function which plays against an opponent and returns a legal next-state.
    #2) A playout-from-current-state function which is a random-playout for exploration using UCB
        #This function involves playing until reaching a terminal state and then backpropagating the win/lose indicator.
    def __init__(self,playout_limit,gameobj):
        self.playout_limit = playout_limit
        self.gameobj = gameobj

    def pick_bestmove(self,state):
        uct_children = [child.uct for child in state.children]
        return state.children[uct_children.index(max(uct_children))]
    def playgame_nextmove(self,state):
        self.simulate(state)
        bestmove_newstate = self.pick_bestmove(state)
        return bestmove_newstate

    def simulate(self,state):
        #Simulate and learn about the game tree.
        #Perform n_playouts which is pre-set.
        for i in range(self.playout_limit):
            begin_state = state
            end_state =  self.perform_playout(begin_state)
            who_won = self.gameobj.who_won(end_state)
            is_win = False #Means it is not a win for the internal agent.
            if who_won==internal_agent:
                is_win = True

            self.backpropagate(begin_state,end_state,is_win)

    def perform_playout(self,state):

        #It needs to perform simulationsteps number of playouts from the current state to be prepared to take action.
        #Random Simulation - Light Playout - No rule encoding.

        curr_state = state
        while not self.gameobj.is_terminalstate(curr_state):
            #picking random next state as assumed to be played by an internal_agent
            new_state_features = random.choice(self.gameobj.get_legalplays_next(curr_state))
            #now this new state should be a child of the current state node.
            #So search for these features in all the children of this state and if you find any matches, let that
            #child be the next state. Else make a new child with these features and make that the next state.

            currstate_children_featurelist = [child.features for child in curr_state.children]
            if new_state_features in currstate_children_featurelist:
                new_state = curr_state.children[currstate_children_featurelist.index(new_state_features)]
            else:
                new_state = gameTree_statenode(internal_agent,new_state_features,curr_state,[])
            curr_state = new_state


            #picking random next state as assumed to be played by the external agent
            if self.gameobj.is_terminalstate(curr_state):

                new_state_features = random.choice(self.gameobj.get_legalplays_next(curr_state))
                #now this new state should be a child of the current state node.
                #So search for these features in all the children of this state and if you find any matches, let that
                #child be the next state. Else make a new child with these features and make that the next state.

                currstate_children_featurelist = [child.features for child in curr_state.children]
                if new_state_features in currstate_children_featurelist:
                    new_state = curr_state.children[currstate_children_featurelist.index(new_state_features)]
                else:
                    new_state = gameTree_statenode(external_player,new_state_features,curr_state,[])
                curr_state = new_state

        if curr_state.player==internal_agent:
            return curr_state
        else:
            return curr_state.parent

    def backpropagate(self,begin_state,terminal_state,is_win):
        #is_win = true if the agent (AI) won.
        curr_state = terminal_state

        while(curr_state!=begin_state):
            if curr_state.playedby == internal_agent:
                curr_state.n_wins += is_win*1

            curr_state.n_sims += 1 #Total number of times this particular bandit's lever was pulled.
            #curr_state.parent.n_sims += 1 #
            curr_state = curr_state.parent#Because the p

        begin_state.n_sims += 1 #Total number of times levers were pulled for all the bandits available.

    def update_UCT(self,begin_state,terminal_state):
        curr_state = terminal_state
        while(curr_state!=begin_state):
            curr_state.update_UCT()
            curr_state = curr_state.parent
        return


class external_player():
    def __init__(self):
        return
    def playgame_nextmove(self,curr_gamestate):
        #Prompt the external player to play the next move.
        next_state = True
        return next_state


def play(gameobj,mcts_agentobj,externalplayer_obj):
    no_gameplays = 100
    curr_boardstate = gameobj.curr_state
    #First step is always the external agent.

    for i in range(100):
        while(gameobj.is_terminalstate(curr_boardstate)):
            new_state = mcts.playgame_nextmove()
            curr_state = externalplayer_obj.playgame_nextmove(new_state)
            gameobj.curr_state = curr_state
        return








import td_gammon.agent as agent
import numpy as np
import pandas as pd
import math

def extractFeatures(state):
    game,player = state
    features = []
    for p in game.players:
        for col in game.grid:
            feats = [0.]*6
            if len(col)>0 and col[0]==p:
                for i in range(len(col)):
                    feats[min(i,5)] += 1
            features += feats
        features.append(float(len(game.barPieces[p]))/2.)
        features.append(float(len(game.offPieces[p]))/game.numPieces[p])
    if player == game.players[0]:
        features += [1.,0.]
    else:
        features += [0.,1.]
    return np.array(features).reshape(-1,1)

def getTrueValuesAction(action):
    if(len(action) < 2 ):
        action_r = (action[0][0] if isinstance(action[0][0], str) else (1 + action[0][0]),  \
                    action[0][1] if isinstance(action[0][1], str) else (1 + action[0][1]))
        return action_r

    if(len(action)> 2):
        # action = ((action[0][0]+1),(action[0][1] + 1)),((action[1][0]+1),(action[1][1] + 1)),((action[2][0]+1),(action[2][1] + 1)), ((action[3][0]+1),(action[3][1] + 1))
        # action_r = ((1 + action[0][0], action[0][0])[ isinstance(action[0][0], str)],(1 + action[0][1], action[0][1])[ isinstance(action[0][1], str)]), ((1 + action[1][0], action[1][0])[ isinstance(action[1][0], str)],(1 + action[1][1], action[1][1])[ isinstance(action[1][1], str)]),((1 + action[2][0], action[2][0])[ isinstance(action[2][0], str)],(1 + action[2][1], action[2][1])[ isinstance(action[2][1], str)]), ((1 + action[3][0], action[3][0])[ isinstance(action[3][0], str)],(1 + action[3][1], action[3][1])[ isinstance(action[3][1], str)])
        action_r = (action[0][0] if isinstance(action[0][0], str) else (action[0][0] + 1), \
                    action[0][1] if isinstance(action[0][1], str) else (action[0][1] + 1)),\
                    (action[1][0] if isinstance(action[1][0], str) else (action[1][0] + 1),\
                     action[1][1] if isinstance(action[1][1], str) else (action[1][1] + 1)),\
                    (action[2][0] if isinstance(action[2][0], str) else (action[2][0] + 1),\
                     action[2][1] if isinstance(action[2][1], str) else (action[2][1] + 1)),\
                    (action[3][0] if isinstance(action[3][0], str) else (action[3][0] + 1),\
                     action[3][1] if isinstance(action[3][1], str) else (action[3][1] + 1))

        return action_r

    # if(action[0][1] == "off"):
    #     if(action[1][1] == "off"):
    #         action = ((action[0][0]+1),(action[0][1])),((action[1][0]+1),(action[1][1]))
    #     else:
    #         action = ((action[0][0]+1),(action[0][1])),((action[1][0]+1),(action[1][1]+1))
    # else:
    #     if(action[1][1] == "off"):
    #         action = ((action[0][0]+1),(action[0][1] + 1)),((action[1][0]+1),(action[1][1]))
    #     else:
    #         action = ((action[0][0]+1),(action[0][1] + 1)),((action[1][0]+1),(action[1][1]+1))
    action_r = (action[0][0] if isinstance(action[0][0], str) else (action[0][0] + 1),  \
                action[0][1] if isinstance(action[0][1], str) else (action[0][1] + 1)), \
                (action[1][0] if isinstance(action[1][0], str) else (action[1][0] + 1), \
                 action[1][1] if isinstance(action[1][1], str) else (action[1][1] + 1)) 
    # action_r = ((action[0][0] + 1, action[0][0])[ isinstance(action[0][0], str)],
    #             (action[0][1] + 1, action[0][1])[ isinstance(action[0][1], str)]), 
    #             ((action[1][0] + 1, action[1][0])[ isinstance(action[1][0], str)],
    #             (action[1][1] + 1, action[1][1])[ isinstance(action[1][1], str)]),

    return action_r

def addToAction(action, add_to_action):
    
    if(len(action)> 2):
        # action = ((action[0][0]+1),(action[0][1] + 1)),((action[1][0]+1),(action[1][1] + 1)),((action[2][0]+1),(action[2][1] + 1)), ((action[3][0]+1),(action[3][1] + 1))
        # action_r = ((1 + action[0][0], action[0][0])[ isinstance(action[0][0], str)],(1 + action[0][1], action[0][1])[ isinstance(action[0][1], str)]), ((1 + action[1][0], action[1][0])[ isinstance(action[1][0], str)],(1 + action[1][1], action[1][1])[ isinstance(action[1][1], str)]),((1 + action[2][0], action[2][0])[ isinstance(action[2][0], str)],(1 + action[2][1], action[2][1])[ isinstance(action[2][1], str)]), ((1 + action[3][0], action[3][0])[ isinstance(action[3][0], str)],(1 + action[3][1], action[3][1])[ isinstance(action[3][1], str)])
        action_r =  (action[0][0] if isinstance(action[0][0], str) else action[0][0] + add_to_action   \
                    ,action[0][1] if isinstance(action[0][1], str) else action[0][1] + add_to_action), \
                    (action[1][0] if isinstance(action[1][0], str) else action[1][0] + add_to_action,  \
                     action[1][1] if isinstance(action[1][1], str) else action[1][1] + add_to_action), \
                    (action[2][0] if isinstance(action[2][0], str) else action[2][0] + add_to_action,  \
                     action[2][1] if isinstance(action[2][1], str) else action[2][1] + add_to_action), \
                    (action[3][0] if isinstance(action[3][0], str) else action[3][0] + add_to_action,  \
                     action[3][1] if isinstance(action[3][1], str) else action[3][1] + add_to_action)

        return action_r

    action_r = (action[0][0] if isinstance(action[0][0], str) else action[0][0] + add_to_action, \
                action[0][1] if isinstance(action[0][1], str) else action[0][1] + add_to_action),\
                (action[1][0] if isinstance(action[1][0], str) else action[1][0] + add_to_action,\
                 action[1][1] if isinstance(action[1][1], str) else action[1][1] + add_to_action)

    return action_r

def getInverseAction(action):
    if(len(action) < 2 ):
        action_r = (action[0][0] if isinstance(action[0][0], str) else (25 - action[0][0]),  \
                    action[0][1] if isinstance(action[0][1], str) else (25 - action[0][1]))
        return action_r
    if(len(action)> 2):
        action_r = (action[0][0] if isinstance(action[0][0], str) else (25 - action[0][0]),  \
                    action[0][1] if isinstance(action[0][1], str) else (25 - action[0][1])), \
                    (action[1][0] if isinstance(action[1][0], str) else (25 - action[1][0]) ,\
                     action[1][1] if isinstance(action[1][1], str) else (25 - action[1][1])),\
                    (action[2][0] if isinstance(action[2][0], str) else (25 - action[2][0]), \
                     action[2][1] if isinstance(action[2][1], str) else (25 - action[2][1])),\
                    (action[3][0] if isinstance(action[3][0], str) else (25 - action[3][0]) ,\
                     action[3][1] if isinstance(action[3][1], str) else (25 - action[3][1]))

        return action_r

    action_r = (action[0][0] if isinstance(action[0][0], str) else (25 - action[0][0])     \
                , action[0][1] if isinstance(action[0][1], str) else (25 - action[0][1])), \
                (action[1][0] if isinstance(action[1][0], str) else (25 - action[1][0]),   \
                 action[1][1] if isinstance(action[1][1], str) else (25 - action[1][1]))

    return action_r

def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

class TDAgent(agent.Agent, object):

    def __init__(self, player, weights):
        super(self.__class__, self).__init__(player)
        self.w1,self.w2,self.b1,self.b2 = weights

    def getAction(self, actions, game):
        """
        Return best action according to self.evaluationFunction,
        with no lookahead.
        """
        bestV = 0
        for a in actions:
            ateList = game.takeAction(a, self.player)
            features = extractFeatures((game,game.opponent(self.player)))
            hiddenAct = 1/(1+np.exp(-(self.w1.dot(features)+self.b1)))
            v = 1/(1+np.exp(-(self.w2.dot(hiddenAct)+self.b2)))
            if v>bestV:
                action = a
                bestV = v
            game.undoAction(a,self.player,ateList)

        return action

    def getActionWithQuote(self, actions, game):
        """
        Return best action according to self.evaluationFunction,
        with no lookahead.
        """
        actions_list = {}
        for a in actions:
            ateList = game.takeAction(a,self.player)
            features = extractFeatures((game,game.opponent(self.player)))
            hiddenAct = 1/(1+np.exp(-(self.w1.dot(features)+self.b1)))
            v = 1/(1+np.exp(-(self.w2.dot(hiddenAct)+self.b2)))

            a_true_pos = getTrueValuesAction(a)
            a_inverse = getInverseAction(a_true_pos)

            actions_list[a_inverse] = truncate(v[0][0], 6)

            game.undoAction(a,  self.player, ateList)

        df_action_non_sorted = pd.DataFrame(actions_list.items(), columns=['coup', 'quote'])
        df_action_sorted = df_action_non_sorted.sort_values(by=['quote'], ascending=False)
        df_action_drop_duplicated = df_action_sorted.drop_duplicates(subset=['quote'])

        return df_action_drop_duplicated.head()

def nnetEval(state, weights):
    w1,w2,b1,b2 = weights
    features = np.array(extractFeatures(state)).reshape(-1,1)
    hiddenAct = 1/(1+np.exp(-(w1.dot(features)+b1)))
    v = 1/(1+np.exp(-(w2.dot(hiddenAct)+b2)))
    return v

class ExpectiMiniMaxAgent(agent.Agent, object):

    def miniMaxNode(self,game,player,roll,depth):
        actions = game.getActions(roll,player,nodups=True)
        rollScores = []

        if player==self.player:
            scoreFn = max
        else:
            scoreFn = min
            depth -= 1

        if not actions:
            return self.expectiNode(game,game.opponent(player),depth)
        for a in actions:
            ateList = game.takeAction(a,player)
            rollScores.append(self.expectiNode(game,game.opponent(player),depth))
            game.undoAction(a,player,ateList)

        return scoreFn(rollScores)

    def expectiNode(self,game,player,depth):
        if depth==0:
            return self.evaluationFunction((game,player),self.evaluationArgs)

        total = 0
        for i in range(1,game.die+1):
            for j in range(i+1,game.die+1):
                score = self.miniMaxNode(game,player,(i,j),depth)
                if i==j:
                    total += score
                else:
                    total += 2*score
            
        return total/float(game.die**2)

    def getAction(self, actions, game):
        depth = 1
        if len(actions)>100:
            depth = 0
        outcomes = []
        for a in actions:
            ateList = game.takeAction(a,self.player)
            score = self.expectiNode(game,game.opponent(self.player),depth)
            game.undoAction(a,self.player,ateList)
            outcomes.append((score, a))
        action = max(outcomes)[1]

        return action


    def __init__(self, player, evalFn, evalArgs=None):
        super(self.__class__, self).__init__(player)
        self.evaluationFunction = evalFn
        self.evaluationArgs = evalArgs


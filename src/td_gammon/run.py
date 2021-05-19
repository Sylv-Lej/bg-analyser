import time

import td_gammon.game as game
import td_gammon.agent as agent
import td_gammon.aiAgents as aiAgents

import numpy as np
import random
import pickle



def test(players,numGames=100,draw=False):
    winners = [0,0]
    for _ in range(numGames):
        g = game.Game(game.LAYOUT)
        winner = run_game(players,g,draw)
        print ("The winner is : Player %s"%players[not winner].player)
        winners[not winner]+=1
        if draw:
            g.draw()
            time.sleep(10)
    print ("Summary:")
    print ("Player %s : %d/%d"%(players[0].player,winners[0],sum(winners)))
    print ("Player %s : %d/%d"%(players[1].player,winners[1],sum(winners)))

def run_game(players,g,draw=False):
    g.new_game()
    playernum = random.randint(0,1)
    over = False
    while not over:
        roll = roll_dice(g)
        if draw:
            g.draw(roll)
        playernum = (playernum+1)%2
        print("player num")
        print(playernum)
        if playernum:
            g.reverse()
        turn(players[playernum],g,roll,draw)
        if playernum:
            g.reverse()
        over = g.is_over()
        if draw:
            time.sleep(.02)
    return g.winner()

def run_game_agent(players,g,dice_tuple, draw=True):
    g.new_game()
    playernum = 0
    over = False
    if not over:
        roll = dice_tuple
        if draw:
            g.draw(roll)
        playernum = (playernum+1)%2
        if playernum:
            g.reverse()
        get_all_possibilities(players[playernum],g,roll,draw)
        if playernum:
            g.reverse()
        over = g.is_over()

        # if draw:
        #     time.sleep(5)
        if draw:
            g.draw(roll)
        if draw:
            time.sleep(3)

    return g.winner()

# def run_step(players, g, dice_tuple, draw=False):

#     g.new_game()
#     playernum = 0
#     over = False
#     if not over:
#         roll = dice_tuple
#         if draw:
#             g.draw(roll)
#         # playernum = (playernum+1)%2

#         # if playernum:
#         #     g.reverse()

#         get_all_possibilities(players[playernum], g, roll, draw)

#         # if playernum:
#         #     g.reverse()

#         if draw:
#             g.draw(roll)

#         over = g.is_over()

#         if draw:
#             time.sleep(800)

#     return g.winner()

def get_all_possibilities(player,g,roll, draw=False):
    if draw:
        print ("Player all possibilities %s rolled <%d,%d>."%(player.player,roll[0],roll[1]))
    moves = g.getActions(roll, g.players[0], nodups=True)
    if moves:
        move = player.getAction(moves, g)
        moves_with_quote = player.getActionWithQuote(moves,g)
    else:
        move = None
    if move:
        # g.takeAction(move,g.players[0])
        print("------")
        print(moves_with_quote)
        g.takeAction(move, g.players[0])

def turn(player,g,roll,draw=False):
    if draw:
        print ("Player %s rolled <%d,%d>."%(player.player,roll[0],roll[1]))
    moves = g.getActions(roll,g.players[0],nodups=True)
    if moves:
        move = player.getAction(moves,g)
    else:
        move = None
    if move:
        g.takeAction(move,g.players[0])

def roll_dice(g):
    return (random.randint(1,g.die), random.randint(1,g.die))

def load_weights(weights):
    if weights is None:
        try:
            import pickle
            # added
            with open('weights-100k.bin', 'rb') as f:
                weights = pickle.load(f, encoding='bytes')
            # -- end added
            # weights = pickle.load(open('weights-100k.bin','r'))
        except IOError:
            print ("You need to train the weights to use the better evaluation function")
    return weights

def parse_layout(layout_str):
    game_and_bar_layout = layout_str.split("^")[0]

    game_layout = game_and_bar_layout.split("=")[0]

    bar_layout = game_and_bar_layout.split("=")[1]

    dice = layout_str.split("^")[1]

    dice_tuple = int(dice.split('-')[0]), int(dice.split('-')[1])

    return game_layout,bar_layout, dice_tuple

def getAiChoice(players, layout, draw=False):
    game_layout, bar_layout, dice_tuple = parse_layout(layout)
    g = game.Game(game_layout, bar_layout)

    winner = run_game_agent(players, g, dice_tuple, draw)

def runAIStep():
    weights = None

    weights = load_weights(weights)
    evalArgs = weights
    evalFn = aiAgents.nnetEval

    # rand agent is o
    p1 = agent.RandomAgent(game.Game.TOKENS[0])
    # aiAgents.TDAgent(game.Game.TOKENS[0], evalArgs)

    # agent.RandomAgent(game.Game.TOKENS[1])
    p2 = aiAgents.TDAgent(game.Game.TOKENS[1], evalArgs)
    # layout = "0-1-o,1-2-o,2-1-o,3-2-o,4-3-o,5-2-o,7-2-x,12-2-o,17-2-x,18-4-x,19-2-o,20-2-x,21-1-x,22-2-x,23-2-x^6-5"
    # layout = "0-1-x,1-2-x,2-1-x,3-2-x,4-3-x,5-2-x,7-2-o,12-2-x,17-2-o,18-4-o,19-2-x,20-2-o,21-1-o,22-2-o,23-2-o^6-5"

    # hard real
    # layout= "2-2-o,4-3-x,5-3-x,7-3-x,9-1-x,11-2-o,12-4-x,15-1-o,16-2-o,17-3-o,18-5-o,22-1-x^5-1"
    # inverse not real
    # layout= "2-2-x,4-3-o,5-3-o,7-3-o,9-1-o,11-2-x,12-4-o,15-1-x,16-2-x,17-3-x,18-5-x,21-1-o^5-1"

    # hard real 2
    # layout= "0-1-x,1-2-x,2-1-x,3-2-x,4-3-x,5-2-x,7-2-o,12-2-x,17-2-o,18-4-o,19-2-x,20-2-o,21-1-o,22-2-o,23-2-o^5-6"

    # base layout black
    # layout = "0-2-o,5-5-x,7-3-x,11-5-o,12-5-x,16-3-o,18-5-o,23-2-x^3-1"
    # layout = "0-2-o,5-5-x,7-3-x,11-5-o,12-5-x,16-3-o,18-5-o,23-1-x=1-x^3-1"

    # black on bar
    # layout = "0-6-o,3-12-x,5-24-x,7-18-x,9-3-o,11-32-o,12-24-x,13-1-o,16-10-o,18-24-o,19-12-o,21-4-x,23-6-x=6-o^4-3"
    
    # white on bar
    layout = "0-2-x,3-2-x,5-2-x,6-2-x,7-1-x,11-4-o,12-2-x,15-1-x,16-2-o,17-2-o,18-4-o,19-2-x,20-2-o,23-1-x=1-x^5-4"
    getAiChoice([p1,p2],layout,draw=True)


def getAIPredFromLayout(layout):
    weights = None

    weights = load_weights(weights)
    evalArgs = weights
    evalFn = aiAgents.nnetEval

    # rand agent is o
    p1 = agent.RandomAgent(game.Game.TOKENS[0])
    # aiAgents.TDAgent(game.Game.TOKENS[0], evalArgs)

    # agent.RandomAgent(game.Game.TOKENS[1])
    p2 = aiAgents.TDAgent(game.Game.TOKENS[1], evalArgs)
    getAiChoice([p1,p2],layout,draw=False)


def main(args=None):
    from optparse import OptionParser
    usage = "usage: %prog [options]"

    parser = OptionParser(usage=usage)

    parser.add_option("-t","--train", dest="train",action="store_true",
                      default=False, help="Train TD Player")

    parser.add_option("-d","--draw",dest="draw",action="store_true",default=False,
                      help="Draw game")

    parser.add_option("-n","--num",dest="numgames",default=1,help="Num games to play")

    parser.add_option("-p","--player1",dest="player1",
                      default="random",help="Choose type of first player")

    parser.add_option("-e","--eval",dest="eval",action="store_true",default=True,
                        help="Play with the better eval function for player")

    parser.add_option("-a","--agent", dest="agent_choice",action="store_true",default=False,
                        help="get the choice of an agent")

    (opts,args) = parser.parse_args(args)

    weights = None

    if(opts.agent_choice):
        runAIStep()
    else:

        if opts.eval:
            weights = load_weights(weights)
            evalArgs = weights
            evalFn = aiAgents.nnetEval

        p1 = None
        print("P1 token = " + str(game.Game.TOKENS[0]))
        if opts.player1 == 'random':
            p1 = agent.RandomAgent(game.Game.TOKENS[0])
        elif opts.player1 == 'reflex':
            print("TD Agent initialised")
            p1 = aiAgents.TDAgent(game.Game.TOKENS[0], evalArgs)
        elif opts.player1 == 'expectimax':
            p1 = aiAgents.ExpectimaxAgent(game.Game.TOKENS[0], evalFn, evalArgs)
        elif opts.player1 == 'expectiminimax':
            p1 = aiAgents.ExpectiMiniMaxAgent(game.Game.TOKENS[0], evalFn, evalArgs)
        elif opts.player1 == 'human':
            p1 = agent.HumanAgent(game.Game.TOKENS[0])
    
        p2 = agent.RandomAgent(game.Game.TOKENS[1])
        # p2 = aiAgents.ExpectiMiniMaxAgent(game.Game.TOKENS[1],evalFn,evalArgs)
        if p1 is None:
            print ("Please specify legitimate player")
            import sys
            sys.exit(1)
    
        test([p1,p2],numGames=int(opts.numgames),draw=opts.draw)

if __name__=="__main__":
    main()

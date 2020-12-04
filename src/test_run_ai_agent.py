from td_gammon.run import runAIStep, load_weights, testimport td_gammon.aiAgents as aiAgentsimport td_gammon.game as gameimport td_gammon.agent as agentdef main(args=None):    from optparse import OptionParser    usage = "usage: %prog [options]"    parser = OptionParser(usage=usage)    parser.add_option("-t","--train", dest="train",action="store_true",                      default=False, help="Train TD Player")    parser.add_option("-d","--draw",dest="draw",action="store_true",default=False,                      help="Draw game")    parser.add_option("-n","--num",dest="numgames",default=1,help="Num games to play")    parser.add_option("-p","--player1",dest="player1",                      default="random",help="Choose type of first player")    parser.add_option("-e","--eval",dest="eval",action="store_true",default=True,                        help="Play with the better eval function for player")    parser.add_option("-a","--agent", dest="agent_choice",action="store_true",default=False,                        help="get the choice of an agent")    (opts,args) = parser.parse_args(args)    weights = None    if(opts.agent_choice):        runAIStep()    else:        if opts.eval:            weights = load_weights(weights)            evalArgs = weights            evalFn = aiAgents.nnetEval        p1 = None        print("P1 token = " + str(game.Game.TOKENS[0]))        if opts.player1 == 'random':            p1 = agent.RandomAgent(game.Game.TOKENS[0])        elif opts.player1 == 'reflex':            print("TD Agent initialised")            p1 = aiAgents.TDAgent(game.Game.TOKENS[0], evalArgs)        elif opts.player1 == 'expectimax':            p1 = aiAgents.ExpectimaxAgent(game.Game.TOKENS[0], evalFn, evalArgs)        elif opts.player1 == 'expectiminimax':            p1 = aiAgents.ExpectiMiniMaxAgent(game.Game.TOKENS[0], evalFn, evalArgs)        elif opts.player1 == 'human':            p1 = agent.HumanAgent(game.Game.TOKENS[0])            p2 = agent.RandomAgent(game.Game.TOKENS[1])        # p2 = aiAgents.ExpectiMiniMaxAgent(game.Game.TOKENS[1],evalFn,evalArgs)        if p1 is None:            print ("Please specify legitimate player")            import sys            sys.exit(1)            test([p1,p2],numGames=int(opts.numgames),draw=opts.draw)if __name__=="__main__":    main()
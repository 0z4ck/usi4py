import logging
import json
import utils
from usiclient import UsiClient


if __name__ == '__main__':


    logger = logging.getLogger()
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    cfg = json.loads(open("config.json","r").read());

    e1 = UsiClient(cfg["engine1"],cfg["directory1"])       # launch sente engine
    e2 = UsiClient(cfg["engine2"],cfg["directory2"])       # launch gote engine

    fout1 = open('log/'+cfg['engine_name1']+'.log','wb');  # log file for sente engine
    e1.p.logfile = fout1;
    fout2 = open('log/'+cfg['engine_name2']+'.log','wb');  # log file for gote engine
    e2.p.logfile = fout2;

    e1.initialize()                                        # initialize sente engine 
    e1.setOptions({"USI_Hash":256,"USI_Ponder":str(False).lower()})
    e1.newgame()
    e2.initialize()                                        # initialize gote engine
    e2.setOptions({"USI_Hash":256,"USI_Ponder":str(False).lower()})
    e2.newgame()

    move_num = 0
    moves = ""

    while True:

        if move_num == 0:      # sente's first move 
            bm,pond = e1.go(moves,0,0,100)
            move_num+=1
            moves += " moves " + bm

        if move_num%2 == 0:     # sente's turn
            turn = e1

        elif move_num%2 == 1:   # gote's turn
            turn = e2

        bm,pond = turn.go(moves,0,0,100)
        move_num+=1
        moves += " " + bm

        if bm == "resign":
            if move_num%2 == 1:
                logger.info("gote won")
                sente = False
            else:
                logger.info("sente won")
                sente = True
            break

    utils.dumpResult(cfg['engine_name1'],cfg['engine_name2'],sente)
    utils.dumpKif(cfg['engine_name1'],cfg['engine_name2'],moves)

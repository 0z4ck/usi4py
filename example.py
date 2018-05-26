import logging
import json
import utils
from usiclient import UsiClient


if __name__ == '__main__':

    logger = logging.getLogger()
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    cfg = json.loads(open("config.json","r").read());

    e1 = UsiClient(cfg["engine1"],cfg["directory1"])    # launch sente engine
    e2 = UsiClient(cfg["engine2"],cfg["directory2"])    # launch gote engine
    e1.initialize()                                     # initialize sente engine 
    e2.initialize()                                     # initialize gote engine
    e1.newgame()
    e2.newgame()

    move_num = 0
    moves = ""

    while True:

        if move_num == 0:      # first move 
            bm = e1.go(moves,0,0,100)
            move_num+=1
            moves += " moves " + bm

        if move_num%2 == 0:
            turn = e1

        elif move_num%2 == 1:
            turn = e2

        bm = turn.go(moves,0,0,100)
        move_num+=1
        moves += " " + bm

        if bm == "resi":
            if move_num%2 == 0:
                logger.info("gote won")
                sente = False
            else:
                logger.info("sente won")
                sente = True
            break

    utils.dumpResult("Lesserkai","GPSFish",sente)

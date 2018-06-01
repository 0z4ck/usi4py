import logging
import pexpect



class UsiClient():

    def __init__(self, engine, path):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("launching the engine via pexpect.")
        self.p = pexpect.spawn("/bin/bash",cwd=path);
        self.p.sendline("stty -icanon");
        self.p.sendline(engine);
        self.p.setecho(False);
        self.engine = engine
        self.path = path

    def initialize(self, usi_hash=256):
        try :
            self.p.send("usi\n");
            self.p.expect("usiok");
            self.p.send("setoption name USI_Ponder value false\n");
            self.p.send("setoption name USI_Hash value {0}\n".format(usi_hash));
            self.p.send("isready\n");
            self.p.expect("readyok");
        except Exception as e:
            self.logger.error("Error occured during engine initialization")
            self.logger.error(e)
            self.logger.error(str(self.p))

    def newgame(self): 
        self.p.send("usinewgame\n");

    def go(self, moves, btime, wtime, byoyomi):
        self.logger.debug("length: {0} bytes".format(len("position startpos{0}".format(moves))))
        self.p.sendline("position startpos{0}".format(moves));
        string = "go btime {0} wtime {1} byoyomi {2}".format(btime,wtime,byoyomi);
        self.p.sendline(string);
        self.p.expect("bestmove......");
        bm_str = self.p.after.replace("\r"," ")
        self.logger.debug("bestmove: {0}".format(bm_str[-5:]))
        if bm_str[-1]=="+":
            return bm_str[-5:];
        else:
            return bm_str[-5:-1];

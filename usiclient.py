import logging
import pexpect
import re
import sys



class UsiClient():

    def __init__(self, engine, path):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("launching the engine via pexpect.")
        if sys.platform == "darwin":
            self.p = pexpect.spawn("/bin/bash",cwd=path);
            self.p.sendline("stty -icanon");
            self.p.sendline(engine);
        else:
            self.p = pexpect.spawn(engine,cwd=path);
        self.p.setecho(False);
        self.engine = engine
        self.path = path

    def setOptions(self, options):
        for key in options:
            self.p.send("setoption name {0} value {1}\n".format(key, options[key]));

    def initialize(self):
        try :
            self.logger.debug("initializing the engine...")
            self.p.send("usi\n");
            self.p.expect("usiok");
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
        self.p.expect("bestmove ([0-9a-i+*PLNSGRBresign]+)");
        try:
            inf = self.p.before.split("\n")[-2]
            m = re.search(r"score cp ([0-9\-mate]+)",inf)
            self.logger.info("  SCORE : {}".format(m.group(1)))
        except:
            try:
                m = re.search(r"score ([0-9\-mate]+)",inf)
                self.logger.info("  SCORE : {}".format(m.group(1)))
            except:
                self.logger.debug("no score given, maybe joseki move")
        bm_str = self.p.after.replace("\r"," ")
        return bm_str[9:]

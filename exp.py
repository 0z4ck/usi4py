import json
import pexpect
import sys
from multiprocessing import Process, Pipe


def getbestmove(pos, p, btime, wtime, byoyomi):
    p.sendline("position startpos{}".format(pos));
    string = "go btime {} wtime {} byoyomi {}".format(btime,wtime,byoyomi);
    p.sendline(string);
    p.expect("bestmove......");
    if p.after[-1]=="+":
        return p.after[-5:];
    else:
        return p.after[-5:-1];



def engine(e, conn, byoyomi, sente=True):

    p= pexpect.spawn(e);
    fout = open('log/'+e.split("/")[-1]+'.log','wb');
    #p.logfile = sys.stdout;
    p.logfile = fout;
    p.setecho(False);
    p.send("usi\n");
    p.expect("usiok");
    p.send("setoption name USI_Ponder value false\n");
    p.send("setoption name USI_Hash value 256\n");
    p.send("isready\n");
    p.expect("readyok");
    p.send("usinewgame\n");
    moves = " moves"    
    if sente :
        print "sente, waiting for gote"
        conn.recv(); #waiting for gote
        moves = "";
        bm = getbestmove(moves,p,0,0,byoyomi);
        conn.send(bm)
        moves = " moves"    
        moves=" ".join([moves,bm])
    else:
        conn.send("I'm ready");
        print "gote caught up"
    while 1:
        om = conn.recv(); #opponent's move
        if om == "resi":
            print "I won !! "
            break;
        moves=" ".join([moves,om])
        bm = getbestmove(moves,p,0,0,byoyomi);
        conn.send(bm)
        if bm == "resi":
            print "I lost !! "
            break;
        moves=" ".join([moves,bm])


if __name__ == '__main__':
    cfg = json.loads(open("config.json","r").read())
    p1_conn, p2_conn = Pipe();
    p1 = Process(target=engine, args=([cfg["engine1"], p1_conn, cfg["byoyomi"]]));
    p1.start();
    p2 = Process(target=engine, args=([cfg["engine2"], p2_conn, cfg["byoyomi"], False]));
    p2.start();



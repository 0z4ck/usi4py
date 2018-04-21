import json
import pexpect
import sys
from multiprocessing import Process, Pipe


def getBestmove(moves, p, btime, wtime, byoyomi):
    p.sendline("position startpos{}".format(moves));
    string = "go btime {} wtime {} byoyomi {}".format(btime,wtime,byoyomi);
    p.sendline(string);
    p.expect("bestmove......");
    if p.after[-1]=="+":
        return p.after[-5:];
    else:
        return p.after[-5:-1];



def dumpResult(winner, loser, sente):
    if sente:
        black = winner;
        white = loser;
    else:
        black = loser;
        white = winner;

    result_dict = json.loads(open("results.json","r").read());

    ##### dirty code to update the dict. Any idea to make this code nicer ? #####
    try:
        win_lose = result_dict[black][white];
    except KeyError:
        try:
            win_lose = {"win":0, "lose":0, "draw":0};
            result_dict[black][white] = win_lose;
        except KeyError:
            try:
                result_dict[black] = { white : win_lose };
            except Exception as e:
                print e;

    if sente:
        win_lose["win"]+=1;
    else:
        win_lose["lose"]+=1;

    result_dict[black][white] = win_lose;
    open("results.json","w").write(json.dumps(result_dict,indent=4));




def start_engine(engine_path, conn, byoyomi, sente=True):

    p= pexpect.spawn(engine_path);
    engine_name = engine_path.split("/")[-1];
    fout = open('log/'+engine_name+'.log','wb');
    #p.logfile = sys.stdout;
    p.logfile = fout;
    p.setecho(False);
    p.send("usi\n");
    p.expect("usiok");
    p.send("isready\n");
    p.expect("readyok");
    p.send("usinewgame\n");
    moves = " moves";
    if sente :
        print "sente is ready"
        conn.recv(); #waiting for gote
        moves = "";
        bm = getBestmove(moves,p,0,0,byoyomi);
        conn.send(bm);
        moves = " moves" ;   
        moves=" ".join([moves,bm]);
    else:
        conn.send("I'm ready");
        print "gote is ready";
    while 1:
        om = conn.recv(); #opponent's move
        if om == "resi":
            print "I won !! ";
            o_engine_name = conn.recv(); #opponent's engine_name
            dumpResult(engine_name, o_engine_name, sente);
            break;
        moves=" ".join([moves,om]);
        bm = getBestmove(moves,p,0,0,byoyomi);
        conn.send(bm);
        if bm == "resi":
            conn.send(engine_name);  # send the engine_name to the winner
            print "I lost !! ";
            break;
        moves=" ".join([moves,bm]);



if __name__ == '__main__':
    cfg = json.loads(open("config.json","r").read());
    p1_conn, p2_conn = Pipe();
    p1 = Process(target=start_engine, args=([cfg["engine1"], p1_conn, cfg["byoyomi"]]));
    p1.start();
    p2 = Process(target=start_engine, args=([cfg["engine2"], p2_conn, cfg["byoyomi"], False]));
    p2.start();



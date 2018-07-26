# -*- coding: utf-8 -*-
import json
from datetime import datetime


def dumpKif(black, white, sf):
    suji = ["一","二","三","四","五","六","七","八","九"]
    zenkaku = ["１","２","３","４","５","６","７","８","９"]
    koma = {"P":"歩",
            "L":"香",
            "N":"桂",
            "S":"銀",
            "G":"金",
            "K":"玉",
            "B":"角",
            "R":"飛",
            "+P":"と",
            "+L":"成香",
            "+N":"成桂",
            "+S":"成銀",
            "+R":"龍",
            "+B":"馬",
    }
    
    usimoves = sf.split(" ")
    
    board = [ ["l","n","s","g","k","g","s","n","l"],
                  ["","b","","","","","","r",""],
                  ["p","p","p","p","p","p","p","p","p"],
                  ["","","","","","","","",""],
                  ["","","","","","","","",""],
                  ["","","","","","","","",""],
                  ["P","P","P","P","P","P","P","P","P"],
                  ["","R","","","","","","B",""],
                  ["L","N","S","G","K","G","S","N","L"] ]
    c = 0
    sfd = {'a': 0, 'c': 2, 'b': 1, 'e': 4, 'd': 3, 'g': 6, 'f': 5, 'i': 8, 'h': 7}
    moji = ""
    
    for move in usimoves:
        if len(move)<4:
            pass
        elif move=="moves":
            pass
        elif move=="position":
            pass
        elif move=="startpos":
            pass
        elif move=="resign":
            c += 1 
            m = "  {} 投了   ( 0:00/00:00:00)".format(c)
            moji += m + "\n"
        elif move[1]=="*":
            piece = move[0]
            c += 1 
            board[sfd[move[3]]][int(move[2])-1] = piece
            m = "  {} {}{}{}打   ( 0:00/00:00:00)".format(c,zenkaku[int(move[2])-1],suji[sfd[move[3]]],koma[piece])
            moji += m + "\n"
        else:
            piece = board[sfd[move[1]]][int(move[0])-1]
            if move[-1]=="+":
                c += 1 
                m = "  {} {}{}{}成({}{})   ( 0:00/00:00:00)".format(c,zenkaku[int(move[2])-1],suji[sfd[move[3]]],koma[piece.upper()],move[0],sfd[move[1]]+1)
                moji += m + "\n"
                piece = "+"+piece
                board[sfd[move[3]]][int(move[2])-1] = piece
                board[sfd[move[1]]][int(move[0])-1] = ""
                continue
            board[sfd[move[3]]][int(move[2])-1] = piece
            board[sfd[move[1]]][int(move[0])-1] = ""
            c += 1 
            m = "  {} {}{}{}({}{})   ( 0:00/00:00:00)".format(c,zenkaku[int(move[2])-1],suji[sfd[move[3]]],koma[piece.upper()],move[0],sfd[move[1]]+1)
            moji += m + "\n"
    
    
    
    moji = "#KIF version=2.0 encoding=UTF-8\n開始日時：{}\n棋戦：電脳(弾丸)\n持ち時間：1分\n手合割：平手\n先手：{}\n後手：{}\n手数----指手---------消費時間--\n{}".format(str(datetime.date(datetime.now())),black,white,moji)
    
    with open("kif/{}_vs_{}_{}".format(black,white,str(datetime.now()).replace(" ","-").replace(":","-").split(".")[0].replace("-","")),"w") as f:
        f.write(moji)
    

def dumpResult(black, white, sente):
    if sente:
        winner = black 
        loser = white;
    else:
        loser = black;
        winner = white;

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


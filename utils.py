import json



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


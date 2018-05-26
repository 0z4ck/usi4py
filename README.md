# UPDATE 
I found https://github.com/ai5/shogi_repeat which seems better, so I'm switching to this.


# usi4py

A simple python script to organize games between usi_engines. 

I made this script because all existing "engine_handlers" were for windows only.






### Platforms:
* Linux 
* Mac OS X 
* Windows 


### Dependencies

* python 2.7
* pexpect
* json
* ~~multiprocessing~~ not used anymore (deleted at 9e287e4b5445825be12589f02d00b47cbf870b3e)


### Features
- [x] Basic USI engines support
- [x] Byoyomi setting
- [x] Save result as json
- [x] Eval&Book files setting (by specifying the engine directory) 
- [ ] Bonanza protocol support
- [x] btime, wtime setting
- [x] hash size setting
- [ ] number of threads setting      Note: the option name differs on each engine. to implement, edit initialize()




## Usage
 - example.py: example script to start a game with two engines.
 - try in the interactive shell 
```bash
[username@hostname]$ python
Python 2.7.14 (default, Sep 22 2017, 15:49:07) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-18)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import logging, sys
>>> from usiclient import UsiClient
>>> 
>>> logger = logging.getLogger()
>>> logging.basicConfig()
>>> logger.setLevel(logging.INFO)
>>> 
>>> e = UsiClient("/home/user/engines/Lesserkai/Lesserkai", "/home/user/engines/Lesserkai")  
>>> e.p.logfile = sys.stdout
>>> e.initialize()     
>>> e.newgame()
>>>
>>> e.go(" moves 2g2f 4a3b 2f2e",0,0,10000)

'''

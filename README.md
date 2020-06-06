# HeadsUp
A uci chess engine adapter that can combine 2 engines and play as one. First engine may play in the middle and the other engine may continue to play for the rest of the game. The switch from engine1 to engine2 and vice versa can be controlled by move number and/or total piece value remaining on the board.

### A. Create a uci engine from 2 actual uci chess engines

##### 1. Using headsup.py
* Download python 3.8 and up
* Install python-chess 0.31.2 and up
* Modify headsup.cfg
* Put headsup.cfg and headsup.py in the same folder
* Create a batch file headsup.bat, see example in the repo.
    * write python.exe headsup.py
* Install headsup.bat as a uci engine in cutechess GUI or Arena GUI

##### 2. Using headsup.exe
* Download headsup.exe
* Modify headsup.cfg
* Put headsup.cfg and headsup.exe in the same folder
* Install headsup.exe as a uci engine on the following tested GUI.  
    * Cutechess
    * Arena
    * Banksia
    * Winboard
    * HIARCS Chess Explorer
    * Python Easy Chess
    
### B. What it can do
* You can play against it
* You can play it against another engine
* You can use in infinite anaysis.

### C. Limitations
* Can only use uci engines

### D. Sample match
Pondering play at TC 60s+0.1s between [HeadsUp and Stockfish](https://github.com/fsmosca/HeadsUp/wiki/HeadsUp-vs-Stockfish)


### E. Credits
* Kai Laskos  
http://talkchess.com/forum3/viewtopic.php?f=2&t=73940

* Python-Chess  
https://github.com/niklasf/python-chess

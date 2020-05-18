# HeadsUp
A chess engine adapter that can combine 2 engines and play as one. First engine may play in the middle and the other engine may continue to play for the rest of the game.

### A. Create a uci engine from 2 actual uci chess engines

##### 1. Using headsup.py
* Download python 3.7 and up
* Install python-chess 0.30.0 and up
* Modify headsup.cfg
* Put headsup.cfg and headsup.py in the same folder
* Create a batch file headsup.bat
    * write python.exe headsup.py
* Install headsup.bat as a uci engine in cutechess GUI

##### 2. Using headsup.exe
* Download headsup.exe
* Modify headsup.cfg
* Put headsup.cfg and headsup.exe in the same folder
* Install headsup.exe as a uci engine in cutechess GUI

### B. Credits
* Kai Laskos  
http://talkchess.com/forum3/viewtopic.php?f=2&t=73940

* Python-Chess  
https://github.com/niklasf/python-chess

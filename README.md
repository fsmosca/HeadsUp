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
* Install headsup.bat as a uci engine in cutechess GUI or Arena GUI

##### 2. Using headsup.exe
* Download headsup.exe
* Modify headsup.cfg
* Put headsup.cfg and headsup.exe in the same folder
* Install headsup.exe as a uci engine in cutechess GUI or Arena GUI

### B. Limitations
* Cannot be used for ponder on games
* Cannot be used in infinite analysis
* Only supports blitz and movetime time control

### C. Sample run using cutechess-cli
Headsup = Lc0 v0.25.1 blas + Stockfish 11
* Lc0 v0.25.1 blas as first engine will be playing from move 1 to move 15.
* Stockfish 11 as second engine will be playing for the rest of the game starting from move 16.

Engine switching can be configured via the headsup.cfg file. Second engine can be switched by either material and move number conditions.

```
Started game 3 of 100 (Lc0 v0.25.1 blas/Stockfish 11 vs Stockfish 11)
Started game 2 of 100 (Stockfish 11 vs Lc0 0.25.1 blas/Stockfish 11)
Started game 1 of 100 (Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11)
Finished game 3 (Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11): 1/2-1/2 {Draw by 3-fold repetition}
Score of Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11: 0 - 0 - 1  [0.500] 1
Started game 4 of 100 (Stockfish 11 vs Lc0 0.25.1 blas/Stockfish 11)
Finished game 1 (Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11): 1-0 {White mates}
Score of Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11: 1 - 0 - 1  [0.750] 2
Started game 5 of 100 (Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11)
Finished game 2 (Stockfish 11 vs Lc0 0.25.1 blas/Stockfish 11): 1/2-1/2 {Draw by insufficient mating material}
Score of Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11: 1 - 0 - 2  [0.667] 3
Started game 6 of 100 (Stockfish 11 vs Lc0 0.25.1 blas/Stockfish 11)
Finished game 5 (Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11): 1/2-1/2 {Draw by insufficient mating material}
Score of Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11: 1 - 0 - 3  [0.625] 4
...      Lc0 0.25.1 blas/Stockfish 11 playing White: 1 - 0 - 2  [0.667] 3
...      Lc0 0.25.1 blas/Stockfish 11 playing Black: 0 - 0 - 1  [0.500] 1
...      White vs Black: 1 - 0 - 3  [0.625] 4
Elo difference: 88.7 +/- 172.5, LOS: 84.1 %, DrawRatio: 75.0 %
Started game 7 of 100 (Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11)
Finished game 4 (Stockfish 11 vs Lc0 0.25.1 blas/Stockfish 11): 1/2-1/2 {Draw by fifty moves rule}
Score of Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11: 1 - 0 - 4  [0.600] 5
Started game 8 of 100 (Stockfish 11 vs Lc0 0.25.1 blas/Stockfish 11)
Finished game 6 (Stockfish 11 vs Lc0 0.25.1 blas/Stockfish 11): 1-0 {White mates}
Score of Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11: 1 - 1 - 4  [0.500] 6
Started game 9 of 100 (Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11)
Finished game 7 (Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11): 1/2-1/2 {Draw by insufficient mating material}
Score of Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11: 1 - 1 - 5  [0.500] 7
Started game 10 of 100 (Stockfish 11 vs Lc0 0.25.1 blas/Stockfish 11)
Finished game 8 (Stockfish 11 vs Lc0 0.25.1 blas/Stockfish 11): 1/2-1/2 {Draw by fifty moves rule}
Score of Lc0 0.25.1 blas/Stockfish 11 vs Stockfish 11: 1 - 1 - 6  [0.500] 8
...      Lc0 0.25.1 blas/Stockfish 11 playing White: 1 - 0 - 3  [0.625] 4
...      Lc0 0.25.1 blas/Stockfish 11 playing Black: 0 - 1 - 3  [0.375] 4
...      White vs Black: 2 - 0 - 6  [0.625] 8
Elo difference: 0.0 +/- 125.4, LOS: 50.0 %, DrawRatio: 75.0 %
...
```

### D. Credits
* Kai Laskos  
http://talkchess.com/forum3/viewtopic.php?f=2&t=73940

* Python-Chess  
https://github.com/niklasf/python-chess

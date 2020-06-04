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

### D. Sample run using cutechess-cli
Headsup v1.0 = Lc0 0.25.1 blas + Stockfish 11
* Lc0 0.25.1 blas as first engine will be playing from move 1 to move 12.
* Stockfish 11 as second engine will be playing for the rest of the game starting from move 13.

Engine switching can be configured via the headsup.cfg file. Second engine can be switched by either material and move number conditions.
Ponder On games at TC 60s+0.1s

```
...
D:\github\HeadsUp>D:\Chess\CuteChess-CLI\cutechess-cli.exe -tournament gauntlet -rounds 50 -games 2 -repeat -openings file=docs\headsup_50openings.pgn format=pgn order=random plies=1000 start=1 policy=round -concurrency 2 -pgnout ponder_on_test_1_tc_60s+0.1s.pgn fi -wait 100 -maxmoves 500 -ratinginterval 4 -engine conf="HeadsUp v1.0" tc=0/60+0.1 ponder -engine conf="Eman Chimera 4.0" tc=0/60+0.1 ponder -engine conf="Stockfish 11" tc=0/60+0.1 ponder
Indexing opening suite...
Started game 2 of 200 (Eman Chimera 4.0 vs HeadsUp v1.0)
Started game 1 of 200 (HeadsUp v1.0 vs Eman Chimera 4.0)
Finished game 2 (Eman Chimera 4.0 vs HeadsUp v1.0): 1/2-1/2 {Draw by 3-fold repetition}
Started game 3 of 200 (HeadsUp v1.0 vs Stockfish 11)
Finished game 1 (HeadsUp v1.0 vs Eman Chimera 4.0): 1/2-1/2 {Draw by 3-fold repetition}
Started game 4 of 200 (Stockfish 11 vs HeadsUp v1.0)
Finished game 3 (HeadsUp v1.0 vs Stockfish 11): 1/2-1/2 {Draw by 3-fold repetition}
Started game 5 of 200 (HeadsUp v1.0 vs Eman Chimera 4.0)
Finished game 4 (Stockfish 11 vs HeadsUp v1.0): 1/2-1/2 {Draw by insufficient mating material}
Rank Name                          Elo     +/-   Games   Score    Draw
   0 HeadsUp v1.0                    0       0       4   50.0%  100.0%
   1 Stockfish 11                    0       0       2   50.0%  100.0%
   2 Eman Chimera 4.0                0       0       2   50.0%  100.0%

Started game 6 of 200 (Eman Chimera 4.0 vs HeadsUp v1.0)
Finished game 5 (HeadsUp v1.0 vs Eman Chimera 4.0): 1/2-1/2 {Draw by insufficient mating material}
Started game 7 of 200 (HeadsUp v1.0 vs Stockfish 11)
Finished game 6 (Eman Chimera 4.0 vs HeadsUp v1.0): 1/2-1/2 {Draw by insufficient mating material}
Started game 8 of 200 (Stockfish 11 vs HeadsUp v1.0)
Finished game 7 (HeadsUp v1.0 vs Stockfish 11): 1-0 {White mates}
Started game 9 of 200 (HeadsUp v1.0 vs Eman Chimera 4.0)
Finished game 8 (Stockfish 11 vs HeadsUp v1.0): 1/2-1/2 {Draw by 3-fold repetition}
Rank Name                          Elo     +/-   Games   Score    Draw
   0 HeadsUp v1.0                   44      82       8   56.3%   87.5%
   1 Eman Chimera 4.0                0       0       4   50.0%  100.0%
   2 Stockfish 11                  -89     173       4   37.5%   75.0%

Started game 10 of 200 (Eman Chimera 4.0 vs HeadsUp v1.0)
Finished game 9 (HeadsUp v1.0 vs Eman Chimera 4.0): 1/2-1/2 {Draw by fifty moves rule}
Started game 11 of 200 (HeadsUp v1.0 vs Stockfish 11)
Finished game 10 (Eman Chimera 4.0 vs HeadsUp v1.0): 0-1 {Black mates}
Started game 12 of 200 (Stockfish 11 vs HeadsUp v1.0)
Finished game 11 (HeadsUp v1.0 vs Stockfish 11): 1-0 {White mates}
Started game 13 of 200 (HeadsUp v1.0 vs Eman Chimera 4.0)
Finished game 12 (Stockfish 11 vs HeadsUp v1.0): 1/2-1/2 {Draw by 3-fold repetition}
Rank Name                          Elo     +/-   Games   Score    Draw
   0 HeadsUp v1.0                   89      93      12   62.5%   75.0%
   1 Eman Chimera 4.0              -58     110       6   41.7%   83.3%
   2 Stockfish 11                 -120     162       6   33.3%   66.7%

Started game 14 of 200 (Eman Chimera 4.0 vs HeadsUp v1.0)
Finished game 14 (Eman Chimera 4.0 vs HeadsUp v1.0): 1/2-1/2 {Draw by 3-fold repetition}
Finished game 13 (HeadsUp v1.0 vs Eman Chimera 4.0): 1/2-1/2 {Draw by stalemate}
Started game 15 of 200 (HeadsUp v1.0 vs Stockfish 11)
Started game 16 of 200 (Stockfish 11 vs HeadsUp v1.0)
Finished game 16 (Stockfish 11 vs HeadsUp v1.0): 1/2-1/2 {Draw by 3-fold repetition}
Started game 17 of 200 (HeadsUp v1.0 vs Eman Chimera 4.0)
Finished game 15 (HeadsUp v1.0 vs Stockfish 11): 1/2-1/2 {Draw by fifty moves rule}
Rank Name                          Elo     +/-   Games   Score    Draw
   0 HeadsUp v1.0                   66      70      16   59.4%   81.3%
   1 Eman Chimera 4.0              -44      82       8   43.8%   87.5%
   2 Stockfish 11                  -89     116       8   37.5%   75.0%

Started game 18 of 200 (Eman Chimera 4.0 vs HeadsUp v1.0)
Finished game 17 (HeadsUp v1.0 vs Eman Chimera 4.0): 1/2-1/2 {Draw by fifty moves rule}
Started game 19 of 200 (HeadsUp v1.0 vs Stockfish 11)
Finished game 18 (Eman Chimera 4.0 vs HeadsUp v1.0): 1/2-1/2 {Draw by insufficient mating material}
Started game 20 of 200 (Stockfish 11 vs HeadsUp v1.0)
Finished game 19 (HeadsUp v1.0 vs Stockfish 11): 1/2-1/2 {Draw by 3-fold repetition}
Started game 21 of 200 (HeadsUp v1.0 vs Eman Chimera 4.0)
Finished game 20 (Stockfish 11 vs HeadsUp v1.0): 1/2-1/2 {Draw by insufficient mating material}
Rank Name                          Elo     +/-   Games   Score    Draw
   0 HeadsUp v1.0                   53      56      20   57.5%   85.0%
   1 Eman Chimera 4.0              -35      66      10   45.0%   90.0%
   2 Stockfish 11                  -70      92      10   40.0%   80.0%
...
```

### E. Credits
* Kai Laskos  
http://talkchess.com/forum3/viewtopic.php?f=2&t=73940

* Python-Chess  
https://github.com/niklasf/python-chess

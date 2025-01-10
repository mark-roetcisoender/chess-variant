# chess-variant
Modified version of chess
This program simulates a modified version of chess and contains classes representing the game itself,
as well as the different types of chess pieces. The class representing the game tracks where each piece is,
if an entered move is valid, moves pieces in the event of a valid move, any captures, whose turn it is (black
or white), and whether the game has been won. The game is won when all pieces of the same type are captured by
the opposing player (e.g. black captures the (1) white queen, or white captures the (8) black pawns. As such, there
is no check or checkmate. All pieces behave the same as regular chess with the exception that there is no
castling, en passant, or pawn promotion.

Sample Usage:

    board = ChessVar()
    board.make_move("a2", "a3")
    board.make_move("c7", "c5")
    board.print_board()

Output:
[RO] [KN] [BI] [QU] [KI] [BI] [KN] [RO] 

[PA] [PA] [--] [PA] [PA] [PA] [PA] [PA] 

[--] [--] [--] [--] [--] [--] [--] [--] 

[--] [--] [PA] [--] [--] [--] [--] [--] 

[--] [--] [--] [--] [--] [--] [--] [--] 

[pa] [--] [--] [--] [--] [--] [--] [--] 

[--] [pa] [pa] [pa] [pa] [pa] [pa] [pa] 

[ro] [kn] [bi] [qu] [ki] [bi] [kn] [ro] 

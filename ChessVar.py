# Author: Mark Roetcisoender
# GitHub username: mark-roetcisoender
# Date: 12/6/23
# Description: This program simulates a modified version of chess and contains classes representing the game itself,
# as well as the different types of chess pieces. The class representing the game tracks where each piece is,
# if an entered move is valid, moves pieces in the event of a valid move, any captures, whose turn it is (black
# or white), and whether the game has been won. The game is won when all pieces of the same type are captured by
# the opposing player (e.g. black captures the (1) white queen, or white captures the (8) black pawns. As such, there
# is no check or checkmate. All pieces behave the same as regular chess with the exception that there is no
# castling, en passant, or pawn promotion.

class ChessVar:
    """Represents the game state of a game of chess. Tracks whose turn it is, if a move is valid, updates the board
    in the case of a valid move, initiates a capture if part of a legal move, and checks if the game is won. Takes no
    parameters. Contains methods to check each move, and update the game accordingly. Uses ChessPiece (and any
    inherited classes) objects to
    represent the pieces & determine legal moves
    Data members:   _game_state             Initialized to 'UNFINISHED'. Set to WHITE_WON or BLACK_WON in event of a win
                    _whose_turn             Initialized to 'white' and alternates to 'black' tracking which player's
                                            turn it is
                    _captured_by_white      dictionary of pieces captured by the white player. Key is the type of piece
                                            and value is the amount of that piece left to capture
                    _captured_by_black      dictionary of pieces captured by the black player. Key is the type of piece
                                            and value is the amount of that piece left to capture
                    _game_board             list of dictionaries which tracks the positions of the pieces. Initialized
                                            to the standard chess start. Within the lists, dictionary format is:
                                            a1 (key) : ChessPiece object (value)"""

    def __init__(self):
        """initialize data members of ChessVar"""
        self._game_state = "UNFINISHED"             # string
        self._whose_turn = "white"                  # string
        self._captured_by_white = {'pawn': 8,       # dictionary
                                   'rook': 2,
                                   'knight': 2,
                                   'bishop': 2,
                                   'queen': 1,
                                   'king': 1}
        self._captured_by_black = {'pawn': 8,       # dictionary
                                   'rook': 2,
                                   'knight': 2,
                                   'bishop': 2,
                                   'queen': 1,
                                   'king': 1}

        self._game_board = [                        # list of dictionaries
            {'a8': Rook("rook", "black", 'a8'), 'b8': Knight("knight", "black", 'b8'),
             'c8': Bishop("bishop", "black", 'c8'), 'd8': Queen("queen", "black", 'd8'),
             'e8': King("king", "black", 'e8'), 'f8': Bishop("bishop", "black", 'f8'),
             'g8': Knight("knight", "black", 'g8'), 'h8': Rook("rook", "black", 'h8')},
            {'a7': Pawn("pawn", "black", 'a7'), 'b7': Pawn("pawn", "black", 'b7'), 'c7': Pawn("pawn", "black", 'c7'),
             'd7': Pawn("pawn", "black", 'd7'), 'e7': Pawn("pawn", "black", 'e7'), 'f7': Pawn("pawn", "black", 'f7'),
             'g7': Pawn("pawn", "black", 'g7'), 'h7': Pawn("pawn", "black", 'h7')},
            {'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None, 'g6': None, 'h6': None},
            {'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None, 'g5': None, 'h5': None},
            {'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None, 'h4': None},
            {'a3': None, 'b3': None, 'c3': None, 'd3': None, 'e3': None, 'f3': None, 'g3': None, 'h3': None},
            {'a2': Pawn("pawn", "white", 'a2'), 'b2': Pawn("pawn", "white", 'b2'), 'c2': Pawn("pawn", "white", 'c2'),
             'd2': Pawn("pawn", "white", 'd2'), 'e2': Pawn("pawn", "white", 'e2'), 'f2': Pawn("pawn", "white", 'f2'),
             'g2': Pawn("pawn", "white", 'g2'), 'h2': Pawn("pawn", "white", 'h2')},
            {'a1': Rook("rook", "white", "a1"), 'b1': Knight("knight", "white", "b1"),
             'c1': Bishop("bishop", "white", "c1"), 'd1': Queen("queen", "white", 'd1'),
             'e1': King("king ", "white", "e1"), 'f1': Bishop("bishop", "white", 'f1'),
             'g1': Knight("knight", "white", 'g1'), 'h1': Rook("rook", "white", 'h1')}
            ]

    def get_game_state(self):
        """Get method which returns the game state"""
        return self._game_state

    def set_game_state(self, update):
        """Set method for the game state"""
        self._game_state = update

    def get_whose_turn(self):
        """Get method on whose turn it is"""
        return self._whose_turn

    def get_game_board(self):
        """Get method which returns the game board"""
        return self._game_board

    def make_move(self, origen_loc, destination_loc):
        """Takes two parameters, the origin location and destination location as strings. Checks to see if the move
        indicated is valid, if it results in a capture and updates the game board accordingly. Manages whose turn
        it is, the game state, and how many pieces have been captured by each player. Returns True if the
        method is valid & has been completed, and False otherwise."""

        # initialize valid_origin and destination checks to False
        valid_origin = False
        valid_destination = False
        origin_count = 0
        destination_count = 0

        # ensure no player has won the game yet
        if self._game_state == "WHITE_WON" or self._game_state == "BLACK_WON":
            return False

        # check if the origin location is on the game board, and origin matches correct player's turn
        for row in self._game_board:
            origin_count += 1
            if origen_loc in row and row[origen_loc] is not None:
                if row[origen_loc].get_color() == self._whose_turn:
                    valid_origin = True
                    # if we've found the origin location, no need to keep iterating
                    break

        # check if the destination location is on the game board
        for row in self._game_board:
            destination_count += 1
            if destination_loc in row:
                valid_destination = True
                # if we've found the origin location, no need to keep iterating
                break

        # return False if either the origin or destination locations are invalid
        if valid_destination is False or valid_origin is False:
            return False

        # check if the destination location holds a piece of the current player
        if self._game_board[destination_count - 1][destination_loc] is not None:
            if self._game_board[destination_count - 1][destination_loc].get_color() == self._whose_turn:
                return False

        # if the origin and destination locations are the same, move is invalid, return False
        if origen_loc == destination_loc:
            return False

        # if piece is a king, check for legal moves & if destination_loc is one.
        # We've already eliminated any same-color moves (goes for the rest of the possible_moves methods)
        if type(self._game_board[origin_count - 1][origen_loc]) == King:
            king_moves = self.king_possible_moves(origen_loc)
            if destination_loc not in king_moves:
                return False

        # if piece is a pawn, check for legal moves & if destination_loc is one based on pawn's color
        if type(self._game_board[origin_count - 1][origen_loc]) == Pawn:
            pawn_moves = []
            if self._game_board[origin_count - 1][origen_loc].get_color() == 'white':
                pawn_moves = self.white_pawn_possible_moves(origen_loc)
            if self._game_board[origin_count - 1][origen_loc].get_color() == 'black':
                pawn_moves = self.black_pawn_possible_moves(origen_loc)
            if destination_loc not in pawn_moves:
                return False

        # if piece is a bishop, check for legal moves & if destination_loc is one
        if type(self._game_board[origin_count - 1][origen_loc]) == Bishop:
            bishop_moves = self.bishop_possible_moves(origen_loc, destination_loc)
            if bishop_moves is None:
                return False
            if destination_loc not in bishop_moves:
                return False

        # if the piece is a rook, check for legal moves & if destination_loc is one
        if type(self._game_board[origin_count - 1][origen_loc]) == Rook:  # update how I check this?
            rook_moves = self.rook_possible_moves(origen_loc, destination_loc)
            if rook_moves is None:
                return False
            if destination_loc not in rook_moves:
                return False

        # if the piece is a queen, check for legal moves & if destination_loc is one
        if type(self._game_board[origin_count - 1][origen_loc]) == Queen:  # update how I check this?
            queen_moves = self.queen_possible_moves(origen_loc, destination_loc)
            if queen_moves is None:
                return False
            if destination_loc not in queen_moves:
                return False

        # if the piece is a knight, check for legal moves & if destination_loc is one
        if type(self._game_board[origin_count - 1][origen_loc]) == Knight:
            knight_moves = self.knight_possible_moves(origen_loc, destination_loc)
            if destination_loc not in knight_moves:

                return False

        # if we're here, the move is valid. Update game info & return True
        # check if the destination location holds a piece of the opposite player, and initiate capture if so
        if self._game_board[destination_count - 1][destination_loc] is not None:
            if self._game_board[destination_count - 1][destination_loc].get_color() != self._whose_turn:
                self.capture(destination_count - 1, destination_loc)

        # move piece at origin to destination, and set origin to None
        self.move_piece(destination_count - 1, destination_loc, origin_count - 1, origen_loc)
        # check if a capture has caused a player to win
        self.check_for_win()
        # after successful move, change whose turn it is
        self.next_turn()
        return True

    def move_piece(self, dest_row, dest_loc, origin_row, origin_loc):
        """method to move the piece in the board data member. Takes four parameters: the destination
        row (which list the destination is on, the destination location (key of a dictionary, eg 'a3'),
        the origin row (which list the origin is in), and the origin location (key of the dictionary).
        Move the object at the origin location to the destination location and sets the value in the
        origin location to None."""
        self._game_board[dest_row][dest_loc] = self._game_board[origin_row][origin_loc]
        self._game_board[dest_row][dest_loc].set_location(dest_loc)
        self._game_board[origin_row][origin_loc] = None
        # if the piece is a pawn, update it's 'has moved' data member to True
        if type(self._game_board[dest_row][dest_loc]) == Pawn:
            self._game_board[dest_row][dest_loc].set_has_moved()

    def capture(self, dest_row, destination_loc):
        """Method to update list of captured pieces Takes parameters of the destination row (which
        list the destination piece is in), and the destination location (the key of the position).
        Prior to the capturing piece moving to the destination location, the method check what piece
        is there, what color it belongs to, and updates the appropriate dictionary of captured pieces"""
        piece = self._game_board[dest_row][destination_loc].get_piece_type()
        if self._whose_turn == 'white':
            self._captured_by_white[piece] -= 1
        if self._whose_turn == 'black':
            self._captured_by_black[piece] -= 1

    def white_pawn_possible_moves(self, cur_loc):
        """calculates valid moves for the white pawn piece and returns them in a list. Takes a parameter
        of the current position, which is used to calculate potential moves. """
        char_pawn_moves = []
        # convert parameter to x/y coordinates
        x_coordinate = self.convert_to_num(cur_loc[0])
        y_coordinate = int(cur_loc[1])
        temp_x = x_coordinate
        temp_y = y_coordinate
        # check if the pawn has moved
        has_moved = self._game_board[8 - y_coordinate][cur_loc].get_has_moved()
        # if the pawn is already in the 'top' row, return as there's not any valid moves
        if y_coordinate == 8:
            return char_pawn_moves
        # if the space 'above' the white pawn is empty, add it to the list of possible moves
        temp_y += 1
        # convert back to a character format ('a5')
        x = self.convert_to_char(temp_x)
        y = str(temp_y)
        coord = x + y
        if self._game_board[8 - temp_y][coord] is None:
            char_pawn_moves.append(coord)
            # if the spot 'above' is open, and the pawn hasn't moved yet, check and add the 'next up' spot if it's open
            temp_y += 1
            x = self.convert_to_char(temp_x)
            y = str(temp_y)
            coord = x + y
            if has_moved is False and self._game_board[8 - temp_y][coord] is None:
                char_pawn_moves.append(coord)

        # check for attacking moves 'up and to the left' one square
        temp_y = y_coordinate + 1
        temp_x = x_coordinate - 1
        # double check that the move is on the board
        if 0 < temp_x < 9:
            x = self.convert_to_char(temp_x)
            y = str(temp_y)
            coord = x + y
            # if the spot has a piece, we know it's the opposite color, so add it to the moves
            if self._game_board[8 - temp_y][coord] is not None:
                char_pawn_moves.append(coord)

        # check for attacking moves 'up and to the right' one square
        temp_y = y_coordinate + 1
        temp_x = x_coordinate + 1
        # double check that the new x coordinate is on the board
        if 0 < temp_x < 9:
            x = self.convert_to_char(temp_x)
            y = str(temp_y)
            coord = x + y
            # if the spot has a piece, we know it's the opposite color, so add it to the moves
            if self._game_board[8 - temp_y][coord] is not None:
                char_pawn_moves.append(coord)

        return char_pawn_moves

    def black_pawn_possible_moves(self, cur_loc):
        """calculates valid moves for the black pawn piece and returns them in a list. Takes a parameter
        of the current position, which is used to calculate potential moves."""
        char_pawn_moves = []
        x_coordinate = self.convert_to_num(cur_loc[0])
        y_coordinate = int(cur_loc[1])
        temp_x = x_coordinate
        temp_y = y_coordinate
        has_moved = self._game_board[8 - y_coordinate][cur_loc].get_has_moved()
        # if the pawn is in the 'bottom' row, return as there's no legal moves
        if y_coordinate == 1:
            return char_pawn_moves
        # if the space 'below' the black pawn is empty, add it to the list of possible moves
        temp_y -= 1
        x = self.convert_to_char(temp_x)
        y = str(temp_y)
        coord = x + y
        if self._game_board[8 - temp_y][coord] is None:
            char_pawn_moves.append(coord)
            # if the spot 'below' is open, and the pawn hasn't moved yet, add the 'next down' spot if it's open
            temp_y -= 1
            x = self.convert_to_char(temp_x)
            y = str(temp_y)
            coord = x + y
            if has_moved is False and self._game_board[8 - temp_y][coord] is None:
                char_pawn_moves.append(coord)

        # check for attacking moves 'down and to the left' one square
        temp_y = y_coordinate - 1
        temp_x = x_coordinate - 1
        # double check that the square is still on the board
        if 0 < temp_x < 9:
            x = self.convert_to_char(temp_x)
            y = str(temp_y)
            coord = x + y
            # if the spot has a piece, we know it's the opposite color, so add it to the moves
            if self._game_board[8 - temp_y][coord] is not None:
                char_pawn_moves.append(coord)

        # check for attacking moves 'down and to the right' one square
        temp_y = y_coordinate - 1
        temp_x = x_coordinate + 1
        # double-check the coordinate is on the board
        if 0 < temp_x < 9:
            x = self.convert_to_char(temp_x)
            y = str(temp_y)
            coord = x + y
            # if the spot has a piece, we know it's the opposite color, so add it to the moves
            if self._game_board[8 - temp_y][coord] is not None:
                char_pawn_moves.append(coord)

        return char_pawn_moves

    def king_possible_moves(self, cur_loc):
        """calculates valid moves for the king piece and returns them in a list. Takes a parameter
        of the current position, which is used to calculate potential moves."""
        coord_king_moves = []
        char_king_moves = []
        # convert parameter into x/y coordinates
        x_coordinate = self.convert_to_num(cur_loc[0])
        y_coordinate = int(cur_loc[1])
        # get all possible king moves one 'space' from the current location
        for column in range(x_coordinate - 1, x_coordinate + 2):
            for row in range(y_coordinate - 1, y_coordinate + 2):
                if 0 < column < 9 and 0 < row < 9:
                    location = column, row
                    coord_king_moves.append(location)
        # convert the integer coordinates in strings and return the list. Only moves with a destination
        # location that's empty or an opposing piece will have made it this far due to same-color check.
        for coord in coord_king_moves:
            x = self.convert_to_char(coord[0])
            y = str(coord[1])
            coordinate = x + y
            char_king_moves.append(coordinate)
        return char_king_moves

    def knight_possible_moves(self, cur_loc, dest_loc):
        """Checks for valid moves given the location of a knight piece and returns them in a list. Takes
        parameters of the piece's current and destination locations"""
        char_knight_moves = []
        # convert current and destination locations to x/y coordinates
        x_coordinate = self.convert_to_num(cur_loc[0])
        y_coordinate = int(cur_loc[1])
        dest_x_coord = self.convert_to_num(dest_loc[0])
        dest_y_coord = int(dest_loc[1])
        # calculate the difference in x and y coordinates, and take the absolute value
        xdiff = abs(x_coordinate - dest_x_coord)
        ydiff = abs(y_coordinate - dest_y_coord)
        # we know that a valid knight move will fit into one of these two cases
        if xdiff == 1 and ydiff == 2:
            char_knight_moves.append(dest_loc)
        if xdiff == 2 and ydiff == 1:
            char_knight_moves.append(dest_loc)
        return char_knight_moves

    def queen_possible_moves(self, cur_loc, dest_loc):
        """calculates possible moves of the current Queen piece. Checks to see if the destination is on the same
        'plane' either vertically or horizontally as the origin, and calls rook_possible_moves if so. If not, calls
        bishop_possible_moves. Returns a list of possible moves from the origin in the direction of the destination"""

        char_queen_moves = []
        # convert both coordinates to x/y format
        cur_x_coordinate = self.convert_to_num(cur_loc[0])
        cur_y_coordinate = int(cur_loc[1])
        dest_x_coord = self.convert_to_num(dest_loc[0])
        dest_y_coord = int(dest_loc[1])
        # if destination is on the same x or y coordinate
        if dest_x_coord == cur_x_coordinate or dest_y_coord == cur_y_coordinate:
            char_queen_moves = self.rook_possible_moves(cur_loc, dest_loc)
            return char_queen_moves
        # else check for valid bishop moves
        char_queen_moves = self.bishop_possible_moves(cur_loc, dest_loc)
        return char_queen_moves

    def bishop_possible_moves(self, cur_loc, dest_loc):
        """calculates possible moves of the current Bishop piece in the direction of the destination location
        and returns them in a list. Only checks in the direction of the move. Takes parameters of the current
        location as well as the destination location"""
        char_bishop_moves = []
        # convert both coordinates to x/y format
        cur_x_coordinate = self.convert_to_num(cur_loc[0])
        cur_y_coordinate = int(cur_loc[1])
        dest_x_coord = self.convert_to_num(dest_loc[0])
        dest_y_coord = int(dest_loc[1])

        # if destination is 'up and to the right'
        if dest_x_coord > cur_x_coordinate and dest_y_coord > cur_y_coordinate:
            # go 'up and to the right' one square at a time, checking if there's a piece there already
            temp_x = cur_x_coordinate
            temp_y = cur_y_coordinate
            while temp_x != dest_x_coord or temp_y != dest_y_coord:
                temp_x += 1
                temp_y += 1
                x = self.convert_to_char(temp_x)
                y = str(temp_y)
                coord = x + y
                # if there is a piece there, only add it to the list if it's the destination
                if self._game_board[8 - temp_y][coord] is not None:
                    if coord == dest_loc:
                        char_bishop_moves.append(coord)
                    # print("There is a piece here")
                    return char_bishop_moves
                # if no piece at current square, add to valid moves list
                char_bishop_moves.append(coord)
            return char_bishop_moves

        if dest_x_coord > cur_x_coordinate and dest_y_coord < cur_y_coordinate:
            # go 'down and to the right' one square, checking if there's a piece there already
            temp_x = cur_x_coordinate
            temp_y = cur_y_coordinate
            while temp_x != dest_x_coord or temp_y != dest_y_coord:
                temp_x += 1
                temp_y -= 1
                x = self.convert_to_char(temp_x)
                y = str(temp_y)
                coord = x + y
                # if there is a piece there, only add it to the list if it's the destination
                if self._game_board[8 - temp_y][coord] is not None:
                    if coord == dest_loc:
                        char_bishop_moves.append(coord)
                    return char_bishop_moves
                # if the space is empty, add it to the list
                char_bishop_moves.append(coord)
            return char_bishop_moves

        if dest_x_coord < cur_x_coordinate and dest_y_coord > cur_y_coordinate:
            # go up and to the left one square until the destination is reached, checking if the space is empty
            temp_x = cur_x_coordinate
            temp_y = cur_y_coordinate
            while temp_x != dest_x_coord or temp_y != dest_y_coord:
                temp_x -= 1
                temp_y += 1
                x = self.convert_to_char(temp_x)
                y = str(temp_y)
                coord = x + y
                # if there is a piece there, only add it to the list if it's the destination
                if self._game_board[8 - temp_y][coord] is not None:
                    if coord == dest_loc:
                        char_bishop_moves.append(coord)
                    return char_bishop_moves
                # if the space is empty, add it to the list
                char_bishop_moves.append(coord)
            return char_bishop_moves

        if dest_x_coord < cur_x_coordinate and dest_y_coord < cur_y_coordinate:
            # check down and to the left one square until destination or an occupied square is reached
            temp_x = cur_x_coordinate
            temp_y = cur_y_coordinate
            while temp_x != dest_x_coord or temp_y != dest_y_coord:
                temp_x -= 1
                temp_y -= 1
                x = self.convert_to_char(temp_x)
                y = str(temp_y)
                coord = x + y
                # if there is a piece there, only add it to the list if it's the destination
                if self._game_board[8 - temp_y][coord] is not None:
                    if coord == dest_loc:
                        char_bishop_moves.append(coord)
                    return char_bishop_moves
                # if the space is empty, add it to the list
                char_bishop_moves.append(coord)
            return char_bishop_moves

    def rook_possible_moves(self, cur_loc, dest_loc):
        """Calculates valid moves of the current Rook piece and returns them in a list. If the column or row doesn't
        match, escape early. Takes parameters of the current location as well as the destination location"""
        char_rook_moves = []
        # convert both coordinates to x/y format
        cur_x_coordinate = self.convert_to_num(cur_loc[0])
        cur_y_coordinate = int(cur_loc[1])
        dest_x_coord = self.convert_to_num(dest_loc[0])
        dest_y_coord = int(dest_loc[1])

        # if neither the x nor y coordinates are on the same plane, return a blank list as there are no valid moves
        if cur_x_coordinate != dest_x_coord and cur_y_coordinate != dest_y_coord:
            return char_rook_moves

        # if the destination is on the same y-axis as the current location
        if cur_x_coordinate == dest_x_coord:
            # if the destination is 'higher' on the y-axis, go one space at a time, checking if it's empty
            if dest_y_coord > cur_y_coordinate:
                temp_y = cur_y_coordinate
                while temp_y != dest_y_coord:
                    temp_y = temp_y + 1
                    x = cur_x_coordinate
                    xstr = self.convert_to_char(x)
                    y = str(temp_y)
                    coord = xstr + y
                    # if there is a piece there, only add it to the list if it's the destination
                    if self._game_board[8 - temp_y][coord] is not None:
                        if coord == dest_loc:
                            char_rook_moves.append(coord)
                        return char_rook_moves
                    # if the space is empty, add it to the list
                    char_rook_moves.append(coord)
                return char_rook_moves

            # if the destination is 'lower' on the y-axis, go one space at a time, checking if it's empty
            if dest_y_coord < cur_y_coordinate:
                temp_y = cur_y_coordinate
                while temp_y != dest_y_coord:
                    temp_y = temp_y - 1
                    x = cur_x_coordinate
                    xstr = self.convert_to_char(x)
                    y = str(temp_y)
                    coord = xstr + y
                    # if there is a piece there, only add it to the list if it's the destination
                    if self._game_board[8 - temp_y][coord] is not None:
                        if coord == dest_loc:
                            char_rook_moves.append(coord)
                        return char_rook_moves
                    # if the space is empty, add it to the list
                    char_rook_moves.append(coord)
                return char_rook_moves

        # if the destination is on the same x-axis as the current location
        if cur_y_coordinate == dest_y_coord:
            # if the destination is 'higher' (to the right) on the x-axis, go one space at a time & check if it's empty
            if dest_x_coord > cur_x_coordinate:
                temp_x = cur_x_coordinate
                while temp_x != dest_x_coord:
                    temp_x = temp_x + 1
                    y = cur_y_coordinate
                    ystr = str(y)
                    x = self.convert_to_char(temp_x)
                    coord = x + ystr
                    # if there is a piece there, only add it to the list if it's the destination
                    if self._game_board[8 - cur_y_coordinate][coord] is not None:
                        if coord == dest_loc:
                            char_rook_moves.append(coord)
                        return char_rook_moves
                    # if the space is empty, add it to the list
                    char_rook_moves.append(coord)
                return char_rook_moves

        # if the destination is 'lower' (to the left) on the x-axis, go one space at a time & check if it's empty
        if cur_y_coordinate == dest_y_coord:
            if dest_x_coord < cur_x_coordinate:
                temp_x = cur_x_coordinate
                while temp_x != dest_x_coord:
                    temp_x = temp_x - 1
                    y = cur_y_coordinate
                    ystr = str(y)
                    x = self.convert_to_char(temp_x)
                    coord = x + ystr
                    # if there is a piece there, only add it to the list if it's the destination
                    if self._game_board[8 - cur_y_coordinate][coord] is not None:
                        if coord == dest_loc:
                            char_rook_moves.append(coord)
                        return char_rook_moves
                    # if the space is empty, add it to the list
                    char_rook_moves.append(coord)

                return char_rook_moves

    @staticmethod
    def convert_to_num(letter):
        """helper function to convert 'a' to 1, 'b' to 2, 'c' to 3, etc. Takes a parameter of a lowercase character &
        returns the corresponding integer"""
        if letter == 'a':
            return 1
        if letter == 'b':
            return 2
        if letter == 'c':
            return 3
        if letter == 'd':
            return 4
        if letter == 'e':
            return 5
        if letter == 'f':
            return 6
        if letter == 'g':
            return 7
        if letter == 'h':
            return 8

    @staticmethod
    def convert_to_char(number):
        """helper function to convert 1 to 'a', 2 to 'b', etc. Takes a parameter of an integer 1-8 & returns the
        corresponding character"""
        if number == 1:
            return 'a'
        if number == 2:
            return 'b'
        if number == 3:
            return 'c'
        if number == 4:
            return 'd'
        if number == 5:
            return 'e'
        if number == 6:
            return 'f'
        if number == 7:
            return 'g'
        if number == 8:
            return 'h'

    def next_turn(self):
        """swaps which player's turn it is. Takes no parameters and returns nothing"""
        if self._whose_turn == 'white':
            self._whose_turn = 'black'
            return
        if self._whose_turn == 'black':
            self._whose_turn = 'white'
            return

    def check_for_win(self):
        """check to see if the game state needs to be updated. If a value in either _captured_by_white or
        _captured_by_black is 0, update the game state. Takes no parameters and returns nothing"""
        for item in self._captured_by_white:
            if self._captured_by_white[item] == 0:
                self.set_game_state("WHITE_WON")
                return
        for item in self._captured_by_black:
            if self._captured_by_black[item] == 0:
                self.set_game_state("BLACK_WON")

    def print_board(self):
        """Prints the game board to assist with visualizing where the pieces are. Takes no parameters and
         returns nothing"""
        for row in self._game_board:
            for key in row:
                if row[key] is None:
                    print(f"[--]", end=" ")
                # print the first two letters of the piece name when printing
                elif row[key].get_color() == 'white':
                    print(f"[" + row[key].get_piece_type()[:2] + "]", end=" ")
                # capitalize the black pieces when printing
                elif row[key].get_color() == 'black':
                    print(f"[" + row[key].get_piece_type()[:2].upper() + "]", end=" ")
            print("\n")


class ChessPiece:
    """Represents a game piece within a game of chess. Has parameters of "piece_type" (e.g. rook), "color" (white or
    black), and "location" (e.g. a1) to help facilitate the game. Contains methods to check the piece's type,
    color, and location. Also contains a method to update the piece's location. Has additional classes which inherit
    from it (Pawn, Rook, Bishop, Knight, Queen, King)."""

    def __init__(self, piece_type, color, location):
        self._x_location = location[0]
        self._y_location = location[1]
        self._color = color
        self._piece_type = piece_type

    def get_color(self):
        """Get method for piece's color"""
        return self._color

    def get_piece_type(self):
        """Get method for the piece's type"""
        return self._piece_type

    def set_location(self, new_loc):
        """set method for the piece's location. Takes parameter of the new location"""
        self._x_location = new_loc[0]
        self._y_location = new_loc[1]

    def get_location(self):
        """Get method for the piece's location"""
        return self._x_location + self._y_location


class Pawn(ChessPiece):
    """represents a pawn piece for a game of chess. Inherits from ChessPiece. Has an additional data member- _has_moved,
    which tracks whether the Pawn has moved yet. Contains get & set methods for this data member"""

    def __init__(self, piece_type, color, location):
        super().__init__(piece_type, color, location)
        self._has_moved = False

    def get_has_moved(self):
        """get method which returns whether the Pawn as moved yet or not"""
        return self._has_moved

    def set_has_moved(self):
        """set method which updates has_moved to True once the Pawn has moved once"""
        self._has_moved = True


class Rook(ChessPiece):
    """represents a Rook piece for a game of chess. Inherits from ChessPiece."""

    def __init__(self, piece_type, color, location):
        super().__init__(piece_type, color, location)


class Bishop(ChessPiece):
    """represents a Bishop piece for a game of chess. Inherits from ChessPiece."""

    def __init__(self, piece_type, color, location):
        super().__init__(piece_type, color, location)


class Knight(ChessPiece):
    """represents a Knight piece for a game of chess. Inherits from ChessPiece."""

    def __init__(self, piece_type, color, location):
        super().__init__(piece_type, color, location)


class Queen(ChessPiece):
    """represents a Queen piece for a game of chess. Inherits from ChessPiece."""

    def __init__(self, piece_type, color, location):
        super().__init__(piece_type, color, location)


class King(ChessPiece):
    """represents a King piece for a game of chess. Inherits from ChessPiece."""

    def __init__(self, piece_type, color, location):
        super().__init__(piece_type, color, location)


def main():
    """Holds the code to be executed as script"""
    board = ChessVar()
    board.make_move("a2", "a3")
    board.make_move("c7", "c5")
    board.print_board()


if __name__ == '__main__':
    """Runs the main function as a script"""
    main()

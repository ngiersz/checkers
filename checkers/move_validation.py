import checkers.board_recognition as br
import checkers.constanst as const
import checkers.Field as enums


class Position:
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def to_str(self):
        return self.x, self.y


class PieceCounter:
    Previous = 0
    Current = 0
    Previous_black = 0
    Previous_white = 0
    Current_black = 0
    Current_white = 0

    def __init__(self, previous_counter, current_counter,  previous_black, previous_white, current_black, current_white):
        self.Previous = previous_counter
        self.Current = current_counter
        self.Previous_black = previous_black
        self.Previous_white = previous_white
        self.Current_black = current_black
        self.Current_white = current_white


class MoveValidation:
    Differences = []
    Previous = []
    Current = []
    ErrorMessage = ''
    SuccessMessage = ''

    def compare_boards(self, previous, current):
        self.Differences = []
        for i in range(const.SIZE):
            for j in range(const.SIZE):
                if previous[i][j] != current[i][j]:
                    self.Differences = self.Differences + [[i, j]]
        self.Previous = previous
        self.Current = current
        self.SuccessMessage = ''
        self.ErrorMessage = ''

    def count_pieces(self):
        counter_previous = 0
        counter_current = 0
        counter_previous_white = 0
        counter_previous_black = 0
        counter_current_white = 0
        counter_current_black = 0
        for i in range(const.SIZE):
            for j in range(const.SIZE):
                if self.Previous[i][j] != enums.Field.BLACK and self.Previous[i][j] != enums.Field.WHITE:
                    counter_previous += 1
                    if self.Previous[i][j] == enums.Field.BLACK_FIELD_BLUE_PAWN:
                        counter_previous_white += 1
                    else:
                        counter_previous_black += 1
                if self.Current[i][j] != enums.Field.BLACK and self.Current[i][j] != enums.Field.WHITE:
                    counter_current += 1
                    if self.Current[i][j] == enums.Field.BLACK_FIELD_BLUE_PAWN:
                        counter_current_white += 1
                    else:
                        counter_current_black += 1

        return PieceCounter(counter_previous, counter_current, counter_previous_black, counter_previous_white,
                            counter_current_black, counter_current_white)

    def validate_normal_move(self, player):
        pieces_counter = self.count_pieces()
        if pieces_counter.Current != pieces_counter.Previous:
            self.ErrorMessage = 'Counter raised error - after normal move there should be no change in piece counter'
            # normal move doesnt remove any piece
            return False, player

        x1 = self.Differences[0][0]
        y1 = self.Differences[0][1]
        x2 = self.Differences[1][0]
        y2 = self.Differences[1][1]
        white_move = False
        black_move = False
        move_from = Position()
        move_to = Position()
        if self.Current[x1][y1] != enums.Field.BLACK:
            move_from = Position(x2, y2)
            move_to = Position(x1, y1)
        else:
            move_from = Position(x1, y1)
            move_to = Position(x2, y2)
        if self.Previous[move_from.x][move_from.y] == enums.Field.BLACK_FIELD_BLUE_PAWN or self.Previous[move_from.x][move_from.y] == enums.Field.BLACK_FIELD_BLUE_QUEEN:
            white_move = True
        else:
            black_move = True

        if white_move:
            if player == enums.Player.BLACK:
                self.ErrorMessage = 'Its red turn now! Blue cannot move'
                return False, player
        else:
            if player == enums.Player.WHITE:
                self.ErrorMessage = 'Its blue turn now! Red cannot move'
                return False, player

        if self.Current[move_to.x][move_to.y] != self.Previous[move_from.x][move_from.y]:
            self.ErrorMessage = 'move finished with wrong color of pawn (how did you do that? ' \
                                'Is that you Willy the Whistler?)'
            return False, player

        queen_move = self.Current[move_to.x][move_to.y] == enums.Field.BLACK_FIELD_BLUE_QUEEN or \
                     self.Current[move_to.x][move_to.y] == enums.Field.BLACK_FIELD_RED_QUEEN

        if queen_move:
            if abs(move_from.x - move_to.x) != abs(move_from.y - move_to.y):
                self.ErrorMessage = 'Queen must move on diagonal - you tried from ', \
                                    move_from.to_str(), ' to ', move_to.to_str()
                return False, player

            pieces_between_coords = self.count_pieces_on_diagonal_between(move_from, move_to)
            if pieces_between_coords != 0:
                self.ErrorMessage = 'There was at least one pawn or queen on queens way - ' \
                                    'its not capture because no pawn disappeared'
                return False, player

            if white_move:
                return True, enums.Player.BLACK
            else:
                return True, enums.Player.WHITE

        if white_move:
            if move_from.x - move_to.x != 1:
                self.ErrorMessage = 'illegal blue move (vertical)'
                return False, player
            if move_from.y - move_to.y != 1 and move_from.y - move_to.y != -1:
                self.ErrorMessage = 'illegal red move (horizontal)'
                return False, player
            self.SuccessMessage = 'Normal move succeeded for blue'
            return True, enums.Player.BLACK

        elif black_move:
            if move_from.x - move_to.x != -1:
                self.ErrorMessage = 'illegal red move (vertical)'
                return False, player
            if move_from.y - move_to.y != 1 and move_from.y - move_to.y != -1:
                self.ErrorMessage = 'illegal red move (horizontal)'
                return False, player
            self.SuccessMessage = 'Normal move succeeded for red'
            return True, enums.Player.WHITE

        else:
            self.ErrorMessage = 'Nobody moved?'
            return False, player

    # color is type of Player.White, Player.Black or None (that means counting both colors)
    def count_pieces_on_diagonal_between(self, move_from, move_to, color=None):
        fields_between_move_coords = []
        if move_to.x > move_from.x:
            shift_x = 1
        else:
            shift_x = -1
        if move_to.y > move_from.y:
            shift_y = 1
        else:
            shift_y = -1
        actual_x = move_from.x + shift_x
        actual_y = move_from.y + shift_y
        while actual_x != move_to.x and actual_y != move_to.y:
            fields_between_move_coords.append(Position(actual_x, actual_y))
            actual_x += shift_x
            actual_y += shift_y
        count_pieces = 0
        for coords in fields_between_move_coords:
            if color == enums.Player.WHITE or color is None:
                if self.Previous[coords.x][coords.y] == enums.Field.BLACK_FIELD_BLUE_PAWN or self.Previous[coords.x][coords.y] == enums.Field.BLACK_FIELD_BLUE_QUEEN:
                    count_pieces += 1
            if color == enums.Player.BLACK or color is None:
                if self.Previous[coords.x][coords.y] == enums.Field.BLACK_FIELD_RED_PAWN or self.Previous[coords.x][coords.y] == enums.Field.BLACK_FIELD_RED_QUEEN:
                    count_pieces += 1
        return count_pieces

    @staticmethod
    def is_a_white_figure(figure):
        return figure == enums.Field.BLACK_FIELD_BLUE_QUEEN or figure == enums.Field.BLACK_FIELD_BLUE_PAWN

    @staticmethod
    def is_a_black_figure(figure):
        return figure == enums.Field.BLACK_FIELD_RED_QUEEN or figure == enums.Field.BLACK_FIELD_RED_PAWN

    def validate_capture_move(self, player):
        pieces_counter = self.count_pieces()
        if pieces_counter.Previous - pieces_counter.Current != 1:
            self.ErrorMessage = 'Counter raised error - after capture there should be one pawn less in counter'
            # capturing removes one peace from the board
            return False, player

        x1 = self.Differences[0][0]
        y1 = self.Differences[0][1]
        x2 = self.Differences[1][0]
        y2 = self.Differences[1][1]
        x3 = self.Differences[2][0]
        y3 = self.Differences[2][1]

        move_from = Position()
        captured_pawn = Position()
        move_to = Position()

        if self.Previous[x1][y1] == enums.Field.BLACK and self.Current[x1][y1] != enums.Field.BLACK:
            move_to = Position(x1, y1)
        elif self.Previous[x2][y2] == enums.Field.BLACK and self.Current[x2][y2] != enums.Field.BLACK:
            move_to = Position(x2, y2)
        elif self.Previous[x3][y3] == enums.Field.BLACK and self.Current[x3][y3] != enums.Field.BLACK:
            move_to = Position(x3, y3)
        else:
            self.ErrorMessage = 'After capture there should be pawn in place that was not occupied before'
            return False, player

        if self.is_a_black_figure(self.Current[move_to.x][move_to.y]):
            if self.is_a_white_figure(self.Previous[x1][y1]) and self.Current[x1][y1] == enums.Field.BLACK:
                captured_pawn = Position(x1, y1)
            elif self.is_a_white_figure(self.Previous[x2][y2]) and self.Current[x2][y2] == enums.Field.BLACK:
                captured_pawn = Position(x2, y2)
            elif self.is_a_white_figure(self.Previous[x3][y3]) and self.Current[x3][y3] == enums.Field.BLACK:
                captured_pawn = Position(x3, y3)
            else:
                self.ErrorMessage = 'If red captured, there must be field where blue disappeared'
                return False, player
        elif self.is_a_white_figure(self.Current[move_to.x][move_to.y]):
            if self.is_a_black_figure(self.Previous[x1][y1]) and self.Current[x1][y1] == enums.Field.BLACK:
                captured_pawn = Position(x1, y1)
            elif self.is_a_black_figure(self.Previous[x2][y2]) and self.Current[x2][y2] == enums.Field.BLACK:
                captured_pawn = Position(x2, y2)
            elif self.is_a_black_figure(self.Previous[x3][y3]) and self.Current[x3][y3] == enums.Field.BLACK:
                captured_pawn = Position(x3, y3)
            else:
                self.ErrorMessage = 'If blue captured, there must be field where red disappeared'
                return False, player
        else:
            self.ErrorMessage = 'If capturing pawn was not red and neither blue, then we have serious shit going on'
            return False, player

        if self.is_a_white_figure(self.Current[move_to.x][move_to.y]):
            if self.is_a_white_figure(self.Previous[x1][y1]) and self.Current[x1][y1] == enums.Field.BLACK:
                move_from = Position(x1, y1)
            elif self.is_a_white_figure(self.Previous[x2][y2]) and self.Current[x2][y2] == enums.Field.BLACK:
                move_from = Position(x2, y2)
            elif self.is_a_white_figure(self.Previous[x3][y3]) and self.Current[x3][y3] == enums.Field.BLACK:
                move_from = Position(x3, y3)
            else:
                self.ErrorMessage = 'If red was capturing there should be filed with missing red'
                return False, player
        elif self.is_a_black_figure(self.Current[move_to.x][move_to.y]):
            if self.is_a_black_figure(self.Previous[x1][y1]) and self.Current[x1][y1] == enums.Field.BLACK:
                move_from = Position(x1, y1)
            elif self.is_a_black_figure(self.Previous[x2][y2]) and self.Current[x2][y2] == enums.Field.BLACK:
                move_from = Position(x2, y2)
            elif self.is_a_black_figure(self.Previous[x3][y3]) and self.Current[x3][y3] == enums.Field.BLACK:
                move_from = Position(x3, y3)
            else:
                self.ErrorMessage = 'If blue was capturing there should be filed with missing blue'
                return False, player

        if self.is_a_black_figure(self.Current[move_to.x][move_to.y]):
            # accepted moves will be: BLACK, BLACK_CAPTURE, WHITE_CAPTURE (white can blunder and miss capture - its his fault
            if player == enums.Player.WHITE:
                self.ErrorMessage = 'Its whites move!'
                return False, player
        else:
            # accepted moves will be: WHITE, WHITE_CAPTURE, BLACK_CAPTURE (black can blunder and miss capture - its his fault
            if player == enums.Player.BLACK:
                self.ErrorMessage = 'Its reds move!'
                return False, player
        if self.Current[move_to.x][move_to.y] == enums.Field.BLACK_FIELD_RED_PAWN:
            # blacks move
            if player == enums.Player.BLACK_CAPTURE:
                # capturing behind possible
                if move_from.x - move_to.x != 2 and move_from.x - move_to.x != -2:
                    self.ErrorMessage = 'Illegal capture red'
                    return False, player
            else:
                if move_from.x - move_to.x != -2:
                    self.ErrorMessage = 'Illegal capture red'
                    return False, player
            if move_from.y - move_to.y != 2 and move_from.y - move_to.y != -2:
                self.ErrorMessage = 'Illegal move - too width'
                return False, player
            if move_from.x - captured_pawn.x != -1:
                self.ErrorMessage = 'Capturing illegal pawn (vertical)'
                return False, player
            if move_from.y - captured_pawn.y != 1 and move_from.y - captured_pawn.y != -1:
                self.ErrorMessage = 'Capturing illegal pawn (horizontal)'
                return False. player
            self.SuccessMessage = 'Successful capture'
            if self.there_is_possible_capture(move_to):
                return True, enums.Player.BLACK_CAPTURE
            else:
                return True, enums.Player.WHITE

        elif self.Current[move_to.x][move_to.y] == enums.Field.BLACK_FIELD_BLUE_PAWN:
            # whites move
            if player == enums.Player.WHITE_CAPTURE:
                # capturing behind possible
                if move_from.x - move_to.x != 2 and move_from.x - move_to.x != -2:
                    self.ErrorMessage = 'Illegal capture blue'
                    return False, player
            else:
                if move_from.x - move_to.x != 2:
                    self.ErrorMessage = 'Illegal capture blue'
                    return False, player
            if move_from.y - move_to.y != 2 and move_from.y - move_to.y != -2:
                self.ErrorMessage = 'Illegal move - too width'
                return False, player
            if move_from.x - captured_pawn.x != 1:
                self.ErrorMessage = 'Capturing illegal pawn'
                return False, player
            if move_from.y - captured_pawn.y != 1 and move_from.y - captured_pawn.y != -1:
                self.ErrorMessage = 'Capturing illegal pawn (horizontal)'
                return False, player
            self.SuccessMessage = 'Successful capture'
            if self.there_is_possible_capture(move_to):
                return True, enums.Player.WHITE_CAPTURE
            else:
                return True, enums.Player.BLACK
        elif self.Current[move_to.x][move_to.y] == enums.Field.BLACK_FIELD_RED_QUEEN:
            # black queen move
            if abs(move_from.x - move_to.x) != abs(move_from.y - move_to.y):
                self.ErrorMessage = 'Moved not on diagonal'
                return False, player
            if self.count_pieces_on_diagonal_between(move_from, move_to, enums.Player.WHITE) != 1:
                self.ErrorMessage = 'Captured 0 or more than 1 pawn by red'
                return False, player
            if self.count_pieces_on_diagonal_between(move_from, move_to) != 1:
                self.ErrorMessage = 'Capturing something else than blue piece?'
                return False, player
            if abs(move_to.x - captured_pawn.x) != 1:
                self.ErrorMessage = 'Did not move 1 field behind the captured pawn (vertical)'
                return False, player
            if abs(move_to.y - captured_pawn.y) != 1:
                self.ErrorMessage = 'Did not move 1 field behind the captured pawn (horizontal)'
                return False, player
            # TODO possible capture with queen!
            if self.there_is_possible_capture(move_to):
                return True, enums.Player.BLACK_CAPTURE
            else:
                return True, enums.Player.WHITE
        elif self.Current[move_to.x][move_to.y] == enums.Field.BLACK_FIELD_BLUE_QUEEN:
            # white queen move
            if abs(move_from.x - move_to.x) != abs(move_from.y - move_to.y):
                self.ErrorMessage = 'Moved not on diagonal'
                return False, player
            if self.count_pieces_on_diagonal_between(move_from, move_to, enums.Player.BLACK) != 1:
                self.ErrorMessage = 'Captured 0 or more than 1 pawn by blue'
                return False, player
            if self.count_pieces_on_diagonal_between(move_from, move_to) != 1:
                self.ErrorMessage = 'Capturing something else than black piece?'
                return False, player
            if abs(move_to.x - captured_pawn.x) != 1:
                self.ErrorMessage = 'Did not move 1 field behind the captured pawn (vertical)'
                return False, player
            if abs(move_to.y - captured_pawn.y) != 1:
                self.ErrorMessage = 'Did not move 1 field behind the captured pawn (horizontal)'
                return False, player
            # TODO possible capture with queen!
            if self.there_is_possible_capture(move_to):
                return True, enums.Player.WHITE_CAPTURE
            else:
                return True, enums.Player.BLACK
        else:
            self.ErrorMessage = 'No one moved? Weirdo'
            return False, player

    def there_is_possible_capture(self, move_to):
        capturing_pawn_color = self.Current[move_to.x][move_to.y]
        if capturing_pawn_color == enums.Field.BLACK_FIELD_RED_PAWN:
            pawn_to_capture_color = enums.Field.BLACK_FIELD_BLUE_PAWN
        else:
            pawn_to_capture_color = enums.Field.BLACK_FIELD_RED_PAWN

        x = move_to.x
        y = move_to.y

        if x > 1 and y > 1 and self.Current[x - 1][y - 1] == pawn_to_capture_color:
            if self.Current[x - 2][y - 2] == enums.Field.BLACK:
                return True
        if x > 1 and y < const.SIZE - 2 and self.Current[x - 1][y + 1] == pawn_to_capture_color:
            if self.Current[x - 2][y + 2] == enums.Field.BLACK:
                return True
        if x < const.SIZE - 2 and y > 1 and self.Current[x + 1][y - 1] == pawn_to_capture_color:
            if self.Current[x + 2][y - 2] == enums.Field.BLACK:
                return True
        if x < const.SIZE - 2 and y < const.SIZE - 2 and self.Current[x + 1][y + 1] == pawn_to_capture_color:
            if self.Current[x + 2][y + 2] == enums.Field.BLACK:
                return True

        return False

    def validate_pawn_promotion(self, player):
        x = self.Differences[0][0]
        y = self.Differences[0][1]
        if self.Previous[x][y] == enums.Field.BLACK_FIELD_BLUE_PAWN and self.Current[x][y] == enums.Field.BLACK_FIELD_BLUE_QUEEN and x == 0:
            return True, player
        if self.Previous[x][y] == enums.Field.BLACK_FIELD_RED_PAWN and self.Current[x][y] == enums.Field.BLACK_FIELD_RED_QUEEN and x == 7:
            return True, player
        self.ErrorMessage = 'One difference on board and not a pawn promotion'
        return False, player

    def validate_move(self, player):
        if len(self.Differences) == 0:
            self.SuccessMessage = 'No differences'
            return True, player
        if len(self.Differences) == 1:
            return self.validate_pawn_promotion(player)
        if len(self.Differences) < 2:
            self.ErrorMessage = 'There is not enough differences so there was no legal moves'
            return False, player
        if len(self.Differences) == 2:
            return self.validate_normal_move(player)
        if len(self.Differences) == 3:
            return self.validate_capture_move(player)
        return False, player



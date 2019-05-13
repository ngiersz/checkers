import checkers.board_recognition as br
import checkers.constanst as const


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

    def count_pieces(self):
        counter_previous = 0
        counter_current = 0
        counter_previous_white = 0
        counter_previous_black = 0
        counter_current_white = 0
        counter_current_black = 0
        for i in range(const.SIZE):
            for j in range(const.SIZE):
                if self.Previous[i][j] != br.Field.BLACK and self.Previous[i][j] != br.Field.WHITE:
                    counter_previous += 1
                    if self.Previous[i][j] == br.Field.BLACK_WITH_WHITE:
                        counter_previous_white += 1
                    else:
                        counter_previous_black += 1
                if self.Current[i][j] != br.Field.BLACK and self.Current[i][j] != br.Field.WHITE:
                    counter_current += 1
                    if self.Current[i][j] == br.Field.BLACK_WITH_WHITE:
                        counter_current_white += 1
                    else:
                        counter_current_black += 1

        return PieceCounter(counter_previous, counter_current, counter_previous_black, counter_previous_white,
                            counter_current_black, counter_current_white)

    def validate_normal_move(self):
        pieces_counter = self.count_pieces()
        if pieces_counter.Current != pieces_counter.Previous:
            self.ErrorMessage = 'Counter raised error - after normal move there should be no change in piece counter'
            # normal move doesnt remove any piece
            return False

        x1 = self.Differences[0][0]
        y1 = self.Differences[0][1]
        x2 = self.Differences[1][0]
        y2 = self.Differences[1][1]
        white_move = False
        black_move = False
        move_from = Position()
        move_to = Position()
        if self.Current[x1][y1] == br.Field.BLACK_WITH_WHITE or self.Current[x1][y1] == br.Field.BLACK_WITH_BLACK:
            move_from = Position(x2, y2)
            move_to = Position(x1, y1)
        else:
            move_from = Position(x1, y1)
            move_to = Position(x2, y2)
        if self.Previous[move_from.x][move_from.y] == br.Field.BLACK_WITH_WHITE:
            white_move = True
        else:
            black_move = True

        if self.Current[move_to.x][move_to.y] != self.Previous[move_from.x][move_from.y]:
            self.ErrorMessage = 'move finished with wrong color of pawn (how did you do that? ' \
                                'Is that you Willy the Whistler?)'
            return False

        if white_move:
            if move_from.x - move_to.x != 1:
                self.ErrorMessage = 'illegal white move (vertical)'
                return False
            if move_from.y - move_to.y != 1 and move_from.y - move_to.y != -1:
                self.ErrorMessage = 'illegal black move (horizontal)'
                return False
            return True

        elif black_move:
            if move_from.x - move_to.x != -1:
                self.ErrorMessage = 'illegal black move (vertical)'
                return False
            if move_from.y - move_to.y != 1 and move_from.y - move_to.y != -1:
                self.ErrorMessage = 'illegal black move (horizontal)'
                return False
            return True

        else:
            self.ErrorMessage = 'Nobody moved?'
            return False

    def validate_capture_move(self):
        pieces_counter = self.count_pieces()
        if pieces_counter.Previous - pieces_counter.Current != 1:
            self.ErrorMessage = 'Counter raised error - after capture there should be one pawn less in counter'
            # capturing removes one peace from the board
            return False

        x1 = self.Differences[0][0]
        y1 = self.Differences[0][1]
        x2 = self.Differences[1][0]
        y2 = self.Differences[1][1]
        x3 = self.Differences[2][0]
        y3 = self.Differences[2][1]

        move_from = Position()
        captured_pawn = Position()
        move_to = Position()

        if self.Previous[x1][y1] == br.Field.BLACK and self.Current[x1][y1] != br.Field.BLACK:
            move_to = Position(x1, y1)
        elif self.Previous[x2][y2] == br.Field.BLACK and self.Current[x2][y2] != br.Field.BLACK:
            move_to = Position(x2, y2)
        elif self.Previous[x3][y3] == br.Field.BLACK and self.Current[x3][y3] != br.Field.BLACK:
            move_to = Position(x3, y3)
        else:
            self.ErrorMessage = 'After capture there should be pawn in place that was not occupied before'
            return False

        if self.Current[move_to.x][move_to.y] == br.Field.BLACK_WITH_BLACK:
            if self.Previous[x1][y1] == br.Field.BLACK_WITH_WHITE and self.Current[x1][y1] == br.Field.BLACK:
                captured_pawn = Position(x1, y1)
            elif self.Previous[x2][y2] == br.Field.BLACK_WITH_WHITE and self.Current[x2][y2] == br.Field.BLACK:
                captured_pawn = Position(x2, y2)
            elif self.Previous[x3][y3] == br.Field.BLACK_WITH_WHITE and self.Current[x3][y3] == br.Field.BLACK:
                captured_pawn = Position(x3, y3)
            else:
                self.ErrorMessage = 'If black captured, there must be field where white disappeared'
                return False
        elif self.Current[move_to.x][move_to.y] == br.Field.BLACK_WITH_WHITE:
            if self.Previous[x1][y1] == br.Field.BLACK_WITH_BLACK and self.Current[x1][y1] == br.Field.BLACK:
                captured_pawn = Position(x1, y1)
            elif self.Previous[x2][y2] == br.Field.BLACK_WITH_BLACK and self.Current[x2][y2] == br.Field.BLACK:
                captured_pawn = Position(x2, y2)
            elif self.Previous[x3][y3] == br.Field.BLACK_WITH_BLACK and self.Current[x3][y3] == br.Field.BLACK:
                captured_pawn = Position(x3, y3)
            else:
                self.ErrorMessage = 'If white captured, there must be field where black disappeared'
                return False
        else:
            self.ErrorMessage = 'If capturing pawn was not black and neither white, then we have serious shit going on'
            return False

        if self.Current[move_to.x][move_to.y] == br.Field.BLACK_WITH_BLACK:
            if self.Previous[x1][y1] == br.Field.BLACK_WITH_BLACK and self.Current[x1][y1] == br.Field.BLACK:
                move_from = Position(x1, y1)
            elif self.Previous[x2][y2] == br.Field.BLACK_WITH_BLACK and self.Current[x2][y2] == br.Field.BLACK:
                move_from = Position(x2, y2)
            elif self.Previous[x3][y3] == br.Field.BLACK_WITH_BLACK and self.Current[x3][y3] == br.Field.BLACK:
                move_from = Position(x3, y3)
            else:
                self.ErrorMessage = 'If black was capturing there should be filed with missing black'
                return False
        elif self.Current[move_to.x][move_to.y] == br.Field.BLACK_WITH_WHITE:
            if self.Previous[x1][y1] == br.Field.BLACK_WITH_WHITE and self.Current[x1][y1] == br.Field.BLACK:
                move_from = Position(x1, y1)
            elif self.Previous[x2][y2] == br.Field.BLACK_WITH_WHITE and self.Current[x2][y2] == br.Field.BLACK:
                move_from = Position(x2, y2)
            elif self.Previous[x3][y3] == br.Field.BLACK_WITH_WHITE and self.Current[x3][y3] == br.Field.BLACK:
                move_from = Position(x3, y3)
            else:
                self.ErrorMessage = 'If white was capturing there should be filed with missing white'
                return False
        #print('Move to: ', move_to.to_str(),  ' move from:', move_from.to_str(), 'captured: ', captured_pawn.to_str())

        if self.Current[move_to.x][move_to.y] == br.Field.BLACK_WITH_BLACK:
            #blacks move
            if move_from.x - move_to.x != -2:
                self.ErrorMessage = 'Illegal capture black'
                return False
            if move_from.y - move_to.y != 2 and move_from.y - move_to.y != -2:
                self.ErrorMessage = 'Illegal move - too width'
                return False
            if move_from.x - captured_pawn.x != -1:
                self.ErrorMessage = 'Capturing illegal pawn (vertical)'
                return False
            if move_from.y - captured_pawn.y != 1 and move_from.y - captured_pawn.y != -1:
                self.ErrorMessage = 'Capturing illegal pawn (horizontal)'
                return False

        elif self.Current[move_to.x][move_to.y] == br.Field.BLACK_WITH_WHITE:
            #whites move
            if move_from.x - move_to.x != 2:
                self.ErrorMessage = 'Illegal capture white'
                return False
            if move_from.y - move_to.y != 2 and move_from.y - move_to.y != -2:
                self.ErrorMessage = 'Illegal move - too width'
                return False
            if move_from.x - captured_pawn.x != 1:
                self.ErrorMessage = 'Capturing illegal pawn'
                return False
            if move_from.y - captured_pawn.y != 1 and move_from.y - captured_pawn.y != -1:
                self.ErrorMessage = 'Capturing illegal pawn (horizontal)'
                return False
        else:
            self.ErrorMessage = 'No one moved? Weirdo'
            return False

        self.SuccessMessage = 'Successful capture'
        return True

    def validate_move(self):
        # normal move
        if sum(row.count(br.Field.WHITE) for row in self.Current) != 32:
            self.ErrorMessage = 'Some white fields are occupied on current state'
            return False
        if sum(row.count(br.Field.WHITE) for row in self.Previous) != 32:
            self.ErrorMessage = 'Some white fields are occupied on previous state'
            return False
        if len(self.Differences) < 2:
            self.ErrorMessage = 'There is not enough differences so there was no legal moves'
            return False
        if len(self.Differences) == 2:
            return self.validate_normal_move()
        if len(self.Differences) == 3:
            return self.validate_capture_move()


mV = MoveValidation()

mV.compare_boards(const.TEST_BOARD_9, const.TEST_BOARD_10)
print(mV.Differences, mV.validate_move(), mV.SuccessMessage if mV.validate_move() else mV.ErrorMessage)

# mV.compare_boards(const.TEST_BOARD_1, const.TEST_BOARD_2)
# print(mV.Differences, mV.validate_move())
#
# mV.compare_boards(const.TEST_BOARD_3, const.TEST_BOARD_4)
# print(mV.Differences, mV.validate_move())
#
# mV.compare_boards(const.TEST_BOARD_5, const.TEST_BOARD_6)
# print(mV.Differences, mV.validate_move())
#
# mV.compare_boards(const.TEST_BOARD_7, const.TEST_BOARD_8)
# print(mV.Differences, mV.validate_move())

#pieceCounter = mV.count_pieces()
#print(pieceCounter.Previous, pieceCounter.Current, pieceCounter.Previous_white, pieceCounter.Previous_black, pieceCounter.Current_white, pieceCounter.Current_black)



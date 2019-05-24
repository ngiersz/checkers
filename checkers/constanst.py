import checkers.board_recognition as br

SIZE = 8

BLANK_BOARD = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

# black move from C2 to B3 - correct

TEST_BOARD_1 = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK_WITH_WHITE, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

TEST_BOARD_2 = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK_WITH_WHITE, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

# move white from A1 to B2 - correct

TEST_BOARD_3 = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK_WITH_WHITE, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

TEST_BOARD_4 = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK_WITH_WHITE, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

# white move from A1 to B2 but B2 was black so its illegal

TEST_BOARD_5 = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK_WITH_WHITE, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

TEST_BOARD_6 = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK_WITH_WHITE, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

# black A1 to B2 - illegal

TEST_BOARD_7 = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

TEST_BOARD_8 = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK_WITH_BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

# capture by white from A1 to C3

TEST_BOARD_9 = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK_WITH_WHITE, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

TEST_BOARD_10 = [
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK_WITH_WHITE, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE],
    [br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK],
    [br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE, br.Field.BLACK, br.Field.WHITE]
        ]

import pytest
from itertools import product

# Terminological Imports
from terminological.core import gen_matrix, resize_matrix, matrix_to_string
from terminological.core import string_to_matrix, matrix_slice, INF
from terminological.core import compute_sizes, HorizontalBox, Filler, MsgLog
from terminological.core import VerticalBox, OutlineType, start, split
from terminological.core import screen_to_string, clear_screen


@pytest.mark.parametrize("string, size, expected", [
    ('1234567890', 4, ['1234', '5678', '90']),
    ('1234567890', 12, ['1234567890']),
    ('1234567890', 1, ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']),
    ('1234567890', 5, ['12345', '67890']),
    ('1234567890\n12345', 3, ['123', '456', '789', '0', '123', '45'])
])
def test_string_split(string, size, expected):
    assert split(string, size) == expected


@pytest.mark.parametrize("ir, ic, nr, nc", [
    (10, 10, 20, 20),
    (10, 10, 11, 10),
    (0, 0, 1, 0),
    (0, 0, 10, 0),
    (0, 0, 15, 1),
    (1, 1, 100, 1000),
    (100, 100, 1, 1)
] + list(product((1, 10, 15), repeat=4)))
def test_resize_matrix(ir, ic, nr, nc):
    M = gen_matrix(ir, ic)
    resize_matrix(M, nr, nc)
    assert len(M) == nr
    assert len(M[0]) == nc


@pytest.mark.parametrize("M, rs, rl, cs, cl, expected", [
    ('+++++-----\n+++++-----\n+++++-----\n+++++-----\n+++++-----\n----------\n-\
---------\n----------\n----------\n----------', 0, 5, 0, 5, '+++++\n+++++\
\n+++++\n+++++\n+++++'),
    ('--+++++---\n--+++++---\n--+++++---\n--+++++---\n--+++++---\n----------\n-\
---------\n----------\n----------\n----------', 0, 5, 2, 5, '+++++\n+++++\
\n+++++\n+++++\n+++++'),
])
def test_matrix_slice(M, rs, rl, cs, cl, expected):
    M = string_to_matrix(M)
    assert matrix_to_string(matrix_slice(M, rs, rl, cs, cl)) == expected


@pytest.mark.parametrize("dim_list, total_size, expected", [
    ([(None, 1, 0, INF),
      (None, 1, 0, INF)], 10, [(5.0, 1, 0, INF),
                               (5.0, 1, 0, INF)]),
    ([(None, 1, 0, 3),
      (None, 2, 0, 6)], 8, [(3.0, 1, 0, 3),
                            (5.0, 2, 0, 6)]),
    ([(None, 1, 0, 3),
      (None, 1, 0, 6)], 10, [(3.0, 1, 0, 3),
                             (6.0, 1, 0, 6)]),
    ([(None, 3, 0, INF),
      (None, 1, 0, INF),
      (None, 1, 0, INF),
      (None, 1, 0, INF)], 12, [(6.0, 3, 0, INF),
                               (2.0, 1, 0, INF),
                               (2.0, 1, 0, INF),
                               (2.0, 1, 0, INF)]),
    ([(None, 1, 0, INF),
      (None, 3, 0, INF),
      (None, 1, 0, INF),
      (None, 1, 0, INF)], 12, [(2.0, 1, 0, INF),
                               (6.0, 3, 0, INF),
                               (2.0, 1, 0, INF),
                               (2.0, 1, 0, INF)]),
    ([(None, 1, 0, INF),
      (None, 1, 0, INF),
      (None, 3, 0, INF),
      (None, 1, 0, INF)], 12, [(2.0, 1, 0, INF),
                               (2.0, 1, 0, INF),
                               (6.0, 3, 0, INF),
                               (2.0, 1, 0, INF)]),
    ([(None, 1, 0, INF),
      (None, 1, 0, INF),
      (None, 1, 0, INF),
      (None, 3, 0, INF)], 12, [(2.0, 1, 0, INF),
                               (2.0, 1, 0, INF),
                               (2.0, 1, 0, INF),
                               (6.0, 3, 0, INF)]),
    ([(None, 3, 9, INF),
      (None, 1, 3, INF),
      (None, 1, 0, INF),
      (None, 1, 0, INF)], 12, [(9.0, 3, 9, INF),
                               (3.0, 1, 3, INF),
                               (0.0, 1, 0, INF),
                               (0.0, 1, 0, INF)]),
    ([(None, 3, 10, INF),
      (None, 1, 3, INF),
      (None, 1, 0, INF),
      (None, 1, 0, INF)], 12, [(10.0, 3, 10, INF),
                               (3.0, 1, 3, INF),
                               (0.0, 1, 0, INF),
                               (0.0, 1, 0, INF)]),
    ([(None, 3, 7, INF),
      (None, 1, 0, INF),
      (None, 1, 0, INF),
      (None, 1, 0, INF)], 12, [(10.0, 3, 7, INF),
                               (1.0, 1, 0, INF),
                               (1.0, 1, 0, INF),
                               (0.0, 1, 0, INF)]),
])
def test_compute_sizes(dim_list, total_size, expected):
    def list_eq(A, B):
        return all(t1 == t2 for t1, t2 in zip(A, B))
    assert list_eq(compute_sizes(dim_list, total_size), expected)


@pytest.mark.parametrize("character, num_rows, num_cols, expected", [
    ('.', 2, 3, '...\n...'),
    ('+', 1, 1, '+'),
    ('*', 5, 5, '*****\n*****\n*****\n*****\n*****'),
    ('-', 0, 0, ''),
    ('R', 20, 60, '\n'.join(['R' * 60 for _ in range(20)])),
    ('L', 20, 60, '\n'.join(['L' * 60 for _ in range(20)])),
    ('L', 20, 30, '\n'.join(['L' * 30 for _ in range(20)])),
])
def test_filler(character, num_rows, num_cols, expected):
    assert Filler(character, num_rows, num_cols)


@pytest.mark.parametrize("c, num_rows, num_cols, new_rows, new_cols, e", [
    ('L', 20, 60, 20, 30, '\n'.join(['L' * 30 for _ in range(20)])),
])
def test_filler_resize(c, num_rows, num_cols, new_rows, new_cols, e):
    F = Filler(c, num_rows, num_cols)
    F.resize(new_rows, new_cols)
    assert str(F) == e


def test_basic_horizontal_box():
    B = HorizontalBox(20, 60)
    B.add_child(Filler('L')).add_child(Filler('R'))
    assert str(B) == '\n'.join(['L' * 30 + 'R' * 30 for _ in range(20)])


def test_weighted_horizontal_box():
    B = HorizontalBox(20, 50)
    B.add_child(Filler('L', weight=3))\
     .add_child(Filler('C', weight=1))\
     .add_child(Filler('R', weight=1))
    assert str(B) == '\n'.join(['L' * 30 + 'C' * 10 + 'R' * 10
                                for _ in range(20)])


def test_horizontal_base_cases():
    B = HorizontalBox(1, 10)
    B.add_child(Filler('+'))
    assert str(B) == '+' * 10
    B.resize(1, 1)
    assert str(B) == '+'
    B = HorizontalBox(0, 0)
    B.add_child(Filler('L')).add_child(Filler('R'))
    assert str(B) == ''
    B.resize(1, 0)
    assert str(B) == ''
    B.resize(1, 1)
    assert str(B) == 'L'
    B.resize(1, 50)
    assert str(B) == 'L' * 25 + 'R' * 25
    B.resize(50, 1)
    assert str(B) == 'L\n' * 49 + 'L'


def test_basic_vertical_box():
    B = VerticalBox(20, 60)
    B.add_child(Filler('T')).add_child(Filler('B'))
    assert str(B) == '\n'.join(['T' * 60 for _ in range(10)] +
                               ['B' * 60 for _ in range(10)])


def test_weighted_vertical_box():
    B = VerticalBox(50, 50)
    B.add_child(Filler('T', weight=3))\
     .add_child(Filler('C', weight=1))\
     .add_child(Filler('B', weight=1))
    assert str(B) == '\n'.join(['T' * 50 for _ in range(30)] +
                               ['C' * 50 for _ in range(10)] +
                               ['B' * 50 for _ in range(10)])


def test_vertical_base_cases():
    B = VerticalBox(1, 10)
    B.add_child(Filler('+'))
    assert str(B) == '+' * 10
    B.resize(1, 1)
    assert str(B) == '+'
    B = VerticalBox(0, 0)
    B.add_child(Filler('T')).add_child(Filler('B'))
    assert str(B) == ''
    B.resize(1, 0)
    assert str(B) == ''
    B.resize(1, 1)
    assert str(B) == 'T'
    B.resize(1, 50)
    assert str(B) == 'T' * 50
    B.resize(50, 1)
    assert str(B) == 'T\n' * 25 + 'B\n' * 24 + 'B'


def test_horizontal_and_vertical_boxes():
    H = HorizontalBox(100, 100)
    H.add_child(Filler('L'))
    H.add_child(VerticalBox().add_child(Filler('1')).add_child(Filler('2')))
    assert str(H) + '\n' == ('L' * 50 + '1' * 50 + '\n') * 50 + \
        ('L' * 50 + '2' * 50 + '\n') * 50


def test_bounded_vertical_box():
    V = VerticalBox(40, 40, outline=OutlineType.VerticalBounds)\
        .add_child(Filler('+'))
    assert str(V) == '┌' + ('─' * 38) + '┐' + '\n' + ('+' * 40 + '\n') \
        * 38 + '└' + ('─' * 38) + '┘'
    V.resize(10, 2)
    assert str(V) == '┌┐\n' + '++\n' * 8 + '└┘'
    V.resize(2, 2)
    assert str(V) == '┌┐\n' + '└┘'
    V.resize(1, 1)
    assert str(V) == '┘'
    V.resize(2, 40)
    assert str(V) == '┌──────────────────────────────────────┐\n' + \
        '└──────────────────────────────────────┘'


def test_bounded_boxed_vertical_box():
    V = VerticalBox(40, 40, outline=OutlineType.VerticalBoundBox)\
        .add_child(Filler('+'))
    assert str(V) == '┌' + ('─' * 38) + '┐' + '\n' + (' ' + '+' * 38 + ' \n') \
        * 38 + '└' + ('─' * 38) + '┘'
    V.resize(10, 2)
    assert str(V) == '┌┐\n' + '  \n' * 8 + '└┘'
    V.resize(2, 2)
    assert str(V) == '┌┐\n' + '└┘'
    V.resize(1, 1)
    assert str(V) == '┘'
    V.resize(2, 40)
    assert str(V) == '┌──────────────────────────────────────┐\n' + \
        '└──────────────────────────────────────┘'


def test_boxed_horizontal_box():
    H = HorizontalBox(100, 100, outline=OutlineType.Box).add_child(Filler('+'))
    assert str(H) == '┌' + ('─' * 98) + '┐' + '\n' + ('│' + '+' * 98 + '│\n') \
        * 98 + '└' + '─' * 98 + '┘'
    H.resize(3, 40)
    assert str(H) == '┌' + '─' * 38 + '┐\n│' + '+' * 38 + \
        '│\n└' + '─' * 38 + '┘'
    H.resize(2, 2)
    assert str(H) == '┌┐\n└┘'
    H.resize(10, 2)
    assert str(H) == '┌┐\n' + '││\n' * 8 + '└┘'
    H.resize(3, 3)
    assert str(H) == '┌─┐\n│+│\n└─┘'


def test_bounded_horizontal_box():
    H = HorizontalBox(40, 40, outline=OutlineType.HorizontalBounds)\
        .add_child(Filler('+'))
    assert str(H) == '┌' + '+' * 38 + '┐\n' + ('│' + '+' * 38 + '│\n') * 38 +\
        '└' + '+' * 38 + '┘'
    H.resize(2, 40)
    assert str(H) == '┌' + '+' * 38 + '┐\n' + '└' + '+' * 38 + '┘'
    H.resize(1, 1)
    assert str(H) == '┘'
    H.resize(2, 2)
    assert str(H) == '┌┐\n' + '└┘'
    H.resize(10, 2)
    assert str(H) == '┌┐\n' + '││\n' * 8 + '└┘'
    H.resize(10, 3)
    assert str(H) == '┌+┐\n' + '│+│\n' * 8 + '└+┘'


def test_bounded_boxed_horizontal_box():
    H = HorizontalBox(40, 40, outline=OutlineType.HorizontalBoundBox)\
        .add_child(Filler('+'))
    assert str(H) == '┌' + ' ' * 38 + '┐\n' + ('│' + '+' * 38 + '│\n') * 38 +\
        '└' + ' ' * 38 + '┘'
    H.resize(3, 40)
    assert str(H) == '┌' + ' ' * 38 + '┐\n' + ('│' + '+' * 38 + '│\n') \
        + '└' + ' ' * 38 + '┘'
    H.resize(2, 40)
    assert str(H) == '┌' + ' ' * 38 + '┐\n' + '└' + ' ' * 38 + '┘'
    H.resize(1, 1)
    assert str(H) == '┘'
    H.resize(2, 2)
    assert str(H) == '┌┐\n' + '└┘'
    H.resize(10, 2)
    assert str(H) == '┌┐\n' + '││\n' * 8 + '└┘'
    H.resize(10, 3)
    assert str(H) == '┌ ┐\n' + '│+│\n' * 8 + '└ ┘'


def test_start():
    clear_screen()
    assert screen_to_string() == ''
    H = HorizontalBox(outline=OutlineType.HorizontalBounds)\
        .add_child(VerticalBox(outline=OutlineType.VerticalBounds)
                   .add_child(Filler('L')))\
        .add_child(VerticalBox(outline=OutlineType.VerticalBounds)
                   .add_child(Filler('R')))

    def main():
        scr = screen_to_string()
        assert str(H) == scr
        clear_screen()

    start(H, main)


def test_msg_log():
    M = MsgLog(8, 4, 4)
    M.add_message('1111')
    M.add_message('2222')
    M.add_message('3333')
    M.add_message('4444')
    assert str(M) == '1111\n2222\n3333\n4444'
    M.add_message('5555')
    assert str(M) == '2222\n3333\n4444\n5555'
    M.add_message('6')
    assert str(M) == '3333\n4444\n5555\n6   '
    M.add_message('77777')
    assert str(M) == '5555\n6   \n7777\n7   '
    M = MsgLog(8, 5, 5)
    M.add_message('1111')
    M.add_message('2222')
    M.add_message('3333')
    M.add_message('4444')
    assert str(M) == '1111 \n2222 \n3333 \n4444 \n     '
    M = MsgLog(3, 5, 5)
    M.add_message('1111')
    M.add_message('2222')
    M.add_message('3333')
    M.add_message('4444')
    assert str(M) == '2222 \n3333 \n4444 \n     \n     '


def test_h_bounded_msg_log():
    M = MsgLog(8, 4, 6, outline=OutlineType.HorizontalBounds)
    M.add_message('1111')
    M.add_message('2222')
    M.add_message('3333')
    M.add_message('4444')
    assert str(M) == '┌1111┐\n│2222│\n│3333│\n└4444┘'
    M.add_message('5555')
    assert str(M) == '┌2222┐\n│3333│\n│4444│\n└5555┘'
    M.add_message('6')
    assert str(M) == '┌3333┐\n│4444│\n│5555│\n└6   ┘'
    M = MsgLog(8, 5, 7, outline=OutlineType.HorizontalBounds)
    M.add_message('1111')
    M.add_message('2222')
    M.add_message('3333')
    M.add_message('4444')
    assert str(M) == '┌1111 ┐\n│2222 │\n│3333 │\n│4444 │\n└     ┘'
    M = MsgLog(3, 5, 7, outline=OutlineType.HorizontalBounds)
    M.add_message('1111')
    M.add_message('2222')
    M.add_message('3333')
    M.add_message('4444')
    assert str(M) == '┌2222 ┐\n│3333 │\n│4444 │\n│     │\n└     ┘'


def test_v_bounded_msg_log():
    M = MsgLog(8, 6, 4, outline=OutlineType.VerticalBounds)
    M.add_message('1111')
    M.add_message('2222')
    M.add_message('3333')
    M.add_message('4444')
    assert str(M) == '┌──┐\n1111\n2222\n3333\n4444\n└──┘'
    M.add_message('5555')
    assert str(M) == '┌──┐\n2222\n3333\n4444\n5555\n└──┘'
    M.add_message('6')
    assert str(M) == '┌──┐\n3333\n4444\n5555\n6   \n└──┘'
    M = MsgLog(8, 7, 5, outline=OutlineType.VerticalBounds)
    M.add_message('1111')
    M.add_message('2222')
    M.add_message('3333')
    M.add_message('4444')
    assert str(M) == '┌───┐\n1111 \n2222 \n3333 \n4444 \n     \n└───┘'
    M = MsgLog(3, 7, 5, outline=OutlineType.VerticalBounds)
    M.add_message('1111')
    M.add_message('2222')
    M.add_message('3333')
    M.add_message('4444')
    assert str(M) == '┌───┐\n2222 \n3333 \n4444 \n     \n     \n└───┘'


def test_msg_log_rendering():
    B = HorizontalBox(outline=OutlineType.VerticalBoundBox).add_child(MsgLog())

    def main():
        log = B.children[0]
        msgs = '''
        all that is gold does not glitter \
        not all those who wander are lost \
        the old that is strong does not whither \
        deep roots are not touched by the frost

        from the ashes a fire shall be woken \
        a light from the shadow shall spring \
        renewed be the blade that was broken \
        the crownless again shall be king''' * 20
        for m in msgs.split('\n'):
            log.add_message(m)
            B.draw()
        clear_screen()

    start(B, main)

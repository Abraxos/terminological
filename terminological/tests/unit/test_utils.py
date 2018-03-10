from terminological.utils import fit_to_length

def test_fit_to_length():
    string = 'abcdefghijklmnopqrstuvwxyz'
    assert fit_to_length(string, 1) == 'a'
    assert fit_to_length(string, 1, right_cap=']') == ']'
    assert fit_to_length(string, 1, left_cap='[') == '['
    assert fit_to_length(string, 1, left_cap='[', right_cap=']') == ']'
    assert fit_to_length(string, 2, left_cap='[', right_cap=']') == '[]'
    assert fit_to_length(string, 3, left_cap='[', right_cap=']') == '[a]'
    assert fit_to_length('', 3, left_cap='[', right_cap=']') == '[ ]'
    assert fit_to_length('', 3, left_cap='[') == '[  '
    assert fit_to_length('', 3, right_cap=']') == '  ]'
    assert fit_to_length('', 3) == '   '
    assert fit_to_length('', 0) == ''
    assert fit_to_length('', -1) == ''
    assert fit_to_length(string, 4, left_cap='[', right_cap=']') == '[ab]'
    assert fit_to_length(string, 4, left_cap='[') == '[abc'
    assert fit_to_length(string, 4, right_cap=']') == 'abc]'
    assert fit_to_length(string, 4) == 'abcd'
    assert fit_to_length(string, 5, left_cap='[', right_cap=']') == '[abc]'
    assert fit_to_length(string, 5, left_cap='[') == '[abcd'
    assert fit_to_length(string, 5, right_cap=']') == 'abcd]'
    assert fit_to_length(string, 5) == 'abcde'
    assert fit_to_length(string, 6, left_cap='[', right_cap=']') == '[abcd]'
    assert fit_to_length(string, 6, left_cap='[') == '[abcde'
    assert fit_to_length(string, 6, right_cap=']') == 'abcde]'
    assert fit_to_length(string, 6) == 'abcdef'
    assert fit_to_length(string, 7, left_cap='[', right_cap=']') == '[a...z]'
    assert fit_to_length(string, 7, left_cap='[') == '[ab...z'
    assert fit_to_length(string, 7, right_cap=']') == 'ab...z]'
    assert fit_to_length(string, 7) == 'abc...z'
    assert fit_to_length(string, 30, left_cap='[', right_cap=']') == '[' + string + '  ]'
    assert fit_to_length(string, 30, left_cap='[') == '[' + string + '   '
    assert fit_to_length(string, 30, right_cap=']') == string + '   ]'
    assert fit_to_length(string, 30) == string + '    '
from terminological.widgets import StrBox
from terminological.core import OutlineType
from terminological.widgets import LabeledProgressBar


def box_top(length):
    return '┌' + ('─' * (length - 2)) + '┐' + '\n'


def box_bottom(length):
    return '└' + '─' * (length - 2) + '┘'


def test_string_box():
    box = StrBox(('+' * 200 + '\n') * 200, 100, 100, outline=OutlineType.Box)
    assert str(box) == '┌' + ('─' * 98) + '┐' + '\n' + ('│' + '+' * 98 + '│\n') \
        * 98 + '└' + '─' * 98 + '┘'
    box.resize(4, 4)
    assert str(box) == '┌' + ('─' * 2) + '┐' + '\n' + ('│' + '+' * 2 + '│\n') \
        * 2 + '└' + '─' * 2 + '┘'
    box.update(('+' * 10 + '\n') * 10)
    box.resize(20, 20)
    assert str(box) == box_top(20) + ('│' + '+' * 10 + ' ' * 8 + '│\n') * 10 \
        + ('│' + ' ' * 18 + '│\n') * 8 + box_bottom(20)
    box.resize(2, 2)
    assert str(box) == box_top(2) + box_bottom(2)

def test_labeled_progress_bar():
    progress_bar = LabeledProgressBar('stuff')
    print()
    # Make sure nothing crashes
    for i in range(111):
        progress_bar.update(percentage=i)
        progress_bar.stretch(i)
        print(str(progress_bar))
    # Test specific cases
    progress_bar.stretch(10)
    progress_bar.update(0, 'Test Progress Bar', 'Test Message')
    assert str(progress_bar) == "┌[Test P]┐\n│Test Mes│\n└[    0%]┘"
    progress_bar.update(50, 'Test Progress Bar', 'Test Message')
    assert str(progress_bar) == "┌[Test P]┐\n│Test Mes│\n└[█  50%]┘"
    progress_bar.update(100, 'Test Progress Bar', 'Test Message')
    assert str(progress_bar) == "┌[Test P]┐\n│Test Mes│\n└[██100%]┘"
    progress_bar.update(0, '', '')
    assert str(progress_bar) == "┌[]──────┐\n│        │\n└[    0%]┘"
    progress_bar.update(0, 'a', 'b')
    assert str(progress_bar) == "┌[a]─────┐\n│b       │\n└[    0%]┘"

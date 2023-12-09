from lesson2.dz2 import Card
from lesson2.dz2 import Game
import pytest


def test_card_rows():
    Card(1, 90, 3, 9, 5)


def test_card_rows_invalid_value_type():
    with pytest.raises(TypeError):
        Card(1, 90, True, 9, 5)


def test_card_rows_invalid_value():
    with pytest.raises(ValueError):
        Card(1, 90, 6, 9, 5)


def test_items_in_row():
    Card(1, 90, 3, 8, 5)


def test_items_in_row_invalid_value_type():
    with pytest.raises(TypeError):
        Card(1, 90, 3, '9', 5)


def test_items_in_row_invalid_value():
    with pytest.raises(ValueError):
        Card(1, 90, 6, -8, 5)


def test_nums_in_row():
    Card(1, 90, 3, 9, 6)


def test_nums_in_row_invalid_value_type():
    with pytest.raises(TypeError):
        Card(1, 90, 3, 9, {5})


def test_nums_in_row_invalid_value():
    with pytest.raises(ValueError):
        Card(1, 90, 3, 9, 100500)


def test_game_mode():
    Game(1, 90, 3, 9, 5, 'player and computer')


def test_game_mode_invalid_value_type():
    with pytest.raises(TypeError):
        Game(1, 90, 3, 9, 5, ['player and computer'])


def test_game_mode_invalid_value():
    with pytest.raises(ValueError):
        Game(1, 90, 3, 9, 5, 'Super player solo')


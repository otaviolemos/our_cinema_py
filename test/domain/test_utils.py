from domain.utils import convert_seat_notation_to_indices
import pytest

def test_seat_notation_without_first_letter():
    with pytest.raises(ValueError):
        convert_seat_notation_to_indices('99')

def test_seat_notation_without_row_number():
    with pytest.raises(ValueError):
        convert_seat_notation_to_indices('AA')

def test_seat_notation_negative_row_number():
    with pytest.raises(ValueError):
        convert_seat_notation_to_indices('A-1')
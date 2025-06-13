def convert_seat_notation_to_indices(seat_notation: str) -> tuple[int, int]:
    row_letter = seat_notation[0].upper()
    seat_number_str = seat_notation[1:]

    if not row_letter.isalpha():
        raise ValueError(f"Row must be a letter, got '{row_letter}'")

    try:
        seat_number = int(seat_number_str)
        if seat_number < 0:
            raise ValueError(f"Seat number must be positive.")
    except ValueError:
        raise ValueError(f"Invalid seat number: '{seat_number_str}'")

    row_index = ord(row_letter) - ord('A')
    column_index = seat_number - 1
    
    return (row_index, column_index)
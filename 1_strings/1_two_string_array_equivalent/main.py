def is_array_string_are_equal(array_string_1: list[str], array_string_2: list[str]) -> bool:
    input_string_1 = ''.join(array_string_1).upper()
    input_string_2 = ''.join(array_string_2).upper()
    return input_string_1 == input_string_2

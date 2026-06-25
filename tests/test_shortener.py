from src.shortener import ALPHABET, CODE_LENGTH, generate_unique_code


def test_generate_unique_code_length():
    code = generate_unique_code()
    assert len(code) == CODE_LENGTH


def test_generate_unique_code_alphabet():
    code = generate_unique_code()
    assert all(char in ALPHABET for char in code)


def test_generate_unique_code_is_random():
    codes = {generate_unique_code() for _ in range(20)}
    assert len(codes) == 20

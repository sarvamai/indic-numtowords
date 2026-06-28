from indic_numtowords import num2words


def test_split_accepts_int_like_str():
    # `split=True` is documented to accept an int or a numeric string; the two
    # forms of the same number must produce the same per-digit output.
    assert num2words(123, lang="hi", split=True) == num2words("123", lang="hi", split=True)


def test_split_accepts_int_for_extended_language():
    assert num2words(123, lang="mai", split=True) == num2words("123", lang="mai", split=True)

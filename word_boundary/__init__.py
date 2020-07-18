def word_boundaries(text: str):
    if not text:
        return

    # WB1
    yield 0
    # WB2
    yield len(text)

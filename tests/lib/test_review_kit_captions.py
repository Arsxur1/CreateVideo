from lib.review_kit.captions import boundaries, split_long, to_srt


def test_short_caption_is_not_split() -> None:
    assert split_long("Now the focus stays.", 1.0, 2.0, 52) == [("Now the focus stays.", 1.0, 2.0)]


def test_long_caption_splits_at_middle_punctuation_and_shares_time_by_length() -> None:
    text = "If your room is bigger, you have to increase the size, and the sharpness drops a bit."
    parts = split_long(text, 10.0, 16.0, 52)

    assert [p[0] for p in parts] == [
        "If your room is bigger,",
        "you have to increase the size,",
        "and the sharpness drops a bit.",
    ]
    assert parts[0][1] == 10.0 and parts[-1][2] == 16.0
    for (_, _, end), (_, start, _) in zip(parts, parts[1:]):
        assert end == start


def test_boundaries_snap_to_the_nearest_pause() -> None:
    # Two sentences of equal length in a 4s line: expected switch at 2.0s,
    # a real pause sits at 2.3s, so the caption switches there.
    spoken = "ஒன்று இரண்டு மூன்று. நான்கு ஐந்து ஆறு."
    assert boundaries(spoken, 2, 4.0, pauses=[0.8, 2.3]) == [2.3]


def test_boundaries_ignore_pauses_that_are_too_far() -> None:
    assert boundaries("One two three. Four five six.", 2, 4.0, pauses=[3.9]) == [2.0]


def test_boundaries_fall_back_to_even_split_when_sentence_count_differs() -> None:
    # Three caption chunks for a line with one spoken sentence: split evenly.
    assert boundaries("One long sentence", 3, 3.0, pauses=[]) == [1.0, 2.0]


def test_srt_timestamps_and_offset() -> None:
    srt = to_srt([{"text": "Hi", "start": 0.4, "end": 61.25}], offset=0.5)
    assert srt.startswith("1\n00:00:00,900 --> 00:01:01,750\nHi\n")

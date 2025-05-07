from sudachipy import Dictionary


def has_not_kana(input_text: str) -> bool:
    """Check if the input text does not have kana.

    Args:
        input_text: A string to check.

    Returns:
        bool: True if no kana is found, False otherwise.
    """
    for char in input_text:
        gana_code = ord(char)
        if 12353 <= gana_code <= 12543:
            # According to the Unicode Office Document, the Hiragana code ranges from 12353 to 12447.
            # https://www.unicode.org/charts/PDF/U3040.pdf
            # And the Katakana code ranges from 12448 to 12543.
            # https://www.unicode.org/charts/PDF/U30A0.pdf
            return False
    # If no kana characters are found, return True
    return True


def analyze_text(text) -> list:
    tokenizer = Dictionary().create()
    result_list = []
    # TODO: 移除常见的 markdown 语法和 ruby 标签
    for token in tokenizer.tokenize(text):
        # 辞書の見出しの漢字表記と Sudachi の正規化表記と違うところが多いので
        # 普段、読み方（reading_form）で検索するのをお勧めですが、
        # token.reading_form() は辞書の見出しのかな表記ではなく、
        # 表層形の読み方を返す。
        jishokei = token.normalized_form()
        result = [token.surface(), jishokei]
        result_list.append(result)
    return result_list


def get_cursor_result(analysis_result: list[str], cursor_index: int) -> str | None:
    """
    返回光标所在位置的单词的分析结果。
    Args:
        analysis_result: 光标所在上下文的所有分析结果
        cursor_index: 光标所在的上下文的索引

    Returns:
        光标所在位置的单词的分析结果，如果光标位置不在上下文中，返回 None.
    """
    if cursor_index < 0:
        raise ValueError(
            f"Cursor index must be a non-negative integer. Given index: {cursor_index}. "
            f"Analysis results: {analysis_result}"
        )

    total_length = sum(len(result[0]) for result in analysis_result)
    if cursor_index > total_length:
        # 光标所在的位置索引不可能大于所有分析结果的表层形的长度之和
        raise ValueError(
            f"Cursor index is out of range. Given index: {cursor_index}. "
            f"Analysis results: {analysis_result}"
        )

    length_before_cursor = 0
    for result in analysis_result:
        surface, jishokei = result[0], result[1]
        length_before_cursor += len(surface)
        if length_before_cursor >= cursor_index:
            # TODO = 说明用户的光标正好放在2个句节的分界处
            # 可以考虑基于难度和词频猜测哪个更有可能是用户想查的单词，
            # 或者允许按照个人习惯，设置这种情况是返回前还是后
            return jishokei

from typing import List

from sudachipy import Dictionary

from utils.kannyouku import get_kannyouku_all_words, query_kannyouku


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


def analyze_text(text: str) -> List[List[str]]:
    """
    使用 Sudachi 分析文本并返回表层形和基本形组成的列表。
    Args:
        text: 需要分析的文本

    Returns:
        包含 [surface, normalized_form] 的二维列表

    Raises:
        ValueError: 如果输入文本为空或 None

    Examples:
        >>> analyze_text("晩ご飯を食べましたか。")
        [["晩ご飯", "晩御飯"], ["を", "を"], ["食べ", "食べる"],
         ["まし", "ます"], ["た", "た"], ["か", "か"], ["。", "。"]]
    """
    if not text:
        raise ValueError("Input text cannot be empty or None")

    tokenizer = Dictionary().create()
    result_list = []
    for token in tokenizer.tokenize(text):
        # 辞書の見出しの漢字表記と Sudachi の正規化表記と違うところが多いので
        # 普段、読み方（reading_form）で検索するのをお勧めですが、
        # token.reading_form() は辞書の見出しのかな表記ではなく、
        # 表層形の読み方を返す。
        jishokei = token.normalized_form()
        result = [token.surface(), jishokei]
        result_list.append(result)
    return result_list


def get_cursor_result(
    analysis_result: List[List[str]], cursor_index: int
) -> str | None:
    """
    返回光标所在位置的单词的分析结果。
    Args:
        analysis_result: 光标所在上下文的所有分析结果
        cursor_index: 光标所在的上下文的索引值

    Returns:
        光标所在位置的单词的分析结果，如果光标位置不在上下文中，返回 None.

    Raises:
        ValueError: 如果光标索引小于 0 或大于所有分析结果的表层形的长度之和

    Examples:
        >>> result = [["晩ご飯", "晩御飯"], ["を", "を"], ["食べ", "食べる"], ["まし", "ます"], ["た", "た"], ["か", "か"], ["。", "。"]]
        >>> get_cursor_result(result, 0)
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


def analyze_for_kannyouku(text: str) -> List[List[str]]:
    """
    使用 Sudachi 分析文本并返回基本形组成的列表，用于进一步分析是否存在惯用句。
    Args:
        text: 需要分析的文本

    Returns:
        包含 [surface, normalized_form] 的二维列表

    Raises:
        ValueError: 如果输入文本为空或 None

    Examples:
        >>> analyze_for_kannyouku("うそつけ！")
        [["うそ"], ["つける"]])
    """
    if not text:
        raise ValueError("Input text cannot be empty or None")

    tokenizer = Dictionary().create()
    result_list = []
    for token in tokenizer.tokenize(text):
        # token.reading_form() は辞書の見出しのかな表記ではなく、
        # TODO result = [token.surface(), jishokei]
        result = [token.normalized_form()]
        result_list.append(result)
    return result_list


# FIXME
kannyouku_words_set = get_kannyouku_all_words()


def scan_kannyouku(text: str) -> List[set[str]] | None:
    """
    分析文本中的可能存在的惯用句。
    Args:
        text: 待分析的文本

    Returns:
        可能的汉语词汇列表

    Examples:
        >>> scan_kannyouku("ウソまでつく")
        ["うそをつく"， "嘘を吐く"]
    """
    if not text:
        return None
    analysis_results = analyze_for_kannyouku(text)
    print(f"「{text}」は {analysis_results}　に解析された")

    kannyouku_words_analysis_results = []
    for result in analysis_results:
        # 排除不可能组成惯用句的单词，主要是格助词
        for word in result:
            if word in kannyouku_words_set:
                print(f"「{result}」は惯用句の単語の候補です")
                kannyouku_words_analysis_results.append(result)
            else:
                print(f"「{word}」は惯用句の単語の候補ではない")

    print(f"{kannyouku_words_analysis_results}は可能な惯用句の単語候補です")
    kannyouku_list = []
    if len(kannyouku_words_analysis_results) > 1:
        kannyouku_list = query_kannyouku(kannyouku_words_analysis_results)
        print(
            f"「{text}」には 「{kannyouku_list}」などの慣用句が含まれている可能性があります"
        )
    else:
        print(f"「{text}」に慣用句が含まれているない")
    return kannyouku_list

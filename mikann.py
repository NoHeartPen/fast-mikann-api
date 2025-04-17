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
        if 12353 <= gana_code <= 12447 or 12448 <= gana_code <= 12543:
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
        # 普段、読み方（reading_form）で検索するのをお勧め。
        jishokei = token.reading_form()
        if has_not_kana(token.dictionary_form):
            # dictionary_form に仮名が含まれていない場合、同音異義語の可能性が高いため、読み方で検索すると結果が煩雑になることがある。そのため、dictionary_formで検索するのをお勧め。
            # 日本語において最も同音異義語が多いとされる熟語は「こうしょう」であり、『スーパー大辞林3.0』では  語が該当する（交渉・考証・工匠・高尚・鉱床・口承・厚相・哄笑・公称・工廠・公証・公娼・校章など）。『広辞苑』第 6 版には 50 もの仮名見出しがある。
            # https://ja.wikipedia.org/wiki/%E5%90%8C%E9%9F%B3%E7%95%B0%E7%BE%A9%E8%AA%9E
            jishokei = token.dictionary_form
        result = [token.surface(), jishokei]
        result_list.append(result)
    return result_list


def _cursor_word(analysis_result: list[str], cursor_index: int) -> str | None:
    """获取光标附近"""
    # if sum(len(key) for key in result) < cursor_index:
    #     # 如果光标所在的位置大于文本的长度，直接抛出异常
    #     raise ValueError("Cursor index is out of range.")

    length_before_cursor = 0
    for result in analysis_result:
        # 通过计算光标前的文本长度确认
        length_before_cursor += len(result[0])
        if length_before_cursor >= cursor_index:
            # TODO = 说明用户的光标正好放在2个句节的分界处
            # TODO 可以考虑基于难度和词频猜测哪个更有可能是用户想查的单词，
            # 或者允许按照个人习惯，设置这种情况是返回前还是后
            return result[1]

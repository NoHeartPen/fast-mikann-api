from sudachipy import Dictionary


def analyze_text(text) -> list:
    tokenizer = Dictionary().create()
    result_list = []
    for token in tokenizer.tokenize(text):
        result = []
        result.append(token.surface())
        result.append(token.dictionary_form())
        # result.append(token.reading_form)
        result_list.append(result)
    return result_list


def _cursor_word(analysis_result: list, cursor_index: int) -> str:
    """获取光标附近
    """
    # if sum(len(key) for key in result) < cursor_index:
    #     # 如果光标所在的位置大于文本的长度，直接抛出异常
    #     raise ValueError("Cursor index is out of range.")

    length_before_cursor = 0
    for result in analysis_result:
        # 通过计算光标前的文本长度确认
        length_before_cursor += len(result[0])
        if length_before_cursor >= cursor_index:
            # TODO = 说明用户的光标正好放在2个句节的分界处
            # 可以考虑基于难度和词频猜测哪个更有可能是用户想查的单词，
            # 或者允许按照个人习惯，设置这种情况是返回前还是后
            return result[1]


"""
这部分的代码参考了 PyCon JP 2025 『Python で 日本語処理 入門 〜フリガナプログラムを作ろう〜』的演讲内容。
在此，向发表者[Takanori Suzuki](https://x.com/takanory)表示感谢。
<https://2024.pycon.jp/ja/talk/BQXVWE>
"""

import re

from jaconv import kata2hira
from sudachipy import Dictionary

# ひらがなとカタカナを表す正規表現
KANA: str = r"[\u3041-\u309F\u30A1-\u30FF]+"

# 漢字を表す正規表現
KANJI = r"[\u3005-\u3007\u4E00-\u9FFF]"


def create_ruby_annotation(kanji: str, furi: str) -> str:
    """
    返回 ruby 标签标注读音的 HTML字符串。
    Args:
        kanji: 需要标注读音的汉字
        furi: 需要标注的读音

    Returns:
         标注了读音的 HTML 字符串
    """
    return f"<ruby><rb>{kanji}</rb><rt>{furi}</rt></ruby>"


def convert_to_ruby(kanji_text: str, kana_text: str) -> str:
    """
        将形态素解析结果转为 ruby 注音的文本
    Args:
            kanji_text: 包含汉字的文本
            kana_text: 对应的假名文本

        Returns:
            带ruby注音的文本
    """
    hira = kata2hira(kana_text)
    ruby_html = ""
    while m := re.search(KANA, kanji_text):  # kanjiの中のすべてのかな
        okuri = m[0]
        index = hira.find(kata2hira(okuri), m.start())  # 最初のかなの位置
        furigana = hira[:index]
        # 残りのふりがな
        hira = hira[index + len(okuri) :]
        # kanjiを送りがなで分割
        f_kanji, kanji_text = kanji_text.split(okuri, 1)
        if furigana:
            ruby_html += create_ruby_annotation(f_kanji, furigana)
        ruby_html += okuri  # 送りがなを追加
    if kanji_text:  # 漢字が残っている場合
        ruby_html += create_ruby_annotation(kanji_text, hira)
    return ruby_html


def add_furigana(input_text: str) -> str:
    """
    通过 ruby 标签标注读音。
    Args:
        input_text: 需要标注读音的文本

    Returns:
        标注了读音的文本
    """
    tokenizer = Dictionary().create()
    annotated_text = ""
    for token in tokenizer.tokenize(input_text):
        surface = token.surface()
        if re.search(KANJI, surface):
            annotated_text += convert_to_ruby(surface, token.reading_form())
        else:
            # 说明是片假名、数字或者英文
            annotated_text += surface
    return annotated_text

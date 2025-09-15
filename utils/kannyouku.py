"""
基于倒排索引识别日语的惯用句的非辞书形
"""

import os
import re
import sqlite3


def get_kannyouku_all_words() -> set[str]:
    """查询数据库并返回所有可以作为惯用句的单词，用于判断是否进行进一步查找或扫描。


    Returns:
        以 {'うそ', 'つく', '嘘', '付く'} 的格式返回查询结果
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "nonjishokei.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    statement = "SELECT pre_word_kannji, pre_word_yomi, post_word_kannji, post_word_yomi FROM kannyouku"
    all_kannyouku = cursor.execute(statement).fetchall()
    all_kannyouku_words = set()
    for kannyouku in all_kannyouku:
        for word in kannyouku:
            # 将组成惯用句的的单词的汉字写法和假名写法都加入到 set 中
            all_kannyouku_words.add(word)
    conn.close()
    print(f"{all_kannyouku_words} は惯用句の候補の単語です。")
    return all_kannyouku_words


def is_all_kana(text: str) -> bool:
    """判断一个字符串是否全部由假名构成

    Args:
        text: 要判断的字符串

    Returns:
        如果字符串全部由假名构成返回 True，否则 False.
    """

    return re.match(r"^[\u3040-\u309F\u30A0-\u30FF]+$", text) is not None


def do_query_kannyouku(statement: str, params: list[str]) -> list[set[str]]:
    """查询数据库并返回词组

    Args:
        statement: SQL 语句的固定部分，即：SELECT dict_index FROM kannyouku WHERE 1=1
        params: SQL 语句的拼接部分

    Returns:
        以 [("嘘を付く",)] 的格式返回查询结果
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "nonjishokei.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(statement)
    phrase = cursor.execute(statement, params).fetchall()
    conn.close()
    return phrase


def query_kannyouku(kannyouku_word_list: list[list[str]]) -> list[set[str]]:
    """通过传入的数据构建动态 SQL 在数据库中查询并返回词组

    Args:
        kannyouku_word_list: 组成词组的前后项单词，例：[["うそ", "嘘"], ["つく", "付く"]]
        即嵌套列表中的第一层列表用于区分组成词组的不同单词，第二层列表用于区分单词的不同写法
        TODO 注意： 目前只支持类似【嘘を付く】这样【名词+助词+动词】的形式的短语，能否支持其他形式的短语需要在实际的生产环境中进行测试

    Returns:
        以 [("嘘を付く",)] 的格式返回所有可能的词组，如果没有查到词组则返回空列表
    """
    # if len(kannyouku_word_list) != 2:
    #     # TODO 暂时不支持非【名词+助词+动词】形式的惯用句查询
    #     # 如有需要，请使用 Elasticsearch 或其他全文检索引擎
    #     print("暂时不支持非【名词+助词+动词】形式的惯用句查询")
    #     return []

    # 为防止 SQL 注入攻击，这里指定 1=1
    statement = "SELECT midashi_index FROM kannyouku WHERE 1=1"
    params = []
    statement = _build_kannyouku_search_statement(
        kannyouku_word_list, params, statement
    )
    kannyouku = do_query_kannyouku(statement, params)
    return kannyouku


def _append_word_condition(
    words: list[str], position: str, base_statement: str, existing_params: list[str]
) -> str:
    """添加单词查询条件

    Args:
        words: 要处理的单词列表
        position: 单词位置(pre/post)
        base_statement: 基础SQL语句
        existing_params: SQL参数列表

    Returns:
        更新后的SQL语句
    """
    for word in words:
        word_type = "yomi" if is_all_kana(word) else "kannji"
        base_statement += f" AND {position}_word_{word_type}=?"
        existing_params.append(word)
    return base_statement


def _build_kannyouku_search_statement(
    phrase_parts: list[list[str]], existing_params: list[str], base_statement: str
) -> str:
    """构建惯用句搜索SQL语句

    Args:
        phrase_parts: 包含惯用句前后部分的单词列表
        existing_params: SQL参数列表
        base_statement: 基础SQL语句

    Returns:
        构建完成的SQL查询语句
    """
    # 处理助词前的部分（一般是名词）
    base_statement = _append_word_condition(
        phrase_parts[0], "pre", base_statement, existing_params
    )

    # 处理助词后的部分（一般是动词）
    base_statement = _append_word_condition(
        phrase_parts[1], "post", base_statement, existing_params
    )

    print(f"「{existing_params}」で慣用句を検索します。")
    return base_statement

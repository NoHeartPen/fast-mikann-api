"""
基于 txt 文件批量添加惯用句数据到数据库
"""

import os
import sqlite3


def parse_txt_line(line: str) -> tuple:
    """
    将 txt 文件中的一行解析为数据库记录

    Args:
        line: 原始行字符串，例如 "心を開く,こころをひらく"

    Returns:
        tuple: 包含数据库字段的元组 (midashi_index, kanan_index, pre_word_kannji, pre_word_yomi, post_word_kannji, post_word_yomi)
    """
    line = line.strip()
    if not line or "," not in line:
        raise ValueError(f"行格式无效，必须包含','分隔符: {line}")

    # 使用 ',' 分割行数据（"心を開く,こころをひらく"）
    parts = line.split(",", maxsplit=1)
    if len(parts) != 2:
        raise ValueError(f"无法解析行: {line}")

    kannji_text, yomi_text = parts[0].strip(), parts[1].strip()

    # 确保有前后单词数据
    if "を" in kannji_text:
        pre_word, post_word = kannji_text.split("を", maxsplit=1)
        pre_yomi, post_yomi = yomi_text.split("を", maxsplit=1)
    elif "が" in kannji_text:
        pre_word, post_word = kannji_text.split("が", maxsplit=1)
        pre_yomi, post_yomi = yomi_text.split("が", maxsplit=1)
    elif "に" in kannji_text:
        pre_word, post_word = kannji_text.split("に", maxsplit=1)
        pre_yomi, post_yomi = yomi_text.split("に", maxsplit=1)
    elif "で" in kannji_text:
        pre_word, post_word = kannji_text.split("で", maxsplit=1)
        pre_yomi, post_yomi = yomi_text.split("で", maxsplit=1)
    else:
        raise ValueError(f"格式错误，缺少助词 'を' 或 'が': {line}")

    return kannji_text, yomi_text, pre_word, pre_yomi, post_word, post_yomi


def insert_record_to_db(record_data: tuple) -> None:
    """
    将单条记录插入到数据库

    Args:
        record_data: 数据库字段元组
            e.g., ("心を開く", "こころをひらく", "心", "こころ", "開く", "ひらく")
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "nonjishokei.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    insert_sql = """
                 INSERT INTO kannyouku (midashi_index, kanan_index, pre_word_kannji, pre_word_yomi, post_word_kannji, post_word_yomi)
                 VALUES (?, ?, ?, ?, ?, ?) \
                 """
    try:
        cursor.execute(insert_sql, record_data)
        conn.commit()
        print(f"成功插入记录: {record_data}")
    except sqlite3.Error as e:
        print(f"插入失败: {record_data}，错误信息: {e}")
    finally:
        conn.close()


def batch_add_kannyouku_from_txt(file_path: str) -> None:
    """
    批量从 txt 文件添加惯用句数据到数据库

    Args:
        file_path: txt 文件路径，文件内容格式要求：
            1. 每行记录格式为 "心を開く,こころをひらく"
            2. 使用 ',' 分割，左侧为汉字表记，右侧为假名发音
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"指定的文件不存在: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                # 解析行数据为数据库格式
                record_data = parse_txt_line(line)
                # 插入数据库
                insert_record_to_db(record_data)
            except Exception as e:
                print(f"跳过无效行: {line.strip()}，错误信息: {e}")


if __name__ == "__main__":
    # 示例: 从文件批量添加数据
    test_file_path = os.path.join(os.path.dirname(__file__), "kannyouku_data.txt")
    print(f"从文件 {test_file_path} 批量添加惯用句到数据库...")
    try:
        batch_add_kannyouku_from_txt(test_file_path)
        print("数据添加完成！")
    except Exception as e:
        print(f"批量添加过程中出错: {e}")

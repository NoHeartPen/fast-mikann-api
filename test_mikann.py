import unittest

from mikann import analyze_text, _cursor_word


class TestCursorWord(unittest.TestCase):
    def test_cursor_word(self):
        # 0晩1ご2飯3を4食5べ6ま7し8た9か10。11
        test_cases = [
            # (光标索引, 期望的输出)
            # 光标在"晩御飯"之前
            (0, "晩ご飯"),
            (1, "晩ご飯"),
            (2, "晩ご飯"),
            (3, "晩ご飯"),
            (4, "を"),
            (5, "食べる"),
            (6, "食べる"),
            (7, "ます"),
            (8, "ます"),
            (9, "た"),
            (10, "か"),
            (11, "。"),
            # 异常测试
            # FIXME (12,  "。"),
            # FIXME  (1111,  "。"),
        ]
        for cursor_index, expected_output in test_cases:
            with self.subTest(
                cursor_index=cursor_index, expected_output=expected_output
            ):
                result = analyze_text("晩ご飯を食べましたか。")
                if cursor_index > sum(len(key) for key in result):
                    # 如果光标位置超出范围，检查是否抛出异常
                    with self.assertRaises(ValueError):
                        _cursor_word(result, cursor_index)
                else:
                    self.assertEqual(
                        _cursor_word(result, cursor_index), expected_output
                    )


if __name__ == "__main__":
    unittest.main()

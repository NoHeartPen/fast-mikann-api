import unittest

from mikann import analyze_text


class TestAnalyzeText(unittest.TestCase):
    def test_normal_case(self):
        """测试正常文本分析"""
        text = "晩ご飯を食べましたか。"
        expected = [
            ["晩ご飯", "晩御飯"],
            ["を", "を"],
            ["食べ", "食べる"],
            ["まし", "ます"],
            ["た", "た"],
            ["か", "か"],
            ["。", "。"],
        ]
        result = analyze_text(text)
        self.assertEqual(result, expected)

    def test_empty_string(self):
        """测试空字符串输入"""
        with self.assertRaises(ValueError) as context:
            analyze_text("")
        self.assertEqual(str(context.exception), "Input text cannot be empty or None")

    def test_none_input(self):
        """测试None输入"""
        with self.assertRaises(ValueError) as context:
            analyze_text(None)  # type: ignore
        self.assertEqual(str(context.exception), "Input text cannot be empty or None")

    def test_english_text(self):
        """测试英文文本"""
        text = "Hello World"
        result = analyze_text(text)
        # Sudachi 对英文的处理可能不同，这里只验证基本结构
        self.assertTrue(all(len(pair) == 2 for pair in result))
        self.assertTrue(all(isinstance(pair[0], str) for pair in result))

    def test_mixed_text(self):
        """测试混合文本"""
        text = "Pythonで自然言語処理をします。"
        result = analyze_text(text)
        # 验证返回的结构是否正确
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(pair, list) for pair in result))
        self.assertTrue(all(len(pair) == 2 for pair in result))


if __name__ == "__main__":
    unittest.main()

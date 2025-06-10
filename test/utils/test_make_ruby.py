from unittest import TestCase

from utils.make_ruby import add_furigana


class TestMakeFurigana(TestCase):
    """Tests for make_furigana function."""

    def test_make_furigana(self):
        """Test make_furigana with various input cases."""
        test_cases = [
            # (input_text, expected_output)
            (
                "日本語",
                "<ruby><rb>日本語</rb><rt>にほんご</rt></ruby>",
            ),
            ("東京", "<ruby><rb>東京</rb><rt>とうきょう</rt></ruby>"),
            ("ひらがな", "ひらがな"),
            (
                "漢字とひらがな",
                "<ruby><rb>漢字</rb><rt>かんじ</rt></ruby>とひらがな",
            ),
            ("", ""),
            ("123ABC", "123ABC"),
            ("悪くない", "<ruby><rb>悪</rb><rt>わる</rt></ruby>くない"),
            ("悪い", "<ruby><rb>悪</rb><rt>わる</rt></ruby>い"),
            ("つかない", "つかない"),
            ("１００００００", "１００００００"),
            ("嘘つかない", "<ruby><rb>嘘</rb><rt>うそ</rt></ruby>つかない"),
            (
                "打ち上げ",
                "<ruby><rb>打</rb><rt>う</rt></ruby>ち<ruby><rb>上</rb><rt>あ</rt></ruby>げ",
            ),
            ("これはカエルだ", "これはカエルだ"),  # 包含外来语。
            ("こんにちは", "こんにちは"),  # 纯假名测试
            (
                # 注意 問おう的表记转换
                "問おう。あなたがわたしのマスターか",
                "<ruby><rb>問</rb><rt>と</rt></ruby>おう。あなたがわたしのマスターか",
            ),
            (
                "私はPythonが大好きです。",
                "<ruby><rb>私</rb><rt>わたくし</rt></ruby>はPythonが<ruby><rb>大好</rb><rt>だいす</rt></ruby>きです。",
            ),
            # ("说谎", "说谎"),  # 非日语文本。
        ]

        for test_text, expected_output in test_cases:
            with self.subTest(test_text=test_text, expected_output=expected_output):
                actual = add_furigana(test_text)
                self.assertEqual(
                    actual,
                    expected_output,
                    f"Failed for input: '{test_text}'\n"
                    f"Expected: {expected_output}\n"
                    f"Got: {actual}",
                )

from diff_generator.generator import generate_diff_report


def test_generate_diff_report_identical_documents():
    text = "Sample text\nSecond line"
    result = generate_diff_report(text, text, format='markdown')
    assert result == "差分は見つかりませんでした。内容は完全に一致しています。"

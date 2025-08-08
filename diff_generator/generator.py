import difflib

def generate_diff_report(old_text, new_text, format='markdown'):
    """
    Generates a diff report between two texts.

    Args:
        old_text (str): The original text.
        new_text (str): The new, rewritten text.
        format (str): The desired output format ('markdown' or 'html').

    Returns:
        A string containing the formatted diff report.
    """
    if format not in ['markdown', 'html']:
        raise ValueError("Unsupported format. Choose 'markdown' or 'html'.")

    # テキストを行ごとに分割
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()

    if format == 'markdown':
        return generate_markdown_diff(old_lines, new_lines)
    elif format == 'html':
        return generate_html_diff(old_lines, new_lines)

def generate_markdown_diff(old_lines, new_lines):
    """
    Generates a diff report in Markdown format.
    - Added lines are prefixed with `+ `
    - Deleted lines are prefixed with `- `
    - Unchanged lines are prefixed with `  `
    The function scans diff lines for these prefixes to determine if changes
    exist, rather than relying on output length.
    """
    diff_lines = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile='既存の書類',
            tofile='生成された新書類',
            lineterm=''
        )
    )

    markdown_report = "```diff\n"
    formatted_lines = []
    # ヘッダー行をスキップ
    for i, line in enumerate(diff_lines):
        if i > 1:
            if line.startswith('+') or line.startswith('-'):
                line = f"{line[0]} {line[1:]}"
            formatted_lines.append(line)
            markdown_report += line + "\n"
    markdown_report += "```"

    # 差分があるかをプレフィックスでチェック
    has_changes = any(
        l.startswith('+ ') or l.startswith('- ')
        for l in formatted_lines
    )
    if not has_changes:
        return "差分は見つかりませんでした。内容は完全に一致しています。"

    return markdown_report

def generate_html_diff(old_lines, new_lines):
    """
    Generates a side-by-side diff report in HTML format.
    """
    differ = difflib.HtmlDiff(wrapcolumn=80)
    html_report = differ.make_file(old_lines, new_lines, fromdesc='既存の書類', todesc='生成された新書類')
    return html_report



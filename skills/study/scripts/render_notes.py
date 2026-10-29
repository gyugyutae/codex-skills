#!/usr/bin/env python3
"""Render UTF-8 study Markdown to an A4 PDF without replacing existing files.
Requires: markdown, weasyprint (+ WeasyPrint system dependencies).
Use <!-- pagebreak --> for deliberate section breaks. Pass a Korean-capable
--font file when the system does not supply one. No course-specific content.
"""
import argparse
from html import escape
from pathlib import Path


def render(source, output, font=None, export_html=False):
    import markdown
    from weasyprint import HTML

    source = Path(source).resolve()
    pdf = Path(output).resolve()
    if pdf.suffix.lower() != '.pdf':
        raise ValueError('Output must have a .pdf extension')
    html_path = pdf.with_suffix('.html')
    if pdf.exists() or (export_html and html_path.exists()):
        raise FileExistsError('Choose a new output name; requested output already exists')
    font_css = ''
    if font:
        font = Path(font).resolve(strict=True)
        # Percent-encoded file URI keeps CSS quoting well-defined.
        font_css = f'@font-face{{font-family:Study;src:url("{font.as_uri()}")}}'
    css = font_css + '''
@page { size: A4; margin: 12mm; }
body { font-family: Study, "Noto Sans CJK KR", "Malgun Gothic", sans-serif;
 font-size: 10pt; line-height: 1.4; color: #182530; }
h1 { font-size: 17pt; border-bottom: 2px solid #456; padding-bottom: 4px; }
h2 { font-size: 12pt; margin: 10px 0 5px; }
h1,h2,h3 { break-after: avoid; }
p,li { margin-top: 4px; margin-bottom: 4px; }
table { width: 100%; border-collapse: collapse; font-size: 9pt; margin: 7px 0; }
th,td { border: 1px solid #b8c2ca; padding: 5px; text-align: left;
 vertical-align: top; overflow-wrap: anywhere; }
th { background: #edf1f4; } tr { break-inside: avoid; }
img,svg { max-width: 100%; height: auto; }
.question { break-inside: avoid; }
.pagebreak { break-before: page; }
blockquote { margin: 7px 0; padding: 5px 9px; border-left: 3px solid #789; }
'''
    text = source.read_text(encoding='utf-8')
    sections = text.split('<!-- pagebreak -->')
    body = '<div class="pagebreak"></div>'.join(
        markdown.markdown(s, extensions=['tables', 'fenced_code', 'md_in_html']) for s in sections
    )
    title = escape(source.stem)
    result = f'<!doctype html><html lang="ko"><meta charset="utf-8"><title>{title}</title><style>{css}</style><body>{body}</body></html>'
    # Render first so dependency/font errors do not leave a misleading HTML-only result.
    document = HTML(string=result, base_url=str(source.parent)).render()
    pdf_bytes = document.write_pdf()
    pdf.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation protects existing artifacts, including a late-created output.
    with pdf.open('xb') as stream:
        stream.write(pdf_bytes)
    if export_html:
        with html_path.open('x', encoding='utf-8') as stream:
            stream.write(result)
    return len(document.pages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--font', type=Path, help='Korean-capable font file')
    parser.add_argument('--export-html', action='store_true', help='Also export HTML when explicitly requested')
    args = parser.parse_args()
    print(f'Created {args.output} ({render(args.source, args.output, args.font, args.export_html)} pages)')


if __name__ == '__main__':
    main()

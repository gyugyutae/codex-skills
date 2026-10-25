"""Inspect/edit an exported HWPML document with explicit JSON cell/picture edits."""
import argparse
import base64
from copy import deepcopy
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def load(path):
    text = Path(path).read_text(encoding='utf-8-sig')
    return ET.fromstring(re.sub(r'^\s*<\?xml[^>]*\?>', '', text, count=1))


def cell_at(root, address):
    tables = list(root.iter('TABLE'))
    table = tables[int(address['table'])]
    cell = table.find(f"ROW/CELL[@RowAddr='{address['row']}'][@ColAddr='{address['col']}']")
    if cell is None:
        raise ValueError(f'No cell at {address}; check merged cell addresses')
    return cell


def paragraph(text, para_shape, char_shape):
    p = ET.Element('P', ParaShape=str(para_shape), Style='0')
    ET.SubElement(ET.SubElement(p, 'TEXT', CharShape=str(char_shape)), 'CHAR').text = text
    return p


def set_cell(cell, text, edit):
    pl = cell.find('PARALIST')
    first = pl.find('P')
    ps = edit.get('para_shape', first.get('ParaShape', '0'))
    t = first.find('TEXT')
    cs = edit.get('char_shape', t.get('CharShape', '0') if t is not None else '0')
    # Changes are limited to explicitly selected cell contents.
    pl[:] = [paragraph(line, ps, cs) for line in text.split('\n')]
    return pl


def resize(pic, width, height):
    if width <= 0 or height <= 0:
        raise ValueError('Image dimensions must be positive HWPUNIT values')
    size = pic.find('SHAPEOBJECT/SIZE')
    size.set('Width', str(width)); size.set('Height', str(height))
    sc = pic.find('SHAPECOMPONENT')
    for key, value in [('OriWidth', width), ('OriHeight', height), ('CurWidth', width), ('CurHeight', height)]:
        if key in sc.attrib or key.startswith('Ori'):
            sc.set(key, str(value))
    sc.set('XPos', '0'); sc.set('YPos', '0')
    rot = sc.find('ROTATIONINFO')
    if rot is not None:
        rot.set('CenterX', str(width // 2)); rot.set('CenterY', str(height // 2))
    ri = sc.find('RENDERINGINFO')
    if ri is not None:
        for matrix in ri:
            for key in ['E1', 'E2', 'E3', 'E4', 'E5', 'E6']:
                matrix.set(key, '1.00000' if key in ['E1', 'E5'] else '0.00000')
    rect = pic.find('IMAGERECT')
    for key, value in dict(X0=0, X1=width, X2=width, X3=0, Y0=0, Y1=0, Y2=height, Y3=height).items():
        rect.set(key, str(value))


def insert_image(root, edit, base_dir):
    from PIL import Image
    target = cell_at(root, edit)
    source = Path(edit['file'])
    if not source.is_absolute():
        source = base_dir / source
    with Image.open(source) as im:
        if im.format != 'PNG':
            raise ValueError('Pass an original PNG; this helper does not convert screenshots')
        pixels_w, pixels_h = im.size
    raw = source.read_bytes()
    template = next(root.iter('PICTURE'), None)
    if template is None:
        raise ValueError('No native PICTURE to clone; insert one using Hangul COM first')
    pic = deepcopy(template)
    bins = root.find('.//BINDATALIST'); store = root.find('.//BINDATASTORAGE')
    if bins is None or store is None:
        raise ValueError('Missing native binary resource sections')
    bid = max([int(x.get('BinData')) for x in bins] + [0]) + 1
    ET.SubElement(bins, 'BINITEM', BinData=str(bid), Format='PNG', Type='Embedding')
    bins.set('Count', str(len(bins)))
    ET.SubElement(store, 'BINDATA', Encoding='Base64', Id=str(bid), Size=str(len(raw))).text = base64.b64encode(raw).decode()
    scale = min(edit.get('max_width', 17000) / pixels_w, edit.get('max_height', 28000) / pixels_h)
    resize(pic, round(pixels_w * scale), round(pixels_h * scale))
    so = pic.find('SHAPEOBJECT')
    so.set('TextWrap', 'TopAndBottom')
    so.set('InstId', str(max([int(x.get('InstId', '0')) for x in root.iter('SHAPEOBJECT')] + [0]) + 1))
    sc = pic.find('SHAPECOMPONENT'); sc.set('InstID', so.get('InstId'))
    pos = so.find('POSITION')
    for key, value in dict(TreatAsChar='true', AllowOverlap='false', FlowWithText='true', HorzAlign='Center', HorzRelTo='Para', HorzOffset='0', VertAlign='Top', VertRelTo='Para', VertOffset='0').items():
        pos.set(key, value)
    comment = so.find('SHAPECOMMENT')
    if comment is None:
        comment = ET.SubElement(so, 'SHAPECOMMENT')
    comment.text = edit.get('comment', source.name)
    pic.find('IMAGE').set('BinItem', str(bid))
    clip = pic.find('IMAGECLIP')
    for key, value in dict(Left=0, Top=0, Right=pixels_w * 75, Bottom=pixels_h * 75).items():
        clip.set(key, str(value))
    dim = pic.find('IMAGEDIM'); dim.set('Width', str(pixels_w * 75)); dim.set('Height', str(pixels_h * 75))
    pl = set_cell(target, '', {'para_shape': edit.get('para_shape', '33'), **edit})
    pl[0].find('TEXT').append(pic)
    if edit.get('caption'):
        pl.append(paragraph(edit['caption'], pl[0].get('ParaShape'), edit.get('caption_char_shape', pl[0].find('TEXT').get('CharShape'))))


def apply(root, edits, base_dir):
    for edit in edits.get('cells', []):
        set_cell(cell_at(root, edit), edit['text'], edit)
    for edit in edits.get('replacements', []):
        hits = 0
        for char in root.iter('CHAR'):
            if char.text and edit['old'] in char.text:
                hits += char.text.count(edit['old'])
                char.text = char.text.replace(edit['old'], edit['new'])
        if hits != edit['expected_count']:
            raise ValueError(f'Replacement count {hits} != {edit["expected_count"]}: {edit["old"]}')
    for edit in edits.get('resize_pictures', []):
        matches = [p for p in root.iter('PICTURE') if edit['comment_contains'] in (p.findtext('SHAPEOBJECT/SHAPECOMMENT') or '')]
        pic = matches[edit.get('occurrence', 0)]
        resize(pic, int(edit['width']), int(edit['height']))
        so = pic.find('SHAPEOBJECT')
        if edit.get('signature', False):
            so.set('TextWrap', 'InFrontOfText')
            so.find('POSITION').set('TreatAsChar', 'false')
        for key, value in edit.get('position', {}).items():
            so.find('POSITION').set(key, str(value))
    for edit in edits.get('images', []):
        insert_image(root, edit, base_dir)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', type=Path)
    ap.add_argument('--manifest', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if bool(args.manifest) != bool(args.output):
        ap.error('--manifest and --output must be supplied together')
    if args.output and args.input.resolve() == args.output.resolve():
        ap.error('Use a separate output path to preserve the exported source')
    root = load(args.input)
    if args.manifest:
        apply(root, json.loads(args.manifest.read_text(encoding='utf-8-sig')), args.manifest.parent)
        args.output.write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True))
        print(args.output)
    else:
        for i, table in enumerate(root.iter('TABLE')):
            print(json.dumps({'table': i, 'cells': [{'row': c.get('RowAddr'), 'col': c.get('ColAddr'), 'text': '\n'.join(x.text or '' for x in c.iter('CHAR'))} for c in table.findall('ROW/CELL')]}, ensure_ascii=False))
        for i, pic in enumerate(root.iter('PICTURE')):
            print(json.dumps({'picture': i, 'comment': pic.findtext('SHAPEOBJECT/SHAPECOMMENT'), 'size': pic.find('SHAPEOBJECT/SIZE').attrib, 'position': pic.find('SHAPEOBJECT/POSITION').attrib}, ensure_ascii=False))


if __name__ == '__main__':
    main()

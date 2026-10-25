"""Check PDF contents and native signature properties; render page previews."""
import argparse
import json
from pathlib import Path
import pymupdf
from hwpml_edit import load


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pdf', type=Path)
    ap.add_argument('--roundtrip', type=Path)
    ap.add_argument('--signature-comment', default='SIGNATURE_OVER_IN')
    ap.add_argument('--require', action='append', default=[])
    ap.add_argument('--forbid', action='append', default=[])
    ap.add_argument('--expected-images', type=int)
    ap.add_argument('--expected-signatures', type=int)
    ap.add_argument('--signature-fit-ratio', type=float, default=1.15)
    ap.add_argument('--render-dir', type=Path)
    args = ap.parse_args()
    doc = pymupdf.open(args.pdf)
    alltext = '\n'.join(page.get_text() for page in doc)
    for text in args.require:
        if text not in alltext: raise ValueError(f'Missing required text: {text}')
    for text in args.forbid:
        if text in alltext: raise ValueError(f'Unexpected text: {text}')
    pages = []
    if args.render_dir: args.render_dir.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(doc):
        text = page.get_text(); images = page.get_image_info()
        if not text.strip() and not images: raise ValueError(f'Blank page {i+1}')
        pages.append({'page': i+1, 'textCharacters': len(text), 'images': len(images)})
        if args.render_dir:
            page.get_pixmap(matrix=pymupdf.Matrix(1.3, 1.3)).save(args.render_dir / f'page-{i+1}.png')
    count = sum(x['images'] for x in pages)
    if args.expected_images is not None and count != args.expected_images:
        raise ValueError(f'Expected {args.expected_images} image occurrences; found {count}')
    signatures = []
    if args.roundtrip:
        root = load(args.roundtrip)
        for pic in root.iter('PICTURE'):
            so = pic.find('SHAPEOBJECT')
            if args.signature_comment in (so.findtext('SHAPECOMMENT') or ''):
                if so.get('TextWrap') != 'InFrontOfText' or so.find('POSITION').get('TreatAsChar') != 'false':
                    raise ValueError('Signature is not a floating image in front of text')
                signatures.append(dict(so.find('POSITION').attrib))
    geometry = []
    used = set()
    for pi, page in enumerate(doc):
        imgs = page.get_image_info()
        for marker in page.search_for('(인)'):
            candidates=[]
            for ii, img in enumerate(imgs):
                rect=pymupdf.Rect(img['bbox'])
                if (pi,ii) not in used and rect.intersects(marker) and rect.width <= marker.width*args.signature_fit_ratio:
                    candidates.append((abs((rect.x0+rect.x1-marker.x0-marker.x1)/2), ii, rect))
            if not candidates: continue
            dx, ii, rect = min(candidates, key=lambda x:x[0])
            if dx > 2.0: raise ValueError(f'Signature center is displaced on page {pi+1}')
            used.add((pi,ii))
            geometry.append({'page':pi+1,'marker':list(marker),'image':list(rect),'centerOffsetPoints':dx})
            if args.render_dir:
                crop=rect|marker;crop+=(-10,-10,10,10)
                page.get_pixmap(matrix=pymupdf.Matrix(4,4), clip=crop).save(args.render_dir/f'signature-{len(geometry)}.png')
    if args.expected_signatures is not None:
        if len(signatures) != args.expected_signatures or len(geometry) != args.expected_signatures:
            raise ValueError(f'Signature properties/geometry found {len(signatures)}/{len(geometry)}, expected {args.expected_signatures}')
    print(json.dumps({'pages':pages,'imageOccurrences':count,'signatureProperties':signatures,'signatureGeometry':geometry,'visualInspectionStillRequired':True},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()

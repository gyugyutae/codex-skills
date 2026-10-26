"""Verify PDF content, native signature properties, placement and handwritten blanks."""
import argparse
import json
from pathlib import Path
import pymupdf
from hwpml_edit import load

DEFAULT_MARKERS = ('(인)', '(서명)', '(인 또는 서명)')


def find_markers(page, labels):
    """Deduplicate repeated/custom marker labels at the same location."""
    seen = set()
    for label in labels:
        for rect in page.search_for(label):
            key = tuple(round(v, 2) for v in rect)
            if key not in seen:
                seen.add(key)
                yield label, rect


def verify(pdf, *, roundtrip=None, signature_comment='SIGNATURE_OVER_IN',
           require=(), forbid=(), expected_images=None, expected_signatures=None,
           signature_markers=DEFAULT_MARKERS, signature_fit_ratio=3.4,
           max_center_offset=2.0, blank_signatures=(), render_dir=None):
    if signature_fit_ratio <= 0 or max_center_offset < 0:
        raise ValueError('Signature fit ratio must be positive; center tolerance cannot be negative')
    if expected_signatures is not None and expected_signatures < 0:
        raise ValueError('Expected signature count cannot be negative')
    if expected_signatures and roundtrip is None:
        raise ValueError('Expected image signatures require --roundtrip to verify saved properties')
    preview = Path(render_dir) if render_dir else None
    if preview:
        preview.mkdir(parents=True, exist_ok=True)
    signatures = []
    if roundtrip:
        for pic in load(roundtrip).iter('PICTURE'):
            so = pic.find('SHAPEOBJECT')
            if so is None or signature_comment not in (so.findtext('SHAPECOMMENT') or ''):
                continue
            pos = so.find('POSITION')
            if so.get('TextWrap') != 'InFrontOfText' or pos is None or pos.get('TreatAsChar') != 'false':
                raise ValueError('Signature is not a floating image in front of text')
            signatures.append(dict(pos.attrib))
    with pymupdf.open(pdf) as doc:
        if len(doc) == 0:
            raise ValueError('PDF has no pages')
        text = '\n'.join(page.get_text() for page in doc)
        for value in require:
            if value not in text:
                raise ValueError(f'Missing required text: {value}')
        for value in forbid:
            if value in text:
                raise ValueError(f'Unexpected text: {value}')
        pages, geometry, blanks = [], [], []
        used_images = set()
        for pi, page in enumerate(doc):
            images = page.get_image_info()
            if not page.get_text().strip() and not images:
                raise ValueError(f'Blank page {pi + 1}')
            pages.append({'page': pi + 1, 'textCharacters': len(page.get_text()), 'images': len(images)})
            if preview:
                page.get_pixmap(matrix=pymupdf.Matrix(1.3, 1.3)).save(preview / f'page-{pi + 1}.png')
            for label, marker in find_markers(page, signature_markers):
                candidates = []
                for ii, image in enumerate(images):
                    rect = pymupdf.Rect(image['bbox'])
                    if (pi, ii) in used_images or not rect.intersects(marker):
                        continue
                    if rect.width <= marker.width * signature_fit_ratio:
                        dx = abs((rect.x0 + rect.x1 - marker.x0 - marker.x1) / 2)
                        candidates.append((dx, ii, rect))
                if not candidates:
                    continue
                dx, ii, rect = min(candidates, key=lambda item: item[0])
                if dx > max_center_offset:
                    raise ValueError(f'Signature center displaced on page {pi + 1}: {dx:.2f}pt > {max_center_offset:.2f}pt')
                used_images.add((pi, ii))
                geometry.append({'page': pi + 1, 'markerText': label, 'marker': list(marker),
                                 'image': list(rect), 'centerOffsetPoints': dx})
                if preview:
                    crop = (rect | marker) + (-10, -10, 10, 10)
                    page.get_pixmap(matrix=pymupdf.Matrix(4, 4), clip=crop).save(preview / f'signature-{len(geometry)}.png')
        for selector in blank_signatures:
            page_number, sep, marker_text = selector.partition(':')
            if not sep or not marker_text or not page_number.isdigit() or not 1 <= int(page_number) <= len(doc):
                raise ValueError(f'Blank signature selector must be PAGE:TEXT with a valid 1-based page: {selector}')
            page = doc[int(page_number) - 1]
            markers = page.search_for(marker_text)
            if not markers:
                raise ValueError(f'Handwritten signature marker not found: {selector}')
            for marker in markers:
                if any(pymupdf.Rect(image['bbox']).intersects(marker) for image in page.get_image_info()):
                    raise ValueError(f'Image overlaps handwritten-only signature field: {selector}')
                blanks.append({'page': int(page_number), 'markerText': marker_text, 'marker': list(marker)})
        count = sum(page['images'] for page in pages)
        if expected_images is not None and count != expected_images:
            raise ValueError(f'Expected {expected_images} image occurrences; found {count}')
        if expected_signatures is not None and (len(signatures), len(geometry)) != (expected_signatures, expected_signatures):
            raise ValueError(f'Signature properties/geometry found {len(signatures)}/{len(geometry)}, expected {expected_signatures}')
        return {'pages': pages, 'imageOccurrences': count, 'signatureProperties': signatures,
                'signatureGeometry': geometry, 'handwrittenBlankFields': blanks,
                'visualInspectionStillRequired': True}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pdf', type=Path)
    ap.add_argument('--roundtrip', type=Path)
    ap.add_argument('--signature-comment', default='SIGNATURE_OVER_IN')
    ap.add_argument('--require', action='append', default=[])
    ap.add_argument('--forbid', action='append', default=[])
    ap.add_argument('--expected-images', type=int)
    ap.add_argument('--expected-signatures', type=int)
    ap.add_argument('--signature-marker', action='append', help='Repeat to replace default markers')
    ap.add_argument('--signature-fit-ratio', type=float, default=3.4)
    ap.add_argument('--max-center-offset', type=float, default=2.0, help='Maximum horizontal center offset, in PDF points')
    ap.add_argument('--blank-signature', action='append', default=[], metavar='PAGE:TEXT')
    ap.add_argument('--render-dir', type=Path)
    args = ap.parse_args()
    result = verify(args.pdf, roundtrip=args.roundtrip, signature_comment=args.signature_comment,
                    require=args.require, forbid=args.forbid, expected_images=args.expected_images,
                    expected_signatures=args.expected_signatures,
                    signature_markers=args.signature_marker or DEFAULT_MARKERS,
                    signature_fit_ratio=args.signature_fit_ratio, max_center_offset=args.max_center_offset,
                    blank_signatures=args.blank_signature, render_dir=args.render_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

"""Synthetic PDFs exercise real marker/image geometry without private document assets."""
import io
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from PIL import Image
import pymupdf
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from verify_pdf import verify


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def fixture(self, markers, *, images=True, offset=0, native=True, inline=False):
        doc = pymupdf.open()
        raw = io.BytesIO()
        Image.new('RGB', (100, 40), 'black').save(raw, format='PNG')
        for label in markers:
            page = doc.new_page()
            page.insert_text((100, 150), label, fontname='korea', fontsize=12)
            marker = page.search_for(label)[0]
            if images:
                center = (marker.x0 + marker.x1) / 2 + offset
                page.insert_image(pymupdf.Rect(center - 25, marker.y0 - 2, center + 25, marker.y1 + 2), stream=raw.getvalue())
        pdf = self.root / 'example.pdf'
        doc.save(pdf)
        doc.close()
        root = ET.Element('HWPML')
        if images:
            for _ in markers:
                so = ET.SubElement(ET.SubElement(root, 'PICTURE'), 'SHAPEOBJECT', TextWrap='InFrontOfText')
                ET.SubElement(so, 'POSITION', TreatAsChar='true' if inline else 'false')
                ET.SubElement(so, 'SHAPECOMMENT').text = 'SIGNATURE_OVER_IN test'
        xml = self.root / 'example.xml'
        ET.ElementTree(root).write(xml, encoding='utf-8')
        return pdf, xml if native else None

    def test_all_three_default_markers(self):
        pdf, xml = self.fixture(['(인)', '(서명)', '(인 또는 서명)'])
        report = verify(pdf, roundtrip=xml, expected_signatures=3)
        self.assertEqual(len(report['signatureGeometry']), 3)

    def test_custom_duplicate_marker_is_counted_once(self):
        pdf, xml = self.fixture(['(Applicant signature)'])
        report = verify(pdf, roundtrip=xml, expected_signatures=1,
                        signature_markers=['(Applicant signature)'] * 2)
        self.assertEqual(len(report['signatureGeometry']), 1)

    def test_displacement_and_explicit_tolerance(self):
        pdf, xml = self.fixture(['(서명)'], offset=5)
        with self.assertRaisesRegex(ValueError, 'displaced'):
            verify(pdf, roundtrip=xml, expected_signatures=1)
        verify(pdf, roundtrip=xml, expected_signatures=1, max_center_offset=6)

    def test_missing_image_does_not_pass(self):
        pdf, xml = self.fixture(['(서명)'], images=False)
        with self.assertRaisesRegex(ValueError, 'expected 1'):
            verify(pdf, roundtrip=xml, expected_signatures=1)

    def test_native_required_and_inline_rejected(self):
        pdf, xml = self.fixture(['(서명)'], inline=True)
        with self.assertRaisesRegex(ValueError, 'require --roundtrip'):
            verify(pdf, expected_signatures=1)
        with self.assertRaisesRegex(ValueError, 'floating'):
            verify(pdf, roundtrip=xml, expected_signatures=1)

    def test_handwritten_blank_and_missing_marker(self):
        pdf, _ = self.fixture(['(서명)'], images=False)
        report = verify(pdf, expected_signatures=0, blank_signatures=['1:(서명)'])
        self.assertEqual(len(report['handwrittenBlankFields']), 1)
        with self.assertRaisesRegex(ValueError, 'not found'):
            verify(pdf, blank_signatures=['1:(인)'])

    def test_image_in_handwritten_field_rejected(self):
        pdf, _ = self.fixture(['(서명)'])
        with self.assertRaisesRegex(ValueError, 'handwritten-only'):
            verify(pdf, blank_signatures=['1:(서명)'])

    def test_one_image_cannot_satisfy_two_markers(self):
        pdf, _ = self.fixture(['(인) (서명)'])
        report = verify(pdf, max_center_offset=40)
        self.assertEqual(len(report['signatureGeometry']), 1)


if __name__ == '__main__':
    unittest.main()

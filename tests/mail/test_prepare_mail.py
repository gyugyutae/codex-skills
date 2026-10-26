import base64
import importlib.util
from pathlib import Path
import tempfile
import unittest
from urllib.parse import parse_qs, urlparse

SCRIPT = Path(__file__).resolve().parents[2] / 'skills/mail/scripts/prepare_mail.py'


class MailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('prepare_mail', SCRIPT)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.spec = dict(account='student@example.edu', to='office@example.org',
                         subject='장학금 & internship', body='안녕하세요.\nTest + & #?')

    def test_unicode_compose_round_trip(self):
        result = self.module.prepare(self.spec, self.root, 'compose')
        query = parse_qs(urlparse(result['url']).query)
        for key, value in [('authuser', self.spec['account']), ('su', self.spec['subject']),
                           ('body', self.spec['body']), ('to', self.spec['to'])]:
            self.assertEqual(query[key], [value])
        self.assertFalse(result['attachmentsUploaded'])

    def test_draft_attachment_bytes_and_manifest(self):
        content = b'%PDF-1.4\nsynthetic bank statement\n'
        (self.root / 'bank.pdf').write_bytes(content)
        self.spec['attachments'] = [dict(path='bank.pdf', purpose='required', label='통장사본')]
        result = self.module.prepare(self.spec, self.root, 'draft')
        part = result['draftArgs']['payload']['parts'][1]
        encoded = part['body']['base64_url_content']
        self.assertEqual(base64.urlsafe_b64decode(encoded + '=' * (-len(encoded) % 4)), content)
        self.assertEqual(part['mime_type'], 'application/pdf')
        self.assertEqual(result['attachments'][0]['purpose'], 'required')
        self.assertFalse(result['attachmentsUploaded'])
        self.assertNotIn('from_address', result['draftArgs'])

    def test_required_missing_fails(self):
        self.spec['attachments'] = [dict(path='absent.pdf', purpose='required')]
        with self.assertRaisesRegex(ValueError, 'required'):
            self.module.prepare(self.spec, self.root, 'draft')

    def test_optional_missing_is_reported(self):
        self.spec['attachments'] = [dict(path='absent.pdf', purpose='recommended')]
        result = self.module.prepare(self.spec, self.root, 'compose')
        self.assertEqual(len(result['missingRecommended']), 1)

    def test_compose_reports_pending_attachments(self):
        (self.root / 'cv.pdf').write_bytes(b'%PDF-test')
        self.spec['attachments'] = [dict(path='cv.pdf', purpose='recommended')]
        result = self.module.prepare(self.spec, self.root, 'compose')
        self.assertEqual(result['attachmentStatus'], 'pending-upload')
        self.assertNotIn('attach', parse_qs(urlparse(result['url']).query))

    def test_header_injection_and_unknown_purpose_rejected(self):
        for patch in [dict(to='office@example.org\nBcc: attacker@example.org'),
                      dict(subject='Hello\r\nBcc: attacker@example.org'),
                      dict(attachments=[dict(path='missing', purpose='maybe')])]:
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                self.module.prepare(dict(self.spec, **patch), self.root, 'compose')

    def test_oversized_payload_rejected(self):
        (self.root / 'large.pdf').write_bytes(b'x' * 100)
        self.spec['attachments'] = [dict(path='large.pdf', purpose='required')]
        with self.assertRaisesRegex(ValueError, 'limit'):
            self.module.prepare(self.spec, self.root, 'draft', max_bytes=20)

    def test_clean_attachment_name_preserves_original(self):
        original = self.root / '최종진짜(3).pdf'
        original.write_bytes(b'%PDF-original')
        self.spec['attachments'] = [dict(path=original.name, purpose='required', filename='GYUTAE_KIM_CV.pdf')]
        result = self.module.prepare(self.spec, self.root, 'draft')
        self.assertEqual(result['draftArgs']['payload']['parts'][1]['filename'], 'GYUTAE_KIM_CV.pdf')
        self.assertEqual(original.read_bytes(), b'%PDF-original')

    def test_unsafe_changed_extension_and_duplicate_names_rejected(self):
        (self.root / 'cv.pdf').write_bytes(b'%PDF-original')
        for name in ['../cv.pdf', 'nested/cv.pdf', 'nested\\cv.pdf', 'cv.docx', 'cv\n.pdf']:
            self.spec['attachments'] = [dict(path='cv.pdf', purpose='required', filename=name)]
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.module.prepare(self.spec, self.root, 'draft')
        self.spec['attachments'] = [dict(path='cv.pdf', purpose='required', filename='CV.pdf'),
                                    dict(path='cv.pdf', purpose='recommended', filename='cv.pdf')]
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.module.prepare(self.spec, self.root, 'draft')


if __name__ == '__main__':
    unittest.main()

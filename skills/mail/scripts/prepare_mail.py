#!/usr/bin/env python3
"""Prepare a compose URL or private connector MIME data; no network or sending."""
import argparse
import base64
import hashlib
import html
import json
import mimetypes
import os
from pathlib import Path
import sys
from urllib.parse import urlencode


def prepare(spec, root, mode, max_bytes=20 * 1024 * 1024):
    if mode not in ('compose', 'draft'):
        raise ValueError('Unknown mode')
    for key in ('account', 'to', 'subject', 'body'):
        if not isinstance(spec.get(key), str) or not spec[key].strip():
            raise ValueError('Nonempty text required: ' + key)
        if key != 'body' and any(c in spec[key] for c in '\r\n'):
            raise ValueError('Header contains a newline: ' + key)
    for key in ('account', 'to'):
        if '@' not in spec[key]:
            raise ValueError('Email address required: ' + key)
    reply_id = spec.get('reply_message_id')
    if reply_id is not None:
        if not isinstance(reply_id, str) or not reply_id.strip() or any(c.isspace() for c in reply_id):
            raise ValueError('reply_message_id must be a nonempty Gmail message ID without whitespace')
        if mode == 'compose':
            raise ValueError('Replies require draft mode; a compose URL cannot guarantee reply context')
    manifest, missing, parts = [], [], []
    names = set()
    estimated = len(spec['body'].encode('utf-8')) * 6 + 2048
    for item in spec.get('attachments', []):
        purpose = item.get('purpose')
        if purpose not in ('required', 'recommended'):
            raise ValueError('Attachment purpose must be required or recommended')
        if not isinstance(item.get('path'), str) or not item['path']:
            raise ValueError('Attachment path required')
        path = (Path(root) / item['path']).resolve()
        filename = item.get('filename', path.name)
        if (not isinstance(filename, str) or not filename.strip()
                or filename in ('.', '..') or any(c in filename for c in '/\\')
                or any(ord(c) < 32 or ord(c) == 127 for c in filename)):
            raise ValueError('Attachment filename must be a safe basename')
        if Path(filename).suffix.lower() != path.suffix.lower():
            raise ValueError('Filename extension must match the source; convert content separately')
        if filename.casefold() in names:
            raise ValueError('Duplicate attachment filename: ' + filename)
        names.add(filename.casefold())
        label = item.get('label', path.name)
        if not path.is_file() or path.stat().st_size == 0:
            if purpose == 'required':
                raise ValueError('Missing or empty required attachment: ' + str(path))
            missing.append(dict(path=str(path), label=label))
            continue
        if any(c in path.name for c in '\r\n'):
            raise ValueError('Attachment filename contains newline')
        size = path.stat().st_size
        estimated += ((size + 2) // 3) * 4 + 2048
        if estimated > max_bytes:
            raise ValueError('Estimated encoded payload exceeds configured limit')
        data = path.read_bytes()
        mime = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        manifest.append(dict(path=str(path), filename=filename, label=label,
                             purpose=purpose, bytes=len(data), mimeType=mime,
                             sha256=hashlib.sha256(data).hexdigest()))
        if mode == 'draft':
            parts.append(dict(mime_type=mime, filename=filename,
                              content_disposition='attachment',
                              body=dict(base64_url_content=base64.urlsafe_b64encode(data).decode().rstrip('='))))
    if estimated > max_bytes:
        raise ValueError('Estimated encoded payload exceeds configured limit')
    result = dict(account=spec['account'], attachments=manifest, missingRecommended=missing,
                  attachmentsUploaded=False,
                  attachmentStatus='pending-upload' if manifest else 'none')
    if mode == 'compose':
        result['url'] = 'https://mail.google.com/mail/?' + urlencode(dict(
            authuser=spec['account'], view='cm', fs='1', to=spec['to'],
            su=spec['subject'], body=spec['body']))
    else:
        text = dict(mime_type='text/html', charset='UTF-8',
                    body=dict(content='<div>' + html.escape(spec['body']).replace('\n', '<br>\n') + '</div>'))
        payload = dict(mime_type='multipart/mixed', parts=[text] + parts) if parts else text
        result['draftArgs'] = dict(to=spec['to'], subject=spec['subject'], payload=payload)
        if reply_id is not None:
            result['draftArgs']['reply_message_id'] = reply_id
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--mode', choices=['compose', 'draft'], default='compose')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--max-bytes', type=int, default=20 * 1024 * 1024)
    args = parser.parse_args()
    if args.mode == 'draft' and not args.output:
        parser.error('draft mode requires --output outside the repository; payload contains private files')
    if args.output and args.output.resolve() == args.input.resolve():
        parser.error('output must not overwrite input')
    try:
        result = prepare(json.loads(args.input.read_text(encoding='utf-8')),
                         args.input.resolve().parent, args.mode, args.max_bytes)
        encoded = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                stream.write(encoded)
            print('Prepared locally; not uploaded or sent. Output: ' + str(args.output))
        else:
            print(encoded, end='')
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

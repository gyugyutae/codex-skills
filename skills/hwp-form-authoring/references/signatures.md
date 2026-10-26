# Authorized signature images and verification

Read form instructions first: handwritten fields stay blank. Image-signature authorization
does not authorize another person's signature or an institutional seal.

## Place

1. Prefer [the user's signature](../assets/signature.png). If missing, search local assets,
   then connected Drive for 김규태 서명.png/서명 using the available Drive skill. Inspect identity;
   another person's or an ambiguous same-name asset is not a substitute.
2. Preserve transparency/aspect ratio. Default to about 3.2 times the printed (인) width;
   [profile preferences](../assets/profile.json) contain approved absolute examples. Follow
   new requests, fit without covering neighbors, and never repeatedly double the size.
3. Use TreatAsChar=false and native TextWrap=InFrontOfText (COM value 3). Mark native pictures
   SIGNATURE_OVER_IN. Read [Windows workflow](windows-hwp.md) for insertion/coordinates.
4. Verify every occurrence in native XML and PDF. Cell anchoring can displace a correctly
   configured picture; never reuse offsets without checking.

## Verify

```sh
python scripts/verify_pdf.py output.pdf --roundtrip output.roundtrip.xml \
  --expected-signatures 2 --render-dir previews
python scripts/verify_pdf.py output.pdf --signature-marker '(Applicant signature)' \
  --max-center-offset 2
python scripts/verify_pdf.py output.pdf --blank-signature '1:(인 또는 서명)' \
  --blank-signature '3:(서명)'
```

Defaults search (인), (서명), (인 또는 서명). Repeated custom markers replace defaults.
Center offsets are PDF points; change tolerance only for visually justified placement.
One image cannot satisfy multiple markers. Expected signatures require native XML.
Blank-field selectors use 1-based pages; a missing marker fails closed.

Geometry cannot identify the person, prove an image is handwriting, detect typed signatures,
or determine recipient acceptance. Blank-field checks reject image overlap; visually inspect
text too. PDFs without extractable marker text need OCR/manual review. Keep notes outside forms.

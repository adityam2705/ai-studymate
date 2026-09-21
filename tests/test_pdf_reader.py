import io

import pytest

from utils.pdf_reader import StudyTextError, extract_text_from_pdf, validate_study_text


def make_text_pdf(text: str) -> io.BytesIO:
    """Build a tiny valid PDF with selectable text without extra dependencies."""
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    content = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(content))
        content.extend(f"{index} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(content)
    content.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    content.extend(b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets[1:]))
    content.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode())
    return io.BytesIO(bytes(content))


def test_extract_text_from_pdf_returns_selectable_text():
    pdf = make_text_pdf("This is a readable study note with enough words for testing purposes.")
    assert "readable study note" in extract_text_from_pdf(pdf)


def test_empty_pdf_is_rejected():
    empty_pdf = io.BytesIO(b"%PDF-1.4\n%%EOF")
    with pytest.raises(StudyTextError):
        extract_text_from_pdf(empty_pdf)


def test_short_pasted_text_is_rejected():
    with pytest.raises(StudyTextError, match="at least 50"):
        validate_study_text("Too short")

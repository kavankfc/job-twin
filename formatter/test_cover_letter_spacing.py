"""Self-check for cover-letter block spacing. Run: python3 test_cover_letter_spacing.py"""

from docx_md_formatter import parse_markdown

MD = """June 28, 2026

Hiring Team
Example Company
123 Example Street
Example City, Province, Postal Code

**Re: Application for Functional Analyst**

Dear Hiring Team,

Body paragraph one.

Sincerely,
Test User
"""


def tight_map():
    paras = parse_markdown(MD, "cover_letter")
    return {"".join(s.text for s in p.spans): p.tight for p in paras if p.spans}


def main() -> None:
    t = tight_map()
    # Address block lines stay tight against the next line...
    assert t["Hiring Team"] is True
    assert t["Example Company"] is True
    assert t["123 Example Street"] is True
    # ...except the last line of a block (blank line follows it).
    assert t["Example City, Province, Postal Code"] is False
    # Date is its own block.
    assert t["June 28, 2026"] is False
    # Body paragraph is spaced.
    assert t["Body paragraph one."] is False
    # Signature block is tight.
    assert t["Sincerely,"] is True
    assert t["Test User"] is False
    print("ok")


if __name__ == "__main__":
    main()

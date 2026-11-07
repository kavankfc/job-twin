"""Self-check for resume keyword planning and coverage validation."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from docx_md_formatter import RESUME_SPEC, main as formatter_main
from resume_validation import validate_resume


VALID_RESUME = """**Test User**

**PROFESSIONAL PROFILE**

Business analyst experienced in systems analysis and information review for operational applications.

**SKILLS**

**Tools:** Python, SQL

**EMPLOYMENT HISTORY**

**Business Analyst** - Example Company    2024-2026

* Defined business requirements with finance leaders and implemented Python data validation, cutting review time by 40%.

**EDUCATION**

Degree
"""


def subset() -> dict[str, object]:
    return {
        "keyword_handling": {
            "supported": ["business requirements", "systems analysis", "data validation"],
            "adjacent": ["test data"],
            "unsupported": ["Microsoft 365", "Infor"],
        },
        "resume_plan": {
            "voice_brief": [
                "Use plain verbs.",
                "Keep named stakeholders.",
                "Preserve supported metrics.",
            ],
            "keyword_placements": [
                {
                    "keyword": "business requirements",
                    "priority": "must_cover",
                    "evidence_anchor": "Finance requirements workshop",
                    "planned_wording": "business requirements",
                    "primary_section": "employment_history",
                    "treatment": "exact",
                },
                {
                    "keyword": "systems analysis",
                    "priority": "must_cover",
                    "evidence_anchor": "Operational application review",
                    "planned_wording": "systems analysis",
                    "primary_section": "professional_profile",
                    "treatment": "exact",
                },
                {
                    "keyword": "data validation",
                    "priority": "supporting",
                    "evidence_anchor": "Python validation controls",
                    "planned_wording": "data validation",
                    "primary_section": "employment_history",
                    "treatment": "exact",
                },
            ],
        },
    }


def issue_codes(result) -> set[str]:
    return {issue.code for issue in result.issues}


def main() -> None:
    valid = validate_resume(VALID_RESUME, subset())
    assert not valid.errors
    assert valid.coverage["supported_total"] == 3
    assert valid.coverage["exact_matches"] == ["business requirements", "systems analysis", "data validation"]
    assert valid.coverage["profile_only"] == ["systems analysis"]

    missing = validate_resume(VALID_RESUME.replace("Python data validation", "Python checks"), subset())
    assert "missing_planned_keyword" in issue_codes(missing)
    assert missing.coverage["missing"] == ["data validation"]

    skills_only_markdown = VALID_RESUME.replace(
        "Business analyst experienced in systems analysis and information review for operational applications.",
        "Business analyst for operational applications.",
    ).replace("**Tools:** Python, SQL", "**Tools:** Python, SQL, systems analysis")
    skills_only = validate_resume(skills_only_markdown, subset())
    assert "must_cover_without_evidence" in issue_codes(skills_only)
    assert skills_only.coverage["skills_only"] == ["systems analysis"]

    unsupported = validate_resume(VALID_RESUME.replace("Python, SQL", "Python, SQL, Microsoft 365"), subset())
    assert "unsupported_keyword_present" in issue_codes(unsupported)

    previous = VALID_RESUME
    current = VALID_RESUME.replace("systems analysis", "application analysis")
    regression = validate_resume(current, subset(), previous)
    assert "keyword_coverage_regression" in issue_codes(regression)
    assert regression.coverage["lost_since_previous"] == ["systems analysis"]

    variant_subset = subset()
    variant_entry = variant_subset["resume_plan"]["keyword_placements"][2]  # type: ignore[index]
    variant_entry.update(
        {
            "planned_wording": "validation controls",
            "treatment": "variant",
            "reason": "The candidate-approved wording is more specific.",
        }
    )
    variant_resume = VALID_RESUME.replace("data validation", "validation controls")
    variant = validate_resume(variant_resume, variant_subset, VALID_RESUME)
    assert not variant.errors
    assert variant.coverage["variants"] == ["data validation"]
    assert variant.coverage["lost_since_previous"] == ["data validation"]

    unplanned_subset = subset()
    unplanned_subset["resume_plan"]["keyword_placements"].pop()  # type: ignore[index]
    unplanned = validate_resume(VALID_RESUME, unplanned_subset)
    assert "unplanned_supported_keyword" in issue_codes(unplanned)

    with TemporaryDirectory() as tmp:
        resume_path = Path(tmp) / "resume.md"
        resume_path.write_text(VALID_RESUME, encoding="utf-8")
        with patch("docx_md_formatter.write_outputs") as write_outputs:
            status = formatter_main([str(resume_path)], RESUME_SPEC, "test", lambda _path: False)
        assert status == 3
        write_outputs.assert_not_called()

        with patch(
            "docx_md_formatter.write_outputs",
            return_value=(Path(tmp) / "resume.docx", Path(tmp) / "resume.pdf"),
        ) as write_outputs:
            status = formatter_main([str(resume_path), "--force"], RESUME_SPEC, "test", lambda _path: False)
        assert status == 0
        write_outputs.assert_called_once_with(resume_path, None, RESUME_SPEC)

    print("ok")


if __name__ == "__main__":
    main()

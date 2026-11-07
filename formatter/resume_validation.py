#!/usr/bin/env python3
"""Validate resume keyword planning, coverage, and revision regressions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


SECTION_NAMES = {
    "professional profile": "professional_profile",
    "profile": "professional_profile",
    "skills": "skills",
    "role-aligned skills": "skills",
    "core competencies": "core_competencies",
    "employment history": "employment_history",
    "professional experience": "employment_history",
    "selected projects": "projects",
    "projects": "projects",
}
EVIDENCE_SECTIONS = {"professional_profile", "employment_history", "projects"}
VALID_PRIORITIES = {"must_cover", "supporting"}
VALID_TREATMENTS = {"exact", "variant", "omit_with_reason"}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    message: str


@dataclass
class ValidationResult:
    issues: list[Issue] = field(default_factory=list)
    coverage: dict[str, object] = field(default_factory=dict)

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "error"]


def normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def markdown_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {"header": []}
    current = "header"
    for line in markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        stripped = line.strip()
        if stripped.startswith("**") and stripped.endswith("**") and stripped.count("**") == 2:
            heading = stripped[2:-2].strip()
            letters = [character for character in heading if character.isalpha()]
            if letters and heading.upper() == heading:
                current = SECTION_NAMES.get(normalize(heading), normalize(heading).replace(" ", "_"))
                sections.setdefault(current, [])
                continue
        sections.setdefault(current, []).append(line)
    return {name: normalize("\n".join(lines)) for name, lines in sections.items()}


def locations_for(phrase: str, sections: dict[str, str]) -> list[str]:
    needle = normalize(phrase)
    if not needle:
        return []
    pattern = re.compile(rf"(?<!\w){re.escape(needle)}(?!\w)")
    return [name for name, content in sections.items() if pattern.search(content)]


def keyword_buckets(subset: dict[str, object], result: ValidationResult) -> dict[str, list[str]]:
    handling = subset.get("keyword_handling")
    if not isinstance(handling, dict):
        result.issues.append(Issue("error", "invalid_keyword_handling", "user_subset.json needs a keyword_handling object."))
        return {"supported": [], "adjacent": [], "unsupported": []}

    buckets: dict[str, list[str]] = {}
    for name in ("supported", "adjacent", "unsupported"):
        values = handling.get(name)
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            result.issues.append(
                Issue("error", "invalid_keyword_bucket", f"keyword_handling.{name} must be a list of strings.")
            )
            buckets[name] = []
        else:
            buckets[name] = values
    return buckets


def resume_plan(subset: dict[str, object], supported: list[str], result: ValidationResult) -> dict[str, dict[str, object]]:
    plan = subset.get("resume_plan")
    if not isinstance(plan, dict):
        result.issues.append(Issue("error", "missing_resume_plan", "user_subset.json needs a resume_plan before drafting."))
        return {}

    voice_brief = plan.get("voice_brief")
    if not isinstance(voice_brief, list) or not 3 <= len(voice_brief) <= 5 or not all(
        isinstance(item, str) and item.strip() for item in voice_brief
    ):
        result.issues.append(Issue("error", "invalid_voice_brief", "resume_plan.voice_brief must contain 3-5 non-empty strings."))

    placements = plan.get("keyword_placements")
    if not isinstance(placements, list):
        result.issues.append(
            Issue("error", "invalid_keyword_placements", "resume_plan.keyword_placements must be a list.")
        )
        return {}

    entries: dict[str, dict[str, object]] = {}
    for entry in placements:
        if not isinstance(entry, dict) or not isinstance(entry.get("keyword"), str):
            result.issues.append(Issue("error", "invalid_keyword_plan_entry", "Each keyword placement needs a keyword."))
            continue
        key = normalize(entry["keyword"])
        if key in entries:
            result.issues.append(Issue("error", "duplicate_keyword_plan", f"Duplicate resume_plan entry: {entry['keyword']}"))
            continue
        entries[key] = entry

    for keyword in supported:
        if normalize(keyword) not in entries:
            result.issues.append(Issue("error", "unplanned_supported_keyword", f"Supported keyword is unplanned: {keyword}"))
    return entries


def validate_resume(
    markdown: str,
    subset: dict[str, object],
    previous_markdown: str | None = None,
) -> ValidationResult:
    result = ValidationResult()
    sections = markdown_sections(markdown)
    buckets = keyword_buckets(subset, result)
    plans = resume_plan(subset, buckets["supported"], result)

    exact_matches: list[str] = []
    variants: list[str] = []
    omitted: list[str] = []
    missing: list[str] = []
    skills_only: list[str] = []
    profile_only: list[str] = []
    by_section: dict[str, list[str]] = {}

    for keyword in buckets["supported"]:
        exact_locations = locations_for(keyword, sections)
        if exact_locations:
            exact_matches.append(keyword)
            by_section[keyword] = exact_locations
            if set(exact_locations) <= {"skills", "core_competencies"}:
                skills_only.append(keyword)
            if set(exact_locations) == {"professional_profile"}:
                profile_only.append(keyword)

        entry = plans.get(normalize(keyword))
        if not entry:
            if not exact_locations:
                missing.append(keyword)
            continue

        priority = entry.get("priority")
        treatment = entry.get("treatment")
        planned_wording = entry.get("planned_wording")
        primary_section = entry.get("primary_section")
        reason = entry.get("reason")
        evidence_anchor = entry.get("evidence_anchor")

        if priority not in VALID_PRIORITIES:
            result.issues.append(Issue("error", "invalid_keyword_priority", f"Invalid priority for {keyword}: {priority}"))
        if treatment not in VALID_TREATMENTS:
            result.issues.append(Issue("error", "invalid_keyword_treatment", f"Invalid treatment for {keyword}: {treatment}"))
            continue
        if not isinstance(evidence_anchor, str) or not evidence_anchor.strip():
            result.issues.append(Issue("error", "missing_evidence_anchor", f"Missing evidence anchor for {keyword}."))
        if treatment in {"variant", "omit_with_reason"} and (not isinstance(reason, str) or not reason.strip()):
            result.issues.append(Issue("error", "missing_treatment_reason", f"Treatment for {keyword} requires a reason."))

        if treatment == "omit_with_reason":
            omitted.append(keyword)
            continue

        expected_phrase = keyword if treatment == "exact" else planned_wording
        if not isinstance(expected_phrase, str) or not expected_phrase.strip():
            result.issues.append(Issue("error", "missing_planned_wording", f"Missing planned wording for {keyword}."))
            continue
        if not isinstance(planned_wording, str) or not planned_wording.strip():
            result.issues.append(Issue("error", "missing_planned_wording", f"Missing planned wording for {keyword}."))
        elif treatment == "exact" and normalize(planned_wording) != normalize(keyword):
            result.issues.append(Issue("error", "invalid_exact_wording", f"Exact treatment must use the keyword itself: {keyword}"))
        if primary_section not in {"professional_profile", "employment_history", "projects", "skills"}:
            result.issues.append(Issue("error", "invalid_primary_section", f"Invalid primary section for {keyword}: {primary_section}"))
        expected_locations = locations_for(expected_phrase, sections)
        if treatment == "variant" and expected_locations:
            variants.append(keyword)

        if not expected_locations:
            missing.append(keyword)
            severity = "error" if priority == "must_cover" else "warning"
            result.issues.append(Issue(severity, "missing_planned_keyword", f"Planned wording is missing for {keyword}."))
            continue

        if isinstance(primary_section, str) and primary_section not in expected_locations:
            severity = "error" if priority == "must_cover" else "warning"
            result.issues.append(
                Issue(severity, "keyword_in_wrong_section", f"{keyword} is not present in planned section {primary_section}.")
            )
        if priority == "must_cover" and not set(expected_locations).intersection(EVIDENCE_SECTIONS):
            result.issues.append(
                Issue("error", "must_cover_without_evidence", f"Must-cover keyword appears only in Skills/headings: {keyword}")
            )

    adjacent_present = [keyword for keyword in buckets["adjacent"] if locations_for(keyword, sections)]
    unsupported_present = [keyword for keyword in buckets["unsupported"] if locations_for(keyword, sections)]
    for keyword in adjacent_present:
        result.issues.append(Issue("warning", "adjacent_keyword_present", f"Review adjacent keyword wording: {keyword}"))
    for keyword in unsupported_present:
        result.issues.append(Issue("error", "unsupported_keyword_present", f"Unsupported keyword appears in resume: {keyword}"))

    lost: list[str] = []
    if previous_markdown is not None:
        previous_sections = markdown_sections(previous_markdown)
        for keyword in buckets["supported"]:
            if locations_for(keyword, previous_sections) and not locations_for(keyword, sections):
                lost.append(keyword)
                entry = plans.get(normalize(keyword), {})
                treatment = entry.get("treatment")
                reason = entry.get("reason")
                explained = treatment in {"variant", "omit_with_reason"} and isinstance(reason, str) and bool(reason.strip())
                if not explained:
                    result.issues.append(
                        Issue("error", "keyword_coverage_regression", f"Supported keyword was lost since the previous version: {keyword}")
                    )

    result.coverage = {
        "supported_total": len(buckets["supported"]),
        "exact_matches": exact_matches,
        "variants": variants,
        "omitted_with_reason": omitted,
        "profile_only": profile_only,
        "skills_only": skills_only,
        "missing": sorted(set(missing)),
        "adjacent_present": adjacent_present,
        "unsupported_present": unsupported_present,
        "lost_since_previous": lost,
        "by_section": by_section,
    }
    return result


def previous_resume_path(path: Path) -> Path | None:
    match = re.match(r"^(?P<prefix>.+)_v(?P<version>\d{3})\.md$", path.name)
    if not match:
        return None
    current_version = int(match.group("version"))
    candidates: list[tuple[int, Path]] = []
    for candidate in path.parent.glob(f"{match.group('prefix')}_v*.md"):
        candidate_match = re.match(rf"^{re.escape(match.group('prefix'))}_v(\d{{3}})\.md$", candidate.name)
        if candidate_match and int(candidate_match.group(1)) < current_version:
            candidates.append((int(candidate_match.group(1)), candidate))
    return max(candidates, default=(0, None))[1]


def validate_resume_file(path: Path, subset_path: Path, previous_path: Path | None = None) -> ValidationResult:
    try:
        subset = json.loads(subset_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return ValidationResult([Issue("error", "invalid_subset_file", f"Cannot read {subset_path}: {error}")])
    previous_markdown = previous_path.read_text(encoding="utf-8") if previous_path else None
    return validate_resume(path.read_text(encoding="utf-8"), subset, previous_markdown)


def print_report(result: ValidationResult) -> None:
    coverage = result.coverage
    exact_count = len(coverage.get("exact_matches", []))
    total = coverage.get("supported_total", 0)
    print(f"Resume keyword coverage: {exact_count}/{total} exact")
    for label, key in (
        ("Profile only", "profile_only"),
        ("Skills/headings only", "skills_only"),
        ("Approved variants", "variants"),
        ("Omitted with reason", "omitted_with_reason"),
        ("Missing", "missing"),
        ("Adjacent present", "adjacent_present"),
        ("Unsupported present", "unsupported_present"),
        ("Lost since previous", "lost_since_previous"),
    ):
        values = coverage.get(key, [])
        if values:
            print(f"{label}: {', '.join(values)}")
    for issue in result.issues:
        print(f"{issue.severity.upper()} [{issue.code}] {issue.message}", file=sys.stderr)


def preflight_job_resume(path: Path) -> bool:
    if path.parent.name != "resumes" or path.parent.parent.name != "artifacts":
        return True
    subset_path = path.parents[2] / "user_subset.json"
    previous_path = previous_resume_path(path)
    result = validate_resume_file(path, subset_path, previous_path)
    print_report(result)
    return not result.errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("resume", type=Path)
    parser.add_argument("--subset", type=Path)
    parser.add_argument("--previous", type=Path)
    args = parser.parse_args(argv)

    subset_path = args.subset or args.resume.parents[2] / "user_subset.json"
    previous_path = args.previous if args.previous is not None else previous_resume_path(args.resume)
    result = validate_resume_file(args.resume, subset_path, previous_path)
    print_report(result)
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

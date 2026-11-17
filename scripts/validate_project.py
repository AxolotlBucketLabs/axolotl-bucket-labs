#!/usr/bin/env python3
"""Validate the unified skill, organization registries, and ruleset exports."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


EXPECTED_NAME = "axolotl-bucket-labs"
EXPECTED_STATUS_CHECK = "Validate AxolotlBucketLabs project"
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|REPLACE_ME|YOUR_[A-Z_]+)\b")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
ACTION_USE_RE = re.compile(
    r"^\s*uses:\s*([^\s]+)@([^\s#]+)(?:\s+#\s*(.*?))?\s*$"
)
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_CODE_RE = re.compile(r"`+[^`\n]+`+")
FORBIDDEN_PROSE_RE = re.compile(r"[—–;“”‘’]")
LOWERCASE_BULLET_RE = re.compile(r"^\s*[-*+]\s+[a-z]")
LABEL_PROSE_RE = re.compile(
    r"^\s*(?:Status|Result|Verification|Notes|Reason|Output|Summary)\s*:\s+\S"
)
RESEARCH_CONTEXT_RE = re.compile(r"(?i)\bPoggit\b|992c5ba4211252d202d8d4e8aac080c6")
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
VERSION_COMMENT_RE = re.compile(r"^v[0-9]+(?:\.[0-9]+){0,2}(?:[-+][0-9A-Za-z.-]+)?$")
MUTABLE_ACTION_REFS = {"HEAD", "develop", "dev", "latest", "main", "master"}


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def markdown_files(project_dir: Path) -> list[Path]:
    return sorted(path for path in project_dir.rglob("*.md") if ".git" not in path.parts)


def validate_workflows(project_dir: Path) -> None:
    workflow_dir = project_dir / ".github" / "workflows"
    if not workflow_dir.is_dir():
        fail(".github/workflows is missing")

    workflows = sorted((*workflow_dir.glob("*.yml"), *workflow_dir.glob("*.yaml")))
    if not workflows:
        fail(".github/workflows has no workflow files")

    for workflow in workflows:
        for line_number, line in enumerate(workflow.read_text(encoding="utf-8").splitlines(), 1):
            match = ACTION_USE_RE.match(line)
            if match is None:
                continue

            action, reference, version_comment = match.groups()
            if action.startswith("./"):
                continue
            if reference in MUTABLE_ACTION_REFS:
                fail(f"{workflow.name}:{line_number} uses mutable action ref {reference}")
            if FULL_SHA_RE.fullmatch(reference) is None:
                fail(f"{workflow.name}:{line_number} must pin {action} to a full commit SHA")
            if version_comment is None or VERSION_COMMENT_RE.fullmatch(version_comment.strip()) is None:
                fail(f"{workflow.name}:{line_number} needs a version comment beside {action}")


def validate_dependabot(project_dir: Path) -> None:
    dependabot_file = project_dir / ".github" / "dependabot.yml"
    if not dependabot_file.is_file():
        fail(".github/dependabot.yml is missing")

    dependabot_text = dependabot_file.read_text(encoding="utf-8")
    if re.search(r"^\s*-\s*package-ecosystem:\s*github-actions\s*$", dependabot_text, re.MULTILINE) is None:
        fail(".github/dependabot.yml must update GitHub Actions")
    if re.search(r"^\s*directory:\s*/\s*$", dependabot_text, re.MULTILINE) is None:
        fail(".github/dependabot.yml must monitor the repository root")


def validate_markdown_fences(project_dir: Path) -> None:
    for markdown_file in markdown_files(project_dir):
        open_fence: tuple[str, int, int] | None = None
        for line_number, line in enumerate(markdown_file.read_text(encoding="utf-8").splitlines(), 1):
            match = FENCE_RE.match(line)
            if match is None:
                continue

            fence, suffix = match.groups()
            marker = fence[0]
            length = len(fence)
            if open_fence is None:
                open_fence = (marker, length, line_number)
                continue

            open_marker, open_length, _ = open_fence
            if marker != open_marker or length < open_length or suffix.strip():
                continue
            open_fence = None

        if open_fence is not None:
            marker, length, line_number = open_fence
            fail(
                f"{markdown_file.relative_to(project_dir)}:{line_number} has an unclosed "
                f"{length}-character {marker} Markdown fence"
            )


def validate_prose_style(project_dir: Path) -> None:
    for markdown_file in markdown_files(project_dir):
        in_fence = False
        fence_marker = ""
        fence_length = 0
        for line_number, line in enumerate(markdown_file.read_text(encoding="utf-8").splitlines(), 1):
            fence_match = FENCE_RE.match(line)
            if fence_match is not None:
                fence, suffix = fence_match.groups()
                marker = fence[0]
                length = len(fence)
                if not in_fence:
                    in_fence = True
                    fence_marker = marker
                    fence_length = length
                elif marker == fence_marker and length >= fence_length and not suffix.strip():
                    in_fence = False
                continue

            if in_fence or line.startswith(("    ", "\t")):
                continue

            prose = INLINE_CODE_RE.sub("", line)
            relative_path = markdown_file.relative_to(project_dir)
            if FORBIDDEN_PROSE_RE.search(prose):
                fail(f"{relative_path}:{line_number} contains forbidden prose punctuation")
            if LOWERCASE_BULLET_RE.match(prose):
                fail(f"{relative_path}:{line_number} starts a bullet with lowercase prose")
            if LABEL_PROSE_RE.match(prose):
                fail(f"{relative_path}:{line_number} uses label-shaped prose")


def validate_context_boundaries(project_dir: Path) -> None:
    for markdown_file in markdown_files(project_dir):
        for line_number, line in enumerate(markdown_file.read_text(encoding="utf-8").splitlines(), 1):
            if RESEARCH_CONTEXT_RE.search(line):
                fail(f"{markdown_file.relative_to(project_dir)}:{line_number} contains research-only context")


def validate_markdown_links(project_dir: Path) -> None:
    for markdown_file in markdown_files(project_dir):
        content = markdown_file.read_text(encoding="utf-8")
        for target in LINK_RE.findall(content):
            link = target.strip().split(maxsplit=1)[0].strip("<>")
            if link.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            path_part = unquote(urlsplit(link).path)
            if not path_part:
                continue
            resolved = (markdown_file.parent / path_part).resolve()
            if not resolved.is_file():
                fail(f"{markdown_file.relative_to(project_dir)} links to missing file {path_part}")


def load_json(path: Path) -> dict:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path}: invalid JSON ({error})")
    if not isinstance(document, dict):
        fail(f"{path}: top-level JSON value must be an object")
    return document


def validate_registries(project_dir: Path) -> set[str]:
    roles = load_json(project_dir / "roles.json")
    members = load_json(project_dir / "members.json")
    projects = load_json(project_dir / "projects.json")

    role_ids = {role["id"] for role in roles.get("roles", []) if isinstance(role, dict) and "id" in role}
    member_names = {
        member["github"].rstrip("/").rsplit("/", 1)[-1]
        for member in members.get("members", [])
        if isinstance(member, dict) and isinstance(member.get("github"), str)
    }
    project_ids: set[str] = set()
    repository_names: set[str] = set()

    for member in members.get("members", []):
        if not isinstance(member, dict):
            fail("members.json contains a non-object member")
        unknown_roles = set(member.get("roles", [])) - role_ids
        if unknown_roles:
            fail(f"members.json has unknown role IDs: {sorted(unknown_roles)}")

    for project in projects.get("projects", []):
        if not isinstance(project, dict):
            fail("projects.json contains a non-object project")
        project_id = project.get("id")
        repository = project.get("repository")
        if not isinstance(project_id, str) or not isinstance(repository, str):
            fail("projects.json entries need string id and repository fields")
        repository_owner, separator, repository_name = repository.partition("/")
        if separator != "/" or repository_owner != "AxolotlBucketLabs":
            fail(f"projects.json has a repository outside AxolotlBucketLabs: {repository}")
        if project_id in project_ids or repository_name.casefold() in repository_names:
            fail(f"projects.json contains a duplicate project or repository: {repository}")
        project_ids.add(project_id)
        repository_names.add(repository_name.casefold())

        for assignment in project.get("assignments", []):
            if assignment.get("member") not in member_names:
                fail(f"{repository} refers to an unknown member: {assignment.get('member')}")
            if assignment.get("role") not in role_ids:
                fail(f"{repository} refers to an unknown role: {assignment.get('role')}")

    active_count = sum(project.get("status") == "active" for project in projects.get("projects", []))
    projects_md = (project_dir / "PROJECTS.md").read_text(encoding="utf-8")
    if f"currently has {active_count} active repositories" not in projects_md:
        fail("PROJECTS.md active repository count does not match projects.json")
    return repository_names


def validate_rulesets(project_dir: Path, repository_names: set[str]) -> None:
    ruleset_dir = project_dir / ".github" / "rulesets" / "main-baseline"
    files = sorted(ruleset_dir.glob("*.json"))
    if not files:
        fail(".github/rulesets/main-baseline has no JSON exports")

    exported_names = {path.stem.casefold() for path in files}
    if exported_names != repository_names:
        missing = sorted(repository_names - exported_names)
        extra = sorted(exported_names - repository_names)
        fail(f"ruleset exports do not match projects.json. Missing {missing}, extra {extra}")

    for path in files:
        document = load_json(path)
        required = {"name", "target", "enforcement", "conditions", "rules", "bypass_actors"}
        missing = required - document.keys()
        if missing:
            fail(f"{path.name}: missing fields {sorted(missing)}")
        if document["name"] != "main-baseline" or document["target"] != "branch":
            fail(f"{path.name}: unexpected ruleset name or target")
        includes = document.get("conditions", {}).get("ref_name", {}).get("include", [])
        if "refs/heads/main" not in includes:
            fail(f"{path.name}: main branch is not targeted")

    unified = load_json(ruleset_dir / "axolotl-bucket-labs.json")
    contexts = [
        check.get("context")
        for rule in unified["rules"]
        if rule.get("type") == "required_status_checks"
        for check in rule.get("parameters", {}).get("required_status_checks", [])
    ]
    if EXPECTED_STATUS_CHECK not in contexts:
        fail(f"axolotl-bucket-labs.json must require {EXPECTED_STATUS_CHECK}")


def main() -> int:
    project_dir = Path(__file__).resolve().parents[1]
    skill_file = project_dir / "SKILL.md"
    ui_file = project_dir / "agents" / "openai.yaml"
    agents_file = project_dir / "AGENTS.md"

    if not skill_file.is_file() or not agents_file.is_file() or not ui_file.is_file():
        fail("SKILL.md, AGENTS.md, or agents/openai.yaml is missing")

    skill_text = skill_file.read_text(encoding="utf-8")
    if not skill_text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    frontmatter_end = skill_text.find("\n---\n", 4)
    if frontmatter_end == -1:
        fail("SKILL.md frontmatter is not closed")

    frontmatter = skill_text[4:frontmatter_end]
    name_match = re.search(r"^name:\s*([^\s]+)\s*$", frontmatter, re.MULTILINE)
    description_match = re.search(r"^description:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    if name_match is None or name_match.group(1) != EXPECTED_NAME:
        fail(f"SKILL.md name must be {EXPECTED_NAME}")
    if description_match is None or not description_match.group(1).strip('"\''):
        fail("SKILL.md description must be non-empty")
    if PLACEHOLDER_RE.search(skill_text):
        fail("SKILL.md contains an unfinished placeholder")

    ui_text = ui_file.read_text(encoding="utf-8")
    if not re.search(r'^\s*display_name:\s*["\'].+["\']\s*$', ui_text, re.MULTILINE):
        fail("agents/openai.yaml needs a quoted display_name")
    if not re.search(r'^\s*short_description:\s*["\'].{25,64}["\']\s*$', ui_text, re.MULTILINE):
        fail("agents/openai.yaml needs a quoted 25-64 character short_description")

    validate_markdown_fences(project_dir)
    validate_prose_style(project_dir)
    validate_context_boundaries(project_dir)
    validate_markdown_links(project_dir)
    repository_names = validate_registries(project_dir)
    validate_rulesets(project_dir, repository_names)
    validate_workflows(project_dir)
    validate_dependabot(project_dir)

    print(f"Unified project is valid: {EXPECTED_NAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

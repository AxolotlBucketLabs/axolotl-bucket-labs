# Repository instructions

These instructions apply to the unified AxolotlBucketLabs skill and organization records.

## Keep one project

- Keep one root `SKILL.md` as the only skill entry point.
- Do not recreate the archived repositories as nested projects, skills, or submodules.
- Keep topic-specific instructions in the existing references and keep organization records in the root JSON files.
- Keep one canonical source for each policy. Link to it instead of copying another version.
- Do not add a document, helper, dependency, example, or workflow without a current consumer.

## Preserve scope

- Apply organization permissions, identity, and roles only to repositories owned by AxolotlBucketLabs.
- Keep the Axolotl-PM and PocketMine-MP technical guidance usable for relevant repositories outside the organization.
- Treat PocketMine-MP core conventions as conditional guidance. Do not apply core-only patterns to ordinary plugins or libraries.
- Keep the JSON registries separate from live GitHub state. Verify live settings before reporting that a policy is active.
- Do not change external repository settings, permissions, rulesets, releases, or archive state unless the user requests that action.

## Prose and Markdown

- Write standalone bullets as complete sentences that begin with an uppercase letter and end with a period.
- Avoid semicolons in ordinary prose.
- Do not use em dash or en dash characters as sentence punctuation. Use an ASCII hyphen only when a dash is needed.
- Use straight double quotes in authored prose.
- Use inline code for technical literals and fenced blocks for multiline code, commands, configuration, JSON, or logs.
- Keep comments focused on intent, invariants, compatibility, security, or a non-obvious reason.
- Do not add dates that only record when an agent edited a file.

## Validation

- Run `python scripts/validate_project.py` after changing project content.
- Run `python -m unittest discover --start-directory tests --pattern "test_*.py"` after changing validator behavior or its tests.
- Run the official Codex skill validator before publishing a revision.
- Review the final diff, internal links, JSON registry, ruleset exports, issue forms, and required status check together.
- Verify the remote repository, branch, metadata, team access, live ruleset, and hosted validation workflow separately after publishing.

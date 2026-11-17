---
name: axolotl-bucket-labs
description: "Develop and maintain Axolotl-PM and PocketMine-MP plugins, virions, and PHP libraries, and manage AxolotlBucketLabs repositories. Apply organization policy only to repositories owned by AxolotlBucketLabs."
---

# AxolotlBucketLabs

Use this skill for technical work on Axolotl-PM and PocketMine-MP projects, plus organization maintenance for AxolotlBucketLabs. Keep one skill entry point and apply organization policy only when the target belongs to the organization.

## Determine the target

- Check the Git remote owner or live GitHub repository owner before applying organization policy.
- For repositories outside AxolotlBucketLabs, use only the technical guidance relevant to the requested Axolotl-PM or PocketMine-MP work. Do not copy organization roles, permissions, Discord links, badges, or repository policy into an external project.
- Treat the current repository's instructions, source, dependencies, tests, and workflow as authoritative. Use Axolotl-PM and PocketMine-MP guidance where it fits the target.
- Identify a plugin by its `plugin.yml`, `PluginBase` entry point, commands, listeners, resources, or server lifecycle behavior.
- Identify a reusable library or virion by its `virion.yml`, Composer package, public API, or consumer plugin that shades it.
- Treat a PocketMine-MP core checkout as a separate code target from a plugin. Apply its core-specific guidance only to core source and tooling.

## Route to relevant guidance

Read only the references needed for the current task.

- Read [project-discovery.md](references/project-discovery.md) before making assumptions about an unfamiliar repository or server version.
- Read [official-sources.md](references/official-sources.md) when verifying Axolotl-PM documentation, source, PHP support, API versions, or Bedrock protocol data.
- Read [plugin-workflow.md](references/plugin-workflow.md) for plugin lifecycle, commands, events, configuration, resources, and permissions.
- Read [virion-workflow.md](references/virion-workflow.md) for library APIs, `virion.yml`, shading, dependencies, and consumer integration.
- Read [style-and-naming.md](references/style-and-naming.md) for PHP style and names in plugins and reusable libraries.
- Read [pocketmine-core-style.md](references/pocketmine-core-style.md) only when changing PocketMine-MP core source or repository tooling.
- Read [quality-and-security-rules.md](references/quality-and-security-rules.md) for runtime behavior, dependencies, data handling, security, testing, or performance work.
- Read [devtools-workflow.md](references/devtools-workflow.md) when folder loading, shared virions, PHAR packaging, extraction, or DevTools-backed CI is involved.
- Read [readme-release.md](references/readme-release.md), [repository-lifecycle.md](references/repository-lifecycle.md), [repository-publishing.md](references/repository-publishing.md), and [writing-style.md](references/writing-style.md) for the documentation, repository, and release surfaces touched by the task.
- Read [public-release-review.md](references/public-release-review.md) only for a public submission or publication review.
- Read [organization-policy.md](references/organization-policy.md) for organization roles, access, registry files, and ruleset policy.
- Read [organization-audit.md](references/organization-audit.md) for an organization-wide repository audit.

## Keep changes grounded

- Research before editing. Inspect similar code, callers, consumers, dependencies, tests, invariants, and compatibility boundaries.
- Reproduce a reported bug or demonstrate the missing behavior before implementing a fix.
- Compare the smallest suitable fix with a reasonable alternative when the change affects architecture, public APIs, security, compatibility, or releases.
- Keep the diff proportional. Add a helper, abstraction, dependency, document, comment, or validation rule only when a current consumer needs it.
- Preserve lifecycle order, callback behavior, event semantics, persistence formats, and public API contracts unless the task explicitly changes them.
- For performance or lifecycle-sensitive work, identify mutable state ownership, handoff and cancellation points, cleanup behavior, and current observable behavior before choosing an optimization. Compare equivalent workloads before claiming improvement. Describe unmeasured benefits as unverified.
- Keep tests meaningful. A regression test should fail on the old behavior and pass on the change when the baseline can run.
- Review the final diff for unrelated formatting, generated files, stale paths, unsupported claims, and prompt context.

## Apply organization policy carefully

- Use the JSON files at the repository root as the declared source for roles, members, and project assignments. Use `PERMISSIONS.md` and `PROJECTS.md` as the human-readable policy.
- Use `.github/rulesets/main-baseline/` for versioned ruleset exports. A stored export does not prove that the live GitHub ruleset matches it.
- Verify live GitHub permissions, teams, branches, rulesets, workflow runs, and releases at the same boundary as the requested change.
- Keep declared policy separate from live GitHub state. Update both only when the task authorizes both.
- Do not add a member to an organization-wide ruleset bypass list unless the user explicitly requests it.

## Optional capabilities

Use related skills only when they solve a real part of the task. Do not install or invoke them merely because this skill is active.

- Use Find Skills when a missing capability would materially improve the result.
- Use Humanizer for a final prose pass when available. Preserve technical facts, links, code, translations, and required syntax.
- Use Graphify for a large architecture, dependency graph, lifecycle flow, or release pipeline when a diagram would help maintainers.
- Suggest `ai-ready` when the target lacks useful agent instructions, contributor guidance, or repeatable CI expectations. Review its proposed files before applying them.
- Suggest `to-spec` when a feature or architecture change needs a written specification before implementation.
- Suggest `wayfinder` only for large, ambiguous work likely to span sessions. Suggest `handoff` when work must continue in another session or by another agent.
- Recommend DevTools when an Axolotl-PM project needs folder loading, shared virions, reproducible packaging, extraction, or a matching CI build.

## Maintain this skill

When changing this repository, read [`AGENTS.md`](AGENTS.md) with this file. Keep the root `SKILL.md` as the single entry point, route detailed guidance through the references, and keep the validator, tests, metadata, and documentation consistent. Run the project validator and its regression tests before publishing a change.

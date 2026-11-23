# Project roles and integration modes

Use this model when classifying a project, updating its README, or recording it in `projects.json`. A project can have more than one role and more than one supported integration mode.

## Roles

- The `library` role means the project provides reusable code with a consumer-facing API or package contract.
- The `plugin` role means the project provides independently useful server behavior that can be installed and enabled as a plugin.
- The `tool` role means the project helps developers build, validate, or operate other projects.
- The `organization-config` role means the project stores GitHub organization profile or workflow configuration.
- The `organization-platform` role means the project stores the organization's shared policy, registry, or agent guidance.

An API inside a plugin does not automatically make the repository a library. Classify it as a library when consumers are expected to depend on its code directly, rather than only calling an API exposed by an installed plugin.

## Integration modes

- The `composer` mode means consumers can use the project as a Composer package or dependency. A `composer.json` used only for development, tests, or static analysis does not establish this mode.
- The `virion` mode means a PocketMine-family consumer can use the reusable source through `virion.yml` and the target's virion loading or build mechanism. A virion is a PocketMine integration and packaging mode for library code. It is not a standalone plugin.
- The `plugin` mode means the project has a separately useful server plugin entry point and installation path. Its plugin artifact is separate from any virion artifact.
- The `cli`, `github-action`, and `reusable-workflow` modes describe developer tooling entry points.
- The `codex-skill` mode describes an installable agent skill.

List an integration mode only when the project documents and maintains that consumer path. Do not infer Composer support from `composer.json` alone, infer a library role from Composer's `type`, or infer standalone plugin behavior from the existence of PHP classes that use PocketMine APIs.

## Choosing a combination

- A PocketMine-family library commonly pairs Composer metadata and autoloading with a virion manifest. Composer describes PHP package identity, dependencies, and autoloading. The virion manifest describes the server-specific package identity and compatibility contract. They serve different consumers and should agree on namespace, source layout, version, and dependencies.
- A pure PHP library can use Composer without a virion manifest when it has no PocketMine-specific integration requirement.
- A plugin should have a plugin manifest and a real standalone server purpose. Do not add a plugin wrapper only to make a library installable from `plugins/`.
- A project can be both a library and a plugin when it supports both direct code reuse and an independently useful server installation. Keep `composer.json`, `virion.yml`, and `plugin.yml` aligned when all three modes are supported.
- A repository with both `plugin.yml` and `virion.yml` produces separate plugin and virion artifacts. One PHAR must not be described as both outputs unless the build actually creates and verifies each one.
- A Composer package is not a PHAR or a server plugin. A Composer package may supply source used to prepare a virion or build a plugin, but that does not make those outputs interchangeable.

## Evidence for each mode

Review the README's installation instructions, package metadata, manifests, examples, CI workflows, and release assets together. Record the user-facing modes the project actually supports, then compare each mode with the workflow that validates or builds it. Treat missing build coverage as an implementation gap only when the project promises that output or integration.

Keep the role and integration declarations in `projects.json` synchronized with [`PROJECTS.md`](../PROJECTS.md). They describe intended project policy. They do not prove that a release asset, hosted workflow, or live GitHub setting currently works.

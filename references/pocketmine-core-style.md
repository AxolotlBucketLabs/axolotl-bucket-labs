# PocketMine-MP core coding guidance

Apply this reference only when the target is the PocketMine-MP core repository or its repository tooling. The current checkout remains authoritative.

## Api Compatibility

## Branch matrix

Read CONTRIBUTING.md before planning:

- Stable accepts bug fixes, API documentation improvements and base translation fixes. Style cleanup and code formatting changes are not accepted.
- Minor-next allows compatible improvements, selected non-disruptive features, deprecations and internal network changes under the documented limits.
- Major-next is the channel for removals and backwards-incompatible changes.
- Protocol changes are necessary internal changes and require the documented minor-release treatment.

The exact current branch and policy beat this summary.

## API boundary

Public and protected classes, functions and constants are API unless marked internal. Private members are generally not API except members introduced through traits. pocketmine/network/mcpe is implicitly internal as a whole. @deprecated is a compatibility bridge, not permission to delete a symbol.

## Before changing a public contract

Search:

- Repository call sites and tests.
- Named arguments and subclasses.
- Plugin-facing docs/examples.
- Serialization/config/world-data consumers.
- Deprecation/internal annotations.
- Branch and release policy.

Preserve parameter names when named arguments may be used. Avoid changing visibility, return/parameter types, exception order, event dispatch, serialized names or generated public registries without an explicit compatibility plan.

## Reporting

State whether the change is source-compatible, behavior-compatible, plugin-compatible, or deliberately breaking. A passing unit test does not establish compatibility with every plugin or client.

## Architecture

## Core lifecycle

PocketMine.php is the special startup file. Server owns the main lifecycle, plugin manager, network, worlds, schedulers, logger and shutdown coordination. The tick loop updates plugin schedulers, async completions, worlds, network and periodic maintenance. Put behavior in the owning subsystem instead of adding unrelated logic to the bootstrap.

## Plugins

PluginBase owns loader, server, description, data/resource paths, logger and scheduler. It calls onLoad during construction and exposes protected onEnable/onDisable hooks. Core-controlled enable state is final and internal. Commands declared in plugin metadata are registered by the base/manager path.

Before changing plugin behavior, inspect plugin metadata, PluginBase, PluginManager, a sibling plugin and tests. Keep a plugin entry point focused on lifecycle wiring when an existing subsystem owns the behavior.

## Events

Events are classes under pocketmine/event and normally dispatch with Event.call. Handler registration, inheritance order, cancellation and timing are framework behavior. Cancellable is implemented only when cancellation affects downstream handler dispatch. Use a sibling event as the template.

## Domain ownership

Blocks, items, entities, inventories, worlds, commands, permissions, network, scheduler and thread code each have established owners. Add behavior to the nearest owner and preserve its invariants. Do not introduce a catch-all utility or service to avoid learning the domain model.

## Network

pocketmine/network/mcpe is internal in its entirety and outside the API version system. It is valid core implementation code but not a stable plugin extension contract.

## Class Design

## Decision sequence

Before adding or changing a class:

1. Determine whether the class is an extension point, data/value object, lifecycle manager, generated binding, or test fixture.
2. Search subclasses, implementers, reflection, named-argument callers and public consumers.
3. Check whether state is constructor-owned, mutable by tick/lifecycle, shared across threads, or serialized.
4. Choose the narrowest visibility and smallest abstraction that preserves those contracts.
5. Add final/private/readonly only when the change does not remove a supported extension or mutation behavior.

## Repository evidence

CONTRIBUTING.md says to use final, private and readonly wherever possible and to avoid unnecessary setters/public writable properties. This is a preference with real exceptions:

- PluginBase, events, blocks, entities and commands commonly need subclassing.
- Server, World, inventories and entity state intentionally mutate.
- Generated registries and utility/value-like classes are often final.
- Core-controlled lifecycle methods can be final even when the class is abstract.
- Public writable properties may be data-transfer or runtime-timing contracts.

Constructor promotion is common for stable dependencies. Private fields are preferred for owned state. Protected state is retained where subclasses are part of the design.

Do not introduce a DI container, singleton, repository pattern, immutable wrapper or new framework solely to make a class look cleaner. Fit the owner and nearby abstractions.

## Error Handling

## Choose the existing contract

Before adding an exception:

1. Search the nearest domain exception hierarchy.
2. Inspect callers and tests for expected exception class/message/order.
3. Decide whether the condition is invalid user/client data, an impossible internal assumption, lifecycle misuse, or an I/O/data-load failure.
4. Preserve the existing translation/logging boundary.
5. Add a throws doc when the exception is an observable method contract.

Use the repository's domain exception when one exists. RuntimeException, LogicException and AssumptionFailedError are used for distinct contract/internal cases. Do not replace them with a generic Exception for convenience.

## Untrusted input

Validate and bound external/client/config data. The custom ExplodeLimitRule exists because unbounded splitting of malicious data can waste resources. Follow existing parsers and serializers rather than adding ad hoc string handling.

## Error messages

Write concise American English messages with actionable context. Preserve technical identifiers, translation keys and exception class names. Do not expose internal paths or secrets merely to make a message more verbose.

## Thread and lifecycle errors

Respect the thread boundary and lifecycle owner. A thread crash, async-task failure, event recursion, disabled scheduler or unloaded world has an established owner and error path. Read that path before adding a catch or retry. Never catch broadly just to make PHPStan quiet.

## Evidence Index

The initial audit ledger was generated from the fixed PocketMine-MP baseline used by this skill. The published skill keeps the resulting guidance in its routed references and fixed upstream links. A future audit may publish a new machine-readable ledger under `audit-output/` when the release needs the full evidence bundle.

Each ledger line contains:

- Rule ID.
- Title, category, description, rationale, and scope.
- Rule type, severity, and confidence.
- Branch applicability and source commit.
- Evidence paths, line ranges, fixed permalinks, and evidence type.
- Positive and negative examples and exceptions.
- Enforcement, agent instruction, validation method, and related rules.

Use it to trace a skill instruction back to the audited revision. The current repository remains authoritative when it has changed since the audit. If a source link is stale or a file moved, refresh the audit rather than silently substituting another source.

## Exceptions

## Conflict resolution

When sources disagree:

1. Identify the branch and commit.
2. Prefer current executable configuration/CI for the rule it actually enforces.
3. Read maintainer policy and current source.
4. Check whether the difference is intentional scope, generated code, external code, legacy, or accidental.
5. Preserve the narrower safe behavior and record unresolved conflict.

Do not choose a generic PHP convention merely because it is familiar.

## Known snapshot conflicts

- Composer permits PHP 8.1 and CI tests 8.1, while BUILDING.md says PHP 8.2 or newer. Use the declared Composer/CI syntax floor and disclose the build-doc discrepancy.
- Formatter scope excludes the bootstrap and mapper/model paths. Do not format them as ordinary core classes.
- CONTRIBUTING prefers final/private/readonly, while framework extension points and runtime state remain mutable.
- PHPStan level 9 has counted ignores for known tool/platform limitations. A clean run is not proof that all design constraints are static.
- Integration needs an initialized DevTools submodule. Not running it is a limitation, not a pass.

## Unknowns

If the current evidence cannot answer a naming, lifecycle or architecture question, mark it unknown, inspect more local evidence or ask a focused question. Do not create a MUST rule from a single file or upstream memory.

## Formatting

Use this reference for PHP formatting or a style review.

## File shape

For files inside the PHP-CS-Fixer finder, use:

1. opening PHP tag
2. PocketMine ASCII/LGPL header
3. declare(strict_types=1)
4. namespace
5. imports
6. declarations

Use LF endings, a final newline, no closing PHP tag and no trailing whitespace. The fixer uses a blank line after the opening tag and after namespace, and a blank line before declare as configured. The exact finder is in .php-cs-fixer.php lines 3-16.

The repository excludes src/PocketMine.php, crafting/json, inventory/json, Bedrock upgrade model directories and the optional DevTools path. Do not run a whole-repository formatter as if those files had the same contract.

## Indentation and braces

- PHP uses tabs. The configured tab size is four spaces for editor display.
- YAML uses two spaces.
- PhpStorm confirms no space before control parentheses and no space before opening braces.
- Source shape is class Server{, function run(){ and if(condition){.
- Use one space after casts and one space before the return-type colon.
- Preserve semantic indentation for arrays, multiline calls, closures and chained expressions. Do not hand-align unrelated code.

## Arrays and operators

- Use short array syntax.
- Use the configured single-space binary operator and concat style.
- Use the configured unary and cast spacing.
- Keep configured blank-line rules. Do not add decorative blank lines.
- Use a trailing comma in a multiline list when nearby code and the parser version support it.

## Imports

- One import per statement.
- Ordered imports are grouped class, function, const and alpha-sorted within the configured groups.
- In namespaced files, native functions and constants are normally imported explicitly. Source examples include use function count and use const PHP_INT_MAX.
- Keep aliases when they prevent collisions or clarify a generated registry/input. Do not shorten fully qualified names in excluded JSON-mapper doc comments.
- Remove unused imports.

## PhpStorm and fixer

The project style is in .idea/codeStyles/Project.xml. The complete PHP-CS-Fixer rule list is in the audited source configuration. CI invokes PHP-CS-Fixer in dry-run/diff mode. Use the tool as the final formatting authority for in-scope files. Do not run it in write mode across unrelated files.

## Safe review checklist

- Is the target path in finder scope?
- Is the file generated or a mapper exception?
- Is strict_types present where expected?
- Are tabs and LF preserved?
- Are imports sorted and complete?
- Are braces/parentheses/return types shaped like siblings?
- Did formatting change unrelated lines?

## Functions And Control Flow

Use this reference for method additions, refactors and bug fixes.

## Local patterns

- Prefer a guard clause when it makes an invalid state explicit and preserves the local flow.
- Use strict comparisons and explicit null handling in public/runtime code.
- Keep cleanup, timing and state restoration in finally blocks when the surrounding subsystem does so.
- Break long calls and expressions at semantic boundaries. Follow nearby continuation indentation.
- Keep short methods concise when the repository does. Do not expand or compress code for aesthetics alone.
- Avoid hidden dynamic construction, unsafe foreach mutation and unbounded parsing because project PHPStan rules reject those patterns.
- Use closures/arrow functions only when their capture, thread ownership and callable signature are clear.

## Refactor boundary

A stable bug fix should not become a control-flow or formatting sweep. Inspect callers and tests first, write the smallest behavior-preserving patch, then inspect the diff for unrelated changes. Performance-sensitive loops may favor an unusual but measured shape. Preserve that invariant and document intent if it is not obvious.

When a branch is deeply nested, refactor only if the task requires it or a focused test proves the behavior. Do not change exception order, event dispatch order, task ownership or serialization while claiming a style-only refactor.

## Naming

Use this reference when adding a class, method, property, event, task, registry or file.

## Path and namespace

Composer maps pocketmine to src and generated. Use the directory that owns the domain and the matching namespace. Typical domains include block, command, crafting, data, entity, event, inventory, item, network, permission, player, plugin, promise, resourcepacks, scheduler, thread, timings, utils and world.

Files use PascalCase.php for class-like types. Domain subdirectories mirror namespace segments. src/PocketMine.php is a special bootstrap exception.

## General observed names

These are strong conventions, not all absolute policy:

- Classes, interfaces, traits and enums: PascalCase.
- Methods, functions, properties and local variables: lowerCamelCase.
- Constants: UPPER_SNAKE_CASE.
- Tests: domain name plus Test where that is the local pattern.
- Exceptions: domain or failure name plus Exception.
- Events: domain plus Event.
- Tasks: operation plus Task.
- Managers/handlers/registries/parsers/serializers: use the suffix only when the class actually owns that responsibility.
- Boolean methods commonly use is, has, can, or should. Match the local API vocabulary.
- Get/set/create/from/to/load/save/read/write names must describe the real direction and ownership. Do not rename solely to match a generic verb list.

## Naming workflow

1. Search for the closest sibling type and its callers.
2. Confirm whether the new symbol is public, protected, internal or private.
3. Check collision and abbreviation conventions in that module.
4. Prefer domain terminology already present in API and tests.
5. Do not infer a required suffix from one class. Mark uncertain naming as observed until repeated evidence exists.

Generated and serialized names follow their generator/external schema. Do not rename generated constants or external fields for aesthetic consistency.

## Performance And Concurrency

## Classify the work

Choose the execution model before writing code:

- Main-thread/tick: world, entity, inventory, plugin lifecycle, event and network state that is not explicitly thread-safe.
- AsyncTask: brief CPU-bound work in the shared reusable pool, such as compression or world-generation calculations.
- Dedicated thread: work that runs for a long time or indefinitely.
- External worker/I/O: follow the existing subsystem. Do not move I/O into the shared AsyncPool by default.

## AsyncTask contract

AsyncTask.onRun cannot access Server and should not perform network, file or database I/O. Use onCompletion or other main-thread callbacks for server state. Store non-thread-safe values using the established local storage/serialization mechanisms. Keep tasks short. A pooled task that runs for seconds or longer harms other work.

## Tick and hot paths

Server and World have explicit tick invariants, queues and caches. Preserve ordering, timing instrumentation, cache invalidation and ownership. Use Event.hasHandlers in hot paths only when the local event pattern calls for it. Avoid allocations, logging, reflection and unbounded parsing in hot loops unless the existing subsystem does so intentionally.

## Verification

A static or unit test does not prove a frame/tick budget or real player load. For performance changes, run the focused test/reproducer, inspect timing/caching implications and report what was not measured. Do not call a successful PHPStan or PHPUnit run a performance result.

## Php Types And Phpdoc

## Native types

The Composer floor is PHP 8.1. Use native parameter, return and property types for real contracts when that syntax is available: nullable, union, intersection, static, self, parent, iterable, callable, closures and class-string where appropriate. Preserve legacy public signatures when changing a stable API.

The codebase is strict-typed in the formatter scope. Do not use a newer PHP feature just because the local runtime supports it. Check Composer and the CI matrix first.

## PHPDoc

Use PHPDoc when it adds information PHP cannot express:

- Generic collections and variance.
- Array shapes and list/key types.
- Callable or closure signatures.
- PHPStan type aliases and imported aliases.
- Template parameters and inheritance.
- Deprecation, internal, compatibility and lifecycle notes.
- Observable throws contracts.
- Serialized or domain invariants.

Use native types instead of repeating them in PHPDoc. PHP-CS-Fixer enables no_superfluous_phpdoc_tags while allowing mixed where needed. Keep PHPDoc aligned and trimmed.

Examples from the source include World type aliases, TaskScheduler templates, RuntimeData generics and collection annotations.

## Project PHPStan rules

The configuration runs level 9, strict rules and PHPUnit extensions. It scans build, src, generated, PHPStan rules, PHPUnit, TesterPlugin and tools, with a bootstrap, stubs and dynamic constants.

The six custom rules are:

- DeprecatedLegacyEnumAccessRule: Do not add deprecated legacy enum access.
- DisallowDynamicNewRule: Do not instantiate using an expression such as `new $class(...)`. Use a typed closure or factory pattern.
- DisallowEnumComparisonRule: Use the enum/value API expected by the repository rather than direct forbidden comparisons.
- DisallowForeachByReferenceRule: Do not use foreach by-reference because of surprising mutation.
- ExplodeLimitRule: Pass a limit when untrusted input could create resource waste.
- UnsafeForeachRule: Make key types explicit. Avoid numeric-string coercion surprises and unspecified keys.

Read the implementation when a finding is involved. The config has counted ignores for platform/tool limitations. A passing analysis does not mean every design rule is static.

## Validation

Run:

~~~text
vendor/bin/phpstan analyze --no-progress --memory-limit=2G
~~~

Then run the narrowest PHPUnit test. Do not suppress or widen a finding merely to make the check pass without a repository-backed reason.

## Pocketmine Patterns

## Events and listeners

Read Event.php, Cancellable.php, HandlerListManager and a related event before adding an event. Preserve:

- The event base class and namespace.
- Payload ownership and mutability.
- Handler registration and inheritance behavior.
- Cancellable semantics and handleCancelled behavior.
- Event.call timing and recursion protection.
- Tests for ordering and cancellation where relevant.

Do not invoke listeners directly or add cancellation merely because a name sounds cancellable.

## Plugins

Use PluginBase lifecycle hooks and metadata. Core calls onLoad, onEnable and onDisable through PluginBase. Core-owned state-changing methods are not plugin extension points. Use the plugin scheduler and manager APIs rather than reaching into internal server arrays.

## Scheduler

TaskScheduler queues Task handlers and runs them from mainThreadHeartbeat. For a repeating or delayed task, use the existing scheduling methods and cancellation semantics. Match task naming and test patterns in tests/phpunit/scheduler.

## Blocks, items and registries

Blocks/items use domain base classes, interfaces and registry/input classes. Generated Vanilla* registries point to source input classes. When adding vanilla content, identify the registry input and the data/codegen pipeline first. Preserve clone/value semantics and local constructor patterns.

## Generated translations and Bedrock data

Known translation classes and Bedrock name/state files are generated. Change the input data or generator and run composer update-codegen. Do not hand-edit generated output.

## Quality Gates

## Required honesty

Before saying a change is complete, identify the command that proves each claim, run it, read its exit code and summary, and report the boundary. Never convert an unrun or partially run check into a pass.

## Gate selection

- Any PHP change: PHP-CS-Fixer dry-run and PHPStan as available.
- Behavior change: focused PHPUnit test.
- Plugin/server lifecycle or gameplay: integration and/or manual evidence.
- Generated input/codegen: composer update-codegen, clean diff and collision check.
- Translation resources: translation verifier.
- Shell scripts: ShellCheck.
- Dependency/PHP floor: Composer install/validate and the relevant PHP runtime/matrix.
- Public API: consumer search, API-focused tests and branch-policy review.

## Diff review

Inspect git diff and git diff --check. Look for unrelated formatting, accidental public API changes, changed serialized keys, generated files without inputs, dependency drift, missing tests and stale docs. Check status after every tool that can write files.

## Known snapshot caveat

The audited snapshot's local PHP was 8.4 while PHP-CS-Fixer 3.75's supported environment was PHP 8.3. A dry-run was possible only with the tool's environment guard overridden. Record this kind of caveat instead of hiding it.

## Repository Context

This reference captures the audited Axolotl-PM PocketMine-MP stable snapshot. Re-check the current checkout before relying on a fact.

## Snapshot

- URL: https://github.com/axolotl-pm/PocketMine-MP
- Audited branch: stable
- Audited commit: 7831952d6a970d1700ca82742ab2ac4dbe61ff80
- Version constants: 5.51.2, development build, stable channel
- Fork relationship: the README identifies the repository as a fork of pmmp/PocketMine-MP
- Composer PHP requirement: ^8.1
- Composer platform PHP: 8.1.0
- CI matrix: PHP 8.1 through 8.5
- Required nonstandard extensions include chunkutils2, crypto, encoding, igbinary, leveldb, morton, pmmpthread and yaml
- Composer maps pocketmine to src and generated. Development mappings cover tests/phpunit and tests/phpstan/rules.

Primary sources:

- The `composer.json` file, lines 7-104.
- The `composer.lock` file at the audited commit.
- The `src/VersionInfo.php` file, lines 22-37.
- The `CONTRIBUTING.md` file, lines 44-75.
- The `BUILDING.md` file, lines 1-33.
- The `src/PocketMine.php` file, lines 58-173.

## Directory ownership

- The `src` directory contains handwritten core server source and APIs.
- The `generated` directory contains code generated from inputs and data.
- The `build` directory contains build and code-generation programs.
- The `tests/phpunit` directory contains domain and unit tests.
- The `tests/phpstan` directory contains PHPStan rules, config, stubs, and test-only types.
- The `tests/plugins` directory contains integration fixtures and the optional DevTools submodule.
- The `tools` directory contains standalone maintenance utilities.
- The `resources` directory contains runtime data, config, and translations.
- The `.github/workflows` directory contains CI, release, and maintenance automation.
- The `.idea` directory contains PhpStorm code style and file templates.
- The `vendor` directory contains external Composer code. Do not infer core style from it.

## Reconnaissance sequence

Before a change:

1. Run git status and identify the branch.
2. Read composer.json and composer.lock if a dependency or PHP syntax is involved.
3. Find the target path with git ls-files and compare it with .php-cs-fixer.php.
4. Search for sibling classes, call sites, subclasses, interfaces and tests.
5. If generated, locate the input and generator before opening the output.
6. If a branch or API question is involved, read CONTRIBUTING.md and the nearest API/internal README.

## Testing

## Select the boundary

- PHPUnit proves isolated/domain behavior and is the default for logic that can be tested without a running server.
- PHPStan proves configured static contracts, not runtime lifecycle or client behavior.
- PHP-CS-Fixer proves configured formatting, not semantics.
- Codegen proves generated output is reproducible from inputs.
- Integration tests build DevTools/server artifacts and launch a server with test plugins.
- Manual playtesting is required when the behavior is gameplay/client-facing and cannot be adapted to PHPUnit.

## Repository commands

Use the current CI commands where available:

~~~text
vendor/bin/phpunit --bootstrap vendor/autoload.php --fail-on-warning tests/phpunit
vendor/bin/phpstan analyze --no-progress --memory-limit=2G
php-cs-fixer fix --dry-run --diff --ansi
composer update-codegen
php build/codegen/check-file-collisions.php
./tests/travis.sh -t4
~~~

The integration command requires initialized submodules and a compatible runtime. Do not run destructive or external release workflows merely to validate a source change.

## Test style

Match the nearest test class, fixture, setup/teardown and assertion vocabulary. Keep tests focused on observable behavior and lifecycle. Do not weaken assertions, delete tests or add mocks that bypass the behavior under test.

## Evidence reporting

Report exact test counts or command summaries when available. Separate passed, failed, skipped, unavailable and not-run. Do not imply that unit/static checks cover real-client, production or performance behavior.

## Anti Patterns

These are SYNTHETIC EXAMPLES. They describe behavior rejected by the audited repository or unsafe agent behavior. They are not claims that the exact snippets occur in source.

## Generic formatter override

~~~php
class Example {
    public function run() {
        $values = array(1, 2);
    }
}
~~~

Why it is wrong for normal formatter-scope code: it uses spaces, a space before the brace, untyped members/methods and long array syntax. Use the repository fixer and nearby source.

## Dynamic construction and foreach reference

~~~php
$object = new $className($argument);
foreach($items as &$item){
	$item = normalize($item);
}
~~~

Why it is wrong: project PHPStan rules reject dynamic new and foreach by-reference. Use a typed closure/factory or a deliberate copy/update pattern.

## Unsafe untrusted parsing

~~~php
$parts = explode(",", $clientData);
~~~

Why it is wrong: pass a limit when untrusted input can create unbounded work. Read the ExplodeLimitRule and existing parser.

## Async misuse

~~~php
final class BadTask extends AsyncTask{
	public function onRun() : void{
		$this->server->getLogger()->info("running");
		file_get_contents($this->url);
		while(true){
			$this->poll();
		}
	}
}
~~~

Why it is wrong: AsyncTask onRun cannot use Server, should not do I/O and should be short-lived. Classify the work first.

## Generated edit

Editing generated/VanillaBlocks.php by hand is not a complete change. Find VanillaBlocksInputs.php or the data/codegen source, regenerate, and check for a clean reproducible diff.

## Stable cleanup

A request to reformat every file on stable conflicts with CONTRIBUTING.md. Report the branch-policy conflict instead of creating a broad formatting diff.

## Good Patterns

These are concise synthetic examples shaped by the audited source. They are SYNTHETIC EXAMPLES, not copied repository code.

## In-scope class

~~~php
<?php

/*
 * PocketMine project header goes here.
 */

declare(strict_types=1);

namespace pocketmine\example;

use pocketmine\utils\Utils;
use function count;

final class ExampleRegistry{
	private array $entries = [];

	public function add(string $name, object $entry) : void{
		$this->entries[$name] = $entry;
	}

	public function has(string $name) : bool{
		return isset($this->entries[$name]);
	}

	/**
	 * @return list<object>
	 */
	public function getAll() : array{
		return array_values($this->entries);
	}
}
~~~

Why it fits: strict types, attached braces, tabs, native types, one-per-line imports, useful PHPDoc and private owned state. Before using it, confirm the real target namespace and nearby class contract.

## Async boundary

~~~php
final class HashTask extends AsyncTask{
	public function __construct(
		private string $payload
	){
	}

	public function onRun() : void{
		$this->setResult(hash("sha256", $this->payload));
	}

	public function onCompletion() : void{
		// Main-thread code may consume the result here.
	}
}
~~~

This remains a synthetic pattern. Check the actual AsyncTask API and do not use it for I/O or long-running work.

## Event boundary

A new event should extend the current event family, expose typed payloads, implement Cancellable only when downstream handlers can suppress the operation, and use Event.call from the owner. Copy a sibling event and add ordering/cancellation tests rather than inventing a listener invocation mechanism.

## Generated boundary

Change VanillaBlocksInputs or the correct data/generator input, run composer update-codegen, run the collision check and inspect the generated diff. Do not patch generated/VanillaBlocks.php directly.

## Task Scenarios

Use these prompts in an isolated checkout. They are designed to test behavior, not merely match headings.

1. Create a typed class in an existing domain directory. Expected: inspect namespace/path siblings, use the header, strict types, tabs, attached braces and imports, and choose final/private only after checking consumers.
2. Add a public method to an established class. Expected: preserve parameter names and compatibility, use native types, add only useful PHPDoc, update a focused test, and search call sites.
3. Create an immutable value object. Expected: use final/private/readonly only when no subclassing, mutation or serialization contract forbids it.
4. Refactor a function with nested branches. Expected: keep the change minimal, preserve exception/event order, run focused tests and avoid a stable style sweep.
5. Add a class where final/private/readonly are tempting. Expected: search subclasses, reflection, lifecycle calls and public consumers before adding modifiers.
6. Add a custom exception. Expected: reuse the nearest domain hierarchy, document observable throws, keep American English and preserve caller handling.
7. Write a PHPUnit test. Expected: match local fixture/setup/assertion style and run the exact PHPUnit command.
8. Add an event or listener. Expected: follow Event.call, HandlerListManager, cancellation and inheritance semantics. Add ordering and cancellation coverage.
9. Change performance-sensitive code. Expected: classify main-thread, pooled CPU or dedicated thread work and preserve tick/cache/ownership invariants.
10. Change a public API. Expected: inspect branch matrix, call sites, named arguments, protected subclasses, deprecation and compatibility strategy.
11. Touch generated source. Expected: locate the generator/input, edit the source of truth, regenerate, check collision and clean diff.
12. Review a file with style violations. Expected: use finder scope and repository fixer/PHPStan evidence, not generic PHP style.
13. Find a legacy file that conflicts with the formatter. Expected: check exclusions, generator/mapper needs and branch. Preserve unrelated legacy code.
14. Edit a file outside formatter scope. Expected: do not impose core PHP-CS-Fixer rules. Inspect the owning tool/template convention.
15. Request PHP 8.4-only syntax. Expected: compare Composer floor/CI matrix and propose a PHP 8.1-compatible alternative or report an intentional compatibility change.
16. Ask for a convention with insufficient evidence. Expected: mark it unknown, inspect more siblings or ask a focused question. Never invent a MUST rule.\n
# Virion and reusable-library workflow

## Boundary

A virion is a PocketMine-family integration and packaging mode for reusable PHP code. It is not a project role, a Composer package, or a standalone server plugin. A repository may support Composer and Virion together, and may also provide a separate plugin when that plugin has independent server behavior. See [project-model.md](project-model.md).

The library should expose a small, stable API. Hide packet formats, resource-pack internals, storage layout, cache coordination, and shading details behind that API.

## Metadata and namespace

Inspect and preserve the repository's `virion.yml` contract, especially:

- Confirm the `name` and version.
- Confirm the `antigen` namespace.
- Confirm Axolotl-PM or PocketMine API and PHP constraints.
- Confirm library dependencies.
- Confirm any resource or build metadata required by the target DevTools or VirionTools version.

Keep PHP namespace, directory layout, Composer autoload, `antigen`, and consumer examples consistent. A namespace collision is a packaging bug, not a cosmetic issue.

## API design

- Prefer explicit construction or a named factory over an undocumented global singleton.
- If a plugin instance is required, make that requirement visible in the constructor/factory and explain why.
- Make cleanup idempotent when consumers may call it from `onDisable()` or error paths.
- Return domain objects or well-defined scalar results instead of leaking implementation arrays when the API will be reused.
- Validate inputs at the public boundary and describe failure behavior.
- Keep callback, async, serialization, and exception contracts documented.

## Packaging and consumers

Composer and Virion describe different contracts. Composer identifies a PHP package, its dependencies, and its autoload rules. `virion.yml` identifies the server-facing reusable package, its antigen, version, and API requirements. When both modes are supported, keep their namespace, source layout, version, and dependency declarations consistent. Do not count development-only Composer metadata as a documented consumer integration.

Verify both development and production modes:

- Verify folder-plugin development with a shared virion source.
- Verify the consumer build that shades or injects the library into a standalone PHAR.
- Verify that resources are retained at the expected protected path.
- Verify that dependency versions resolve exactly as the build expects.
- Verify multiple consumers, static runtime state, and resource-pack UUID behavior where relevant.

Do not tell users to install a virion directly in `plugins/`. A virion PHAR belongs to the virion path or is included in a consumer plugin build. A plugin PHAR belongs in `plugins/`. If both manifests exist, document and verify the two outputs separately.

## README expectations

A virion README should answer:

1. What problem does the library solve?
2. Is it a standalone plugin? Usually no.
3. What PHP, API, extension, and consumer-build requirements apply?
4. How is it installed through DevTools/VirionTools or Composer?
5. What is the smallest working usage example?
6. What are the public API and lifecycle calls?
7. What limitations, compatibility gaps, or resource conflicts exist?
8. What license applies to source and bundled assets?

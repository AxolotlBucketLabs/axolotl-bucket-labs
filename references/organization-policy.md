# Organization policy reference

This reference records stable identifiers and routing rules. Live GitHub state remains authoritative when a value can change.

## Organization identity

- Organization: `AxolotlBucketLabs`.
- Organization profile: `https://github.com/AxolotlBucketLabs`.
- Community invite: `https://discord.gg/Pk4FrNvHnM`.
- Discord server ID for badges: `1568295845374206052`.
- Ruleset export path: `.github/rulesets/main-baseline/` in this repository.

## Role and access mapping

| Organization role | GitHub access policy | Normal implementation |
| --- | --- | --- |
| `Lab Founder` | Admin access to all organization repositories | Organization owner and `NhanAZ` |
| `Lab Associate` | Maintain access to all organization repositories | Member of the `Lab Associates` team |
| `Lab Member` | No default repository access | Organization member with project access granted separately |
| `Lab Maintainer` | Maintain access to assigned repositories | Explicit repository or project assignment |
| `Lab Collaborator` | Write access to selected repositories | Explicit repository assignment |
| `Lab Contributor` | No default repository access | Access granted only when a project needs it |
| `Lab Fellow` | No repository or organization permission | Honorary recognition only |

## Team policy

- Team display name: `Lab Associates`.
- Team slug: `lab-associates`.
- Normal team repository permission: `maintain`.
- Team members do not become organization owners.
- Team members do not automatically enter a ruleset bypass list.

Use the live team endpoint to verify membership and repository access. Do not treat a public repository's effective `read` permission as an explicit collaborator grant.

## Ruleset policy

The `main-baseline` ruleset targets `refs/heads/main`. Its common policy includes one approval, approval from someone other than the latest pusher, stale approval dismissal, resolved review threads, required status checks, deletion protection, and force-push protection. Required status check contexts are repository-specific.

The only normal bypass actor is `NhanAZ`. A `Maintain` team member is not a bypass actor unless the user explicitly changes the live ruleset.

## Repository identity rule

Use organization links and badges only in repositories owned by `AxolotlBucketLabs`. For a repository outside the organization, preserve its own identity and community links even when the code targets Axolotl-PM.

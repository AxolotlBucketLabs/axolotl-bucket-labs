# Repository audit sequence

Use this reference when auditing or changing an AxolotlBucketLabs repository, repository registry, team access, or ruleset.

## Discover the target

1. Read the current local instructions and working tree status.
2. Read the Git remote and confirm the owner is `AxolotlBucketLabs`.
3. Read the live repository metadata, default branch, visibility, license, homepage, topics, and archive state.
4. Read the root `projects.json`, `members.json`, and `roles.json` records when the task depends on organization policy. Read the target repository's README, Composer metadata, plugin and virion manifests, workflows, and release files. Compare declared project roles and supported integration modes with those sources. Do not infer a library role from a Composer package type or manifest alone.

## Check repository state

- Confirm the default branch is `main`.
- List branches and look for stale branches such as `master`, `pm5`, or an old documentation branch.
- Check workflows for triggers that target old branches.
- Check status checks on the current `main` commit and compare them with the required contexts in the live ruleset.
- Search current tracked files for stale organization Discord invites, old badge server IDs, private links, prompt context, and unsupported claims.

## Check team access

Use the organization team repository endpoint for the team permission. Confirm:

- The `Lab Associates` team exists.
- The intended member has an active team membership.
- The team has `maintain` access on the intended repository.
- The team does not have `admin` access unless explicitly requested.
- The member is not in the `main-baseline` bypass list unless explicitly requested.

Do not use public repository visibility as proof of explicit access. Do not replace a team policy with a long list of direct collaborator grants unless the project needs an exception.

## Check the ruleset

Inspect the repository's `main-baseline` ruleset and verify:

- It is active and targets `refs/heads/main`.
- It requires one approval.
- The latest push approval must come from another person.
- Stale approvals and unresolved review threads are handled according to policy.
- Required status checks are real contexts produced by the repository workflows.
- The bypass list contains only the authorized actor.

## Verify after a write

After changing GitHub state:

1. Read the live object again through the API or GitHub interface.
2. Verify the repository, team, permission, ruleset, or metadata at the same boundary that was changed.
3. Check the hosted workflow if a workflow or required status check changed.
4. Check the pushed commit and local working tree separately.

Report any layer that was not verified. Do not turn a successful API response into a claim that a workflow, release, or runtime artifact is healthy.

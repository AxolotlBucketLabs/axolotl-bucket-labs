# GitHub ruleset exports

This directory contains versioned `main-baseline` exports for AxolotlBucketLabs repositories. The export filename matches its repository name. Each file preserves that repository's required status checks while sharing the organization review and branch policy.

The baseline targets `main`, requires one approval from someone other than the latest pusher, dismisses stale approvals, requires resolved review threads, blocks deletion and force pushes, and grants the normal bypass only to `NhanAZ`.

An export is configuration data. It does not apply itself or prove that the live GitHub ruleset matches. Import changes through GitHub and verify the live ruleset separately.

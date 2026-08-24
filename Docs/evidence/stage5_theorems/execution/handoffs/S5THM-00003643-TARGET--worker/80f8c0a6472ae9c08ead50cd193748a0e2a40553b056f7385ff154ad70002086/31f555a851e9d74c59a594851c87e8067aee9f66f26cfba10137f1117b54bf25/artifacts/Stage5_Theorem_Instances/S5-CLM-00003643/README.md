# S5-CLM-00003643 — Erdős–Szekeres bounds

This target package closes the worker-side INTAKE, STATEMENT, ANCHOR, TREE, MACHINE, READABLE, VALIDATE, and RELEASE evidence surfaces for the frozen `Erdos107.variants.ersz_bounds` record.

The theorem states, for `n ≥ 3`,

`2^(n-2) + 1 ≤ f(n) ≤ choose(2n-4,n-2) + 1`,

where `f(n)` is the least number of planar points in general position forcing a convex `n`-gon. The readable proof separates the extremal lower construction, the cup–cap upper theorem, both transfers through `Nat.sInf`, and the final conjunction. The structured DAG and R0 ledger give each of those steps a unique reverse-covered fragment.

The source module path is retained only as frozen provenance in the Lean files; each uses `import Mathlib`. This worker ran only the claim-authorized `--no-lean` preflight. The release decision is provisional and explicitly leaves `master_accepted=false`; canonical trust-zero compilation and semantic recomputation occur after harvest.

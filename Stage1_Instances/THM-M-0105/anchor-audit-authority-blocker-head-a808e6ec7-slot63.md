# THM-M-0105 anchor-audit authority blocker

Item: `S56-M-0105-ANCHOR_AUDIT`

Worker base: `a808e6ec7a16a99e6ab3471085952287d4e24728` (tree
`9a77a1024e5129433c6dc9db23455b64c811abe1`)

Claim order: `(v2_execution_rank=264, phase_layer=2,
S56-M-0105-ANCHOR_AUDIT)`

Verdict: `blocked`; proposed state remains `[ ]`.

## First failed gate

`G05-AUTHORITY-REPLAY`

The mandatory HEAD phase contract declares two anchor-audit validator
candidate paths:

- `Stage1_Instances/THM-M-0105/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0105/check_anchor.py`

Neither path exists at the worker-base commit or in the worktree. The contract
requires exactly one candidate already present at the base, and the scheduler
owns both paths. This worker therefore cannot lawfully create or modify a
candidate. There is no declared argv to run and no
`stage1-validator-semantic-result/1.0` object from which a phase receipt or
self-test handoff could be supported.

Topology independently prevents master closure: predecessor
`S56-M-0105-STATEMENT` remains `[_]`, not master-accepted `[x]`.

## Dependency and reuse audit

The authoritative theorem node has no direct hard parent, transitive hard
ancestor, hard edge, reuse hint, or shared group. The supplied
`parent_inspection_order` is exactly empty and that complete empty closure was
traversed once before any proof work. No proof work was performed, and no
provider declaration, proof body, receipt, checkbox, or acceptance was
consumed or transferred.

The current theorem-DAG SHA-256 is
`de71a3ca00b2ac64f96f4a0b7363cf56d09acb943716310332e693d9c9503c6a`;
the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The tracked schema-1.1 ledger has all required empty arrays, but it binds a
prior graph/revision and the statement item at phase layer 1. A stale ledger is
not presented as current phase evidence, and a ledger-only refresh cannot
repair the missing immutable validator.

## Bounded observations

The current local replay confirms only the existing bounded guidance:

- `Stage1Instances.THM_M_0105.RiemannRochTarget` and its definitional
  expansion elaborate at trust level 0. The root remains `M3`, with no terminal
  Riemann-Roch body.
- The tracked legacy `S1_M_027.lean` module elaborates support and blocker
  declarations, but its existential abstract divisor package is not the
  frozen universal target and grants no proof credit.
- Pinned mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`
  (tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`) supplies relevant
  geometry, sheaf-cohomology, function-field, Euler-characteristic, and
  elliptic-curve substrate. Bounded exact-topic replay found no pinned-mathlib
  terminal Riemann-Roch declaration.
- The immutable external leads remain blocked or mismatched:
  `cguth7/roch-riemann-refactor@8e67e8941a083617a8b34a0da3a35a7c2c845f59`
  has build, placeholder/axiom, trust, locality, and exact-transport blockers;
  `vaca22/riemann-roch-function-fields@dbca5beed1da77e2ecd1eec207d0451fa57e8aa6`
  lacks a locally checked scheme/function-field transport; the finite-graph
  project is a different theorem.
- Hartshorne IV.1.3 remains a bibliographic lead, not `H0`; exact source bytes,
  incorporated definitions, assumptions, errata, convention bridges, and
  independent review remain open.

These observations are not a newly precommitted, receipt-bound seven-lane
inventory. They claim neither phase completion nor global discovery
saturation.

## Checks run

The untouched base passed the rev-5.6 standard validator, v2 theorem-DAG
validator, phase-contract validator, target-manifest validator, and target
lookup. Both the frozen target and legacy module elaborated through the
existing pinned `lake env lean --trust=0` environment. The topic search found
no mathlib terminal declaration, and the target-owned Lean hygiene search
found no prohibited construct. No network access, Lake update/build,
dependency clone/fetch, or `.lake` mutation was performed.

After these blocker files were added, the phase-contract and target-manifest
validators still passed, as did JSON and whitespace checks. The standard and
theorem-DAG validators then failed only because deterministic generation now
inventories these new owned evidence files while the worker is forbidden to
regenerate the read-only authority projection. Scheduler integration must
perform that projection refresh atomically.

## Retry condition

The scheduler must commit exactly one declared anchor-audit validator and
issue a fresh claim whose base contains that unchanged blob. After the
statement predecessor is master-accepted `[x]`, a worker can execute the
complete seven-lane protocol, bind immutable positive and negative evidence,
refresh the empty dependency ledger for the current graph/base/claim, produce
exactly one `stage1-node-receipt/1.0`, and run the unchanged validator to
exactly one typed semantic JSON result.

No anchor-audit receipt and no `.stage1-worker-selftest.json` are produced.
This target-scoped blocker does not satisfy the phase, transfer acceptance,
change H/M/R debt, prove the root, claim `AUDIT-Z` or `THEOREM-Z`, change task
state, or claim master acceptance.

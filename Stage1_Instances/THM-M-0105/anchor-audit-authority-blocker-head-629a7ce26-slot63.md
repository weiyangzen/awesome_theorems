# THM-M-0105 anchor-audit authority blocker

Item: `S56-M-0105-ANCHOR_AUDIT`

Worker base: `629a7ce266289b9ad49a37c0cc4d89b7b148cf36` (tree
`97daff5e375fca5b6781ccf0dede0d1c25648e19`)

Claim order: `(v2_execution_rank=264, phase_layer=2,
S56-M-0105-ANCHOR_AUDIT)`

Verdict: `blocked`; proposed state remains `[ ]`.

## First failed gate

`G05-AUTHORITY-REPLAY`

The mandatory HEAD phase contract declares exactly two validator candidates:

- `Stage1_Instances/THM-M-0105/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0105/check_anchor.py`

Neither candidate exists in the worker-base commit or worktree. The contract
requires exactly one candidate already present at the worker base, with the
same blob at HEAD, and assigns ownership to the scheduler master lane. This
worker is forbidden to create or modify either path. Consequently there is no
lawful validator argv and no `stage1-validator-semantic-result/1.0` object from
which to support an anchor receipt or worker self-test.

Topology separately prevents master closure: predecessor
`S56-M-0105-STATEMENT` is `[_]`, not master-accepted `[x]`.

## Dependency and reuse audit

The authoritative theorem node has no direct hard parent, transitive hard
ancestor, hard edge, reuse hint, or shared group. The supplied
`parent_inspection_order` is exactly empty. That complete empty closure was
traversed once before any proof work. No proof work was performed and no
provider declaration, body, receipt, checkbox, or acceptance was consumed or
transferred.

The current graph SHA-256 is
`de71a3ca00b2ac64f96f4a0b7363cf56d09acb943716310332e693d9c9503c6a`;
the stable context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The tracked schema-1.1 ledger contains the required empty arrays but is exact
statement evidence bound by `statement-receipt.json`: it records the earlier
graph/revision and phase layer 1. Refreshing only that ledger would invalidate
the predecessor receipt and still could not satisfy this phase without the
immutable validator, so no misleading partial refresh is presented.

## Bounded observations

These observations are immutable local guidance, not a newly precommitted,
receipt-bound complete seven-lane inventory.

- The frozen `Stage1Instances.THM_M_0105.RiemannRochTarget` and its exact
  definitional expansion elaborate at trust level 0. No terminal proof body
  exists, so the honest root classification remains `M3` with no proof credit.
- The tracked legacy `S1_M_027.lean` module elaborates support declarations,
  statement-shape wrappers, audit metadata, and explicit blockers. Its
  existential abstract divisor package is not expression-identical to the
  frozen universal target and transfers no acceptance or proof credit.
- Pinned mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`
  (tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`) contains useful
  algebraic-geometry, sheaf-cohomology, function-field, Dedekind, Euler, and
  elliptic-curve substrate. A bounded exact-topic search found no pinned
  Riemann-Roch declaration or complete divisor/canonical/genus interface.
- Immutable guidance identifies
  `cguth7/roch-riemann-refactor@8e67e8941a083617a8b34a0da3a35a7c2c845f59`
  as blocked by build, trust, placeholder/axiom, closure, and exact-transport
  gaps. It remains `M5`.
- A content-bound read-only snapshot records
  `vaca22/riemann-roch-function-fields@dbca5beed1da77e2ecd1eec207d0451fa57e8aa6`,
  declaration `FunctionField.riemann_roch`, source SHA-256
  `bc360e7800a10e3800f14751f17047564c4c8d052434540bd30c4d0dfcf0e82d`.
  It lacks a checked function-field/scheme transport and consumer validation,
  so it remains `M5` guidance. The finite-graph candidate is a material theorem
  mismatch.
- No target-owned content-bound statement-collection, historical, or
  other-prover search result is available. Network denial cannot be upgraded to
  a global negative result.
- Hartshorne IV.1.3 remains a bibliographic lead, not `H0`: exact source bytes,
  incorporated definitions, assumptions, errata, convention bridges, and
  independent review remain open.

## Checks run

The untouched base passed the rev-5.6 standard, theorem-DAG, phase-contract,
target-manifest, and target-lookup checks. Both the frozen target and legacy
module elaborated with `lake env lean --trust=0`. The pinned-mathlib exact-topic
search and target Lean hygiene scan returned the expected no-match result. No
network access, Lake update/build, dependency clone/fetch, or `.lake` mutation
was performed; the automation-provided canonical `.lake` symlink was reused
read-only.

After writing this blocker, JSON parsing, owned-path whitespace checking,
contract validation, and target-manifest validation pass. The aggregate
standard and theorem-DAG checks are expected to report evidence-inventory
projection drift because these two new target-owned blocker files are not yet
in the scheduler-generated read-only DAG projection. This worker does not edit
that authority.

## Retry condition

The scheduler must commit exactly one declared anchor-audit validator and issue
a new claim whose base contains the unchanged blob. After dependency-ordered
master acceptance of the statement predecessor, a worker can precommit and run
the complete seven-lane protocol, content-bind immutable positive and negative
evidence, refresh the empty dependency ledger for that graph/base/claim,
produce exactly one `stage1-node-receipt/1.0`, and replay the unchanged
validator to exactly one typed semantic JSON object.

No anchor-audit receipt and no `.stage1-worker-selftest.json` are produced.
This target-scoped blocker does not satisfy the phase, propose `[_]`, transfer
acceptance, change H/M/R debt, prove the root, claim `AUDIT-Z` or `THEOREM-Z`,
change task state, or claim master acceptance.

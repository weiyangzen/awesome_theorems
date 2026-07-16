# THM-M-0104 anchor-audit authority blocker

Item: `S56-M-0104-ANCHOR_AUDIT`

Theorem: `THM-M-0104`

Worker base revision: `3045b020487392327c4752460c5b048f1cca5331`

Worker base tree: `a3abeb4373c7513d12024c11ee1a363181f923f9`

Claim order: `(v2_execution_rank=266, phase_layer=2, phase_item_id=S56-M-0104-ANCHOR_AUDIT)`

Worker verdict: `blocked`

Proposed state: `[ ]` (unchanged)

Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`.
For `anchor_audit` it declares these scheduler-owned validator candidates:

- `Stage1_Instances/THM-M-0104/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0104/check_anchor.py`

Neither path exists in the worktree or in the worker-base commit. The contract requires exactly
one candidate, requires it to exist at the worker base, and requires its authoritative HEAD blob
to equal its worker-base blob. The worker contract expressly forbids creating, refreshing,
renaming, replacing, or deleting either candidate. Consequently no eligible command can emit the
required single `stage1-validator-semantic-result/1.0` JSON object. An undeclared adapter, a zero
exit from another command, prose, or a worker-authored receipt cannot replace scheduler-owned
replay. Per the assignment contract, this run therefore leaves no anchor-audit receipt and no
`.stage1-worker-selftest.json`.

The independent topology gate `G02-TOPOLOGY` is also closed for master acceptance. The sole
intra-theorem predecessor, `S56-M-0104-STATEMENT`, is authoritatively `[_]`, not master-accepted
`[x]`. Its receipt has `accepted=false`, `verdict=blocked`, an empty statement-fingerprint list,
and no canonical Lean target. Those facts are useful negative evidence but cannot confer an
accepted statement boundary.

## Claim-order and parent inspection

The exact claim key was checked as
`(266, 2, S56-M-0104-ANCHOR_AUDIT)`, in the contract order
`v2_execution_rank`, `phase_layer`, `phase_item_id`.

`Docs/Stage1_Theorem_DAG_v2.json` has SHA-256
`6c46a13db8e9d6a299fca9894fba72529f3cd80df81c82e6e4937cbef997f038`.
The target's dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The complete `parent_inspection_order`, direct-hard-parent list, transitive-hard-ancestor list,
incoming hard-edge list, reuse-hint list, and shared-group list are all exactly `[]`. The complete
closure was traversed exactly once as the empty ordered sequence. Zero provider phase states,
receipts, declaration bodies, reusable artifacts, proof bodies, copies, transports, or acceptance
states were consumed. Empty graph context is not a claim of mathematical independence.

The existing target-owned `dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1` and correctly contains empty inspections, decisions, and
unresolved obligations, but it binds the earlier graph
`cb4b83c4c4a5474fce51f98098f1421315fe7f1bd8cd52205932e57eced9f675` and repository revision
`74d4c272070069bc62df15798895293b4795940a`. It is also a byte-bound input of the still-pending
statement receipt. This blocked run does not rewrite it: new ledger bytes cannot repair missing
scheduler authority, would invalidate that prior binding, and could not support a lawful semantic
receipt or handoff. A fresh eligible anchor-audit run must refresh it to the then-current base and
graph before proof work or self-test handoff.

## Target-scoped discovery observations

These observations are bounded guidance, not the contract's completed precommitted seven-lane
inventory and not proof credit:

- The repository catalog supplies only the gloss "an upper bound on the number of intersection
  points of algebraic curves." It does not select affine versus projective curves, distinct versus
  multiplicity-weighted points, coefficient field or characteristic, curve and component models,
  degree convention, local multiplicity, points at infinity, or the exact conclusion. The current
  statement evidence therefore leaves the canonical human and Lean propositions unfrozen at
  `M4`.
- The target-owned `Statement.lean`, SHA-256
  `9587255d33e025d5d3454cdc9a73bc5354fbed064df61f7f8633a2088033fe9e`, imports only
  `Mathlib.RingTheory.MvPolynomial.Homogeneous` and kernel-elaborates three substrate symbols. It
  declares no target, wrapper, or proof body.
- The historical repo-local discovery module
  `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_029.lean`, SHA-256
  `3996e85414e4d43ac9c624d4ba9131dbc26a5bae0f7f36a5f46a06d0ff715628`, is tracked at this base
  and re-elaborates under Lean 4.29.0. Its `PlaneCurveIntersectionData` stores the missing geometry,
  component, finiteness, multiplicity, and projective-support facts as abstract fields. Its local
  theorems derive only arithmetic bridges from an assumed `BezoutConclusion`. It is an `M5`
  circular or materially mismatched root candidate, while its scheme, homogeneous-polynomial,
  finite-length, ideal-sheaf, and Hilbert-polynomial declarations are adjacent `M3` substrate.
- The automation-provided pinned mathlib checkout is revision
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, dated `2026-03-30T18:47:58Z`, with a clean
  worktree. A bounded source search located generic Proj, homogeneous-polynomial, ideal-sheaf,
  finite-length, and Hilbert-polynomial infrastructure plus unrelated Bezout-ring and Bezout-identity
  declarations. It located no projective-plane Bezout or local intersection-multiplicity terminal
  theorem. These are `M3` support candidates, not an exact root.
- The legacy audit records immutable research leads for `WuProver/groebner_proj` at
  `c92d123e526cea653f20b66e6d226038fbd7118f` and `Hagb/lean-groebner` at
  `3b9a7bfe8c009cbc5f9fcbfd55942be67e798a03`. No source archive, tree/blob digest, toolchain
  closure, terminal Bezout declaration, or compatibility witness for either project is admitted in
  this repository. They remain unverified `M5` affine-elimination leads with no proof credit.
- No immutable official primary Lean project, additional public Lean repository response,
  statement-only collection snapshot, historical-prover snapshot, or human primary-source bytes
  were admitted at this base. Network access is denied. Absence of admitted bytes is an access
  boundary, not a global not-found or saturation claim. The source crosswalk remains `H1` guidance:
  it has no edition, theorem/page, incorporated definitions, assumptions, errata disposition, or
  independent reviewer.

Accordingly, no candidate is established as `M0-L`, `M0-W`, `M0-P`, `M1`, or `M2`. These scoped
observations do not complete `A01-ARTIFACTS`, `A02-DISCOVERY`, or `A03-CLASSIFICATION` and do not
substitute for a future precommitted protocol, immutable evidence record, inventory, or semantic
validator replay.

## Checks run

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, v2 DAG, phase contracts, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed dependencies, and acyclicity passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and twenty-three source references passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0104` | 0 | Rank 29, planned, legacy artifacts unaccepted, theorem incomplete |
| worktree checks for both declared validator paths | expected absent | Exactly zero scheduler-owned candidates exist |
| `git cat-file -e HEAD:<candidate>` for both declared paths | 128 each, expected absent | Neither validator exists at the immutable worker base |
| from `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC timeout --foreground --kill-after=5s 300s lake env lean --trust=0 ../../Stage1_Instances/THM-M-0104/Statement.lean` | 0 | Three homogeneous-polynomial substrate types printed; no target declaration |
| from `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC timeout --foreground --kill-after=5s 300s lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_029.lean` | 0 | Historical boundary and adjacent APIs elaborated; captured stdout SHA-256 `3aa7c7c88bbd78e87b58596c17d60edf6355da4c6fdfc190929cb387923bd97a` |
| bounded repo-local, pinned-mathlib, and pinned-`flt-regular` Lean source search | 0 | Historical target material, adjacent substrate, and unrelated Bezout identities/rings; no exact terminal body |

The Lean commands emitted nonfatal sandbox stream-fd warnings before their normal output. Their
zero exits cover only the displayed declarations and cannot supply semantic phase acceptance. No
`lake update`, `lake build`, dependency clone/fetch, checkout, network search, or `.lake` mutation
was performed.

## Retry condition and status boundary

The scheduler must commit exactly one declared anchor-audit validator and issue a fresh claim whose
base contains the identical validator blob. The statement predecessor must separately become
master-accepted `[x]` with an exact source-selected canonical statement before this phase can pass
master topology. A fresh worker must then precommit the seven ordered discovery lanes, refresh the
empty schema-1.1 dependency ledger to that base and graph, content-bind every candidate, negative
result, and access failure at immutable revisions, normalize and classify the complete frozen
inventory, create exactly one contract-selected `stage1-node-receipt/1.0`, replay the unchanged
validator at its exact contract argv, and emit a worker self-test handoff only if the typed semantic
result supports it.

This target-scoped blocker is the only artifact created by this run. It grants no state transition,
phase acceptance, H0, M0, R0, proof credit, accepted reuse, `AUDIT-Z`, `THEOREM-Z`, theorem
completion, or master acceptance.

# THM-M-0007 anchor-audit authority blocker

Item: `S56-M-0007-ANCHOR_AUDIT`

Theorem: `THM-M-0007`

Worker base revision: `7d8182914615a5f5f0445f515fbd635a74bf1faa`

Worker base tree: `8b4e8697f3cc153b4bc2ae68ff0efc2bf0ccddb3`

Worker verdict: `blocked`

Proposed state: `[ ]` (unchanged)

Phase accepted: `false`

## First Failed Gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`.
For `anchor_audit` it declares these two candidate paths:

- `Stage1_Instances/THM-M-0007/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0007/check_anchor.py`

Neither file exists in the worker-base commit. The contract requires exactly one matching candidate,
requires that candidate to exist at the worker base, and requires its HEAD blob to equal its
worker-base blob. The integration lane also rejects a worker delta that creates, changes, renames, or
deletes either declared candidate. Therefore this worker cannot lawfully manufacture a validator,
substitute an undeclared adapter, create a phase receipt that claims validator replay, or emit a
`.stage1-worker-selftest.json` handoff. Exit code zero from any other command cannot repair this
scheduler-ownership gate.

The independent topology gate `G02-TOPOLOGY` is also not ready for master closure: the sole
intra-theorem predecessor, `S56-M-0007-STATEMENT`, is worker-self-tested `[_]`, not master-accepted
`[x]` in the sole task-state authority.

## Dependency And Claim Order Audit

The assigned claim position is exactly
`(v2_execution_rank=316, phase_layer=2, phase_item_id=S56-M-0007-ANCHOR_AUDIT)`.
The target node has no direct hard parent, transitive hard ancestor, hard edge, reuse hint, or shared
lemma group. Thus the complete `parent_inspection_order` is exactly empty and was traversed once as
an empty closure. No provider phase state, receipt, declaration body, reusable artifact, proof body,
or acceptance state was consumed, copied, or inherited.

The authoritative theorem-DAG SHA-256 is
`6ce46e0d9e79e1a40c423ae1074db34e889702b9a5b5989034cd462615fed604`; the target
dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`. The existing
`dependency-reuse-ledger.json` is schema `stage1-dependency-reuse-ledger/1.1` and already contains
the required empty inspections, reuse decisions, and unresolved-compatibility lists, but it binds a
prior graph and repository revision. It is not refreshed here: without the scheduler-owned
validator, a ledger-only delta cannot yield a lawful self-test or receipt, and this blocker must not
pretend otherwise.

## Bounded Anchor Observations

These observations are discovery guidance only. They do not satisfy the phase receipt contract and
do not claim global search saturation.

- Repo-local search found only the legacy discovery module
  `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_094.lean` (SHA-256
  `99790fe00cca6aaa5429cb183e410095cd1febe648f5162af232abc2feaef5b7`, Git blob
  `085ac544d4536e1137ae8a2de119236c5c889a04`) plus the target-owned statement-boundary artifacts.
  The legacy module packages expected page and abutment objects, bare naturality/convergence
  propositions, metadata, and local substrate wrappers. It contains no source-exact terminal theorem
  and is uniformly L0 discovery evidence, not an accepted proof body.
- The manifest pins mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, under Lean `v4.29.0`. Read-only source search located
  right-derived-functor and spectral-sequence page substrate, but no Grothendieck spectral-sequence
  module, terminal declaration, convergence/abutment predicate, or compatible proof body. This is
  nonterminal machine substrate, not root closure.
- The legacy module records one material external Lean 4 lead:
  `joelriou/lean-derived-categories` at commit
  `c1d75ecdb3bbb9d85b161bade0aadfa1c2b7f6e4`, with `joelriou/mathlib4` at
  `d886e33fd2f029f2304dfd20d9069d5fa7f3aa1a`, toolchain `v4.21.0-rc3`, module
  `Mathlib.Algebra.Homology.SpectralSequence.Examples.Grothendieck`, and declarations
  `DerivedCategory.Plus.grothendieckSpectralSequence`, `.page₂Iso`,
  `.stronglyConvergesToInDegree'`, and `.stronglyConvergesTo`. The external source bytes are not in
  the repository or pinned Lake closure, so the revision, declaration types, terminal bodies,
  placeholders, axioms, trust closure, and statement compatibility cannot be rechecked here. It
  remains an unverified `M5` research lead with explicit repo-local port/import debt and no proof
  credit. It cannot reach `M1` until immutable source, type, body, dependency, trust, and adapter
  feasibility checks are independently reproducible.
- The statement evidence identifies Weibel, *An Introduction to Homological Algebra* (1994), section
  5.8, especially Theorem 5.8.3, as a primary-source anchor. No owned page transcription, exact
  definition crosswalk, or errata review fixes the convergence, filtration, naturality, indexing,
  and acyclicity conventions. The human-source lane therefore remains open and cannot support H0.
- Searches of the eleven manifest-pinned Lean packages found no second exact formal candidate.
  Public-project, statement-only, historical/other-prover, and primary-source lanes remain bounded by
  tracked bytes and prior access observations; network fetches were not attempted and global absence
  is not asserted.

The honest provisional boundary is unchanged: the current source family remains `H2`, the local
root remains `M4`, the external Riou lead remains `M5` pending immutable-byte and compatibility
audit, and readability remains `R4`. No candidate is classified as `M1`, `M0-L`, `M0-W`, or
`M0-P`.

## Checks Run

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure, manifest, v2 DAG, and contract checks pass at the untouched worker base |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546-node graph is covered and acyclic |
| `python3 scripts/stage1_target.py check` | 0 | ordered 1546-target manifest passes |
| `python3 scripts/stage1_target.py show THM-M-0007` | 0 | target identity, execution rank 94, L0 baseline, and open lifecycle agree |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phase contracts and twelve common gates pass |
| `test ! -e Stage1_Instances/THM-M-0007/check_anchor_audit.py && test ! -e Stage1_Instances/THM-M-0007/check_anchor.py` | 0 | zero declared anchor-audit validator candidates exist at the worker base |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_094.lean` | 0 | the repo-local legacy discovery module elaborates; the sandbox prints nonfatal stream-fd warnings before the checked declarations |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0007/Statement.lean` | 0 | the target-owned statement boundary elaborates; the same nonfatal sandbox stream-fd warnings precede the checked substrate |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

## Retry Condition

The scheduler must first commit exactly one declared anchor-audit validator at one of the two
contract paths, then issue a fresh claim whose worker base contains that identical blob. After the
statement predecessor is separately master-accepted `[x]`, a fresh worker can precommit and execute
the complete seven-lane protocol, content-bind the external and negative evidence, refresh the empty
dependency ledger to that fresh graph/base, produce exactly one `stage1-node-receipt/1.0`, and replay
the unchanged validator. The Riou candidate additionally requires immutable source bytes and a
checked compatibility or port decision before it can receive any consumer proof credit.

No `.stage1-worker-selftest.json` and no anchor-audit receipt are produced. This target-scoped
blocker grants no state transition, phase acceptance, provider acceptance transfer, H0, M0, R0,
audit completion, theorem completion, or master acceptance.

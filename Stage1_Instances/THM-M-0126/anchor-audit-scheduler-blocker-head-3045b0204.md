# THM-M-0126 anchor-audit scheduler blocker

Item: `S56-M-0126-ANCHOR_AUDIT`

Theorem: `THM-M-0126`

Claim order: `(v2_execution_rank=279, phase_layer=2,
phase_item_id=S56-M-0126-ANCHOR_AUDIT)`

Worker base revision: `3045b020487392327c4752460c5b048f1cca5331`

Worker base tree: `a3abeb4373c7513d12024c11ee1a363181f923f9`

Worker verdict: `blocked`

Proposed state: `[ ]` (unchanged)

Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The mandatory HEAD contract, `Docs/Stage1_Phase_Acceptance_Contracts.json` at
SHA-256 `1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`,
declares exactly these scheduler-owned candidates for `anchor_audit`:

- `Stage1_Instances/THM-M-0126/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0126/check_anchor.py`

Neither candidate exists in the worker tree or in commit
`3045b020487392327c4752460c5b048f1cca5331`. The contract requires exactly one
candidate, requires it to exist at the worker base, and requires its HEAD blob to equal its
worker-base blob. This worker is expressly forbidden to create, refresh, rename, replace, or delete
either candidate. Therefore no lawful command can emit the required single
`stage1-validator-semantic-result/1.0` JSON object. An undeclared adapter, another phase's
validator, prose output, or exit code zero cannot satisfy authority replay.

The independent topology gate `G02-TOPOLOGY` is also closed for master acceptance. The sole
intra-theorem predecessor, `S56-M-0126-STATEMENT`, is authoritative `[_]`, not master-accepted
`[x]`. Its receipt truthfully reports `verdict: blocked`, `phase_accepted: false`, no canonical
source-faithful expression, and no statement fingerprint. Audit observations remain useful, but
this phase cannot be master accepted at the current task state.

## Dependency and reuse audit

The authoritative theorem-DAG SHA-256 is
`6c46a13db8e9d6a299fca9894fba72529f3cd80df81c82e6e4937cbef997f038`; the target
dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The complete `parent_inspection_order`, direct-parent list, transitive-ancestor list, hard-edge
list, reuse-hint list, and shared-group list are all exactly empty. The prescribed traversal is
therefore the empty sequence and was audited once as the complete closure. No provider statement,
phase state, receipt, declaration body, reusable artifact, checkbox, copy, transport, or acceptance
was consumed or inherited. The empty graph context is not a mathematical-independence claim.

The target-owned `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and correctly records empty inspections, reuse decisions, and
unresolved-compatibility obligations, but it binds the earlier statement-worker graph and base.
It is deliberately not refreshed by this blocked run. Refreshing it alone cannot repair the absent
scheduler-owned validator or support a genuine phase self-test, and it is an exact content-bound
input of the existing statement receipt. A fresh eligible anchor-audit worker must refresh the
ledger to its own immutable base and current graph before producing a handoff.

## Bounded anchor observations

These observations are immutable or content-bound discovery guidance only. They are not the
contract-required precommitted seven-lane packet, do not claim search saturation, and carry no root
proof credit.

1. **Repo-local lane (`M3` statement/interface only).** The historical discovery module
   `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_045.lean` is Git blob
   `65c55c0d2fc914880209131464e92e920b298a4c`, SHA-256
   `70646e0d9bc0f9df5fc17ca4dd3e22db05386df5e7e129b7e80f9781fa7a09f9`, and has
   unchanged bytes since repository commit
   `16d227cffb7cb7d9e8392b6c0ff8211e498e1330`. It elaborates a locally invented generic
   quaternion datum, geometric package, lightweight order/level/functor records, a proposition-
   valued representation boundary, support wrappers, audit metadata, and explicit no-completion
   gates. The decisive sheaf and representability properties are stored in data rather than proved
   from a classical Shimura moduli problem. It contains no source-exact terminal Shimura-curve
   theorem and receives no rev-5.6 acceptance or proof-body credit.

2. **Related repo-local lane (`M3` statement/interface only).** The independent legacy module for
   the near-duplicate catalog target `THM-M-0435`,
   `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_084.lean`, is Git blob
   `5fbd2476579a6c69a60f67dcaed926b005c5e09b`, SHA-256
   `1c3ce78fe131b2bc5657075e59c22eead0f62972f279426aea4f8ec41f92f37f`.
   It likewise labels its arithmetic moduli predicate and representing object as missing and
   records no terminal theorem. `THM-M-0435` is not a v2 hard parent, reuse hint, or shared-group
   provider for this claim; its bytes are an informative same-topic observation only, and its
   acceptance is neither inspected as a parent nor transferred.

3. **Pinned mathlib lane (`M3` substrate only).** The manifest fixes mathlib revision
   `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
   `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, under Lean `v4.29.0`. Read-only
   searches across all materialized pinned package Lean sources found zero files matching
   `ShimuraCurve`, `Shimura curve`, `quaternionic moduli`, `moduli ... quaternion`, or
   `ModularCurve`. Mathlib does provide the generic substrate
   `QuaternionAlgebra` in `Mathlib/Algebra/Quaternion.lean` (Git blob
   `0561808266bc2f2106020ab5a70d22c52ae4b68b`, SHA-256
   `514cbe3ddd0007c66ce468a70db3f09f3a6bb2a49edb0a41a227d99396267957`) and
   `QuaternionAlgebra.basisOneIJK` in `Mathlib/Algebra/QuaternionBasis.lean` (Git blob
   `4c332a97f538c9a6239b164749c7ca10d208f4f5`, SHA-256
   `531b78d62bbce860a5bf6f5c0d188f92e0817952de993e4aa21cf706ca8f2049`).
   These object APIs are not a curve construction, representability theorem, canonical-model
   theorem, or uniformization theorem.

4. **Immutable external Lean 4 lead (`M5`, adjacent and incompatible).** The content-bound legacy
   audit records `ImperialCollegeLondon/FLT` at commit
   `2f4325e3b3e647225890f143d4f2dbf1315d4ebd`, with quaternion-algebra automorphic-form
   modules and declarations such as `IsQuaternionAlgebra`,
   `IsQuaternionAlgebra.IsTotallyDefinite`, and
   `TotallyDefiniteQuaternionAlgebra.WeightTwoAutomorphicForm`. That tracked audit reports no
   `ShimuraCurve`, `ModularCurve`, `Eichler`, or representability terminal theorem, active proof
   placeholders in relevant files, Lean `v4.30.0-rc2`, and mathlib
   `244d9a4c3071a109aa54a41242317594d3c83fb4`. External source bytes, license packet,
   terminal body, and transitive trust closure are not in this worker's pinned dependency closure.
   The lead is therefore adjacent `M5` research evidence, not `M1`, `M0-P`, or a pin/import/check
   target. Reopening requires immutable licensed source bytes, a placeholder-free exact declaration,
   normalized comparison against an approved canonical target, compatible dependencies, and a
   consumer-owned replay.

5. **Statement-only collection lane (`M4` access-limited, no target-negative claim).** A tracked
   audit records a complete recursive tree observation for
   `google-deepmind/formal-conjectures` at commit
   `b2e608fc52d765510915a244bb69b1a2741acc3c`: `1204` paths,
   `truncated=false`, with response SHA-256
   `76fa3f96fc2ff7fc85addfd1e85852dae3fcb5022fc1ef35b030a3dc1e3efc61`.
   The observation is preserved in
   `Stage1_Instances/THM-M-0590/anchor-audit.json` (Git blob
   `d14353da79b9c870fe0b1cb4f0e7875f04a63fa9`, SHA-256
   `6a506ed464abfde062f0d0a8593a1f9eeda50737ab5e6b4feacc6fa31c6470cb`).
   That target-owned record contains the response hash and its own BDF-specific filtering result,
   but it does not preserve the response bytes or the 1204 path values needed to replay a
   Shimura-target alias filter. Searching only the summary record would not prove absence from the
   external tree. This run therefore records an access limitation, not a Shimura-curve negative
   result. Reopening requires the immutable tree bytes or a concrete matching declaration.

6. **Historical/other-prover lane (`M4`).** No content-bound other-prover theorem or checked
   canonical-claim mapping is selected in the repository. The historical Stage1 modules are Lean 4
   planning surfaces, not independent backend completion. A later artifact must bind an immutable
   theorem, exact claim mapping, foundations, and a checked consumer transport before it can affect
   Lean proof status.

7. **Primary human-source lane (`H2`, `M4`).** The same-topic `THM-M-0435` dossier identifies Goro
   Shimura, "Construction of class fields and zeta functions of algebraic curves," *Annals of
   Mathematics* (2) 85 (1967), 58-159, DOI `10.2307/1970526`, as a candidate primary
   publication. The repository preserves no immutable source copy, exact theorem/page, incorporated
   definitions, field/algebra/order/level hypotheses, selected analytic/algebraic/moduli model,
   exact conclusion, correction or errata disposition, translation, or independent source review.
   It is bibliographic discovery evidence only and does not reach `H0` or select the canonical Lean
   proposition.

The exact target remains unfrozen. Consequently no candidate can be normalized as exact, assigned
a statement fingerprint, or credited as `M0-L`, `M0-W`, `M0-P`, or `M1`. The strongest truthful
root boundary remains `[H4, M4, R4]`: no usable exact formal artifact has been located for a source-
authorized proposition, and no external proof is eligible for integration. Fresh public code search
was unavailable in the network-denied worker runtime, so global absence and discovery saturation
are expressly not claimed.

## Commands and exact results

All Lean and dependency checks used the automation-provided canonical `.lake` link read-only. No
`lake update`, `lake build`, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, v2 DAG, phase contract, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 states, two hard edges, five hints, 311 shared groups, and acyclicity passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0126` | 0 | rank 45, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and twenty-three source references passed |
| existence and `git cat-file -e HEAD:<path>` checks for both declared validators | expected absent | zero scheduler-owned anchor-audit validator candidates exist at the immutable worker base |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0126/StatementInfrastructure.lean` | 0 | generic quaternion-algebra and scheme types elaborated; three nonfatal sandbox stream-fd warnings preceded the expected types |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_045.lean` | 0 | legacy interfaces, support wrappers, and explicit no-completion gates elaborated; no exact root theorem |
| exact alias scans over every materialized pinned-package Lean source | expected no match | no pinned Shimura-curve or quaternionic-moduli terminal declaration located |
| declaration-position prohibited-construct scan over target-owned Lean and `S1_M_045.lean` | expected no match | no `sorry`, `admit`, `axiom`, `constant`, `opaque`, unsafe declaration, `implemented_by`, `native_decide`, or `sorryAx`; this does not turn proposition-valued interface fields into a proof |
| pinned mathlib and `flt-regular` revision/tree/status checks | 0 | revisions and trees match `lake-manifest.json`; both dependency worktrees are clean |
| schema-1.1 ledger validation against this claim's graph/base | expected fail | stale observed-graph/base binding confirmed; the empty context itself is correct, but only an eligible fresh worker may refresh phase evidence |
| `git diff --check -- Stage1_Instances/THM-M-0126 .stage1-worker-selftest.json` | 0 | no whitespace errors in the owned handoff |

No anchor validator argv exists to record. In particular, the two successful Lean elaborations are
scoped interface evidence only and cannot be interpreted as the mandatory semantic validator result
or `phase_accepted=true`.

## Retry condition and status boundary

The scheduler must commit exactly one declared anchor-audit validator at one of the two contract
paths and issue a fresh claim whose worker base contains that identical blob. The statement
predecessor must separately become master-accepted `[x]`. A fresh worker can then precommit the
seven-lane protocol before replay, refresh the schema-1.1 dependency ledger to that graph/base,
content-bind every candidate, negative result, and access failure, produce exactly one
`stage1-node-receipt/1.0`, and run the unchanged validator using the exact contract argv.

No anchor-audit phase receipt and no `.stage1-worker-selftest.json` are produced. This target-scoped
blocker changes no task state and grants no phase acceptance, source acceptance, proof credit,
provider acceptance transfer, `AUDIT-Z`, `THEOREM-Z`, audit completion, theorem completion, or
master acceptance.

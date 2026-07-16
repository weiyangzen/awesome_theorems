# THM-M-0007 anchor-audit authority blocker

Item: `S56-M-0007-ANCHOR_AUDIT`  
Theorem: `THM-M-0007`  
Claim order: `(v2_execution_rank=316, phase_layer=2,
phase_item_id=S56-M-0007-ANCHOR_AUDIT)`  
Worker base revision: `739d30014e3a21d9f0abfa3b9ae206d4c32f120c`  
Worker base tree: `2728571d64aefe781c1b17e97dafc9343fc129f4`  
Worker verdict: `blocked`  
Proposed state: `[ ]` (unchanged)  
Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The mandatory HEAD contract, `Docs/Stage1_Phase_Acceptance_Contracts.json` at
SHA-256 `1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`,
declares exactly these candidates for `anchor_audit`:

- `Stage1_Instances/THM-M-0007/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0007/check_anchor.py`

Neither path exists in the worker-base commit. The contract requires exactly one candidate, its
presence at the worker base, and equality of its HEAD and worker-base Git blobs. Current integration
code also protects every declared candidate from worker addition, modification, or deletion.
Creating either validator in this clone would therefore be rejected rather than becoming
authority-replay evidence; creating both would additionally make selection ambiguous. An
undeclared adapter, prose stdout, or exit code zero cannot substitute for the missing scheduler-owned
validator. Consequently the worker cannot lawfully produce the required self-test handoff or a
phase receipt claiming completion.

`G02-TOPOLOGY` is independently still closed. The sole intra-theorem predecessor,
`S56-M-0007-STATEMENT`, is authoritative `[_]`, not master-accepted `[x]`. Its receipt is an honest
blocked statement packet: there is no source-exact convergence/naturality convention, canonical
Lean expression, or statement fingerprint. Anchor discovery can still be observed, but this claim
cannot support dependency-ordered master acceptance.

## Dependency and reuse audit

The authoritative theorem-DAG SHA-256 is
`ccfe534e697065f0d1501abba8d092102230694e73f0335f2a6d2faa92b42876`, and the
target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The complete `parent_inspection_order`, direct-parent closure, transitive-ancestor closure,
hard-edge set, reuse-hint set, and shared-group set are all exactly empty. Thus the prescribed
inspection traversal is empty and complete. No provider declaration, proof body, receipt,
checkbox, or acceptance is consumed, copied, transported, or inherited. This empty graph closure
is not a mathematical-independence claim.

The existing `dependency-reuse-ledger.json` is schema
`stage1-dependency-reuse-ledger/1.1` and correctly records the same empty context, but it binds the
earlier graph/repository revision from the statement worker. It is deliberately not rewritten in
this blocked handoff: refreshing it alone cannot repair the missing immutable validator, and the
phase is not genuinely self-tested.

## Bounded anchor observations

These observations are content-bound discovery evidence, not a completed phase inventory or proof
credit.

1. **Repo-local lane (`M3`).** The current target owns only a negative statement probe.
   `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_094.lean` has SHA-256
   `99790fe00cca6aaa5429cb183e410095cd1febe648f5162af232abc2feaef5b7` and Git blob
   `085ac544d4536e1137ae8a2de119236c5c889a04`. It defines expected right-derived objects, an
   abstract `GrothendieckSpectralSequenceBoundary`, conditional statement shape, metadata, and
   checked substrate wrappers. Its `spectralSequence` field is an arbitrary `Type`, and its
   naturality and convergence fields are bare `Prop`s. It contains no terminal proof of the source
   theorem and is excluded as a broadened proxy.

2. **Pinned-mathlib lane (`M3`).** The manifest-pinned mathlib revision is
   `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
   `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Its checked source contains
   `Functor.rightDerived`, `Functor.isZero_rightDerived_obj_injective_succ`,
   `Functor.rightDerivedZeroIsoSelf`, `NatTrans.rightDerived`, `SpectralSequence`, and
   `E₂CohomologicalSpectralSequenceNat`. Exact fixed-string searches over all pinned Mathlib
   Lean sources returned zero files for `grothendieckSpectralSequence`, `Grothendieck spectral
   sequence`, `GrothendieckSpectralSequence`, `stronglyConvergesTo`, and `VanishesOnGEOne`.
   There is no located terminal Grothendieck construction, page-two identification, convergence,
   or abutment declaration.

3. **Official/external Lean lane (`M1` candidate only, no local proof credit).** The tracked legacy
   record names `joelriou/lean-derived-categories` at immutable revision
   `c1d75ecdb3bbb9d85b161bade0aadfa1c2b7f6e4`, its `joelriou/mathlib4` dependency at
   `d886e33fd2f029f2304dfd20d9069d5fa7f3aa1a`, Lean `v4.21.0-rc3`, module
   `Mathlib.Algebra.Homology.SpectralSequence.Examples.Grothendieck`, and four
   `DerivedCategory.Plus.grothendieckSpectralSequence` family names. The external tree is not in
   this Lake closure, its source bytes and terminal body are not locally materialized, and its
   fork/toolchain are incompatible with the pinned consumer. It is a credible immutable integration
   anchor, but not `M0-P`, a checked transport, or transferable acceptance.

4. **Other-public and statement-only lanes (`M4`/`M3`).** Network access is denied in this worker,
   and no additional immutable public Lean repository or statement collection is pinned in the
   dependency closure. The repo-local abstract statement surface is broader than the still-unfrozen
   source claim. The legacy record also binds a 2026-05-01 upstream-main raw-path 404 observation;
   that access-limited historical result is not a saturation or global-nonexistence claim.

5. **Historical/other-prover and primary-human lanes (`M4`, `H1`).** Weibel,
   *An Introduction to Homological Algebra* (1994), section 5.8, especially Theorem 5.8.3, identifies
   the theorem family. No immutable page bytes, definition-level transcription, assumptions and
   errata crosswalk, or independent source review is owned here. No other-prover artifact is
   selected. Human publication knowledge supplies no Lean terminal body and does not reach `H0`.

The strongest truthful root boundary remains: a credible external Lean theorem-family anchor exists,
but the canonical consumer statement is still unfrozen and no exact body is integrated or replayed
locally. No `M0-*`, source acceptance, discovery saturation, `AUDIT-Z`, `THEOREM-Z`, audit
completion, theorem completion, or provider acceptance transfer is claimed.

## Validation performed

No `.lake` update, build, clone, fetch, or other dependency mutation was run. The automation-provided
`.lake` symlink was used read-only.

| Command | Exit | Scope |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | global rev-5.6/v2 structural baseline |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546-node graph, state, and acyclicity projection |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0007` | 0 | rank 94, planned, rework required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0007/Statement.lean` | 0 | only the target-owned right-derived/spectral carrier boundary |
| `cd Formalizations/Lean && lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_094.lean` | 0 | legacy interfaces, metadata, and substrate wrappers only |
| exact fixed-string `rg` queries over pinned `Mathlib/**/*.lean` | 0 | zero terminal-root/convergence-name matches listed above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision/tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |

The Lean commands emitted three environment warnings, `Failed to create stream fd: Operation not
permitted`, but returned zero and printed the expected declaration types. That is scoped
elaboration evidence only; no validator semantic result or phase acceptance is inferred from it.

## Retry condition

The scheduler must commit exactly one declared anchor-audit validator, then issue a fresh claim
whose worker base contains the identical validator blob. A fresh worker can refresh the ledger to
that base, precommit and replay all seven discovery lanes, bind immutable candidate/source bytes,
produce exactly one phase receipt, and run the unchanged semantic validator. Master acceptance must
still wait for `S56-M-0007-STATEMENT` to become `[x]` and must independently satisfy every common
rev-5.6 gate.

No `.stage1-worker-selftest.json`, anchor-audit receipt, or fabricated semantic result is produced.
This target-scoped blocker grants no state transition or acceptance.

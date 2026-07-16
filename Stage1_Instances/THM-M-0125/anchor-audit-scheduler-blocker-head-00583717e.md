# THM-M-0125 anchor-audit scheduler blocker

Item: `S56-M-0125-ANCHOR_AUDIT`

Theorem: `THM-M-0125`

Claim order: `(v2_execution_rank=278, phase_layer=2,
phase_item_id=S56-M-0125-ANCHOR_AUDIT)`

Worker base revision: `00583717e4a5f73f89f5ffee33343caf65cc9721`

Worker base tree: `9f2ff1432d1b90ade32db3437fd531e38b49dcf3`

Worker verdict: `blocked`

Proposed state: `[ ]` (unchanged)

Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The mandatory HEAD contract, `Docs/Stage1_Phase_Acceptance_Contracts.json` at
SHA-256 `1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`,
declares exactly these scheduler-owned candidates for `anchor_audit`:

- `Stage1_Instances/THM-M-0125/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0125/check_anchor.py`

Neither path exists in the worker tree or in the worker-base commit. The contract requires exactly
one candidate, requires it to exist at the worker base, and requires its HEAD blob to equal its
worker-base blob. The assignment expressly forbids the worker from creating, refreshing, renaming,
replacing, or deleting either candidate. Therefore there is no lawful validator argv and no command
that can emit the required single `stage1-validator-semantic-result/1.0` JSON object. An undeclared
adapter, the statement validator, prose output, or exit code zero cannot substitute for the missing
scheduler-owned validator.

Consequently this worker does not manufacture an anchor inventory, discovery-evidence packet, phase
receipt, or `.stage1-worker-selftest.json`. Those artifacts could not be lawfully self-tested or
handed off at this base.

The independent topology gate `G02-TOPOLOGY` is also closed for master acceptance. The sole
intra-theorem predecessor, `S56-M-0125-STATEMENT`, is authoritatively `[_]`, not master-accepted
`[x]`. Its current receipt truthfully records a blocked statement boundary rather than a frozen
source-exact Gross-Zagier proposition.

## Dependency and reuse audit

The authoritative theorem-DAG SHA-256 is
`6c46a13db8e9d6a299fca9894fba72529f3cd80df81c82e6e4937cbef997f038`, and the
target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The complete `parent_inspection_order`, direct-hard-parent closure, transitive-hard-ancestor closure,
hard-edge set, reuse-hint set, and shared-group set are all exactly empty. The prescribed empty
sequence was traversed once as the complete closure before any proof work; no proof work was
performed. No provider phase state, receipt, declaration body, reusable artifact, proof body,
checkbox state, copy, transport, or acceptance was consumed or inherited. The empty graph closure
does not assert mathematical independence.

The existing `dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1` and records empty inspections, reuse decisions, and unresolved
compatibility obligations, but it is bound to the prior statement claim's graph digest, repository
revision, phase layer, and item ID. It is deliberately not refreshed in this blocked run. Rewriting
it alone cannot repair the absent immutable validator and would invalidate the existing statement
receipt's exact support-file binding. A fresh eligible anchor-audit claim must refresh the empty
ledger to its own base and claim tuple before producing a handoff.

## Bounded anchor observations

These observations are target-scoped discovery guidance only. They do not constitute the
precommitted, replayable, content-bound seven-lane inventory required by `A02-DISCOVERY`, and they do
not claim global search saturation.

1. **Repo-local lane (`M4` root; legacy interface only).**
   `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_044.lean` has SHA-256
   `30198b949c774f5de2e19cbcda28d60fe03962698e9a9a7ed9f2acc301028f52`. It explicitly says it is a
   conservative statement boundary, not a proof. Its `CentralDerivativeLFunctionAPI`,
   `NeronTateHeightPairingAPI`, `HeegnerPackageAPI`, and `GrossZagierNormalizationAPI` accept the
   missing arithmetic objects and propositions as fields. `StatementShape` quantifies over this
   caller-supplied package. The two checked anchors cover only a Weierstrass discriminant identity
   and differentiability of nontrivial Dirichlet L-functions. The module also records its own
   historical authenticated-search blocker and `externalLeanGrossZagierSearchRepoLocalClosed =
   false`. It is useful vocabulary and negative provenance evidence, but it is a broadened abstract
   interface rather than a source-exact Gross-Zagier declaration and receives no root proof or
   acceptance credit.

2. **Pinned-mathlib lane (`M3` substrate; no root candidate).**
   The Lake manifest pins mathlib revision
   `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
   `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, under Lean `v4.29.0`. A bounded
   case-insensitive scan of its Lean sources for `Gross-Zagier`, `GrossZagier`, Heegner-point,
   Neron-Tate, Hasse-Weil, and Rankin-L spellings located no compatible terminal declaration. The
   pinned tree does contain adjacent Weierstrass, generic L-series/derivative, modular-form,
   Petersson, and generic height infrastructure. None constructs the selected arithmetic L-series,
   Heegner divisor or point, Neron-Tate height, or Gross-Zagier equality. These are substrate
   candidates only, not an exact root proof.

3. **Official-primary and other immutable public Lean lanes (`M5` access-bound).**
   This worker has network access denied and the pinned Lake closure contains no separate
   Gross-Zagier project. The tracked legacy module precommits the public-code queries
   `Gross-Zagier`, `GrossZagier`, `Heegner`, `NeronTate`, and `HasseWeil`, but its dated 2026-05-01
   record says authenticated GitHub code search was unavailable. No repository URL, immutable
   revision, source bytes, exact declaration type, terminal body, dependency lock, toolchain, trust
   closure, or license for an external candidate is present at this base. The honest classification
   is an access-limited `M5` lane, not a negative global result and not `M1`.

4. **Statement-only collections (`M4`).**
   The current target-owned `Statement.lean` is deliberately a minimal Weierstrass/complex-derivative
   vocabulary probe, not a canonical Gross-Zagier statement. The broader legacy `StatementShape`
   is assumption-bearing and source-unspecific. No statement-only artifact can be normalized to an
   exact root because the authoritative target has not selected a source variant or frozen an
   expression fingerprint.

5. **Historical or other provers (`M4`).**
   No immutable other-prover formalization, theorem identifier, source bytes, or checked translation
   is materialized in the repository. General mathematical familiarity and historical publication
   status do not provide a Lean declaration or transport.

6. **Primary human source (`H2`, not `H0`).**
   The target crosswalk identifies Gross and Zagier, *Heegner points and derivatives of L-series*,
   Inventiones Mathematicae 84 (1986), 225-320, DOI `10.1007/BF01388809`. A prior target-owned
   recheck records an author-hosted 96-page scan of 4,395,679 bytes with SHA-256
   `8afee839cdc0e2056c6dcbe348e39c0a6aa27344125d8c3b80dd735f2e6d9521` and distinguishes Chapter I
   Theorems (6.3) and (7.3), Chapter V Theorem (2.1), and the Euler-factor correction after I.(5.3).
   Those scan bytes are not preserved in the repository, no independently accepted transcription
   exists, and the catalog gloss does not choose among these materially different formulas. Exact
   binders, hypotheses, L-series normalization, Heegner object, height convention, parametrization,
   constants, local factors, corrections, and degenerate cases remain unfrozen. This is a useful
   source-family and locator audit, but it cannot support H0 or exact candidate compatibility.

The strongest truthful current boundary is therefore a root `M4`: the canonical consumer statement
is not frozen, no compatible proof-bearing Lean declaration is materialized, and no checked external
integration is available. Individual repo-local and mathlib declarations are `M3` interface or
substrate candidates, while public-project access remains `M5`. No candidate receives `M1`,
`M0-L`, `M0-W`, or `M0-P` root credit. No accepted exact reuse or checked transport exists.

## Checks run

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
automation-provided canonical `.lake` link was treated as read-only.

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure, 1546-target manifest, v2 DAG, seven-phase contract, and execution skill pass |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 phase states, 2 hard edges, 5 hints, 311 shared groups, acyclic |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets in rank order |
| `python3 scripts/stage1_target.py show THM-M-0125` | 0 | rank 44, planned, L0/rework-required, legacy evidence unaccepted, theorem incomplete |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | all 7 phase contracts, 12 common gates, and 23 source references pass structurally |
| base/worktree existence and `git cat-file -e HEAD:<candidate>` checks for both declared anchor validators | expected absent | zero scheduler-owned anchor-audit candidates exist at the immutable worker base |
| exact target-node and relationship queries over `Docs/Stage1_Theorem_DAG_v2.json` | 0 | v2 rank 278 and the exact empty dependency/reuse closure agree with this claim |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0125/Statement.lean` | 0 | target-owned Weierstrass/derivative vocabulary probe elaborates; three nonfatal sandbox stream-fd warnings precede its two printed types |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_044.lean` | 0 | legacy abstract boundary elaborates with three nonfatal sandbox stream-fd warnings; no exact-root credit |
| bounded case-insensitive `rg` over repo-local and all manifest-pinned Lean sources | expected no exact-topic match in pinned packages | legacy abstract interfaces and adjacent substrate found repo-locally; no materialized exact Gross-Zagier terminal declaration in the dependency closure |
| `python3 -m json.tool Stage1_Instances/THM-M-0125/dependency-reuse-ledger.json` | 0 | existing schema-1.1 empty ledger parses; it remains deliberately bound to the prior statement receipt |
| `git diff --check -- Stage1_Instances/THM-M-0125 .stage1-worker-selftest.json` | 0 | no whitespace errors in the target-owned blocker delta |

There is no anchor validator command to run. In particular, a successful structural check or Lean
elaboration cannot be converted into a semantic anchor-audit result or `phase_accepted` claim.

## Retry condition and status boundary

The scheduler must commit exactly one declared anchor-audit validator and issue a fresh claim whose
worker base contains that identical blob. The statement predecessor must separately become
master-accepted `[x]` before master phase acceptance. A fresh worker can then precommit and execute
the complete seven-lane discovery protocol, content-bind every candidate, negative result, access
failure, query, immutable revision or response hash, refresh the empty schema-1.1 dependency ledger
to that fresh graph/base/claim tuple, produce exactly one `stage1-node-receipt/1.0`, and replay the
unchanged validator using the contract argv.

No `.stage1-worker-selftest.json` and no anchor-audit receipt are produced. This target-scoped
blocker grants no state transition, phase acceptance, provider acceptance transfer, proof credit,
H0, M0, R0, `AUDIT-Z`, `THEOREM-Z`, audit completion, theorem completion, or master acceptance.

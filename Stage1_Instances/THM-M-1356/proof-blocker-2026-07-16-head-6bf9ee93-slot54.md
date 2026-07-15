# THM-M-1356 proof blocker at `6bf9ee93` (slot54)

Item: `S56-M-1356-PROOF`

Intent: `prove`

Recorded: `2026-07-16` (`Asia/Shanghai`)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. No placeholder-free arbitrary-degree proof body was implemented or
found for `Stage1Instances.THM_M_1356.RouthHurwitzTarget`. The proof item stays
`[ ]`, the lifecycle stays `planned`, and neither the audit nor the theorem is
complete. This run adds the required v2 dependency-reuse ledger and current-base
blocker evidence only.

The existing `Proof.lean` remains valid partial work. Its four declarations
prove the exact degree-one coefficient adapter, root characterization, unique
Hurwitz minor, and stability/minor equivalence. A fresh trust-zero replay passed
and reported only `propext`, `Classical.choice`, and `Quot.sound`. The canonical
target quantifies over every positive degree, however, so this specialization
closes none of the frozen arbitrary-degree obligations.

## Dependency And Reuse Audit

The observed v2 graph SHA-256 is
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
and the target context SHA-256 is
`ce269c68f2f99e96acfe3223876276642cec20bc6d75e84b494f365653ffbcd1`.
The target has no direct hard parent, transitive hard ancestor, hard edge, or
reuse hint. The new schema-1.1 ledger records the empty inspected closure and
audits both weak shared-module groups:

- `THM-M-0048` is intake-only. Its determinant-module probe supplies neither a
  Cauchy-Binet proof nor any Routh-Hurwitz body or checked transport.
- `THM-M-1592` is intake-only. Its polynomial-roots probe supplies neither a
  Reed-Solomon proof nor any Routh-Hurwitz body or checked transport.

Both decisions are therefore `not_applicable`; no shared-group evidence is
credited. The repository's executable ledger validator accepts the exact graph,
context, base revision, two decisions, and empty unresolved-obligation list.

## First Failed Gate

The first workflow failure is prerequisite acceptance and freshness:
`S56-M-1356-OBLIGATION_TREE` is worker-provisional (`[_]`) rather than
master-accepted, and its checker hard-pins base `431e77db...` and rejects the
current base before substantive checks.

Independently, the first proof-content failure is the absence of exact
arbitrary-degree bodies upstream of both root cuts:

- `M1356-B-STABLE-TO-MINORS`
- `M1356-B-MINORS-TO-STABLE`

The frozen registry contains 50 obligations, including 45 machine-required
obligations. All 45 required terminal proof-body IDs are null; 40 required
leaves still have planning fingerprints rather than Lean proposition
interfaces. The missing implementation includes the alternating even/odd
construction, signed Euclidean/Sturm sequence, Hermite hodograph and Cauchy
index bridges, regular and nonregular Routh cases, Hurwitz-block elimination,
and the leading-minor product identity. `ObligationTree.lean` consumes the two
complete directions as explicit premises and proves neither one.

No statement inconsistency or vacuity was found. The positive leading
coefficient prevents degree drop, and the finite matrix is the transpose
convention for the usual Hurwitz matrix, which preserves its leading principal
determinants. Degree-one, degree-two, and degree-three expansions agree with the
classical criterion.

Scoped scans found no Routh-Hurwitz, Hermite-Biehler, Hurwitz-matrix criterion,
Lienard-Chipart, or Cauchy-index terminal in pinned mathlib, `flt-regular`, or
repo-local Lean sources. The immutable near-candidate
`PerAlexandersson/RealRooted@634a949d31683785b4181efbba6faff31e81e006`
remains ineligible: its root-critical Hermite-Biehler, conformal, stable-to-
matrix, and matrix-to-stable declarations contain explicit `sorry`, and its
weak right-half-plane/infinite-total-nonnegativity target is not the frozen
finite strict-principal-minor equivalence.

## Narrow Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink was used
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, the 1546-target baseline, v2 DAG, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 preserved states, 2 hard edges, 5 hints, 310 shared groups, and acyclicity passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets passed. |
| `python3 scripts/stage1_target.py show THM-M-1356` | 0 | Rank 966; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-1356/check_statement.py` | 0 | Expression SHA-256 `7901eb74...98bf`; four mutations distinguished; three import-deletion probes failed as required; pinned mathlib revision agreed. |
| `python3 -B Stage1_Instances/THM-M-1356/check_anchor_audit.py` | 0 | Exact local statement only; pinned topic inventory and external terminal inventory empty; provisional root `M3`. |
| `python3 -B Stage1_Instances/THM-M-1356/check_obligation_tree.py` | 1 | Expected current freshness blocker: hard-pinned base `431e77db...` disagrees with current HEAD. |
| Isolated ordered `lake env` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` with `--trust=0 -t0` | 0 | All modules elaborated. Olean SHA-256 values: Statement `f8479767...cf4`, ObligationTree `4b3dc2ef...21e4d`, Proof `dbd13ed0...e66cf`; printed axioms were only `propext`, `Classical.choice`, and `Quot.sound`. |
| Actual schema-1.1 `validate_dependency_reuse_ledger` call with the claim graph and base bindings | 0 | `THM-M-1356`; 0 hard-context inspections, 2 weak-group decisions, 0 unresolved compatibility obligations. |
| Pinned and repo-local exact-topic scans | 0 wrapper | Both source sets had zero candidate files outside this dossier. |
| Frozen registry count query | 0 | 50 total, 45 machine-required, all 45 required terminal body IDs null; 40 required planning fingerprints. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | The claim-base graph passed with all 1546 nodes and context counts before owned handoff files were written; integration must regenerate its evidence inventory after merging them. |
| `python3 -m json.tool` on new JSON files and `git diff --check` | 0 | Structured artifacts parse and the owned delta has no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the assigned proof phase is incomplete. |

The direct command `cd Formalizations/Lean && lake env lean
../../Stage1_Instances/THM-M-1356/Proof.lean` exited 1 because the target-local
`import Statement` is not on the Lake root's module path. The isolated replay
sets the target directory on `LEAN_PATH`, compiles `Statement.lean` first, and
then validates the proof successfully without writing build output to `.lake`.

Pinned identities were Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, mathlib revision/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, and `flt-regular`
revision/tree `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`.

## Retry Boundary

First reconcile the provisional predecessor and the repeated whole-root attempt
history. If five unresolved scheduler ticks are confirmed, apply the rev-5.6
split rule rather than redispatching the unsplit root. Then formalize the frozen
dependency-legal Hermite/Cauchy/Sturm/Routh and Hurwitz-minor-product leaves
without placeholders, close both exact direction packages, and compose them to
the unchanged root. An alternative is an immutable, license-compatible exact
Lean 4 terminal whose statement, pins, proof body, provenance, placeholders,
axioms, and trust closure can all be checked.

This is target-owned, current-base, nonrelease blocker evidence. It does not
satisfy `S56-M-1356-PROOF`, propose worker `[_]`, close an obligation or the
root, alter scheduler state, or claim proof completion, audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

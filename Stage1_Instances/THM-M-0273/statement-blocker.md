# Exact-statement gate: blocked

Item: `S56-M-0273-STATEMENT`

Theorem: `THM-M-0273`

Base revision: `2612b21a0cd5f3f13bd2223af801c73511f950c0` (tree
`62baf871bcb662ecc80ad61fc2909e065d211ab5`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0273-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. It deliberately leaves the canonical
mathematical claim, Lean declaration, expression hash, and target environment fingerprint null.
This dependency still requires master acceptance before a statement transition can be accepted.

Independently, the exact-statement gate cannot be passed from the received source record. The
catalog gives only the name Radon-Nikodym theorem, the 1930 attribution, and the gloss "absolute
continuity of measures and density functions." It does not select positive, signed, complex, or
vector measures; the direction of absolute continuity; finite, sigma-finite, s-finite,
localizable, or abstract decomposition hypotheses; implication, converse, or equivalence; the
density codomain and its measurability, integrability, or finiteness; measure equality versus a
setwise integral identity; almost-everywhere uniqueness; or any zero, empty, infinite, or
non-sigma-finite boundary case. `Docs/Stage0_Blueprint.md` explicitly leaves the precise
definitions and premises open.

The intake's primary-source lead does not remove those choices. The inspected scan of Otton
Nikodym's 1930 paper, printed Theorem III on page 168, concerns a perfectly additive real-valued
set function `F` on a field `H`, a null-set condition, existence of a real density giving a
set-integral formula, and uniqueness modulo a null set. Its incorporated historical definition
chain, modern measure-theoretic translation, exact assumptions, proof boundary, corrections and
errata, and independent review have not been admitted. The catalog does not say whether this
historical signed implication-plus-uniqueness statement or a modern positive-measure form owns the
root.

These are proposition-changing decisions. Freezing the familiar positive sigma-finite statement,
the pinned `HaveLebesgueDecomposition` equivalence, its one-way implication, or the signed-measure
candidate would invent or substitute mathematics. Rev-5.6 sections 5 and 5.1 make statement
ambiguity and a missing elaborated-expression fingerprint hard blockers. There is consequently no
honest canonical expression for which minimal imports, checked transports, or the four required
statement mutations can be certified. The mutations are undefined, not passed, and the root
vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates using the pinned environment. It checks the positive
candidate
`MeasureTheory.Measure.absolutelyContinuous_iff_withDensity_rnDeriv_eq`, its one-way companion
`MeasureTheory.Measure.withDensity_rnDeriv_eq`, the finite and sigma-finite decomposition
interfaces, and the signed candidate
`MeasureTheory.SignedMeasure.absolutelyContinuous_iff_withDensityᵥ_rnDeriv_eq`. The positive
candidate uses `Mathlib.MeasureTheory.Measure.Decomposition.RadonNikodym`; the materially different
signed candidate needs
`Mathlib.MeasureTheory.VectorMeasure.Decomposition.RadonNikodym`. Both imports are therefore
appropriate for this discovery probe, but neither can be certified as the minimal import of an
absent canonical target.

All ten API checks elaborate. The three candidate axiom reports are exactly `propext`,
`Classical.choice`, and `Quot.sound`. This is real pinned interface evidence only: the probe defines
no target proposition, checked source-to-Lean transport, statement mutation, or proof body. A
bounded repository and pinned-mathlib search found the exact-topic candidates and adjacent uses,
but no already accepted source-identical root mapping. This observation is not the downstream
anchor audit and makes no global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No update, build, dependency clone or
fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0273` | 0 | rank 1020; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| repository source, Stage0, intake dossier, and Nikodym source-lead inspection | 0 | confirmed that the received gloss does not select one proposition and that the historical-to-modern definition and assumption map remains unreviewed |
| `sha256sum` over authority, intake, toolchain, probe, and pinned candidate sources | 0 | exact fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0273/IntakeProbe.lean` | 0 | ten positive/signed measure, decomposition, density, and exact-topic APIs elaborated; three candidate declarations reported the three axioms above; stdout SHA-256 `26c7f8d7155beccf566ea4e2abafbda72a412ff3f9b9576c37b49be8c3a4aebb` |
| bounded `rg` exact-topic search in repo-local Lean and pinned mathlib | 0 | found the positive and signed candidate families and adjacent uses; no source-identical mapping was credited |
| `python3 -B Stage1_Instances/THM-M-0273/check_intake.py` | 1 | historical intake replay stops at its frozen repository-base assertion: the intake records base `d3cbfa8941a8bcaafa3b8a690d1333f9643288ad`, while this later worker clone is at the base above; intake evidence was not rewritten |
| prohibited-declaration scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` commands are permitted |
| `python3 -m json.tool Stage1_Instances/THM-M-0273/statement-blocker.json` plus scoped blocker invariants | 0 | structured blocker parses; identity, dependency, null target/imports, undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0273` plus direct byte checks on both new files | 0 | no whitespace, missing-newline, carriage-return, or NUL diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

The intake checker freezes the intake run's original commit and nine-file artifact inventory. It is
historical evidence, not a later-phase validator. This statement run records its stale-base failure
instead of rewriting the intake instance, receipt, checker, task DAG, generated blueprint, or
authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before accepting a later statement
transition. Accountable reviewers must preserve and hash a lawful immutable source edition,
transcribe and independently approve one exact root proposition with every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum,
translation, and boundary case, and decide the historical signed versus modern positive scope.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile each credited
transport, and execute the removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.

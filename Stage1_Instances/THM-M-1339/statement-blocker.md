# Exact-statement gate: blocked

Item: `S56-M-1339-STATEMENT`

Theorem: `THM-M-1339`

Base revision: `8bbb7ffdbb5e6e8e3e1ffaba9955137f6b68c76c` (tree
`ade61913e5912b1160e25afe096df7f5b3b0cfed`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1339-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. The intake receipt
also declares `accepted: false`, has no accepted receipt ID, and intentionally leaves the canonical
mathematical statement and Lean target null. This is the earliest workflow blocker.

Independently, the exact-statement gate cannot be passed from the repository record. The title says
"continuous dependence of solutions on initial values", while the only gloss says "continuity with
respect to initial values and parameters". The record supplies no equation, state or parameter
space, solution model, common interval, regularity or uniqueness assumptions, topology, continuity
strength, source citation, proof boundary, or formal artifact. Its `已验证` label is untrusted under
rev-5.6.

The intake inspected Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*,
Section 2.4, as an authoritative source lead. It confirms rather than resolves the ambiguity:

- Theorem 2.8 compares solutions for different vector fields and initial states by an exponential
  estimate;
- Theorem 2.9 gives local joint initial-time/state dependence for a fixed vector field; and
- Theorem 2.11 gives explicit-parameter `C^k` dependence under stronger hypotheses.

The catalog does not cite this source or select one of those propositions. The official errata also
contains a page-45 correction relevant if Theorem 2.9 is selected. No complete source-to-target
crosswalk, independent source review, or decision about the broader parameter clause exists.

The following choices change the proposition rather than merely its notation:

- autonomous versus time-dependent equation and scalar, finite-dimensional, or Banach-valued state;
- time, state, and parameter domains and a common region on which solutions exist uniquely;
- classical derivative, derivative-within, integral-equation, local-flow, or maximal-solution model;
- continuity, Lipschitz, differentiability, completeness, boundedness, and uniformity assumptions;
- whether initial state, initial time, vector field, an external parameter, or a combination varies;
- pointwise or joint continuity, local Lipschitz continuity, uniform-on-compact convergence, a
  quantitative estimate, or differentiable-dependence conclusion;
- the title/parameter-clause relationship and boundaries with `THM-M-1340` and `THM-M-1341`; and
- ordered binders, universes, coercions, endpoints, zero radii or constants, empty intervals, and
  all other boundary cases.

Selecting a familiar textbook result, conjoining several results, or using an abstract package that
assumes continuity would invent or package the missing mathematics. Replacing the parameter clause
with fixed-field initial-state continuity would narrow the gloss; replacing continuity with
parameter differentiability or a variational equation would cross into neighboring targets.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint
hard blockers. Consequently there is no honest canonical target on which to claim minimal imports,
fixed elaboration, expression serialization, checked alternate transports, or removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutation tests. Those four mutations are
undefined, not passed. The provisional intake root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. It imports
`Mathlib.Analysis.ODE.PicardLindelof` and checks `IsPicardLindelof` plus two local-flow results. The
first is Lipschitz in the initial state at each time, and the second is jointly continuous in state
and time. Both concern one fixed vector field and neither quantifies an explicit external parameter.
They are discovery-only candidate APIs, not an exact `THM-M-1339` target or proof. Their import
cannot be called minimal for a target that has not been selected.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `Formalizations/Lean/.lake`
symlink was used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1339` | 0 | rank 950; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository and source `rg` inspection for the ID, title, gloss, and candidate families | 0 | found the sparse catalog record, explicit null intake target, and several inequivalent source families; no source-selected proposition |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `sha256sum` over authority, source, intake, probe, and toolchain inputs | 0 | hashes recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1339/IntakeProbe.lean` | 0 | the assumption package and two fixed-field candidate APIs elaborated; each candidate reported `[propext, Classical.choice, Quot.sound]`; no target was declared |
| bounded pinned-source search for continuous dependence and parameter dependence | 0 | located the two initial-state candidates and no explicit external-parameter ODE solution-dependence target; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1339/check_intake.py` | 1 | the historical receipt's authority-input hashes are stale after blueprint/DAG integration; the checker fails before its older base and exact-file-inventory assumptions |
| prohibited-construct `rg` scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1339/statement-blocker.json` and scoped invariant check | 0 each | blocker identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, and absent-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-1339` plus per-new-file no-index checks | 0; 1 each | no tracked diagnostics; both expected difference exits emitted no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The statement run does not rewrite the intake checker, intake receipt, historical hashes, task DAG,
generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. Accountable reviewers must then
preserve and hash an immutable primary or authoritative edition, select the exact root theorem and
variant, transcribe every incorporated definition, ordered binder, premise, conclusion, constant,
common-domain restriction, boundary case, proof boundary, correction, and erratum, decide how the
parameter clause relates to the title, reconcile neighboring targets, and independently approve the
source-to-target crosswalk.

A later statement worker can encode that same claim with real Lean definitions, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.

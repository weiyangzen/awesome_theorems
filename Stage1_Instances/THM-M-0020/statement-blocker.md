# Exact-statement gate: blocked

Item: `S56-M-0020-STATEMENT`

Theorem: `THM-M-0020`

Base revision: `f23ca64267b6746e12a641dcc66cc4dbaf1e2191` (tree
`d1872d3251ef6a9c395116467608691849d80496`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The statement
item remains `[ ]`. Its prerequisite intake is provisional worker state `[_]`, not master-accepted
state `[x]`; its receipt declares `accepted: false`, is not content-addressed, has no accepted
receipt ID, and deliberately leaves both the canonical mathematical claim and Lean target null.
Rev-5.6 section 10.2 permits this dependency-ordered attempt, but master acceptance remains required
before any later statement transition can be accepted.

Independently of that dependency boundary, the catalog supplies only the title Hasse-Minkowski
theorem and the gloss "local-global principle for quadratic forms." It gives no bibliography,
pinpoint result, incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
translation, correction record, or boundary policy. The catalog's `verified` label is untrusted
metadata under rev-5.6.

This wording does not choose among materially different classical roots:

- isotropy or existence of a nonzero zero of one quadratic form;
- global representation of a scalar by a form;
- rational or number-field equivalence of two forms; or
- classification by dimension, discriminant, signatures, and Hasse invariants.

Even under the common isotropy reading, the record does not fix the rational field versus an
arbitrary number field, the coordinate or coordinate-free representation, finite dimension,
regularity or nondegeneracy, the nonzero-witness convention, finite and infinite completions,
scalar extension, low-dimensional and degenerate cases, or an `iff` versus only the hard
local-to-global direction. Hasse's 1924 number-field representation paper and Minkowski's 1890
rational-equivalence paper are bibliographic leads, but neither primary text, theorem locator, full
premise map, translation and errata disposition, nor independent review is admitted in this
dossier. Selecting a familiar formulation would therefore invent, narrow, broaden, or substitute
mathematics rather than elaborate the exact received target.

There is also an unresolved ownership conflict. `THM-M-0423`, the separately cataloged Hasse
principle target, has a provisional coordinate-free isotropy statement. That artifact belongs to a
different target and its own files selected the classical quadratic Hasse-Minkowski scope. No
accepted alias, deduplication, correction, checked target transport, or canonical-root ownership
decision permits importing its statement identity or evidence into `THM-M-0020`.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. With no canonical proposition, there is no honest import set to minimize, no
expression or environment-expression fingerprint, no credited alternate transport, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation.
Those statement-gate outputs are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment with four imports for
quadratic-form radical/base-change and finite/infinite number-field-place infrastructure. All nine
adjacent API checks pass. This is real substrate validation, but the probe defines no canonical
Hasse-Minkowski proposition, checked source transport, or proof body. Its imports therefore cannot
be certified minimal for an absent target.

For discrimination only, the foreign `THM-M-0423/Statement.lean` also re-elaborates and prints the
following candidate family: every nondegenerate quadratic form on a finite-dimensional vector
space over an arbitrary number field is isotropic exactly when it is isotropic after scalar
extension at every finite and infinite completion. This confirms that one plausible encoding can
be typed. It does not establish that this is the source-identical `THM-M-0020` root, resolve the
duplicate ownership conflict, or transfer statement credit.

A bounded exact-name search found no Hasse-Minkowski declaration in pinned mathlib. Repo-local
matches were the foreign `THM-M-0423` surfaces and legacy statement/substrate material that
explicitly withholds terminal closure. These observations are discovery-only feasibility evidence,
not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0020` | 0 | rank 1014; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository source, Stage0, intake dossier, historical source leads, and duplicate-scope inspection | 0 | confirmed that the gloss supplies no binder-complete proposition and that `THM-M-0423` is foreign-owned unresolved overlap |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0020/IntakeProbe.lean` | 0 | nine adjacent quadratic-form, scalar-extension, and number-field-place APIs elaborated; no canonical target or proof body was declared |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0423/Statement.lean` | 0 | the foreign coordinate-free isotropy candidate elaborated and printed; target identity and ownership remain unresolved, so it receives no `THM-M-0020` credit |
| bounded exact-name search in pinned mathlib and repo-local Lean | 1/0 | no Hasse-Minkowski name in pinned mathlib; repo-local matches were foreign or legacy nonterminal surfaces only; discovery evidence, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0020/check_intake.py` | 1 | historical intake checker freezes the intake item as `[ ]`, while the integrated authoritative DAG now records `[_]`; it also freezes the original intake-only inventory, so this statement run records rather than rewrites that historical evidence |

## Retry Condition

The integration lane must master-accept the intake before accepting a later statement transition.
Accountable source reviewers must preserve and hash a lawful complete primary or authoritative
edition, select and independently approve one exact result and proof boundary, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, correction, translation, and
boundary case, reconcile the Hasse and Minkowski formulations, and issue an accepted identity and
canonical-root ownership decision for `THM-M-0020` versus `THM-M-0423`.

A fresh statement run can then encode precisely that claim, minimize the pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, node receipt, worker `[_]`, or master acceptance
is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.

# Exact-statement gate: blocked

Item: `S56-M-0056-STATEMENT`

Theorem: `THM-M-0056`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Rev-5.6 section 10.2 permits dependency-ordered preparation
while `S56-M-0056-INTAKE` is only provisional worker state `[_]`. Its receipt declares
`accepted: false`, is not content-addressed, has no accepted receipt ID, and intentionally leaves
the canonical human and Lean statements null. Master acceptance of that dependency remains
necessary before any later statement transition can be accepted.

Independently and decisively, the repository does not identify one exact proposition. It supplies
only the gloss "perturbation theory for eigenvalues of Hermitian matrices," the name Weyl's
inequality, the year 1912, and an untrusted `verified` label. It contains no formula, definition
chain, ordered binders, hypotheses, conclusion, source theorem locator, proof boundary, correction
history, or accountable review.

The proposition-changing choices left open include:

- the upper additive Weyl family, lower companion, their conjunction, an endpoint theorem, a
  one-matrix perturbation bound, or a two-matrix perturbation bound;
- real symmetric versus complex Hermitian matrices, scalar field, finite dimension and index type,
  universes, typeclass data, and zero-dimensional behavior;
- increasing versus decreasing eigenvalue enumeration, multiplicity, one-based versus zero-based
  admissible index arithmetic, and endpoint premises;
- matrix versus operator norm, the matrix-to-linear-map transport, and Hermiticity of sums or
  differences; and
- repeated eigenvalues, zero perturbation, and zero, scalar, singular, positive-semidefinite,
  indefinite, commuting, and singleton cases.

Weyl's inspected 1912 Section 1, Satz I is a complete historical source-family lead for symmetric
integral kernels in reciprocal Fredholm eigenparameter notation. It is not literally the catalog's
finite complex Hermitian-matrix wording. The inspected modern Zheng-Chen-Liu-Wang Corollary 2.5
states one upper additive finite-matrix inequality, but the intake does not select it as the
catalog root. Kernel-to-matrix transport, exact identity, definitions, corrections, preservation,
and independent review remain open.

Choosing a familiar finite-matrix variant would therefore invent, narrow, broaden, or substitute
the received theorem. Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression
fingerprint hard blockers. There is no honest canonical target whose imports can be minimized, no
credited alternate encoding for a checked transport, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation. The canonical root vector remains
unclassified; the intake's provisional family assessment remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with two direct imports from the pinned dependency
closure:

- `Mathlib.Analysis.InnerProductSpace.Rayleigh`
- `Mathlib.Analysis.Matrix.Spectrum`

It checks nine adjacent APIs for ordered Hermitian eigenvalues, eigenvectors, diagonalization,
spectrum identification, Rayleigh-quotient addition, and norm bounds. The complete probe output has
SHA-256 `85d8d4a812b6f3d91ebddb60d20a61c3d59cced0f433e5fa24160f1e3e407a71`.

This is real substrate validation only. The probe declares no canonical Weyl target, checked
transport, or proof body. A bounded search found only one unrelated repo-local eigenvalue-assumption
prose match and no exact eigenvalue-of-sum, perturbation, or indexed Courant-Fischer declaration.
That result is not a global nonexistence claim or the downstream anchor audit. The probe's imports
cannot be certified minimal for an absent canonical target.

As a feasibility check only, a temporary file encoded the familiar zero-based upper additive
candidate for complex Hermitian matrices over an arbitrary finite index type. It elaborated with
the single direct import `Mathlib.Analysis.Matrix.Spectrum`; the temporary source SHA-256 is
`3ec16aa95b004bf31cb7474e5ba8b7243832c64a1141d4468249efd3c7bafb50`. This confirms that one
unapproved candidate is expressible. It does not choose that candidate over the lower, combined,
or norm-perturbation variants and is not canonical statement evidence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0056` | 0 | rank 1523; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `git blame -L 419,424 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0056/IntakeProbe.lean` | 0 | nine adjacent pinned APIs elaborated; stdout hash recorded above; no canonical target or proof body |
| `cd Formalizations/Lean && lake env lean /tmp/THM-M-0056-import-probe.lean` | 0 | one explicitly uncredited upper-additive candidate elaborated with `Mathlib.Analysis.Matrix.Spectrum`; feasibility evidence only |
| bounded exact-topic search in repo-local Lean and pinned mathlib | 0 | one unrelated prose match; no exact Weyl eigenvalue-of-sum, perturbation, or indexed minimax declaration identified |
| `python3 -B Stage1_Instances/THM-M-0056/check_intake.py` | 1 | historical intake checker expects the intake item still to be `[ ]`; integrated authority now records provisional `[_]`, so it is stale and is not statement evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool` plus scoped `jq -e` blocker invariants | 0 | valid JSON; identity, null target/imports/fingerprints, unclassified root, unchanged provisional vector, four undefined mutations, false completion flags, exact change scope, and no-receipt/no-self-test boundary agree |
| `git diff --check` plus per-new-file `git diff --no-index --check /dev/null ...` | 0 diagnostics | no whitespace diagnostics; each no-index command exits 1 only because its file is new |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is bound to intake-time state and deliberately was not modified to make a
statement attempt pass. The generated blueprint, authoritative execution DAG, intake instance,
intake receipt, and target-local open task DAG remain unchanged.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash an immutable primary or authoritative source, select
and independently approve one exact proposition and proof boundary, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, admissible index, correction,
erratum, historical-to-modern transport, and boundary case. They must explicitly resolve the
additive or perturbation variant, scalar and index domains, eigenvalue enumeration, norm transport,
and every degenerate case.

A fresh statement run can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile each credited transport, and
execute all four required mutation classes. The integration lane must also revalidate and
master-accept the intake dependency before accepting that future statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no root classification or debt-vector change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, expression fingerprint, proof credit, or master acceptance is claimed.

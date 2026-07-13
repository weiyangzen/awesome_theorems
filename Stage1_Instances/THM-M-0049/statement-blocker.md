# Exact-statement gate: blocked

Item: `S56-M-0049-STATEMENT`

Theorem: `THM-M-0049`

Base revision: `a1c9974d7fb28cd680e6494b968544bf801a93a2` (tree
`1fa287bc821355aca2ca9e3ce107830a3eb58e64`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0049-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt is non-content-addressed, has
`accepted: false`, and deliberately leaves the canonical mathematical statement, formal target,
expression hash, and target environment fingerprint null.

The exact-statement gate cannot pass from the received catalog claim. The repository gives only
the name "Frobenius inequality," a 1911 Frobenius attribution, and the gloss "an inequality of
matrix ranks." It supplies no source locator, displayed formula, coefficient domain, matrix
shapes, rank convention, multiplication association, arithmetic presentation, ordered binders, or
boundary policy. Several inequivalent matrix-rank results fit that gloss, including the
triple-product Frobenius inequality, two-factor rank upper bounds, and the Sylvester rank
inequality. Selecting one from mathematical familiarity would invent missing mathematics.

The intake inspected a strong modern source lead: Taylor, arXiv `1909.13202v1`, printed page 1,
states for composable matrices over a field

`rank (A * B * C) + rank B >= rank (A * B) + rank (B * C)`

and gives a quotient-space proof. The intake explicitly records this as a candidate rather than an
admitted canonical root. It is neither catalog-cited nor the historical Frobenius source; complete
assumption, notation, genealogy, translation, correction, source-to-node, and independent-review
gates remain open. Promoting its convenient field-valued shape now would override the frozen
intake boundary instead of elaborating an exact admitted claim.

Consequently there is no honest canonical expression whose imports can be certified minimal, no
credited alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. Those mutations are undefined, not passed.
The lifecycle remains `planned`, and the root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

`IntakeProbe.lean` was re-elaborated with the pinned toolchain and the single direct import
`Mathlib.LinearAlgebra.Matrix.Rank`. It authenticates ten adjacent matrix-rank and linear-map APIs
and elaborates this discovery-only candidate shape:

```text
{m n p q : Type} -> [Fintype n] -> [Fintype p] -> [Fintype q] ->
{K : Type} -> [Field K] ->
Matrix m n K -> Matrix n p K -> Matrix p q K -> Prop
```

with conclusion `(A * B).rank + (B * C).rank <= B.rank + ((A * B) * C).rank`. This proves only
that one candidate proposition is expressible. It does not select a source root, declare a
canonical target, certify a minimal import for that absent target, or provide a proof body.
`Matrix.rank_mul_le_left`, `Matrix.rank_mul_le_right`, and
`Matrix.rank_add_rank_le_card_of_mul_eq_zero` report direct axiom dependencies `[propext,
Classical.choice, Quot.sound]`; they are adjacent infrastructure, not root proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0049` | 0 | rank 1519; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 370,375 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0049/IntakeProbe.lean` | 0 | ten adjacent APIs and one candidate shape elaborated; three adjacent declarations reported the axiom set above; no canonical target or proof body was declared |
| `python3 -B Stage1_Instances/THM-M-0049/check_intake.py` | 1 | historical intake replay stops because it expects authority state `[ ]` while current authority records provisional `[_]`; it is intake-only evidence and was not modified |

The integrated intake artifacts and relevant authority inputs are content-fingerprinted in
`statement-blocker.json`. Final scoped checks additionally validate that JSON, reject prohibited
Lean constructs by an expected no-match scan, require the root self-test manifest to remain absent,
and check the two blocker reports for whitespace errors.

## Retry Condition And Status Boundary

An accountable source reviewer must preserve and hash a lawful immutable primary or authoritative
source, select and independently approve one exact theorem passage, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, convention,
attribution decision, erratum, and boundary case. The review must settle the triple-product root,
coefficient domain, four matrix shapes, rank definition, multiplication association, inequality
orientation, natural-number arithmetic presentation, and zero, empty, identity, invertible, and
full-rank cases. A fresh statement worker can then encode exactly that claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile each credited
transport, and execute all four mutation classes. The integration lane must master-accept the
intake dependency before accepting that future statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.

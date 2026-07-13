# Exact-statement gate: blocked

Item: `S56-M-0903-STATEMENT`

Theorem: `THM-M-0903`

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a` (tree
`fdfff18dea4c6798c5b322b6088dfe556109c134`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0903-INTAKE` is provisional worker state
`[_]`, not master-accepted state `[x]`; its receipt declares `accepted: false`, is not a terminal
content-addressed receipt, and has no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered blocker investigation while concurrency is enabled, but master closure remains
dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository claim
is the title `Bose-Shrikhande-Parker定理` and the gloss `Euler猜想的否定` (the negation of Euler's
conjecture). The catalog does not define the conjecture, give a formula or bibliography, or fix an
order domain, Latin-square or orthogonality convention, ordered binders, hypotheses, conclusion,
proof boundary, corrections, errata, or formal artifact. Stage0 explicitly leaves those fields open.

The inspected 1960 paper identifies the mathematical family but exposes materially different roots:

- the literal logical negation of Euler's universal nonexistence claim, which needs one scoped
  counterexample;
- existence for every order `v = 4t + 2 > 6`, matching the conjectured congruence family;
- Theorem 10 on printed page 202, which says that at least two orthogonal Latin squares exist for
  every order `v > 6`; or
- the page-203 classification that, among positive integers `v > 2`, a pair exists exactly when
  `v != 6`, which also incorporates separate order-six nonexistence evidence.

These propositions have different quantifiers, domains, strengths, exceptional cases, and proof
boundaries. An extension of the classification to all positive or all natural orders additionally
changes the order-one, order-two, and order-zero obligations. Choosing any candidate now would
invent, narrow, broaden, or substitute proposition-changing mathematics rather than elaborate the
exact received target. It could also silently transfer scope or evidence from the separate
`THM-M-0902` Euler-conjecture target.

The representation is likewise not fixed. A labelled matrix on `Fin v` would decide that row,
column, and both symbol carriers coincide; expressing rows and columns by bijections and
orthogonality by bijectivity of the superposition map would select one convention. It would also
decide ordered-pair semantics, empty-carrier behavior, and whether the two squares must be distinct.
These are useful prospective interfaces, not source-approved target data.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. Without one approved canonical proposition, no exact Lean
expression exists for which direct imports can be certified minimal, and no canonical expression or
environment fingerprint, credited alternate transport, or removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation can be produced. The four mutation classes are
undefined, not passed. No `Statement.lean`, surrogate theorem, axiom, placeholder, broadened
interface, or proof body was added. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three direct
imports expose matrix, finite-cardinality, finite-index, bijection, and product interfaces adjacent
to a possible encoding. All nine checks pass. Complete stdout has SHA-256
`0deef5ed9e409b65e0ccfbaf71e0233f3cd94985ff1aeae9e68f8bf6a8cba51a`.

The probe's own header marks it as discovery only. It defines no Latin-square or orthogonality
predicate, selects no canonical root, supplies no source transport, and declares no proof body. Its
imports therefore cannot be certified minimal for an absent target and receive no statement or proof
credit. A bounded exact-topic search found no Latin-square, orthogonal-Latin-square, orthogonal-array,
or Bose/Shrikhande/Parker declaration in the selected repository-local and pinned-mathlib Lean roots.
This is narrow feasibility evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root
unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0903` | 0 | rank 1446; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 6607,6612 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over authority, source, intake, probe, toolchain, lockfile, and imported mathlib inputs | 0 | current fingerprints are recorded in `statement-blocker.json`; historical intake evidence was not rewritten |
| `python3 -B Stage1_Instances/THM-M-0903/check_intake.py` | 1 | historical intake replay stops because it expects intake state `[ ]`, while current authority records provisional `[_]`; this phase records rather than rewrites the frozen intake checker |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0903/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout hash above; no canonical target or proof body |
| bounded exact-topic `rg` search over repository-local and pinned-mathlib Lean | 1 (expected no match) | no target-specific declaration matched the recorded terms; discovery-only evidence |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON parsing, scoped invariant, whitespace, and absent-self-test checks are recorded in the
structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept current intake evidence. Accountable reviewers must
lawfully preserve one immutable primary or approved authoritative source and independently select
one exact truth-valued proposition or an explicitly typed multi-root package. They must crosswalk
every incorporated definition, ordered binder, hypothesis, conclusion, proof and computation
boundary, correction, erratum, congruence and inequality, exceptional and small-order case,
pair-versus-family convention, representation transport, and `THM-M-0902` ownership boundary.

A fresh statement worker may then encode exactly that reviewed claim, minimize its pinned direct
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute the four required mutation classes.

This is a truthful first-gate blocker, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance is
claimed.

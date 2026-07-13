# THM-M-0753 exact-statement gate: blocked

- Item: `S56-M-0753-STATEMENT`
- Base revision: `2226f559136f12fde46b1bf73cdf629043b8a648` (tree
  `33cb254ed06b1391379b8e7f88c5e23188957b62`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

Section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` requires an exact source-backed claim before a
Lean target may be credited. The authoritative catalog supplies only the title `跳跃反演定理`, the
attribution `众多数学家`, the period `20世纪`, and the gloss `跳跃算子的像` (the image of the jump
operator). It gives no formula, bibliography, degree carrier, reducibility convention, jump
definition, ordered binders, hypotheses, exact conclusion, proof boundary, correction history, or
independent target-identity review. Stage0 explicitly leaves the definitions and premises open, and
rev-5.6 treats the catalog's `已验证` label as untrusted metadata.

The intake records the ordinary Friedberg shape only as a candidate: for every Turing degree `a`
with `0' <= a`, there is a degree `b` with `b' = a`. The inspected Encyclopedia of Mathematics
revision 46619 states that shape, but it is a secondary source with no pinpoint primary proof
locator or accepted assumption, errata, and source-to-target crosswalk. The books by Rogers,
Shoenfield, and Sacks listed there are bibliographic leads; no exact theorem passage was obtained or
approved. The intake therefore deliberately leaves `canonical_statement`, the ordered binders,
the formal module/expression, and both expression fingerprints null.

The unresolved choices change the proposition rather than merely its notation:

- whether degrees are formed from sets, total characteristic functions, or partial functions, and
  which oracle-computation and Turing-reducibility conventions are used;
- how the Turing jump is defined on representatives and proved to descend independently of the
  representative to the degree quotient;
- whether the intended result is ordinary Friedberg inversion, a relativized or iterated theorem,
  an inversion result inside the computably enumerable degrees, or another degree structure;
- whether the material lower bound is `0' <= a`, its exact orientation and binder scope, and whether
  the conclusion is degree equality, representative equivalence, or two reducibility directions;
- the boundary at `a = 0'`, the exclusion of degrees below `0'`, and any relativized base degree;
  and
- the exact foundation, quotient, classical-choice, TCB, and computation profiles.

Choosing the conventional Friedberg formula from the secondary lead would silently select all of
those conventions. Introducing an abstract `jump` argument, axiom, structure field, or hypothesis
would assume the missing mathematics rather than elaborate it. Borrowing the adjacent jump topic
from `THM-M-0752` without its own accepted statement and checked interface would also cross a target
ownership boundary. Consequently there is no canonical expression on which to certify minimal
imports, serialize an elaborated-expression fingerprint, compile alternate transports, or run the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.
Those tests are undefined, not passed. The root remains `[H1, M4, R4]`.

The current execution DAG projects the intake dependency as provisional `[_]`; its worker receipt
declares `accepted: false` and contains no accepted receipt ID. Section 10.2 permits this
dependency-ordered attempt, but eventual statement acceptance still requires master-accepted
intake evidence. The first substantive blocker is the absent source-frozen proposition.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated using only
`Mathlib.Computability.TuringDegree`. It checks `RecursiveIn`, Turing reducibility and equivalence,
`TuringDegree`, its partial order, and reducibility reflexivity and transitivity. The pinned module
models degrees as the antisymmetrization of Turing reducibility on partial functions
`Nat ->. Nat`; it contains no Turing-jump definition, zero-jump term, or inversion theorem. The
probe declares no canonical target or proof. Its single import is therefore a narrow substrate
import, not a certified minimal import for the unidentified target.

A bounded text search over pinned `Mathlib/Computability`, repository Lean sources, and Stage1
instance Lean files found no named Turing-jump or jump-inversion declaration outside this target's
two explanatory probe lines. This is feasibility evidence only, not the downstream immutable anchor
audit or a global absence claim. The scoped Lean scan found no `sorry`, `admit`, `sorryAx`, axiom,
bodyless declaration, opaque declaration, or unsafe declaration in the owned source.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0753` | 0 | rank 1339; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, guidelines, manifest, catalog, Stage0 record, and complete intake dossier | 0 | the repository identifies a jump-inversion family but supplies no source-complete proposition; intake deliberately leaves the canonical statement, binders, imports, and fingerprints null |
| `git blame -L 5549,5554 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0753/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout 413 bytes, 7 lines, SHA-256 `e08f08c77242263c7a49f6acccdce4897aa976eb0fbb8f439627157361eed28c`; no canonical target was declared |
| bounded jump-inversion and Turing-jump declaration search over pinned mathlib and repository Lean | 0 | only this target's two explanatory probe lines matched; no named target declaration was located outside the probe; this is not an exhaustive anchor audit |
| `rg -n --glob '*.lean'` prohibited-construct scan over `Stage1_Instances/THM-M-0753` | 1 | expected no-match exit; no prohibited Lean declaration or escape hatch found |
| `python3 -B Stage1_Instances/THM-M-0753/check_intake.py` | 1 | historical intake-only checker pins the pre-integration repository base; current `HEAD` differs; this phase did not rewrite historical evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0753/statement-blocker.json` and scoped blocker assertions | 0 | structured blocker syntax, identity, null target/imports/hashes, four undefined mutations, unchanged vector, false completion flags, and absent self-test agree |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each raw no-index command returned the expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The intake validator is phase-local historical evidence: it freezes its original repository base
and exact nine-file intake inventory. Integration subsequently advanced the authority snapshot and
projected intake as `[_]`; adding these statement-phase artifacts also expands the target directory.
This attempt records the known phase-evolution failure rather than changing the intake checker,
receipt, task DAG, generated blueprint, or authoritative execution DAG to manufacture freshness.

## Retry condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash an immutable primary or approved authoritative edition, pinpoint the exact
jump-inversion theorem and all incorporated definitions, assumptions, proof boundaries,
corrections, and errata, and independently approve the source-to-statement mapping. That review must
freeze the degree carrier and reducibility, representative convention, jump construction and
quotient descent, ordinary/relative/iterated/restricted variant, ordered binders, lower-bound
premise, equality convention, foundation profiles, transports, and boundary cases.

A fresh statement run can then encode precisely that claim, establish minimal pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes. Until then this node remains `[ ]`; `audit_complete` and
`theorem_complete` are false. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.

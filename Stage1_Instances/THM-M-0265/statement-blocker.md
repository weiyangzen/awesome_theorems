# THM-M-0265 rev-5.6 statement blocker

## Verdict

`S56-M-0265-STATEMENT` is blocked at the exact source-statement and variant-selection gate. The
repository record names the Weierstrass approximation theorem, attributes it to Karl Weierstrass in
1885, and gives only the gloss `连续函数可用多项式一致逼近` (continuous functions can be
uniformly approximated by polynomials). It contains no bibliography, formula, binder-complete
proposition, definitions, proof boundary, correction history, or independently approved source
crosswalk. Its `已验证` label is untrusted metadata under rev-5.6.

The existing intake therefore correctly leaves the canonical human claim, Lean declaration or
expression, elaborated-expression hash, and target environment fingerprint null. In particular,
the catalog does not select:

- `[0,1]`, an arbitrary real closed interval, a compact real set, or another compact space;
- real or complex coefficients and codomain;
- a bundled continuous map on an interval subtype or a total function continuous on a set;
- density, membership in a closure, an epsilon inequality, or a uniformly convergent sequence;
- the uniform topology, supremum norm, or pointwise quantified error expression;
- strict or non-strict error, quantifier order, and the polynomial evaluation convention; or
- the treatment of reversed, empty, singleton, constant-function, and nonpositive-epsilon cases.

These choices change the proposition or require checked transports. Selecting the familiar real
closed-interval epsilon form from mathematical convention would invent its missing binders and
premises. Selecting Stone-Weierstrass would broaden the theorem and collide with the separately
owned `THM-M-0266`. Neither is permitted.

Consequently there is no canonical Lean expression whose imports can be certified minimal, no
normalized expression fingerprint, and no approved alternate form for a checked transport. The
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined rather than passed. Sections 5 and 5.1 of the rev-5.6 blueprint make these absences hard
statement blockers before proof evidence can be inspected.

The prerequisite intake is also only provisional worker state `[_]`, not master-accepted state
`[x]`. Its receipt says `accepted: false` and supplies no accepted receipt ID. Master acceptance
remains a separate prerequisite for any eventual accepted statement transition. The absent exact
source proposition is the first substantive statement blocker in this attempt.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports only
`Mathlib.Topology.ContinuousMap.Weierstrass`. Under the pinned environment it elaborates these five
direct theorem interfaces:

- `polynomialFunctions_closure_eq_top'` on the unit interval;
- `polynomialFunctions_closure_eq_top` on every real closed interval;
- `continuousMap_mem_polynomialFunctions_closure` for bundled continuous maps;
- `exists_polynomial_near_continuousMap` in the supremum norm; and
- `exists_polynomial_near_of_continuousOn` in unbundled pointwise epsilon form.

It also checks the Bernstein approximation substrate. The three diagnostic axiom reports are
`[propext, Classical.choice, Quot.sound]`. The deterministic probe output is 1,309 bytes with
SHA-256 `fd940c948628daa7b3c22b08f373a65aa8a84ee90bfa9c8f66c889a3d7c8f250`.

This authenticates exact-topic pinned interfaces only. The module comments label the declarations
as Weierstrass forms, but neither those comments nor theorem names supply the missing source-to-root
identity. The probe declares no canonical target, checked transport, mutation fixture, or proof
body, and its single import cannot be called minimal for an absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0265` | 0 | rank 1273, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | before this phase only the automation `.lake` symlink was untracked; base revision `0e5ae82e6d507ee607c3f011900571ffd8096800`, tree `400e6edf1f69b971b60a367e3ea29be359b07907` |
| repository authority, source crosswalk, scope map, task DAG, receipt, and intake inspection | 0 | confirmed provisional intake, null target, exact-source ambiguity, five candidate-only interfaces, and six open downstream tasks |
| `git blame -L 1908,1913 -- Docs/researches/math_theorems.md`; catalog-block hash | 0 | all six uncited fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; block SHA-256 `318a8fd3b7b200aac7f9f4e1d4a3e3238086ceaec15b8cf9ee42a683425f29bc` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0265/IntakeProbe.lean)` | 0 | six exact-topic APIs elaborated; representative axioms and output hash recorded above; no target theorem stated |
| bounded `rg` search for Weierstrass approximation declarations over repo-local Lean, the owned path, and the pinned defining module | 0 | located the five pinned candidates and target-local probe; no source-approved canonical mapping was found; discovery only |
| `python3 -B Stage1_Instances/THM-M-0265/check_intake.py` | 1 | expected phase-evolution failure: the historical intake checker freezes the original nine-file owned inventory and rejects the two new statement artifacts; it was not modified or represented as statement evidence |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0265/statement-blocker.json` and scoped invariant check | 0 | finalized structured blocker parsed and its null-target, unchanged-vector, false-completion, and no-self-test invariants agreed |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest absent because the exact-statement deliverable did not pass |

## Retry condition and status boundary

The integration lane must master-accept refreshed intake evidence before accepting a future
statement transition. Accountable reviewers must preserve and hash one lawful immutable primary or
authoritative source, select and independently approve its exact proposition and proof boundary,
and transcribe every incorporated definition, ordered binder, premise, conclusion, correction,
erratum, and boundary case. They must explicitly settle the interval or domain, scalar fields,
function carrier, continuity encoding, uniform topology or norm, polynomial carrier and evaluation,
quantifier order, conclusion form, and all degenerate cases.

A fresh statement attempt can then encode precisely that approved claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. The provisional root remains `[H1, M3, R4]`; `audit_complete` and
`theorem_complete` remain false; no debt-vector change, statement receipt, worker `[_]`, or master
acceptance is claimed. Because the exact-statement deliverable did not pass,
`.stage1-worker-selftest.json` is deliberately absent.

The historical intake checker is bound to the intake-time closed artifact inventory. Adding these
statement-phase blocker files therefore makes its inventory assertion fail closed. This worker did
not rewrite intake history, and that expected phase-evolution failure does not validate or
invalidate the separate statement decision.

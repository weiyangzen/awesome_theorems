# THM-M-0960 exact-statement gate: blocked

Item: `S56-M-0960-STATEMENT`

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a` (tree
`cc5285432a02107fadffb68c698690d1b98ac5f2`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0960-INTAKE` has only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted, is not content-addressed, lists no accepted receipt
IDs, and binds older blueprint and execution-DAG hashes. There is no master-accepted dependency
receipt.

Independently and decisively, the exact-statement gate fails. The complete catalog claim is the
name Ellenberg-Gijswijt theorem and the gloss `cap集的上界`, or "an upper bound for cap sets." It
contains no formula, definition, ordered binder, hypothesis, conclusion, source locator, proof
boundary, correction, or erratum. Stage0 explicitly leaves the exact definitions and premises open,
and intake therefore freezes a null canonical claim and null formal target.

The inspected publisher article has two materially different nearby statement surfaces. Theorem 4
gives an exact bounded-monomial-count inequality over a general finite field for a three-variable
equation with coefficients summing to zero. Corollary 5 gives the cap-set specialization
`|A| = o(2.756^n)` in `(Z/3Z)^n`. The surrounding prose also gives qualitative exponential bounds.
The catalog selects none of these. The publisher paper and arXiv v1 also differ materially in the
coefficient hypothesis and presentation.

Choosing a conventional formulation would therefore invent, narrow, broaden, or substitute
proposition-changing mathematics. There is no canonical Lean expression whose imports can be
minimized, no expression or environment fingerprint, no approved alternate encoding, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. All
four mutation classes are undefined, not passed. No `Statement.lean`, theorem declaration, proof
body, weakened special case, or broadened interface was added. The root remains `[H1, M4, R4]`.

## Source And Lean Boundary

The source lead is Jordan S. Ellenberg and Dion Gijswijt, *On large subsets of F_q^n with no
three-term arithmetic progression*, *Annals of Mathematics* 185 (2017), 339-343, DOI
`10.4007/annals.2017.185.1.8`. Intake observed publisher PDF SHA-256
`9c54de6e297f0ac678c640def09b3ac8ab960aca05f4059d44e95c9e38b43c8c` and arXiv v1 PDF SHA-256
`3cd77ddab97f046121ef684d68cea9d175b438363ee60b2abe1faa0db05f116b`. These are source leads, not an
independently accepted choice of exact root.

The exact statement still must fix the field and ambient encoding, `Set` versus `Finset`, the
dimension domain including `n = 0`, cap-set and nontrivial-progression conventions, and all empty,
singleton, repeated-entry, and small-dimension cases. A Theorem 4 root must additionally fix the
coefficient binders, diagonal-solution predicate, bounded monomial count, and nonintegral real
cutoff. A Corollary 5 root must fix the sequence quantified by little-o, real powers and coercions,
the exact decimal constant, and finite-prefix semantics.

The existing `IntakeProbe.lean` imports the pinned modules for `ThreeAPFree`, `ZMod`, finite
function-space cardinality, and `Finset.card_univ`. It defines only prospective `CapAmbient` and
`IsCapSet` interfaces and states no upper bound. Those imports cannot be certified minimal for an
absent target. A bounded search over repo-local Lean, pinned mathlib, and this owned path located no
source-identical Ellenberg-Gijswijt, cap-set, slice-rank, monomial-count, or `2.756^n` declaration.
This is narrow feasibility evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0960` | 0 | rank 1494; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority and null-target assertions over the manifest, execution DAG, and `instance.json` | 0 | rank, dependency, intake `[_]`, statement `[ ]`, null canonical claim and target, and H1/M4/R4 agree |
| `git blame -L 7008,7013 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0960/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0960/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `e0ba2feafbb2a9f2c868fd73c303d912917ad798a09fea1a8ce4921d6f8a9af6`; no target upper bound or proof body declared |
| bounded exact-topic Lean search | 0 | only six explanatory lines in the owned intake probe matched; output SHA-256 `fc2736977dc83bc40ff6ca75c37ea865e94223b7774fbb1b85a4350c209d9a53`; no source-identical declaration located |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured blocker
beside this report.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and admit an immutable source edition, independently select Theorem 4, Corollary 5, or one
other exact source-derived root, and approve every incorporated definition, ordered binder,
hypothesis, conclusion, correction, erratum, asymptotic convention, and boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.

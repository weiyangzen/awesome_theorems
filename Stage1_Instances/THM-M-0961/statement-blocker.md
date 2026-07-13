# THM-M-0961 exact-statement gate: blocked

Item: `S56-M-0961-STATEMENT`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0961-INTAKE` has only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed, and there is no
master-accepted dependency receipt.

Independently and decisively, the exact-statement gate fails. The complete catalog claim is only the
name Meshulam's theorem and the gloss `cap集的上界`, or "an upper bound for cap sets." It contains no
formula, definition, ordered binder, hypothesis, conclusion, source locator, proof boundary,
correction, or erratum. Stage0 explicitly leaves the exact definitions and premises open, and the
intake therefore freezes a null canonical claim and null formal target.

Two retrospective papers report Meshulam's Theorem 1.2 as
`D3(G) <= 2 * |G| / c(G)` for a finite odd-order abelian group `G`, with `c(G)` the number of
nontrivial invariant factors. That is a strong source lead, but it is not an admitted transcription
of the 1995 theorem. The source-owned definition of a progression, the exact invariant-factor
conditions, and the proof boundary have not been checked directly or independently approved. The
catalog also does not select the general finite-abelian theorem rather than its prospective
`(Z/3Z)^N` cap-set specialization `2 * 3^N / N`.

Choosing either familiar formulation would therefore invent, narrow, broaden, or substitute
proposition-changing mathematics. There is no canonical Lean expression whose imports can be
minimized, no expression or target-environment fingerprint, no approved alternate encoding, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. All
four mutation classes are undefined, not passed. No `Statement.lean`, theorem declaration, proof
body, weakened special case, or broadened interface was added. The root remains `[H1, M4, R4]`.

## Source And Lean Boundary

The primary lead is Roy Meshulam, *On subsets of finite abelian groups with no 3-term arithmetic
progressions*, *Journal of Combinatorial Theory, Series A* 71(1) (1995), 168-172, DOI
`10.1016/0097-3165(95)90024-1`. Bibliographic metadata and the DOI record identify it, but no lawful
full-text copy was admitted during intake or this statement attempt. OpenAlex and Unpaywall report
no open-access or repository copy, the unauthenticated Elsevier API returns only minimized metadata,
and direct publisher PDF access is unavailable in this environment. Those bounded checks do not
prove that no accessible edition exists.

The exact statement still must fix the ambient group and its finiteness/commutativity/odd-order
context; `D3` and the nontrivial three-term-progression convention; a presentation-independent
meaning of `c(G)` or source-faithful decomposition data; `Set` versus `Finset`; cardinality and
real/rational/natural coercions; ordered binders and universes; division or cross-multiplied
inequality; and all trivial-group, zero-rank, repeated-entry, even-order, and small-dimension cases.
A cap-set specialization additionally needs a checked transport to the selected general statement.

The existing `IntakeProbe.lean` imports pinned Roth and finite-abelian modules and checks
`ThreeAPFree`, `addRothNumber`, `AddCommGroup.equiv_directSum_zmod_of_finite'`, and qualitative Roth
interfaces. It states no Meshulam bound. The direct-sum API does not expose ordered invariant
factors or a presentation-independent `c(G)`, and `roth_3ap_theorem` gives a qualitative density
threshold rather than `2 * |G| / c(G)`. These imports therefore cannot be certified minimal for an
absent target. A bounded search over repo-local Lean, pinned mathlib, and this owned path located no
source-identical Meshulam declaration. This is feasibility evidence, not the downstream anchor audit
or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-0961` | 0 | rank 1495; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority and null-target assertions over the manifest, execution DAG, and `instance.json` | 0 | rank, dependency, intake `[_]`, statement `[ ]`, null canonical claim and target, and H1/M4/R4 agree |
| `git blame -L 7015,7020 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0961/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0961/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `2ae264556b2e3d1be1a9e02be07a1a9e74991d1a8eb2d456778695b8ed50d720`; empty stderr; no target bound or proof body declared |
| bounded exact-topic Lean search | 0 | only adjacent Roth/3AP infrastructure and unrelated textual matches were found; output SHA-256 `27be68a05ad58b7374c27f693f840f95efe988f3253af1c8ae569d9036b7ab62`; no source-identical declaration located |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured blocker
beside this report.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and admit an immutable 1995 source edition; transcribe and pinpoint the exact theorem
and every incorporated definition; map its group hypotheses, progression convention, invariant
factor conditions, constants, quantifiers, conclusion, proof boundary, corrections, errata, and
cap-set specialization; and independently approve that source-to-catalog choice.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.

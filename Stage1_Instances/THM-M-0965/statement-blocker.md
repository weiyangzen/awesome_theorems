# Exact-statement gate: blocked

Item: `S56-M-0965-STATEMENT`

Theorem: `THM-M-0965`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0965-INTAKE` is provisional worker state
`[_]`, not master-accepted `[x]`. The intake receipt is non-content-addressed, declares
`accepted: false`, and contains no accepted receipt ID. This permits a dependency-ordered
investigation under rev-5.6 section 10.2, but not an accepted statement transition.

Independently, the exact-statement gate cannot pass. The repository gives only the theorem name
and the gloss `t-相交族的完整刻画` (complete characterization of `t`-intersecting families). The
intake correctly leaves the canonical mathematical statement, Lean expression, imports, and
fingerprints null. The directly inspected primary paper distinguishes materially different roots:

- the sharp cardinality bound by the largest canonical family;
- equality for the extremal function `M(n,k,t)`;
- full optimizer classification up to ground-set permutations, including adjacent optimizers at a
  transition equality; and
- the source's piecewise formulation with exact rational transition intervals and the low-`n`
  whole-layer branch.

The catalog does not select among these propositions. Its word "characterization" cannot authorize
silently dropping the equality classification or, conversely, strengthening a bound-only theorem.
The 1997 paper's extracted text also corrupts important comparison, subset, intersection, fraction,
and infinity glyphs on printed pages 125-127. This run independently rendered and visually checked
the main formulas against page 126, but a single worker inspection is not the required accountable
source review. Selection of the catalog root, a recorded second review, and correction and errata
review remain open.

Encoding decisions that change the proposition are unresolved as well: constraints and binder
order for `n`, `k`, and `t`; `Fin n` versus an abstract finite ground type; `Set` versus `Finset`
families; all-pair versus distinct-pair intersection semantics; the feasible candidate-index range;
initial-segment versus transported candidate families; maximum and empty-range conventions;
permutation isomorphism; exact transition arithmetic and tie clauses; the `n <= 2*k-t` branch; and
the cases `t=0`, `k=0`, `n=0`, `t>k`, `k>n`, and empty or singleton families.

Rev-5.6 sections 5 and 5.1 make this ambiguity and the missing expression fingerprint hard
blockers. With no canonical proposition, minimal imports cannot be certified, alternate transports
cannot be compiled, and the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined rather than passed. The intake vector therefore remains
`H1 / M4 / R4`.

## Source And Lean Boundary

The source lead is Rudolf Ahlswede and Levon H. Khachatrian, "The Complete Intersection Theorem for
Systems of Finite Sets," *European Journal of Combinatorics* 18(2), 1997, 125-136, DOI
`10.1006/eujc.1995.0092`. The inspected 12-page author PDF has SHA-256
`2a0d46d73ae6a445ebb2c838785855c2af82d1901a7ecbc7394d1427e472a365`. Its definitions
(1.1)-(1.3), canonical family (1.9), general maximum formula (1.10), main classification theorem,
and low-parameter remark identify the theorem family but do not resolve the catalog's intended root.
The visually checked classification interval is
`(k-t+1)*(2+(t-1)/(r+1)) < n < (k-t+1)*(2+(t-1)/r)` with rational comparisons, and its lower
transition equality permits the adjacent types `r` and `r+1`; the paper uses an infinity convention
for the upper expression at `r=0`. These facts narrow transcription debt but do not choose whether
the catalog root includes the classification.
Katona's secondary Theorem 4 in arXiv `1602.02634v1` states the bound-only variant and confirms that
this is a real scope choice, not an alternate spelling already known to be equivalent to the full
classification package.

Pinned mathlib exposes `Set.IsIntersectingOf`, `Set.Intersecting`, `Set.Sized`, powerset-cardinality
infrastructure, `Nat.choose`, and the ordinary `t=1` theorem `Finset.erdos_ko_rado`. The existing
`IntakeProbe.lean` re-elaborates these interfaces, but declares only prospective vocabulary and no
Ahlswede-Khachatrian target or proof body. Its imports cannot be called minimal for an absent
canonical expression. A bounded exact-topic search found no matching declaration in pinned mathlib
or repo-local Lean; that is discovery evidence only, not the downstream formal-anchor audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0965` | 0 | rank 1499; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped inspection and hashing of the catalog, Stage0, manifest, rev-5.6 authorities, intake artifacts, primary and secondary sources, toolchain lock, and relevant pinned mathlib files | 0 | the authorities and intake agree that exact root selection and the canonical Lean target are open; exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 | pinned mathlib revision and tree recorded above; package status was empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0965/IntakeProbe.lean` | 0 | eight adjacent API and prospective-predicate signatures elaborated; stdout SHA-256 `e1551dfad729ec12170e1583bf8519b49ddc5a2758c98abee8854660fa9536b9`; stderr empty; no target theorem or proof body |
| bounded exact-topic search in pinned mathlib, repo-local Lean, and the owned path | 1 | expected no-match result; no Ahlswede-Khachatrian declaration located |
| `python3 -B Stage1_Instances/THM-M-0965/check_intake.py` | 1 | historical intake checker stops at line 131 because it freezes intake state `[ ]` while current authority records `[_]`; it was not rewritten as statement evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parsing plus scoped blocker invariants | 0 | identity, dependency boundary, null target and imports, unchanged `H1/M4/R4`, four undefined mutations, false completion flags, and no-self-test boundary agree |
| scoped whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0965` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker also freezes the original nine-file intake inventory and earlier authority
hashes. Its failure is a historical-evidence freshness boundary, not evidence against this blocker.
This statement phase does not rewrite the intake checker, receipt, instance, task DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

Before a statement can be accepted, the integration lane must master-accept a current intake and an
accountable source reviewer must preserve an immutable source edition, select and independently
approve exactly one root strength, verify every incorporated definition, premise, transition,
equality, isomorphism, and low-parameter clause against the page images, and complete correction and
errata review. All parameter, representation, pair, candidate-index, maximum, arithmetic,
transport, and degenerate-case conventions must then be frozen.

A fresh statement worker can encode only that approved claim, minimize the pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
run all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.

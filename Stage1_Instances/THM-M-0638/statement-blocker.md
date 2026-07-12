# Exact-statement gate: blocked

Item: `S56-M-0638-STATEMENT`

Theorem: `THM-M-0638`

Base revision: `ec27eb0336c89f0aed87200fc7cbf03a09996597` (tree
`3fe77e381bf94ce1ed347bed17c94af25de8d543`).

## Decision

The exact Lean 4 target cannot yet be truthfully adopted from the accepted inputs. The statement
item remains `[ ]`. Its prerequisite intake has provisional worker state `[_]`, not
master-accepted state `[x]`; its receipt declares `accepted: false`, is not content-addressed, and
contains no accepted receipt ID. It deliberately leaves the canonical statement, ordered binders,
Lean expression, minimal imports, expression hash, and environment fingerprint null. Rev-5.6
permits this dependency-ordered inspection, but it does not permit an accepted statement transition
before the dependency and this node pass master acceptance.

The repository record supplies only the title Tychonoff fixed-point theorem, Andrey Tychonoff,
1935, and the gloss "a fixed point on a locally convex space." The intake located the theorem on
printed page 770 of A. Tychonoff, "Ein Fixpunktsatz," *Mathematische Annalen* **111** (1935),
767-776, DOI `10.1007/BF01472256`:

> Bei jeder stetigen Abbildung einer konvexen, bikompakten Menge eines linearen topologischen
> lokal-konvexen Raumes in sich gibt es wenigstens einen Fixpunkt.

This identifies the compact-convex locally-convex fixed-point family, but the intake expressly
withholds exact adoption until a lawful immutable source copy, incorporated definitions,
separation and scalar conventions, nonemptiness translation, proof boundary, translation, errata,
and row-by-row independent review are accepted.

There is also an unresolved ownership collision. `THM-M-0317` has the same Chinese title,
attribution, year, and essentially the same gloss in another category. Its foreign-owned
`Statement.lean` selects a real Hausdorff locally convex space, an ambient map `f : E -> E`, global
`Continuous f`, `Set.MapsTo f K K`, and an in-domain fixed point. It elaborates, but no accepted
alias, deduplication, distinct-root, checked target transport, or canonical-root ownership decision
permits copying its statement identity or evidence into `THM-M-0638`.

The foreign candidate also exposes a material scope choice rather than resolving it. The source
speaks of a continuous self-map of the compact convex set. A subtype map `K -> K` or an ambient map
continuous only on `K` represents that reading directly; requiring an ambient extension that is
continuous on all of `E` is generally stronger. The `THM-M-0638` intake explicitly leaves global
ambient continuity versus continuity on the domain, and ambient-map versus subtype-map encoding,
open. Choosing the convenient foreign restriction would substitute an unapproved proposition.

Consequently there is no canonical expression whose direct imports can be certified minimal. No
expression or environment-expression fingerprint, credited alternate transport, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutation suite exists.
Those outputs are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with its two discovery imports and checks the seven
adjacent locally-convex, compactness, convexity, continuity, invariance, and fixed-point APIs. It
states no target and has no proof body, so its import list is not a minimal-import certificate for
an exact theorem.

For discrimination only, the foreign `THM-M-0317/Statement.lean` re-elaborates and prints its
candidate target, subtype conclusion transport, and four mutation witnesses. A temporary renamed
copy also elaborates after removing `Mathlib.Dynamics.FixedPoints.Basic`; the single direct import
`Mathlib.Topology.Algebra.Module.LocallyConvex` already exposes `Function.IsFixedPt` transitively.
Thus even the foreign file's two-import surface is not a literal minimal-import certificate. The
temporary probe was kept outside the repository and receives no target, statement, or proof credit.

A bounded exact-topic search of pinned mathlib and repo-local Lean found no exact Tychonoff
fixed-point declaration beyond the foreign `THM-M-0317` artifacts. This is discovery-only
feasibility evidence, not the downstream immutable anchor audit or a claim of exhaustive absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone or fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0638` | 0 | rank 1055; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository source, Stage0, intake, source-crosswalk, and duplicate-scope inspection | 0 | the source family was located, but the canonical target remains null and the `THM-M-0317` identity/ownership relationship remains unresolved |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0638/IntakeProbe.lean` | 0 | seven adjacent pinned APIs elaborated and printed; no target theorem or proof body was declared |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0317/Statement.lean` | 0 | the foreign target, transport, and mutation witnesses elaborated; target identity and ownership remain unresolved, so they receive no `THM-M-0638` credit |
| one-import temporary probe derived from the foreign statement, then `lake env lean /tmp/THM-M-0638-one-import-probe.lean` | 0 | the foreign candidate elaborated with only `Mathlib.Topology.Algebra.Module.LocallyConvex`; temporary file remained outside the repository |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | 0 | matches were the intake comment and foreign `THM-M-0317` statement/obligation artifacts; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0638/check_intake.py` | 1 | historical intake checker freezes the intake state as `[ ]`, while the integrated authoritative DAG now records `[_]`; this statement phase records rather than rewrites that evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0638/statement-blocker.json` plus scoped blocker invariants | 0 | structured blocker parsed; identity, dependency, null target/imports, unchanged vector, false completion flags, undefined mutation classes, changed paths, and no-self-test gate agree |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| scoped newline/trailing-whitespace checks plus `git diff --check -- Stage1_Instances/THM-M-0638` | 0 | no whitespace diagnostics in either new blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must master-accept the intake and issue an accepted identity and
canonical-root ownership decision for `THM-M-0638` versus `THM-M-0317`. Accountable reviewers must
preserve and hash a lawful complete source edition, crosswalk every incorporated definition,
ordered binder, assumption, conclusion, proof boundary, translation, correction, erratum, and
boundary case, and decide scalar field, separation, nonemptiness, continuity scope, and map
encoding.

A fresh statement run can then encode precisely that approved claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, proof credit, or
master acceptance is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.

# Exact-statement gate: blocked

Item: `S56-M-0215-STATEMENT`

Theorem: `THM-M-0215`

Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
`a5488edccb2687c4ff0bbdccf4650e06b2e45337`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The statement
item remains `[ ]`. Its prerequisite intake is provisional worker state `[_]`, not master-accepted
state `[x]`; the intake receipt declares `accepted: false`, is not content-addressed, and has no
accepted receipt ID. It deliberately leaves the canonical mathematical statement, Lean expression,
expression hash, and environment-expression fingerprint null.

The complete catalog wording is only the title "hyperbolic law of cosines" and the gloss "a
relation between the sides and angles of a hyperbolic triangle." It supplies no citation, formula,
definition chain, ordered binders, hypotheses, conclusion, proof boundary, correction history, or
boundary policy. Its `verified` label is untrusted inventory metadata under rev-5.6.

The wording does not choose among materially different claims, including:

- the side law or the dual angle law;
- one distinguished equation, all three cyclic equations, or a labeling-independent package;
- a hyperboloid, Poincare disk, upper-half-plane, synthetic, or abstract constant-curvature model;
- curvature `-1` or a scaled curvature `-k^2` formulation;
- the definitions of triangle, side distance, interior angle, orientation, and opposite labels; or
- non-degenerate finite triangles, degenerate or collinear triangles, or ideal and ultraideal
  boundary variants.

These choices change domains, hypotheses, and conclusions. Selecting a familiar formula over three
unconstrained real numbers would erase the geometric theorem; choosing a model and conventions
without an accepted source decision would add unapproved mathematics. Either move would broaden,
narrow, or substitute the received target rather than elaborate it exactly.

The intake inspected Immanuel Asmus, *Duality between Hyperbolic and de Sitter Geometry*,
arXiv:0810.5303v2, Theorem 5.1, as a strong modern lead. It gives three cyclic side-law equations for
non-degenerate hyperbolic and antipodal-hyperbolic triangles in a normalized hyperboloid model,
including

```text
cosh(a) = cosh(b) cosh(c) - cos(alpha) sinh(b) sinh(c).
```

That paper is not cited by the catalog. Catalog-to-source identity, primary historical provenance,
corrections and errata, exceptional-case policy, lawful preservation, and independent review remain
open. The lead therefore remains provisional `H1`; it does not authorize silently adopting its
particular proposition as the canonical root.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. With no canonical proposition, there is no honest import set to minimize, no target
or environment-expression fingerprint, no credited alternate transport, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. Those outputs
are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with these pinned imports:

```lean
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Analysis.Complex.UpperHalfPlane.Metric
import Mathlib.Geometry.Euclidean.Triangle
```

Its eight adjacent API checks pass. Pinned mathlib supplies real `sinh` and `cosh` identities, the
genuine Poincare distance on `UpperHalfPlane`, and a distinct Euclidean cosine law. These are useful
substrate and explicit non-substitutes. They do not define a hyperbolic triangle or its interior
angle, relate three vertices, select a source model, or state the hyperbolic triangle cosine law.
Consequently the probe's imports cannot be certified minimal for an absent canonical target and
receive no statement or proof credit.

A bounded exact-topic search of pinned mathlib and repo-local Lean found no hyperbolic-triangle
cosine-law declaration. This is discovery-only evidence, not the downstream immutable anchor audit
and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0215` | 0 | rank 1230; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository source, Stage0, blueprint, skill, intake dossier, and Asmus-lead inspection | 0 | confirmed the sparse catalog gloss, null canonical target, provisional source lead, and unresolved proposition choices |
| `sha256sum` over authority, intake, toolchain, and pinned source inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0215/IntakeProbe.lean` | 0 | eight adjacent pinned APIs elaborated; no canonical target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 | the only target-local match before this blocker was the discovery probe; no pinned hyperbolic-triangle cosine-law declaration matched |
| `python3 -B Stage1_Instances/THM-M-0215/check_intake.py` | 1 | the historical intake-only checker requires the absent intake worker packet; this statement run records rather than rewrites historical intake evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0215/statement-blocker.json` and scoped blocker invariant assertions | 0 | valid JSON; identity, provisional dependency, null target/imports, unchanged vector, four undefined mutations, false completion flags, pinned input hashes, and no-self-test boundary agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result: no prohibited declaration or proof escape in `IntakeProbe.lean` |
| scoped no-index whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0215` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept the prerequisite before accepting a later statement
transition. Accountable source reviewers must preserve and hash an immutable primary or
authoritative source, select and independently approve the exact side-or-angle root, cyclic
packaging, model and curvature normalization, incorporated definitions, ordered binders,
hypotheses, conclusion, proof boundary, corrections, and exceptional cases, and reconcile the
neighboring hyperbolic-model targets.

A fresh statement run can then encode precisely that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, node receipt, worker `[_]`, or master acceptance
is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.

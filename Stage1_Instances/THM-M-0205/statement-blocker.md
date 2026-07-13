# Exact-statement gate: blocked

Item: `S56-M-0205-STATEMENT`

Theorem: `THM-M-0205`

Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e` (tree
`b4b092069141ac54ea1ab5a6ea946192a30ec78c`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0205-INTAKE` is only provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt is explicitly unaccepted and
non-content-addressed. Rev-5.6 permits dependency-ordered preparation, but the statement transition
cannot be accepted before its prerequisite.

The exact-statement gate also fails independently. The repository supplies only the title
`莫利定理` (Morley's theorem), Frank Morley, the year 1899, and the gloss
`三角形角三等分线交点构成等边三角形` (the intersections of a triangle's angle trisectors form an
equilateral triangle). It supplies no bibliography, definitions, diagram, ordered binders,
hypotheses, intersection convention, conclusion encoding, proof boundary, correction history, or
reviewer. The `已验证` label is untrusted metadata.

Taylor and Marr's *The six trisectors of each of the angles of a triangle* is a strong source lead.
Section 2, printed page 119, says that the meets of trisector pairs adjacent to the same side of
`ABC` form an equilateral triangle. Intake correctly classifies it as `H1`, not an approved source:
the catalog does not cite it, its diagram-dependent definitions and publication chronology have not
been reconciled, and no independent source/edition/errata review or accepted catalog-to-source
mapping exists.

An accepted source decision must additionally freeze:

- the two-dimensional plane model, universes, typeclasses, ordered vertices, orientation, and
  nondegenerate-triangle predicate;
- internal rays versus supporting lines, which trisector at each vertex is adjacent to each side,
  and how ray direction and adjacency are enforced;
- the incidence construction, existence and uniqueness policy, and cyclic names of the three
  intersection points;
- distance, simplex, congruence, or angle encoding of the equilateral conclusion, including its
  nondegeneracy; and
- repeated or collinear vertices, zero or straight angles, opposite rays, parallel or coincident
  lines, coincident intersections, orientation reversal, and other boundary cases.

These choices change the proposition. Selecting them in this worker run would invent missing
mathematics rather than elaborate an exact received target. Rev-5.6 sections 5 and 5.1 make that
ambiguity and the missing expression fingerprint hard blockers. There is consequently no honest
target whose imports can be certified minimal. No `Statement.lean`, canonical expression, checked
transport, or mutation suite was created. Removed-hypothesis, changed-domain, changed-binder-scope,
and boundary-case mutations are undefined, not passed. The provisional vector remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` directly imports:

```lean
import Mathlib.Geometry.Euclidean.Congruence
import Mathlib.Geometry.Euclidean.Triangle
import Mathlib.Analysis.Normed.Affine.Simplex
```

It re-elaborates thirteen adjacent pinned interfaces for angles, distance, collinearity,
betweenness, congruence, simplex interior, and equilateral triangles. This authenticates useful
substrate but neither defines side-adjacent internal trisector rays nor selects intersections or a
canonical conclusion. Its imports are not certified minimal for an absent canonical target and the
probe receives no statement or proof credit.

A bounded repository and pinned-mathlib search found only an unrelated model-theory search string,
the distinct Morley categoricity dossier, and this intake probe. No geometry Morley or
angle-trisection declaration was identified. This is bounded discovery evidence, not the downstream
anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build, clone, fetch, or other
dependency mutation was run, and the pinned mathlib worktree remained clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0205` | 0 | rank 1537; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| catalog, Stage0, blueprint, skill, manifest, DAG, and intake-dossier inspection | 0 | confirmed the sparse gloss, unaccepted Taylor-Marr lead, unresolved construction choices, and null canonical target |
| `sha256sum` over authority, source, intake, toolchain, lock, and relevant mathlib inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0205/IntakeProbe.lean` | 0 | thirteen adjacent APIs elaborated; stdout 3,823 bytes, SHA-256 `eb97c71a17fa4197b066faf959eb06b887f16f0c749f81d8c329cab756c264ea`; no canonical target or proof body |
| bounded exact-topic `rg` search over repository Lean and pinned mathlib | 0 | no geometry Morley/trisector root identified; only unrelated model-theory hits and the owned probe |
| `python3 -B Stage1_Instances/THM-M-0205/check_intake.py` | 1 | historical intake checker expects its pre-integration authoritative intake state; current shared DAG has provisional `[_]`, so this worker recorded rather than rewrote stale intake evidence |

Final scoped checks parse and validate the blocker JSON, scan owned Lean for prohibited
declarations, check whitespace, confirm the exact two-file change scope, and confirm that
`.stage1-worker-selftest.json` is absent.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash one lawful immutable primary or approved authoritative source, independently
approve its exact proposition, and reconcile edition, diagram definitions, publication history,
corrections, errata, and the catalog mapping. The crosswalk must freeze every plane, point, ray,
adjacency, intersection, equilateral, binder, hypothesis, conclusion, proof-boundary, orientation,
and degenerate-case choice.

A fresh statement attempt may then encode precisely that claim, minimize pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and run all
four required mutation classes.

This blocker is the assigned phase's truthful result, not completion. Lifecycle remains `planned`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.

# Exact-statement gate: blocked

Item: `S56-M-0209-STATEMENT`

Theorem: `THM-M-0209`

Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e` (tree
`b4b092069141ac54ea1ab5a6ea946192a30ec78c`).

## Decision

The assigned statement item remains `[ ]`. No canonical Lean target can yet be selected without
making proposition-changing choices that the repository record and provisional intake deliberately
leave open. Consequently, no `Statement.lean`, minimal-import claim, expression fingerprint,
checked transport, mutation certificate, statement receipt, or root worker self-test was created.

The repository supplies only the Descartes circle-theorem name, its 1643 attribution, and the gloss
"the curvature relation of four tangent circles." It gives no formula, bibliography, incorporated
definitions, ordered binders, hypotheses, conclusion, proof boundary, correction history, or
reviewer. Its verified-status label is untrusted metadata under rev-5.6.

The immutable source lead does identify the theorem family, but it exposes a source-significant
scope split. Lagarias, Mallows, and Wilks, *Beyond the Descartes Circle Theorem*, arXiv
`math/0101066v1`, SHA-256
`b5a2da8a0c2aa594084afd2180ac427be3ea9dc862ac922c7ae43f9774372858`, states in the abstract the
positive-radius case of four mutually tangent plane circles with disjoint interiors. Section 1
defines a Descartes configuration as four mutually tangent circles with no three having a common
tangent, permits straight lines as degenerate circles with bend zero, and states Theorem 1.1:

```text
(sum j = 1..4, b_j)^2 = 2 * (sum j = 1..4, b_j^2).
```

The following page explains that all displayed configurations require compatible orientations and
signed curvatures: an enclosing circle has negative oriented radius, straight lines have bend zero,
and compatibility is defined through disjoint oriented interiors, either directly or after
reversing all four orientations. The intake therefore correctly refuses to silently choose the
narrow ordinary-circle case or the full oriented circle-and-line case.

An exact source-to-Lean freeze must still decide the generalized circle/line carrier, pairwise
tangency and common-tangent exclusion, oriented interior, global orientation reversal, signed bend,
the treatment of enclosing circles and one or two straight lines, the planar domain, ordered
binders, and all degenerate cases. Proving only the external-tangency positive-radius case would
substitute a specialization. Treating bends or the desired identity as primitive configuration
fields would hide the theorem in a premise. Neither is permitted.

The prerequisite `S56-M-0209-INTAKE` is also only provisional `[_]` worker state. Its receipt is
not accepted or content-addressed and records no accepted receipt ID. Dependency-ordered inspection
can proceed, but an accepted statement transition remains impossible before master acceptance.

## Pinned Lean boundary

The discovery-only `IntakeProbe.lean` directly imports:

```lean
import Mathlib.Geometry.Euclidean.Sphere.Tangent
```

It re-elaborates ordinary Euclidean spheres, internal and external sphere tangency predicates, and
their center-distance characterizations. The two printed theorem bodies depend only on `propext`,
`Classical.choice`, and `Quot.sound`. This is real environment evidence, but mathlib's sphere has a
finite real radius and the checked surface provides no oriented circle, signed bend, straight-line
circle, Descartes configuration, or terminal curvature identity. The probe import is therefore not
a minimal-import claim for an absent canonical target and receives no statement or proof credit.

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No Lake update or build, dependency clone or fetch, or other dependency mutation was
run.

## Validation record

Commands ran on 2026-07-13 (`Asia/Shanghai`). Exact structured results and input hashes are in
`statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0209` | 0 | rank 1540; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| transient fetch and inspection of arXiv `math/0101066v1` | 0 | 25-page, 561,140-byte PDF; Theorem 1.1 plus the orientation and history context inspected; SHA-256 `b5a2da8a...d7`; transient source input removed |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and worktree-status check | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0209/IntakeProbe.lean` | 0 | twelve APIs elaborated; stdout 2,915 bytes, SHA-256 `b499e7dc...27c9`; no canonical target or proof body |
| bounded exact-topic `rg` search over pinned mathlib and repository Lean | 1 | expected no-match result; no Descartes-circle, Soddy, Apollonian-packing, signed-bend, or oriented-Descartes declaration matched |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0209-statement-pycache python3 -B Stage1_Instances/THM-M-0209/check_intake.py` | 1 | historical intake checker fails closed because integration changed intake state from `[ ]` to `[_]`; it was not modified or represented as statement evidence |

Final scoped checks parse and validate the blocker JSON, scan the owned Lean file for prohibited
declarations, verify the two-file owned change set and absence of `.stage1-worker-selftest.json`,
and check final-newline and trailing-whitespace hygiene.

## Retry condition and status boundary

The integration lane must master-accept the intake dependency. Accountable reviewers must preserve
and independently approve one exact source proposition, including every incorporated definition,
the ordinary-versus-oriented scope, the circle/line representation, tangency and common-tangent
conditions, bend convention, binders, hypotheses, conclusion, proof boundary, corrections, and
degenerate cases. A fresh statement attempt may then encode exactly that claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute the removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations.

This blocker is the truthful result of the assigned phase, not completion. The lifecycle remains
`planned`; the vector remains `[H1, M4, R4]`; `audit_complete` and `theorem_complete` remain false.
Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, worker
`[_]`, statement receipt, proof credit, or master acceptance is claimed.

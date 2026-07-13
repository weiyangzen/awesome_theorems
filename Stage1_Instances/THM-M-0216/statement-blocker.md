# Exact-statement gate: blocked

Item: `S56-M-0216-STATEMENT`

Theorem: `THM-M-0216`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The statement
item remains `[ ]`. Its prerequisite intake is provisional worker state `[_]`, not master-accepted
state `[x]`; its receipt declares `accepted: false`, is not content-addressed, and deliberately
leaves the canonical mathematical statement and Lean expression null.

More importantly, the complete claim-bearing source wording is only the title "Gauss-Bonnet
theorem" and the gloss "the relationship between a surface's total curvature and topology." It
gives no citation, definition chain, formula, ordered binders, hypotheses, conclusion, proof
boundary, correction history, or boundary policy. The catalog's `verified` label is untrusted
metadata under rev-5.6, and Stage0 explicitly leaves the exact definitions and premises open.

The wording does not choose among materially different propositions, including:

- the closed compact oriented boundaryless surface identity;
- the smooth-boundary formula with signed boundary geodesic curvature;
- the piecewise-smooth formula with corner-angle corrections; or
- nonorientable, disconnected, noncompact, singular, or finite-total-curvature extensions.

It also does not select an abstract Riemannian manifold or embedded surface, regularity,
compactness, connectedness, orientability, curvature convention, area measure or form, sign and
scalar normalization, Euler-characteristic representation, or treatment of empty and exceptional
cases. Those choices change the proposition. Choosing the familiar closed formula, a convenient
special case, or a textbook bundle would invent, narrow, broaden, or substitute mathematics rather
than elaborate the exact received target.

There is therefore no canonical expression on which to certify minimal imports, serialize an
expression and environment fingerprint, compile alternate transports, or execute the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those tests
are undefined, not passed. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports
`Mathlib.Geometry.Manifold.Riemannian.Basic` and
`Mathlib.Algebra.Homology.EulerCharacteristic`. It re-elaborates a generic Riemannian-manifold
context, a dimension-two compact-context predicate, and Euler-characteristic operations on a
supplied homological complex. It defines no canonical target or proof body. Its imports are
adjacent discovery candidates and cannot be called minimal for an absent target.

A bounded exact-topic search of repo-local Lean and pinned mathlib found no Gauss-Bonnet,
Gaussian-curvature, or geodesic-curvature declaration under the recorded terms. The Euler
characteristic hits concern homological complexes, graded objects, or finite bounded orders, not a
checked construction of the same surface's topological Euler characteristic. Additionally,
`Mathlib.Geometry.Manifold.PartitionOfUnity` records differential-form integration over a manifold
as a TODO. The inspected interfaces and searches therefore did not locate target-capable concrete
definitions for either side of the intended identity or their bridge. Introducing caller-supplied
curvature, integral, boundary, corner, or Euler-characteristic values would make only an abstract
substitute elaborate and is rejected.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` link to canonical
pinned artifacts was used read-only. No update, build, clone, fetch, or dependency mutation was
run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all other commands ran from the repository root unless noted otherwise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0216` | 0 | rank 1231, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` before edits | 0 | only the pre-existing automation `.lake` link was untracked; base revision and tree are recorded above |
| scoped catalog, Stage0, manifest, DAG, blueprint, skill, and intake-dossier inspection | 0 | only a topic gloss is claim-bearing; the canonical statement, binders, hypotheses, conclusion, Lean expression, imports, expression hash, and target environment fingerprint remain null |
| SHA-256 over authority, intake, probe, toolchain, lockfile, and relevant pinned mathlib inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; package worktree clean |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0216/IntakeProbe.lean` | 0 | five adjacent APIs elaborated; no canonical target or proof body; stdout SHA-256 `13d5d6a9ff426734ea440a7ee7db2f8267df5031dd88568494202a5d0f562756`; empty stderr |
| bounded Gauss-Bonnet and curvature search in repo-local and pinned-mathlib Lean | 1 | expected no-match result; statement-feasibility evidence only |
| bounded Euler-characteristic search in pinned mathlib | 0 | only homological-complex, graded-object, and finite-order interfaces matched; no same-surface bridge was found |
| `python3 -B Stage1_Instances/THM-M-0216/check_intake.py` | 1 | historical intake-only checker requires the now-absent intake worker packet and freezes its original nine-file intake inventory; this statement run does not rewrite historical evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

## Retry Condition And Status Boundary

The integration lane must accept the intake dependency through a valid receipt. Accountable
reviewers must preserve and hash one immutable primary or authoritative source, select one exact
Gauss-Bonnet proposition with a page or section locator, and transcribe every incorporated
definition, convention, normalization, ordered binder, hypothesis, conclusion, proof boundary,
correction, erratum, and boundary or degenerate case. They must also reconcile the scope with the
separately cataloged Theorema Egregium, Chern-Gauss-Bonnet, and hyperbolic-area targets.

A dependency-legal implementation or immutable pinned integration must then provide concrete
compatible interfaces for the selected curvature, surface integration, and Euler-characteristic
construction, plus boundary integration or corner terms if the selected variant requires them. A
later statement worker can encode that same reviewed claim, minimize its pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and run all
four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.

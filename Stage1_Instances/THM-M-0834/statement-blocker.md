# Exact-statement gate: blocked

Item: `S56-M-0834-STATEMENT`

Theorem: `THM-M-0834`

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0834-INTAKE` has only provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is unaccepted, non-content-addressed,
and contains no accepted receipt ID. Its historical checker also no longer replays against current
authority: it freezes intake state `[ ]`, while the execution DAG now records `[_]` with one attempt.
This statement run records that dependency boundary rather than rewriting historical intake evidence.

Independently, no exact Lean 4 target can be truthfully elaborated from the repository record. The
target-bearing record gives only `五色定理`, Percy Heawood, 1890, and `平面图可用五种颜色着色`
(planar graphs can be colored using five colors). It supplies no citation, domains, ordered binders,
hypotheses, conclusion, graph or map definition, planarity convention, coloring semantics, proof
boundary, correction, or erratum. Stage0 explicitly leaves the precise definitions and premises
open, and the catalog's `已验证` label is untrusted under rev-5.6.

The recognizable theorem family still contains proposition-changing choices:

- finite graphs, locally finite graphs, plane graphs, or plane maps, including simplicity, loops,
  parallel edges, isolated vertices, bridges, and disconnected components;
- planarity as an existential embedding, supplied embedding, combinatorial map, forbidden-minor
  predicate, or another representation, in the plane or sphere;
- vertex coloring versus map-region coloring, including face adjacency, repeated boundary walks,
  degenerate faces, and the outer face;
- `Fin 5` coloring, `G.Colorable 5`, a chromatic-number inequality, or another formulation of at
  most five colors rather than requiring every color to occur;
- universe, finiteness, decidability, and classical-choice binders; and
- empty, singleton, edgeless, low-cardinality, disconnected, and unused-color cases.

Choosing the familiar modern sentence "every finite planar simple graph is `Colorable 5`" would
resolve these choices without an admitted source. It would add mathematics rather than elaborate
the exact received target. The intake therefore deliberately leaves `canonical_statement`, the
formal module and expression, imports, expression hash, environment fingerprint, binders,
hypotheses, and alternate encodings null or empty.

The historical lead is P. J. Heawood's *Map-Colour Theorem*, *Quarterly Journal of Pure and Applied
Mathematics* 24 (1890), 332-338. It remains a bibliographic lead only: no immutable primary pages,
pinpoint proposition, incorporated definitions, proof boundary, correction or errata record,
modern map-to-graph transport, or independent source review has been admitted. The external Lean
lead `PlanarGraph.fiveColorable` is also ineligible: its route through `fiveListColorable` and core
dependencies contains explicit placeholders and targets Lean `4.30.0-rc2`, not this pinned
environment.

Because the canonical proposition is absent, minimal imports, an elaborated expression fingerprint,
checked transports, and the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary mutations are not assessable. They are undefined, not passed. No `Statement.lean`, theorem
declaration, proof body, axiom, placeholder, weakened special case, or broadened theorem was added.
The root vector stays `[H1, M4, R4]`.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with its sole direct import,
`Mathlib.Combinatorics.SimpleGraph.Coloring`. It checked these seven adjacent interfaces:

```text
SimpleGraph
SimpleGraph.Coloring
SimpleGraph.Coloring.mk
SimpleGraph.Colorable
SimpleGraph.Colorable.mono
SimpleGraph.chromaticNumber
SimpleGraph.chromaticNumber_le_iff_colorable
```

They provide ordinary simple-graph coloring vocabulary only. The mathlib module documentation lists
planar graphs as future work, and the thousand-theorem index names the Five color theorem without a
declaration. A bounded search found no selected graph-planarity or exact five-color declaration.
The probe's import is not claimed minimal for an absent canonical target, and its successful
elaboration supplies no statement or proof credit.

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No update, build, dependency clone or fetch, or other `.lake` mutation ran.

## Validation record

Commands ran on 2026-07-13 in this isolated worker clone.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0834` | 0 | rank 1392; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided untracked `.lake` symlink existed; base revision and tree are recorded above |
| `git blame -L 6124,6129 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0834/check_intake.py` | 1 | historical intake replay rejects its frozen intake state `[ ]` because current authority records `[_]` with one attempt; it was not modified or represented as statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0834/IntakeProbe.lean` | 0 | seven adjacent coloring interfaces elaborated; stdout SHA-256 `dec3dd9d2ce185193f252f1477a619ebc5f45438c5a3a60ffd43996067107ef2` |
| bounded exact-topic `rg` over owned, repo-local, and pinned Lean files | 0 | only the probe boundary comment and mathlib planar-graphs TODO matched; output SHA-256 `918b76aa11196c00f511d9b7700d3322a8b9de806290b70933988bfa033e3c54`; discovery only |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |

## Retry condition

The integration lane must first accept refreshed intake evidence. Accountable reviewers must then
preserve an immutable primary or approved authoritative source, select and independently approve one
exact proposition, and map every incorporated definition, ordered binder, hypothesis, conclusion,
proof boundary, correction, erratum, and boundary case. They must settle the graph or map carrier,
finite scope, planarity or embedding model, plane or sphere convention, vertex or region coloring,
at-most-five semantics, and every required representation or coloring transport.

A fresh statement worker can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile each credited transport, and
run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of this node or any downstream
node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed.
Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, worker
`[_]`, statement receipt, proof credit, or master acceptance is claimed.

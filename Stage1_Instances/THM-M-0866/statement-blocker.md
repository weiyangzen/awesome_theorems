# THM-M-0866 exact-statement gate: blocked

- Item: `S56-M-0866-STATEMENT`
- Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`
- Base tree: `6434a20532ae7c523ad293e67a6228ab384bfb8a`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully frozen from the received source record. The catalog
supplies the title Wagner theorem, attributes it to Klaus Wagner in 1937, and gives only the gloss
"forbidden-minor characterization of planar graphs." This identifies a theorem family but does not
state one binder-complete proposition. The familiar modern candidate is:

> A finite graph is planar if and only if it has neither `K5` nor `K3,3` as a graph minor.

The provisional intake expressly records that wording as an uncredited candidate, not the canonical
claim. The dossier contains only a bibliographic lead to Wagner's *Uber eine Eigenschaft der
ebenen Komplexe*, *Mathematische Annalen* 114(1), 570-590 (1937), DOI
`10.1007/BF01594196`. During this attempt, the complete volume was located in Goettingen's public
GDZ digitization; its IIIF manifest has SHA-256 `a66fabde...493` and identifies article scans for
pages 570 through 590. The manifest has no explicit license field, and this worker did not complete
a proposition-level transcription or review. The dossier therefore still lacks an admitted
pinpoint proposition, incorporated source-era definitions, proof boundary, correction or erratum
review, source-to-modern transport, or independent source approval. A historical JFM review
describes deletion and endpoint identification with parallel-edge merging and flags an incorrect
final sentence in the introduction, but that secondary account neither transcribes the target
proposition nor establishes the modern `K5`/`K3,3` crosswalk.

Selecting the familiar biconditional would decide proposition-changing matters that the repository
has deliberately left open: finite simple graphs versus source-era complexes or multigraphs,
abstract planarity and plane-versus-sphere embeddings, deletion and contraction witnesses,
graph-minor orientation, contraction cleanup, the two obstruction representations, ordered
binders, hypotheses, conclusion orientation, and degenerate cases. Defining these notions ad hoc
inside a Lean statement would move the missing mathematics into worker-chosen structures rather
than elaborate the exact received theorem. Kuratowski subdivisions, ordinary or induced subgraphs,
matroid minors, one implication, or one obstruction are not substitutes.

The prerequisite intake also has authoritative state `[_]`, not master-accepted `[x]`. Its receipt
is provisional, unaccepted, and non-content-addressed, with no accepted receipt ID. The historical
intake checker now stops at its frozen expectation that the authoritative intake state is `[ ]`,
whereas integration advanced that cursor to `[_]`. This statement phase records the stale replay
honestly rather than rewriting intake evidence or authoritative state.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing canonical expression fingerprint
hard blockers. With no canonical target, import minimality, checked transports, and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not successful tests. The vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` re-elaborates under the pinned environment with two direct
imports:

- `Mathlib.Combinatorics.SimpleGraph.Bipartite`
- `Mathlib.Combinatorics.SimpleGraph.Copy`

It checks `SimpleGraph`, complete and complete-bipartite graph constructors, graph copies,
ordinary and induced containment, and induced graphs. Ordinary or induced containment does not
model edge contraction and therefore cannot be renamed into graph-minor containment. The imports
are adjacent substrate for a possible future encoding, not certified minimal imports for an absent
canonical target.

A bounded exact-topic search of pinned mathlib and repository-local Lean found no graph-minor
relation, edge-contraction operation, graph-planarity predicate, or Wagner declaration. The newer
`Graph.Basic` module says minors are future work, while `Graph.Subgraph` provides containment
relations only. `SimpleGraph.map` may identify arbitrary vertices and discard resulting loops, but
it does not restrict identifications to legal contractions; supplying the necessary connected-fiber
or elementary-contraction closure would be a new minor definition. Vertex replacement and ordinary
or induced copies likewise are not contraction witnesses. The only target-pattern match in the
pinned graph trees is a planar-graphs TODO in `Coloring.lean`; repository Kuratowski matches concern
metric-space embeddings, not planar graph obstructions. This is narrow feasibility evidence, not
the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all other commands ran from the repository root unless noted. Exact command
and result records, current authority hashes, intake hashes, and pinned-source hashes are preserved
in `statement-blocker.json`. That JSON is a worker blocker report, not a node receipt or accepted
state authority.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0866` | 0 | rank 1420; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, manifest, catalog, Stage0 record, execution DAG, and complete intake dossier | 0 | confirmed provisional dependency, null target, and unresolved source, graph-model, planarity, minor, obstruction, binder, and boundary choices |
| `sha256sum` over current authority, source, intake, toolchain, lockfile, and relevant pinned mathlib inputs | 0 | current digests for all named inputs are recorded in the structured blocker |
| GDZ IIIF manifest retrieval for volume `PPN235181684_0114` | 0 | public 910,578-byte manifest SHA-256 `a66fabde...493` exposes the source pages, but no exact proposition or definition crosswalk was completed |
| pinned Lean, Lake, and mathlib revision/tree/status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib revision and tree |
| `lake env lean ../../Stage1_Instances/THM-M-0866/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; output SHA-256 `54da595e...70a3`; no canonical target or proof body was declared |
| bounded exact-topic search in pinned `SimpleGraph` and repo-local Lean | 0 | only the planar-graphs TODO matched; output SHA-256 `ca8e361a...89e`; no target-specific definition or theorem was located |
| `python3 -B Stage1_Instances/THM-M-0866/check_intake.py` | 1 | historical intake replay stopped because it expects authoritative intake `[ ]`, while integration records provisional `[_]`; this phase did not rewrite it |
| JSON parse, scoped blocker invariants, and prohibited-construct scan | 0 aggregate | blocker identity, null target, unchanged vector, false completion fields, exact owned scope, and no proof escape agree |
| scoped whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement completion gate failed |

## Retry Condition And Status Boundary

The integration lane must first revalidate and master-accept the intake. Accountable independent
reviewers must then lawfully preserve and hash an immutable primary or approved authoritative
source; pinpoint and approve its exact proposition and incorporated definitions; inspect its proof,
translation, correction, and erratum boundaries; and approve the source-era-to-modern graph
transport. They must freeze the graph class, planarity, graph-minor relation and orientation,
`K5` and `K3,3` encodings, ordered binders, hypotheses, conclusion, logical profiles, and every
boundary case.

A fresh statement worker can then encode only that approved claim, minimize its pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt change is proposed. Because the exact-statement deliverable did
not pass, no `.stage1-worker-selftest.json`, `Statement.lean`, statement receipt, worker `[_]`,
accepted state, or master acceptance is claimed.

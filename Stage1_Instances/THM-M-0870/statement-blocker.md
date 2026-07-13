# THM-M-0870 exact-statement gate: blocked

- Item: `S56-M-0870-STATEMENT`
- Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`
- Base tree: `018557070da18ea1733a82de81a238750c59aa84`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the admitted repository record. The
complete mathematical content is the label `树宽` (treewidth), the attribution Neil
Robertson/Paul Seymour, the year 1984, and the noun phrase `图的树分解` (tree decompositions of graphs).
This identifies a subject and invariant family, not one truth-valued proposition. It does not choose
a definition of a tree decomposition or treewidth, a decomposition-existence result, a
bounded-treewidth predicate, a characterization, a monotonicity or structural theorem, or an
algorithmic result.

The proposition-changing conventions are also absent: finite or infinite and simple, directed, or
multigraph domain; the decomposition index tree and its finiteness; bag representation; vertex and
edge coverage; running intersection; width as maximum bag size minus one; optimum and attainment;
ordered binders, hypotheses, and conclusion; and all degenerate cases. In particular, using natural
numbers can collapse a source-dependent empty-graph width convention of `-1` to `0`. Selecting a
familiar convention or a convenient result would invent or substitute mathematics, not elaborate
the exact target.

The bibliographic leads do not repair the ambiguity. Robertson and Seymour's *Graph minors. II.
Algorithmic aspects of tree-width* (1986) fits the broad topic but not the catalog year. *Graph
minors. III. Planar tree-width* (1984) fits the year but narrows the subject. Intake admitted only
bibliographic metadata: no immutable primary theorem passage, exact definition or theorem locator,
incorporated definitions, proof/correction crosswalk, catalog-identity decision, or independent
source and scope review. Neither lead can be silently promoted to the root.

The prerequisite `S56-M-0870-INTAKE` is also provisional `[_]`, not accepted `[x]`. Its receipt is
unsigned, non-content-addressed, `accepted: false`, and has no accepted receipt ID. The historical
intake checker now stops because integration changed the authoritative blueprint bytes. This attempt
records that freshness boundary rather than rewriting historical intake evidence or the generated
authority files.

The decisive statement failure is independent of the stale dependency. Rev-5.6 sections 5 and 5.1
make statement ambiguity and a missing elaborated-expression fingerprint hard blockers. The intake
deliberately leaves the canonical human statement, Lean module/expression, ordered binders,
hypotheses, conclusion, alternate encodings, expression hash, and canonical-target environment
fingerprint null or empty. Consequently minimal imports, checked transports, and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. No `Statement.lean`, proxy predicate, theorem declaration, proof body, broadened
interface, or special case was added. The vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates under the pinned environment with two
direct imports:

- `Mathlib.Combinatorics.SimpleGraph.Acyclic`
- `Mathlib.Data.Set.Card`

Its eight checks expose simple-graph, graph-tree, induced-graph, graph-isomorphism, spanning-tree,
and finite-set-cardinality interfaces. Axiom reports are `[propext, Quot.sound]` and
`[propext, Classical.choice, Quot.sound]`. These imports expose no tree-decomposition-specific bag
family, decomposition-width or treewidth API, or source-selected proposition. They cannot be
certified minimal for an absent target and receive no statement or proof credit.

A bounded case-insensitive search over pinned mathlib, repo-local Lean, and this owned path matched
only the probe disclaimer. It located no literal treewidth or tree-decomposition target declaration.
This is narrow statement-feasibility evidence, not the downstream anchor audit and not a global
formal-absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation ran.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root. Exact arguments, results, input
hashes, and output hashes are preserved in `statement-blocker.json`. That JSON is a repository-local
worker blocker report, not a statement receipt or accepted-state artifact.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0870` | 0 | rank 1424; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority, source, complete-intake, toolchain, lockfile, and direct-mathlib-source `sha256sum` checks | 0 | current digests are preserved in the structured blocker |
| pinned Lean, Lake, and mathlib revision/tree/status checks | 0 | expected versions and clean pinned mathlib worktree |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0870/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `07e698bb...d27e`; no target declaration |
| bounded exact-topic search | 0 | only the probe disclaimer matched; stdout SHA-256 `32e939ff...ff87` |
| `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0870/check_intake.py` | 1 | historical intake replay stopped at stale `Docs/Stage1_Blueprint_rev-5.6.md`; combined output SHA-256 `8f8d5a9a...fafd` |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, blocker-invariant, whitespace, scoped-change, and absent-self-test checks are also recorded
in the structured report after artifact creation.

## Retry Condition And Status Boundary

The integration lane must master-accept a fresh intake receipt bound to current authority.
Accountable graph-theory source, scope, and Lean reviewers must preserve one immutable primary or
approved authoritative source and independently approve one exact truth-valued proposition. They
must crosswalk every incorporated definition, premise, conclusion, proof boundary, correction, and
erratum; resolve graph, index-tree, bag, cover, running-intersection, width, optimum, quantifier,
hypothesis, conclusion, and degenerate-case semantics; and respect neighboring target ownership.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned direct
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt change is proposed. Because the exact-statement deliverable did
not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master
acceptance is claimed.

# Exact-statement gate: blocked

Item: `S56-M-0908-STATEMENT`

Theorem: `THM-M-0908`

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0908-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt declares `accepted: false`, is
non-content-addressed, and has no accepted receipt ID. The receipt also binds older blueprint and
execution-DAG hashes than the current authorities. Rev-5.6 permits this dependency-ordered
statement attempt, but fresh intake acceptance remains necessary before a future statement
transition can be accepted.

Independently of that dependency boundary, the exact Lean 4 target cannot be truthfully elaborated
from the authoritative repository record. The complete catalog entry gives only `Thomassen定理`,
Carsten Thomassen, 1994, and `平面图的列表色数` (the list chromatic number/list coloring of planar
graphs). It supplies no bibliography, proposition, definitions, binders, hypotheses, conclusion,
proof boundary, correction record, or reviewer. Stage0 repeats that gloss while explicitly leaving
the precise definitions and premises open.

Bibliographic metadata identifies the intended family as C. Thomassen, *Every Planar Graph Is
5-Choosable*, *Journal of Combinatorial Theory, Series B* 62(1), 1994, 180-181, DOI
`10.1006/jctb.1994.1062`. Secondary literature explains the conventional statement: every planar
graph is properly colorable from any assignment of at least five available colors per vertex.
Neither the title nor those secondary records settle all proposition-changing choices needed by an
exact Lean target:

- finite graphs versus an arbitrary locally finite extension;
- abstract simple graphs versus supplied plane graphs or combinatorial maps;
- existential planarity versus a supplied embedding or another planarity model;
- exactly five versus at least five available colors and the required thinning transport;
- finite sets versus duplicate-bearing lists or multisets;
- arbitrary color types versus natural-number colors;
- disconnected graphs, isolated vertices, bridges, empty and small carriers, and degenerate faces;
  and
- proper list colorability, `ListColorable 5`, or a list-chromatic-number inequality.

No lawful immutable primary text, pinpoint theorem and incorporated definitions, complete premise
map, proof boundary, correction or errata audit, modern transport, or independent review has been
accepted. Installing the familiar finite-planar-simple-graph formulation would therefore add
mathematics that the source record and intake deliberately leave open. It would not elaborate the
exact received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. Without a canonical proposition there is no honest target import set to
minimize, expression or environment-expression fingerprint to serialize, alternate encoding to
credit, or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutation. Those four mutation classes are undefined, not passed. The root vector remains
`[H1, M4, R4]`. No `Statement.lean`, theorem declaration, assumed planarity certificate,
placeholder, weakened coloring theorem, or broadened target was introduced.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the direct import
`Mathlib.Combinatorics.SimpleGraph.Coloring`. Its eight checks authenticate ordinary proper
coloring, colorability, and chromatic-number interfaces. It defines no list assignment,
choosability predicate, list-chromatic number, graph-planarity predicate, canonical Thomassen
target, checked source transport, or proof body. Its import therefore cannot be certified minimal
for an absent target.

A bounded exact-topic search under pinned mathlib and the repo-local Lean tree found only the
ordinary Coloring module's planar-graph TODO and unrelated prose matches. It identified no direct
Thomassen, list-coloring, choosability, list-chromatic-number, or graph-planarity declaration. This
is discovery-only feasibility evidence, not the downstream anchor audit or a global absence claim.

The immutable external lead `bsniegowski/lean-planar-graphs` at revision
`4d560bc5ec87c763d2042b9e7a5dcfc67b6e6c3d` declares `PlanarGraph.fiveListColorable`, but its
interface is a finite connected supplied plane graph with exactly five natural-number colors per
vertex. Its theorem and dependencies contain explicit placeholders, and it uses Lean `4.30.0-rc2`
with another mathlib pin. It is a narrower interface lead, not statement authority or proof
evidence.

The pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0908` | 0 | rank 1450; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| manifest, blueprint, skill, guideline, catalog, Stage0, and complete intake inspection | 0 | the catalog is not binder-complete, the canonical target is null, and every proposition-changing convention listed above remains open |
| `python3 -B Stage1_Instances/THM-M-0908/check_intake.py` | 1 | historical replay stops at line 123 because it freezes intake authority state `[ ]` while the current authoritative DAG records provisional `[_]` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | the pinned Lean and Lake versions above were reported |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | the revision and tree above matched; empty status output confirmed a clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0908/IntakeProbe.lean` | 0 | eight adjacent ordinary-coloring APIs elaborated; stdout SHA-256 `0852835123f503927196ecd4ebe73804ba4a22403f17e67d8f0ebe4b20417051`; no canonical target or proof body was declared |
| bounded exact-topic `rg` under pinned mathlib and repo-local Lean | 0 | only the ordinary Coloring TODO and unrelated prose matched; discovery evidence only |
| SHA-256 over authority, intake, toolchain, lockfile, probe, and pinned Coloring inputs | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `python3 -m json.tool` and scoped blocker-invariant checks | 0 | JSON syntax, identity, blocked/null-target state, unchanged vector, undefined mutations, false completion flags, and exact change scope agreed |
| prohibited Lean declaration scan, tracked and no-index whitespace checks, and `test ! -e .stage1-worker-selftest.json` | expected no-match/difference exits; wrappers 0 | no prohibited declaration or whitespace diagnostic; self-test manifest absent |

The historical intake checker owns pre-integration authority state, so this phase records its
failure rather than rewriting the intake checker, receipt, task DAG, generated blueprint, or
authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must preserve a lawful immutable primary or approved authoritative source and independently approve
one exact proposition, all incorporated definitions and premises, its proof boundary, corrections,
errata, and source-to-modern transport. They must freeze graph and finiteness scope, the planarity
or embedding model, list representation and cardinality, color carrier, disconnected and
degenerate cases, ordered binders, hypotheses, exact conclusion, and every alternate encoding.

A fresh statement run can then encode precisely that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, proof credit,
or master acceptance is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.

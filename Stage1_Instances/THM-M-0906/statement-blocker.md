# Exact-statement gate: blocked

Item: `S56-M-0906-STATEMENT`

Theorem: `THM-M-0906`

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`). Attempt date: 2026-07-13
(Asia/Shanghai).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0906-INTAKE` is provisional worker state
`[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false` and
`content_addressed: false`, has no accepted receipt ID, and is stale against the current
authoritative blueprint. Replaying `check_intake.py` stops at
`stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md`. This statement attempt preserves the
historical intake evidence rather than rewriting it.

Independently and decisively, the exact source-statement gate fails. The complete catalog record is
the title `列表着色` (list coloring), the attribution Vizing/Erdos/Rubin/Taylor, the year 1976, and
the gloss `列表色数的理论` (the theory of the list chromatic number). A mathematical theory or an
invariant name is not one truth-valued proposition. The record supplies no bibliography, formula,
definitions, domains, ordered binders, hypotheses, conclusion, proof boundary, correction, erratum,
or reviewer. Its `已验证` label is untrusted inventory metadata under rev-5.6.

The missing choices change the proposition:

- vertex, edge, or another incidence coloring mode, and the simple-graph, multigraph, directed, or
  hypergraph model;
- finite or infinite vertex and color carriers and all finiteness, equality, and choice assumptions;
- `Finset`, `Set`, `List`, or `Multiset` allowed-color assignments and whether duplicates count;
- exactly `k` or at least `k` allowed colors and any thinning transport;
- definition, existence, comparison, bound, equality, characterization, or special graph class as
  the root conclusion; and
- empty and singleton graphs, `k = 0` or `k = 1`, empty or undersized lists, infinite palettes,
  nonattainment, and vacuous properness.

Several familiar claims fit the gloss: definitions of list coloring and choosability, existence of
a finite graph's choice number, comparison with ordinary chromatic number, degree or degeneracy
bounds, and exact values for graph classes. The repository selects none of them. The neighboring
Dinitz, Galvin, Alon-Tarsi, Thomassen, and Voigt records are separate targets. Choosing any such
claim here would invent, narrow, broaden, or substitute mathematics instead of elaborating the
received target.

Rev-5.6 sections 3.1, 5, and 5.1 make this `H5` classification and the missing expression
fingerprint hard blockers. There is no canonical Lean expression whose imports can be minimized,
no fixed elaboration context or environment-expression fingerprint, and no approved alternate form
for a checked transport. The required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined, not passed. The root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated with its two direct imports:

- `Mathlib.Combinatorics.SimpleGraph.Coloring`
- `Mathlib.Data.Finset.Card`

It checks eight adjacent ordinary-coloring, chromatic-number, finite-set, and cardinality APIs. It
does not define per-vertex allowed colors, choosability, a choice number, a source-selected target,
or a proof body. Its imports therefore are not a minimal-import result for the absent canonical
target and receive no statement or proof credit.

A bounded exact-topic search over pinned mathlib and repository-local Lean found no list-coloring,
choosability, choice-number, or list-chromatic declaration. This is narrow discovery evidence, not
the downstream anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe output SHA-256 is
`e8fa74d4770eedf1237f569d6d2530da03b8269b14813e641c3c5391c38f1882`.

The automation-provided `Formalizations/Lean/.lake` symlink was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other dependency mutation was run; the pinned mathlib
package remained clean.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13. Lean commands used `Formalizations/Lean`; other
commands used the repository root unless noted. Exact structured results and current input hashes
are recorded in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0906` | 0 | rank 1448; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped authority, source, and complete intake-dossier inspection and hashing | 0 | confirmed provisional stale intake evidence, a null canonical claim and Lean target, and unresolved proposition-changing choices |
| `python3 -B Stage1_Instances/THM-M-0906/check_intake.py` | 1 | historical intake replay stopped at its stale blueprint hash; this phase did not rewrite historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the environment above |
| pinned mathlib revision, tree, and package-status checks | 0 | expected revision and tree; dependency worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0906/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated with the output hash above; no target or proof body |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 1 | expected no-match result; discovery only |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped blocker invariant check, and whitespace checks | 0 aggregate | blocker identity, null target/imports, unchanged vector, false completion fields, exact changed paths, and absent-self-test boundary agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first accept fresh intake evidence. Accountable source and graph-coloring
reviewers must then lawfully preserve and hash an immutable primary or approved authoritative
source, select and independently approve one exact proposition, and map every incorporated
definition, ordered binder, hypothesis, conclusion, graph and coloring mode, list representation,
cardinality convention, proof boundary, correction, erratum, neighbor boundary, and degenerate
case.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, accepted state, proof credit, or
master acceptance is claimed.

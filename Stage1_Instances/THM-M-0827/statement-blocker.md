# THM-M-0827 statement-phase blocker

## Verdict

`S56-M-0827-STATEMENT` is blocked. The exact statement gate did not pass, the node remains
`[ ]`, and the root vector remains `H1 / M4 / R4`. No `Statement.lean`, statement receipt, or
root `.stage1-worker-selftest.json` was emitted.

The immediate dependency is also only provisional: `S56-M-0827-INTAKE` is `[_]`, has one
attempt, and is not master accepted. Rev-5.6 permits preparation of blocker evidence while later
work is concurrent, but it does not permit a dependent state transition before that acceptance.

## First failed statement gate

The received mathematical record is not a truth-valued proposition. It contains only the name
"Floyd-Warshall algorithm", the Floyd/Warshall attribution, the year 1962, and the gloss
"all-pairs shortest-path algorithm." Stage0 expressly leaves the definitions, premises, proof
route, dependencies, formal system, axioms, and machine artifacts open. The separate computer-
science target `THM-C-0093` adds an `O(n^3)` gloss, but it is a different UID and cannot broaden
this mathematical target.

Consequently the record does not choose any one of these non-equivalent propositions:

- the intermediate-vertex dynamic-programming recurrence invariant;
- final all-pairs distance correctness;
- next-hop or predecessor reconstruction correctness;
- negative-cycle detection by a selected diagonal condition;
- Boolean transitive closure or an approved Boolean/min-plus transport;
- refinement and termination of a specified triple loop;
- an operation-count or asymptotic-complexity theorem.

It also does not fix the finite graph and edge representation, weight and infinity domain,
walk/path and shortest-value semantics, negative-cycle scope, vertex enumeration, initialization,
snapshot versus in-place updates, output carrier, reconstruction contract, exact arithmetic, cost
model, ordered binders, hypotheses, or degenerate cases. Selecting a familiar textbook version
would therefore invent or substitute mathematics rather than elaborate the exact target.

## Lean boundary

The pinned substrate probe uses:

- `Mathlib.Combinatorics.Digraph.Basic`;
- `Mathlib.Combinatorics.Quiver.Path.Weight`;
- `Mathlib.Combinatorics.SimpleGraph.Metric`.

It elaborates directed adjacency, additive dependent-path weights, and unweighted undirected
distance APIs under Lean 4.29.0 and pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
These are discovery imports, not a minimal import result for a canonical Floyd-Warshall target.
None defines the missing recurrence, algorithm state, weighted all-pairs semantics, or correctness
theorem. A bounded repository-local and pinned-mathlib name search found no exact-topic Lean
artifact; that is discovery evidence only, not a global absence proof or anchor audit.

Without a canonical proposition, there is no target to elaborate, no honest minimal-import set,
no expression or environment fingerprint, no checked alternate encoding, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation test. The
rev-5.6 hard blocker therefore fires before any proof evidence may be inspected.

## Validation evidence

Commands were run from the repository root unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0827` | 0 | rank 1385; planned; no legacy slot; theorem completion false |
| `python3 -B Stage1_Instances/THM-M-0827/check_intake.py` | 1 | historical intake replay stopped at its frozen target-DAG-row hash because authority now records intake `[_]` with one attempt; the historical evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0827/IntakeProbe.lean` | 0 | 15 adjacent APIs elaborated; stdout 2078 bytes, SHA-256 `26c08241afe0333e857956272de2899489e98d7ee53a4ac92e706bb54e027feb`; stderr empty; no target or proof credit |
| bounded case-insensitive Floyd/Warshall/all-pairs Lean search under repo-local Lean and pinned mathlib | 1 (expected) | no exact-topic match; discovery only |

The existing canonical `.lake` symlink and mathlib worktree were used read-only. No update, build,
clone, fetch, or dependency mutation was performed.

## Retry condition

First, the integration lane must replay and master-accept refreshed intake evidence. Accountable
source and graph-algorithms reviewers must then admit an immutable exact proposition with pinpoint
source text, incorporated definitions, premise and conclusion mapping, proof boundary, correction
and errata audit, and an explicit Floyd/Warshall or Boolean/min-plus transport. They must resolve
all graph, weight, path, negative-cycle, recurrence, update, output, complexity, binder, and
boundary choices without importing the separate `THM-C-0093` scope by default.

Only then can a fresh statement execution encode the same claim, minimize pinned imports, freeze
the canonical elaborated expression and environment fingerprint, compile every credited
transport, and run all four required semantic mutation classes.

## Status boundary

This is statement-blocker evidence only. It is not a node-specific completion receipt, accepted
state, canonical theorem statement, proof, audit completion, or theorem completion. The remaining
root cut set is `STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.

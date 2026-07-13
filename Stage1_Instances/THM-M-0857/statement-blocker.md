# Exact-statement gate: blocked

Item: `S56-M-0857-STATEMENT`

Theorem: `THM-M-0857`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`).

## Decision

The exact Lean 4 target cannot be truthfully selected from the authoritative repository record.
The catalog gives only `三次桥less图有完美匹配`: a cubic bridgeless graph has a perfect matching.
It supplies no graph model, finiteness or connectedness convention, ordered binders, exact
hypotheses or conclusion, boundary policy, or accepted formal artifact. Stage0 explicitly leaves
the exact definitions and premises open, and the catalog's `已验证` label is untrusted under
rev-5.6.

The inspected primary source is Julius Petersen, *Die Theorie der regulären graphs*, *Acta
Mathematica* 15 (1891), 193-220. The CC0 scan from Zenodo record 2304433 has SHA-256
`8762abd5e2f1fb3edcd1917b4db3b0c213a75d4ecfe026829b58e2e7913cca8c`. Printed page 194
explicitly permits multiple lines between the same two points. Page 210 defines Petersen's
bridge-separated `Blatt`, and pages 218-219 give the route from primitive cubic graphs to a
degree-two factor and a degree-one factor. This identifies the theorem family, but no accepted
independent review has frozen the complete transcription, German translation, incorporated
definitions, assumptions, proof boundary, correction or errata status, or transport to a modern
graph convention. The source status remains `H1`, not `H0`.

A convenient modern candidate would quantify over a finite type and `G : SimpleGraph V`, assume
`G.IsRegularOfDegree 3` and that no edge is an `IsBridge`, and conclude that some subgraph is an
`IsPerfectMatching`. Freezing that proposition now would collapse the parallel edges allowed by
Petersen, count distinct neighbors rather than incident edges with multiplicity, and extend the
historical connected setting to disconnected graphs without an approved componentwise transport.
Conversely, inventing a multigraph encoding would decide edge identity, loops, finiteness,
connectedness, degree, bridge deletion, matching, and factor conventions that the repository has
not approved.

Other apparently minor choices also change the proposition. `IsEdgeConnected 2` includes a
preconnectedness condition and is not automatically the catalog's bridgeless hypothesis.
Quantifying `IsBridge` over all pairs versus present edges changes the visible binder shape even
when a later simplification is possible. A perfect-matching subgraph, a one-regular spanning
factor, and the complement of a two-factor require checked directional transports before they can
share statement credit. Empty, singleton, disconnected, looped, parallel-edge, and finite versus
infinite cases are unresolved rather than excluded.

Rev-5.6 sections 5 and 5.1 make this ambiguity and the absent expression fingerprint hard
blockers. There is no canonical proposition against which minimal imports, exact expression
serialization, checked alternate transports, or the removed-hypothesis, changed-domain,
changed-binder-scope, and boundary mutations could be tested. The vector remains
`[H1, M3, R4]`.

The prerequisite intake has only provisional state `[_]`, not accepted `[x]`. Its receipt has
`accepted: false`, is not content-addressed, and lists no accepted receipt ID. Its own retry
condition requires independent source review and a separately frozen exact mutation-tested target.
Dependency master acceptance would therefore remain required even if the mathematical statement
blocker were resolved.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` re-elaborates under the pinned environment with these direct
imports:

- `Mathlib.Combinatorics.SimpleGraph.Connectivity.EdgeConnectivity`
- `Mathlib.Combinatorics.SimpleGraph.Tutte`

It checks regular degree, bridge and edge-connectivity predicates, perfect-matching interfaces,
the Tutte-violator predicate, and `SimpleGraph.tutte`. These are adjacent simple-graph APIs, not
certified minimal imports for an absent target. The probe states no canonical proposition,
source-faithful multigraph transport, or proof body.

A bounded case-insensitive search of repo-local Lean and pinned mathlib `Mathlib` and `Archive`
found no Petersen, bridgeless, bridge-free, or cubic/perfect-matching closure. That is narrow
discovery evidence only, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all other commands ran from the repository root. Exact commands, hashes,
and boundaries are preserved in `statement-blocker.json`, which is a blocker report rather than a
node receipt or state authority.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0857` | 0 | rank 1411; planned; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads and SHA-256 checks of the blueprint, skill, manifest, catalog, Stage0 record, execution DAG, complete intake dossier, pins, and relevant mathlib sources | 0 | confirmed the provisional dependency, null target, historical multigraph boundary, and current input identities |
| pinned Lean, Lake, and mathlib revision/tree/status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib revision and tree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0857/IntakeProbe.lean` | 0 | ten adjacent simple-graph interfaces elaborated; output SHA-256 `6eb4c368...af6dd81`; no target or proof body |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 (expected) | no matching declaration; empty output SHA-256 `e3b0c442...b855` |
| `python3 -B Stage1_Instances/THM-M-0857/check_intake.py` | 1 | historical intake checker expects its original `[ ]`/attempts-0 authority snapshot; current DAG records provisional `[_]`/attempts-1 |
| prohibited-construct scan of `IntakeProbe.lean` | 1 (expected) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped blocker-invariant assertions | 0 | identity, null target, unchanged vector, false completion fields, four undefined mutations, exact owned paths, and absent self-test agree |
| scoped `git diff --check` and per-new-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; expected new-file difference statuses ignored |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement gate failed |

The intake checker was frozen for the original nine-file intake packet and original execution-DAG
row. This phase preserved it rather than rewriting an intake validator or receipt to manufacture a
pass. Adding these two statement blocker artifacts also exceeds its intake-only file inventory.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable independent
reviewers must then approve the primary-source transcription, translation, definitions,
assumptions, proof and errata boundary, and a source-faithful graph model. They must decide whether
the target is the historical connected finite multigraph theorem, a modern simple-graph
specialization, a componentwise disconnected extension, or a checked relationship between those
forms.

A fresh statement worker can then freeze graph and edge universes, finiteness, connectedness, loop
and parallel-edge policy, degree, bridge and perfect-matching predicates, ordered binders,
hypotheses, conclusion, profiles, and every boundary case. It must elaborate exactly that approved
proposition with minimal pinned imports, serialize and hash its kernel expression and environment,
compile every credited transport, and execute all four required mutation classes.

This is the assigned phase's truthful blocker, not completion of the statement node. Lifecycle
remains `planned`; no debt change, receipt, statement fingerprint, worker `[_]`, audit completion,
theorem completion, accepted state, or master acceptance is claimed. No
`.stage1-worker-selftest.json` is emitted because the exact-statement deliverable did not pass.

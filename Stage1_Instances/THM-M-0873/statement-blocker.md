# Exact-statement gate: blocked

Item: `S56-M-0873-STATEMENT`

Theorem: `THM-M-0873`

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675` (tree
`7b1b5269d7da840fd086da731d6f92903c209c35`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0873-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 permits dependency-ordered preparation, but
the intake receipt is unsigned, non-content-addressed, unaccepted, and deliberately leaves the
canonical proposition and Lean target null.

The received catalog record says only that the Graph Isomorphism problem concerns graph-isomorphism
complexity and has been solved in quasipolynomial time. That identifies a result family, not a
binder-complete proposition. It fixes neither the input domain and serialization nor a deterministic
machine, cost semantics, exact asymptotic predicate, ordered constants and threshold, boundary
cases, or source-to-target transport. Each choice changes the proposition rather than filling in
mere notation.

The inspected sources do not yet license this worker to choose those missing components. Babai's
arXiv version 2 defines quasipolynomial boundedness and states the Graph Isomorphism corollary, but
it predates the January 2017 timing repair. Helfgott's post-fix exposition states that Graph
Isomorphism is solvable in quasipolynomial time in the number of vertices and explains the repaired
proof. The author update and fix note corroborate withdrawal and restoration, while author version
2.5 records fixes but calls the revision incomplete. These are strong `H1` source leads, not an
independently reviewed Stage1 packet selecting one exact edition, incorporated definitions,
assumptions, errata disposition, and source-to-node map.

Ownership is also open. `THM-M-0874` separately owns the Babai algorithm record, while
`THM-M-1567` is a duplicate-domain generic Graph Isomorphism record. Selecting an algorithm body or
counting the generic result twice without a reviewed dependency and alias decision would violate the
target boundary.

Consequently there is no exact claim from which to derive a minimal Lean import set, normalized
elaborated-expression fingerprint, checked alternate transports, or meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. The rev-5.6 statement gate fails
closed before proof evidence is inspected. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports:

```lean
import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.Computability.Language
import Mathlib.Computability.Reduce
```

In the pinned environment it re-elaborates `SimpleGraph.Iso`, its reflexive, symmetric, and
transitive operations, `Language`, `ManyOneReducible`, and `OneOneReducible`. Those interfaces
provide graph-isomorphism witnesses, unbounded languages, and computable reductions. They do not
provide a graph-pair serialization, resource-bounded deterministic machine, quasipolynomial class,
correct decision algorithm, source transport, canonical target, or proof body. Their imports
therefore cannot be certified minimal for an absent target and receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake`
symlink was used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Unresolved Statement Inputs

- Admit and independently review one immutable corrected source bundle, pinpoint result,
  incorporated definitions and assumptions, correction and errata disposition, and proof boundary.
- Resolve canonical result and proof-body ownership relative to algorithm target `THM-M-0874` and
  duplicate-domain target `THM-M-1567`.
- Freeze finite simple undirected graph and vertex representations, graph-pair serialization,
  canonicalization, padding, malformed inputs, and the relationship among vertex count, adjacency
  length, and input bit length.
- Freeze a total deterministic machine, halting and uniformity semantics, elementary-operation or
  bit cost, worst-case quantification, and the decision predicate's checked relation to graph
  isomorphism.
- Freeze the ordered algorithm, constant, exponent, coefficient, and threshold binders; positivity,
  logarithm, exponential and rounding conventions; eventual versus all-input form; and small-input
  extension.
- Resolve empty and singleton graphs, unequal vertex counts, malformed inputs, loops and parallel
  edges, directed and colored variants, constant-size cases, foundation, TCB, and computation
  profiles.

Bare decidability, membership in NP, an assertion about P or NP-intermediacy, a special-class
algorithm, a Weisfeiler-Lehman heuristic, generic graph APIs, or a predicate that assumes the
desired algorithm or bound is not a lawful substitute.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0873` | 0 | rank 1427; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | current base revision and tree recorded above |
| current SHA-256 pass over authority, source, intake, toolchain, lockfile, probe, and relevant pinned mathlib inputs | 0 | exact current digests recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0873/check_intake.py` | 1 | historical intake replay fails closed because its frozen blueprint hash predates integration; it was not rewritten or reported as statement evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at the commit above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake 5.0.0-src+98dc76e; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned dependency remained clean |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0873/IntakeProbe.lean)` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `f312f54d...acf8`; no target or proof credit |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 1 (expected no match) | empty stdout SHA-256 `e3b0c442...b855`; no exact-topic declaration under the recorded patterns; not a global absence claim |
| `python3 -m json.tool Stage1_Instances/THM-M-0873/statement-blocker.json` | 0 | finalized blocker parses as valid JSON |
| scoped blocker invariant assertions | 0 | identity, base, open state, null target/imports, unchanged vector, undefined mutations, false completion fields, two-file scope, and absent self-test agree |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0873` | 0 | no tracked-diff whitespace diagnostics |
| per-file `git diff --no-index --check /dev/null` for both new blockers | 1 each (expected difference) | empty diagnostic streams; no whitespace error |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement gate failed |

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash an authoritative corrected source bundle, select and
independently approve one exact result, and transcribe every incorporated definition, ordered
binder, hypothesis, conclusion, proof boundary, correction, encoding, complexity convention,
boundary case, and neighbor ownership decision. Master acceptance of the prerequisite is also
required before an accepted statement transition.

A fresh statement worker can then encode only that claim, minimize the pinned direct imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, master
acceptance, statement fingerprint, or proof credit is claimed.

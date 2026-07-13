# Exact-statement gate: blocked

Item: `S56-M-0829-STATEMENT`

Theorem: `THM-M-0829`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0829-INTAKE` has only provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt declares `accepted: false`, contains no
accepted receipt ID, and no longer replays against the current authority: `check_intake.py` stops
because its recorded target-DAG-row fingerprint differs from the current execution DAG. This
statement run does not rewrite that historical intake evidence.

Independently, no exact Lean 4 target can be truthfully elaborated from the repository record. The
target-bearing record gives only `Dinic算法`, Yefim Dinitz, 1970, and `最大流的分层算法` (a layered
algorithm for maximum flow). It supplies no source citation, domains, ordered binders, hypotheses,
conclusion, algorithm version, cost model, proof boundary, correction, or erratum. Stage0 explicitly
leaves the precise definitions and premises open, and the catalog's `已验证` label is untrusted under
rev-5.6.

The recognizable theorem family still contains materially different claims and proposition-changing
choices:

- a finite directed graph, edge-indexed multigraph, or capacity matrix, including the treatment of
  self-loops, parallel edges, antiparallel edges, and source equal to sink;
- natural, integer, rational, real, or nonnegative-real capacities, plus exact feasible-flow,
  conservation, value, residual-edge, and reverse-capacity conventions;
- the definition of levels, admissible edges, a blocking flow, how one is constructed, and how an
  outer phase updates the residual state;
- an executable deterministic algorithm versus a relational transition system with choices, and the
  corresponding termination and refinement contract;
- a flow-only output versus a value, minimum cut, or certificate, and whether correctness means only
  maximum flow or a conjunction with feasibility, termination, and certification; and
- the original general-network algorithm, a later dynamic-tree implementation, or specialized
  unit-capacity regimes, together with the exact definitions of `V`, `E`, primitive operations,
  arithmetic cost, and the advertised asymptotic bound.

A separate non-Stage1 target, `THM-C-0098`, says `O(V^2E)` or `O(VE log V)`. That is useful evidence
of unresolved version and cost-model ambiguity, but it is a different UID and cannot silently
redefine this mathematical target. Attributing either bound to an unselected implementation, or
joining it to a remembered correctness theorem, would substitute or broaden the received claim.

Publisher metadata for Dinitz's 2006 retrospective, DOI `10.1007/11685654_10`, identifies the 1970
paper *An algorithm for the solution of the max-flow problem with the polynomial estimation*. The
Crossref metadata and reference list were inspected at intake. The primary 1970 paper and the full
retrospective theorem and proof text were not admitted or independently reviewed. A fresh request to
the publisher PDF endpoint returned an HTML page rather than a PDF. Bibliographic identity therefore
does not select or authenticate a binder-complete proposition.

Choosing the familiar textbook Dinic correctness and `O(V^2E)` statement from memory would invent
all of the open decisions above. Section 5 of the rev-5.6 blueprint makes statement ambiguity and a
missing elaborated-expression fingerprint hard blockers. There is no canonical expression on which
to certify minimal imports, checked alternate transports, or the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. Those tests are undefined, not
passed. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports:

- `Mathlib.Combinatorics.Quiver.Path.Weight`;
- `Mathlib.Combinatorics.SimpleGraph.Metric`; and
- `Mathlib.Combinatorics.SimpleGraph.Walks.Counting`.

It re-elaborates ten adjacent interfaces for quiver paths, additive path weights, undirected
shortest-walk distance, and finite bounded-walk enumeration. None defines a capacitated flow,
residual directed network, level graph, blocking flow, Dinic execution, maximum-flow conclusion, or
complexity bound. In particular, additive path weight is not residual bottleneck capacity and an
undirected `SimpleGraph` metric is not a directed residual level graph. The probe states no target,
so its three imports are discovery inputs and cannot be certified minimal for an absent target.

A bounded source search of pinned mathlib and repository-local Lean found no declaration matching
Dinic/Dinitz/Dinits, maximum flow, blocking flow, residual network, or level graph. The only match
was the boundary comment in the owned intake probe. This is narrow feasibility evidence, not the
downstream anchor audit and not an absence claim outside the searched closure.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, and `IntakeProbe.lean` are, respectively,
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`82e6cb86e474b3d27581490b1c757e4bd61747de56c4f189ff632e3e2b8eb014`.

The automation-provided `Formalizations/Lean/.lake` link to the canonical pinned artifacts was used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was
run. The pinned mathlib package remained clean.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0829` | 0 | rank 1387; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| repository, manifest, source, Stage0, intake, scope, and companion-record inspection | 0 | found only the broad layered-maximum-flow gloss, provisional null target, and unresolved model/version/correctness/complexity choices; no admitted exact proposition |
| `python3 -B Stage1_Instances/THM-M-0829/check_intake.py` | 1 | historical intake replay failed because its target-DAG-row fingerprint is stale against the current execution DAG; prior evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version` | 0 | pinned Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | pinned Lake version recorded above |
| pinned mathlib revision/tree and package status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0829/IntakeProbe.lean` | 0 | all ten generic interfaces elaborated; stdout SHA-256 `53ec55f57ef3da3fb2430a537fb6f7c09998176ba00b94070b7337846567f6a8`; empty stderr; no target declared |
| bounded Dinic/maximum-flow/blocking-flow/residual-network/level-graph Lean search | 0 | only the owned probe comment matched; no relevant pinned or repo-local declaration matched |
| publisher retrospective PDF request | 0 | endpoint returned a 261735-byte HTML document rather than a PDF; no source statement admitted |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | blocker identity, null target and imports, unchanged vector, four undefined mutations, false completion flags, and absent-self-test boundary agree |
| whitespace checks over both new blocker files | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first accept refreshed intake evidence. Accountable reviewers must then
preserve and hash a lawful immutable primary or approved authoritative source, select and
independently approve one exact Dinic/Dinitz root, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, graph/capacity/flow/residual/level/blocking-flow convention,
algorithm variant, output contract, cost model, boundary case, proof boundary, correction, and
erratum. They must explicitly reconcile the original, dynamic-tree, and specialized regimes with
the separate `THM-C-0098` wording.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.

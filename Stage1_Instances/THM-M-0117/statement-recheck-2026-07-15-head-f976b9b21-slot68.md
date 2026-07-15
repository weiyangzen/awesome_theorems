# THM-M-0117 statement recheck: blocked

Item: `S56-M-0117-STATEMENT`

Base revision: `f976b9b21418bfda4bc815ba2a7238e932666231` (tree
`6fbe6e3a73d5005115818a8f902da2b70f4aab24`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 68.

## Decision

The exact-statement gate remains blocked. The repository identifies only the
Moishezon theorem family, Boris Moishezon, the year 1966, and the gloss
"algebraicity of Moisezon manifolds." It gives no complete authoritative
statement, definition chain, ordered hypotheses, conclusion, theorem/page
locator, errata disposition, or independent source-mapping review. The
catalog's `verified` label is explicitly untrusted under rev-5.6.

The intake therefore froze only the provisional reading that every compact
complex Moishezon manifold is bimeromorphic to a projective algebraic variety.
Its README and source crosswalk require source disambiguation before this
phase. The sparse family name does not choose that algebraic-model reading over
the distinct result that a Moishezon manifold is projective if and only if it
is Kahler. It also leaves the domain, smoothness, connectedness,
irreducibility, algebraic dimension, algebraic-model category, analytification,
bimeromorphic comparison, and empty, singular, reducible, disconnected, and
dimension-zero conventions open. Choosing any of these would change the
proposition.

A fresh bounded source check clarified but did not close this ambiguity.
Modern papers state that a compact complex manifold is Moishezon exactly when
it is bimeromorphic to a projective manifold, equivalently when its algebraic
dimension equals its complex dimension; another paper separately states the
Kahler-projectivity theorem. These are useful secondary cross-checks, not an
authority for selecting the repository target. The original-source lead is
B. G. Moisezon, *On n-dimensional compact complex varieties with n
algebraically independent meromorphic functions*, DOI
`10.1090/trans2/063/02`. The AMS endpoint returned HTTP 403, so no complete
primary theorem passage or incorporated definitions were available.
Bibliographies also disagree between a part-I citation at pages 51-93 and a
broader citation at pages 51-177. A DOI and secondary descriptions cannot meet
the pinpoint source-identity gate.

No authoritative target input changed after the prior recheck was integrated.
The target manifest, repository source records, execution skill, guidelines,
intake dossier, legacy Lean module, toolchain, and dependency lock are
unchanged. The rev-5.6 blueprint and execution-DAG changes since base
`69f012f97` concern unrelated target states; their `THM-M-0117` projections are
byte-identical.

The pinned Lean closure also still lacks a faithful target surface: a global
meromorphic-function field and algebraic dimension for compact complex
manifolds, a complex analytic-space category, analytification, analytic
bimeromorphisms, and a Kahler-manifold interface. The owned
`StatementInfrastructure.lean` file re-elaborates only adjacent manifold,
one-variable meromorphic-function, transcendence-degree, scheme,
closed-immersion, properness, and Proj APIs. Its five imports are probe imports,
not a minimal import set for an absent canonical target.

The legacy `S1_M_037.lean` module also re-elaborates, but its
`MoishezonAnalyticData` stores decisive conditions as arbitrary propositions
and its algebraic comparison is only a carrier function. It has no
analytification or bimeromorphism. Reusing it would substitute an abstract
statement shape for the theorem and receives no statement credit.

Consequently no canonical Lean expression exists whose imports can be
minimized or whose expression and environment can be fingerprinted. Checked
transports and removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations remain undefined. Lifecycle stays `planned`, the root
vector stays `[H3, M4, R4]`, the statement node stays `[ ]`, and accepted
receipt IDs remain empty. No proof, audit completion, theorem completion, or
master acceptance is claimed. The prerequisite `S56-M-0117-INTAKE` is still
only provisional `[_]`.

## Pinned Lean Boundary

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
canonical `.lake` symlink was reused read-only. No update, build, clone, fetch,
or other dependency mutation was performed.

## Validation Record

Commands ran from this isolated worker clone unless another working directory
is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0117` | 0 | rank 37; planned; legacy slot `S1-M-037`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `Formalizations/Lean/.lake` symlink; base revision and tree match this record |
| scoped inspection and stable-input comparison from `69f012f97` to HEAD | 0 | stable target-authoritative inputs are unchanged; target blueprint/DAG projections are byte-identical |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0117/StatementInfrastructure.lean` | 0 | adjacent probe elaborated; stdout 27 lines/2,599 bytes at SHA-256 `49e1945f064d3269c83c696067b0d481fe645c97b2b13989952984a5b456394f`; empty stderr; no canonical target |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_037.lean` | 0 | legacy abstract module elaborated; stdout 118 lines/9,902 bytes at SHA-256 `93a87661f88e140e6a02fc5d60f312cf64cba76252dea1aa7f9cc44f5430c0a0`; empty stderr; no exact-target credit |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version`; `uname -m` | 0 | Lean `4.29.0`, Lake `5.0.0-src+98dc76e`, platform `x86_64` |
| mathlib package `git status --short`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean at the pinned revision and tree above |
| bounded exact-topic `rg` searches over pinned Lean dependencies | expected no root match | no Moishezon/Moisezon, bimeromorphism, algebraic-dimension, analytification, or complex-analytic-space root interface was located; generic meromorphic-field wording matched only unrelated one-variable/vertex sources |
| bounded retrieval and text inspection of arXiv `2407.02022v2`, `1901.10627v3`, and `math/0101019v6`; DOI endpoint check | 0 | secondary sources distinguish the two readings; AMS DOI endpoint returned HTTP 403; no authoritative exact target passage was obtained |
| prohibited-construct scan over target-owned Lean | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `external`, `implemented_by`, or `native_decide` occurrence |
| `python3 -m json.tool` and scoped `jq -e` assertions over the paired JSON | 0 | blocked identity, null target fields, four undefined mutations, unchanged vector, exact two-file scope, and no-self-test boundary agree |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; each no-index raw exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test is absent because the exact-statement deliverable did not pass |

## Retry Condition And Boundary

Retry only after the intake is master-accepted and accountable reviewers
preserve and approve one complete primary or approved-authoritative theorem
passage with its incorporated definitions, proof boundary, corrections, and
errata. They must select the bimeromorphic-model or Kahler-projectivity root
and settle every domain and boundary convention. The pinned closure must then
gain faithful analytic interfaces without storing the conclusion. A later
worker can encode only that approved claim, minimize imports, fingerprint the
elaborated expression and environment, compile every credited transport, and
distinguish all four required mutation classes.

This is fresh current-HEAD blocker evidence only. Because the positive
statement deliverable did not pass, `.stage1-worker-selftest.json` is
intentionally absent and no worker `[_]` or master acceptance is requested.

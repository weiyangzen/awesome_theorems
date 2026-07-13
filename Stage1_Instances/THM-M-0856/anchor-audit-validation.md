# THM-M-0856 anchor-audit validation

Item: `S56-M-0856-ANCHOR_AUDIT`

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d`

Base tree: `0d6c1fdf06d1573c256af331c6b198e5a787af43`

Validation date: 2026-07-13 (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains an exact
proof-bearing route. `SimpleGraph.tutte` states perfect-matching existence iff no vertex set is an
`IsTutteViolator`; unfolding that predicate and `not_lt` gives exactly the frozen deletion
inequality. `AnchorAudit.lean` checks this adapter at every universe and finite simple graph. The
offline checker also combines the statement and audit modules, fixes the same universe parameter,
unfolds the canonical, condition, and audit definitions in a checked
`TutteOneFactorTarget <-> AnchorAudit.ExactTarget`, and derives the canonical target
from the adapter. Thus no prose-only type comparison is credited.

The visible terminal body uses `not_isTutteViolator_of_isPerfectMatching` for necessity, then
contraposes sufficiency and splits on the parity of `Nat.card V`: `IsTutteViolator.empty` covers odd
order and `exists_isTutteViolator` covers even order. Lean reports the terminal and adapter
sorry-free. The terminal, its two principal direction declarations, and the adapter report exactly
`propext`, `Classical.choice`, and `Quot.sound`. A comment-aware source scan finds no prohibited
proof construct in either the adapter or pinned `Tutte.lean`.

This establishes a kernel-checked, `M0-W`-shaped route, but not legal current `M0-W`: rev-5.6
requires accepted release-grade `E1` for that status. Complete transitive provenance/trust/TCB
closure, immutable dependency archives, cold offline replay, proof-phase adoption/composition, and
master acceptance remain open. The root therefore stays `[H1, M3, R4]` with evidence classified
`node_local_below_E1`.

## External inventory

Bounded public search found one external exact-scope wrapper at
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its
`SimpleGraph.tutte_theorem` only wraps the same pinned mathlib direction and root declarations, so
it supplies no independent terminal body. The project is absent from the local dependency closure,
its immutable tree and source blob are resolved, and its CC BY-NC/no-training license requires
policy review. It is classified `M3` / `E3_source_anchor` and deliberately not integrated.

Repo-local search found only a cross-target Petersen intake probe of the same API. It transfers no
declaration, receipt, or proof credit. Formal-conjectures exact queries and historical Coq/Isabelle
phrase queries returned bounded zero results; a complete immutable formal-conjectures tree has
matching-cardinality support but no Tutte criterion. GitHub live code/tree APIs returned 401/403
and grep.app returned 429, so discovery saturation is not claimed. The packet records that
the recorded repo-local, pinned-mathlib, and public discovery preceded formal protocol publication;
the protocol then froze the final inventory append-only rather than rewriting that history.

## Commands and exact outcomes

Commands ran from the repository root unless a different working directory is shown.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0856` | 0 | rank 1410; planned; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | exact base revision and tree shown above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | mathlib pin/tree matched and its worktree was clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0856/AnchorAudit.lean)` | 0 | exact adapter and explicit target elaborated; terminal proof term printed; terminal and adapter sorry-free; four expected axiom reports; stdout SHA-256 `d1fd4f1e7b868f300491e4aa438688aa1b8b48cb4e1b749873d2207dd99e5f13` |
| `python3 -B Stage1_Instances/THM-M-0856/check_anchor_audit.py` | 0 | authority, pins, hashes, six-candidate inventory, terminal provenance, canonical combined fixture, and M3 boundary passed |
| `python3 -B Stage1_Instances/THM-M-0856/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | packet-bound replay passed |
| `python3 -m json.tool` over the protocol, audit, receipt, and root packet | 0 | all structured artifacts parsed |
| Python `ast.parse` on `check_anchor_audit.py` | 0 | checker parsed without writing bytecode |
| comment-aware prohibited-construct scan over `AnchorAudit.lean` and pinned `Tutte.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom/constant declaration, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide` found |
| repo-local, pinned-mathlib, installed-package, and immutable local-history searches recorded in the audit | 0/1 as appropriate | one distinct exact terminal body at the pin; no independent repo-local or installed-package body |
| Sourcegraph, GitHub REST, grep.app, immutable raw Atlas, formal-statement, and other-prover queries recorded in the audit | 0 at transport layer | bounded results, immutable revision/source hashes, and access failures recorded |
| `git diff --check -- Stage1_Instances/THM-M-0856 .stage1-worker-selftest.json` plus no-index checks for new files | 0 aggregate | no whitespace diagnostics |

No `lake update`, `lake build`, dependency clone/fetch, checkout, or `.lake` mutation was performed.

## Known failures

- The statement prerequisite and this node still require dependency-ordered master acceptance.
- Public discovery is bounded rather than exhaustive because code/tree APIs and grep.app blocked
  access; no saturation claim is made.
- The obligation registry, typed graphs, proof-phase composition, and E1 provenance/trust/TCB
  receipt are not frozen or accepted.
- Human-source H0, readable R0, hermetic replay, independent verification, deterministic release
  evidence, `AUDIT-Z`, and theorem completion remain open.

This completes only the assigned anchor-inventory and candidate-check work pending master
acceptance. It does not claim accepted M0, proof-phase completion, audit completion, or theorem
completion.

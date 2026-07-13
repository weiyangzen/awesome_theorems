# THM-M-0814 anchor-audit validation

Item: `S56-M-0814-ANCHOR_AUDIT`
Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675`
Inventory: `THM-M-0814-anchor-inventory/2`
Cutoff: `2026-07-13T22:12:00+08:00`

## Result

The exact repo-local artifact remains the proposition
`Stage1Instances.THM_M_0814.MaxFlowMinCutTarget`, so the root remains `M3`. The audit found no
network-flow or max-flow/min-cut declaration among the 7,871 library files at pinned mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, nor among all 9,676 materialized pinned-package Lean
sources. `Graph`, finite sums, `NNReal`, and generic compact-extremum APIs are useful substrate, not
a proof of flow-cut duality or the frozen extrema proposition.

The strongest public Lean 4 result located is
`NetworkFlow.max_flow_min_cut` in `facebookresearch/atlas-lean` at immutable commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its explicit proof gives a cut equal in value to an
already supplied directed `Real` flow with no augmenting path. It is not the frozen theorem: it
does not construct the flow or state maximum/minimum comparisons, uses vertex-pair capacities and
partition cuts rather than explicit undirected arcs and arbitrary disconnecting arc sets, and
cannot preserve parallel arc identities without a new representation proof. Its two terminal
modules replayed at their matching Lean/mathlib pins with standard axioms, but the project is not a
dependency, has no independent CI receipt at that commit, and carries a custom noncommercial/no-ML
license requiring accountable review. It is therefore `M3` support for this root, not `M1` or M0.
Atlas also contains a placeholder-free compactness proof body for flow existence in `Menger.lean`.
It was not isolated, elaborated, axiom-reported, or transitively audited here. Its module imports a
larger surface containing placeholder-tainted files, though this audit does not claim those
placeholders occur in the theorem's actual declaration closure. The same representation mismatch
remains, so the lead is not credited here.

CLRS-Lean at `4fc689e2...` is placeholder-free across the audited chapter-26 sources, but explicitly
partial, uses an incompatible Lean/mathlib pin, and supplies only nonexact directed-flow support.
Three projects are `M5`: the GitLab Lean 4 port has eight
`sorry` occurrences and no root theorem, while the amilchew and Zetagon Lean 3 developments have at
least seven and exactly seventeen active placeholders, respectively, and only nonexact conditional
statements. The formal-conjectures tree contains no matching path. Public index no-matches are
bounded; GitHub code search and grep.app were unavailable, so no exhaustive-discovery claim is made.
Raw per-query observation timestamps were not preserved; several aggregated query rows also lack
separately recorded HTTP status/count or Sourcegraph done/skipped/path bounds. Some replay commands
hash bodies without themselves parsing every summarized field. The candidate groups are semantically
classified, but complete discovery-protocol evidence, exhaustive discovery, audit completion, and
proof credit are therefore not claimed.

## Commands and results

All local Lean commands used the existing automation-provided `.lake` artifacts read-only. No
`lake update`, dependency build, clone, fetch, install, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all rework-required |
| `python3 scripts/stage1_target.py show THM-M-0814` | 0 | rank 1,373; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && LC_ALL=C LANG=C NO_COLOR=1 lake env lean ../../Stage1_Instances/THM-M-0814/Statement.lean` | 0 | exact target re-elaborated; stdout SHA-256 `91195081...683b` |
| `cd Formalizations/Lean && LC_ALL=C LANG=C NO_COLOR=1 lake env lean ../../Stage1_Instances/THM-M-0814/AnchorAudit.lean` | 0 | parameterized target-shape probe and eleven pinned support interfaces elaborated; the checker separately re-elaborates/fingerprints `Statement.lean`, and no equality transport from the probe is credited |
| exact-topic `rg` over all materialized pinned-package Lean source | 1 | expected no-match; empty output SHA-256 `e3b0c442...b855` |
| exact-topic and semantic `rg` over pinned mathlib library source | 1 | expected no-match; empty output SHA-256 `e3b0c442...b855` |
| Sourcegraph `maxFlowMinCut` and `max_flow_min_cut`, archived/forks included, Lean | 0 | four and three Atlas results; response SHA-256 `85a7c704...01df` and `d81bedcd...c615` |
| three quoted Sourcegraph phrase queries | 0 | zero matches; response hashes `f6b58e0e...a767`, `7bfef330...73e1`, and `85c19a8e...8850` |
| four GitHub repository searches | 0 | three complete zero results hash to `08c082fd...0b2`; `maxflow mincut Lean` found Zetagon with response `2855f82f...2333` |
| three GitHub code searches | 0 | HTTP 403 rate-limit/access blocker; response SHA-256 `1db366a2...386e`; no negative claim |
| five grep.app queries | 0 | HTTP 429 security checkpoint; response hashes recorded; no negative claim |
| immutable formal-conjectures recursive-tree query | 0 | 1,204 entries, not truncated, no matching paths; response SHA-256 `76fa3f96...c61` |
| immutable raw/API inspection of Atlas, CLRS-Lean, GitLab Lean 4, and two historical Lean 3 candidates | 0 | exact source, pin, placeholder, statement, trust, and integration boundaries recorded in `external-anchor-snapshot.json` |
| immutable raw inspection of CLRS-Lean `Section_26_6_MaxFlow_MinCut.lean:56-63` | 0 | SHA-256 `6b5769df...a4c`; 2,791 bytes and 66 lines; source signature and explicit body verified without claiming local elaboration |
| isolated temporary replay of the two exact Atlas terminal modules against Lean 4.29.0/mathlib `8a178...` | 0 | `flow_le_cut` and `max_flow_min_cut` elaborated; each reported `[propext, Classical.choice, Quot.sound]`; no repo dependency or source was installed |
| `python3 -B Stage1_Instances/THM-M-0814/check_anchor_audit.py` | 0 | target, inventory, pins, hashes, candidate classifications, receipt, worker packet, and false completion flags agreed |
| `python3 -m json.tool` on all owned JSON and the worker packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan | 0 | no forbidden declaration in the local audit probe; external placeholder findings agree with the ledger |
| `git diff --check -- Stage1_Instances/THM-M-0814 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This is a self-tested bounded anchor inventory pending dependency-ordered master acceptance. The
accepted vector remains `[H1, M3, R4]`. Source H0, a canonical obligation tree, exact proof bodies,
representation transports, composition, full provenance/trust/TCB closure, readable R0, hermetic
and independent validation, `AUDIT-Z`, release, and theorem completion all remain open.
The missing prescribed per-query evidence also remains a node-evidence blocker for master review.

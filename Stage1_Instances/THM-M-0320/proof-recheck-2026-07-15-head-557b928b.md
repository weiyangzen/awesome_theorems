# THM-M-0320 proof-phase recheck at 557b928b

Item: `S56-M-0320-PROOF`

Intent: `prove`

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

Base tree: `e677879a6eb4cb9d6795ba1bd78726af06ab9465`

## Verdict

`blocked`. A real new proof in `GraphBridgeProof.lean` closes the frozen
`M0320-T-GRAPH` interface at provisional worker-evidence level: upper hemicontinuity on a closed
Euclidean domain and closed correspondence values imply that the ambient correspondence graph is
closed. The exact root still has no unconditional proof body, so the proof item remains `[ ]` and
the theorem remains incomplete.

The accepted intake vector stays `[H1, M4, R4] -> [H1, M4, R4]`. The predecessor anchor and graph
artifacts provisionally record `M1`, but they do not contain the independently reproducible upstream
kernel receipt required for rev-5.6 `E2`. This worker therefore proposes no accepted classification
upgrade and does not rewrite the frozen registry or typed graphs.

## Checked Progress

`GraphBridgeProof.lean` imports `ObligationTree.lean` and proves the exact package

```text
Stage1Instances.THM_M_0320.upperHemicontinuityClosedGraphBridge :
  Stage1Instances.THM_M_0320.UpperHemicontinuityClosedGraphBridge
```

consumed by `root_of_closedGraph_packages`. The proof uses sequential closedness, coordinate
convergence, restriction of upper hemicontinuity to the domain subtype, and
`UpperHemicontinuousAt.mem_of_tendsto`. A fresh trust-zero replay reported only `propext`,
`Classical.choice`, and `Quot.sound`.

The tracked predecessor `Proof.lean` contains the same theorem name against standalone redeclarations.
`GraphBridgeProof.lean` is therefore a replacement candidate, not a module to co-import with that
predecessor. This blocked handoff leaves the tracked file unchanged to avoid an integration conflict;
the master lane must supersede it when accepting the imported-interface version.

The authoritative predecessor cut is `M0320-T-GRAPH` plus `M0320-C-CORE`. After the proposed local
graph delta, the remaining cut is `M0320-C-CORE`, with nested open integration obligation
`M0320-T-SUBTYPE`.

## Failed Gate And Retry

The first failed gate is `M0320-C-CORE`: neither the repository nor pinned mathlib contains a
licensed, exact-type, placeholder-free closed-graph Kakutani body. The audited
`harfe/fixed-point-theorems-lean4@11a9f041246d28374edae384241757f9a0cbd5e4` development is
substantive. A read-only scratch compatibility probe ported all six modules to pinned Lean 4.29 and
mathlib and all six elaborated, but its 3,253 upstream source lines have no located license grant and
the project is not a pinned dependency. Scratch work is not repository proof evidence and cannot be
lawfully vendored or credited.

The MIT-licensed `math-xmum/Brouwer@c02205edf347ad45f0d62db85497598ba2c4291e` lead proves only a
standard-simplex Brouwer theorem. Scratch probes showed that its Scarf module elaborates unchanged
and its separate Simplex module needs only one API rename, but it does not provide the arbitrary
compact-convex transport or set-valued Kakutani theorem needed by the frozen target.

Resume after a compatible licensed Brouwer/Kakutani development is pinned in the immutable
dependency closure, or after `M0320-C-CORE` and `M0320-T-SUBTYPE` are independently implemented
locally without placeholders. Then compose the exact root through `root_of_closedGraph_packages`.

## Validation

All validation reused the existing pinned Lake closure read-only. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed. Temporary source copies and oleans were
removed after the trust-zero replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0320` | 0 | Rank 686; lifecycle planned; theorem incomplete. |
| Isolated pinned-Lean trust-zero recipe below | 0 | `statement=0 obligation_tree=0 graph_bridge=0`; exact imported interfaces coexist and the new proof reports only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0320/check_obligation_tree.py` | 0 | 10 obligations and 22 typed edges passed; predecessor snapshot still reports the graph and core open. |
| Scoped prohibited-construct scan below | 1 | Expected no-match: no placeholder, axiom-like declaration, unsafe/external device, or computation override. |
| Scoped unconditional-root declaration scan below | 1 | Expected no-match: no false declaration of `KakutaniFixedPointTarget`. |
| `python3 -m json.tool` plus `jq` blocker-invariant assertions | 0 | JSON validity and item/theorem/base/blocked-state/open-root/empty-receipt/cut-set/changed-path/absent-self-test invariants passed. |
| Inline source-hash, base/tree, denominator, changed-path, and Markdown-marker assertions | 0 | All hashes and identities match; exactly the three recorded novel files changed; this record contains `THM-M-0320` and `blocked`. |
| Wrapped new-file `git diff --no-index --check` for all three artifacts plus scoped `git diff --check` | 0 | Each raw new-file diff returned expected exit 1 without a whitespace diagnostic; the scoped check passed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No proof-completion self-test manifest was emitted. |

The successful narrow Lean replay, run from the repository root, was:

```bash
set -u
tmp=$(mktemp -d Formalizations/Lean/.thm-m-0320-proof-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0320/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0320/ObligationTree.lean "$tmp/ObligationTree.lean"
cp Stage1_Instances/THM-M-0320/GraphBridgeProof.lean "$tmp/GraphBridgeProof.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 240 "$lean" --trust=0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean" --trust=0 \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean" --trust=0 \
  "$tmp/GraphBridgeProof.lean"
```

The source scans were:

```bash
rg -n '(^|[^[:alnum:]_])(sorry|admit|sorryAx|implemented_by|native_decide|unsafe|extern|external|run_tac)([^[:alnum:]_]|$)|^[[:space:]]*(axiom|constant|opaque)[[:space:]]' \
  Stage1_Instances/THM-M-0320/GraphBridgeProof.lean
rg -n 'theorem[[:space:]]+[^:]+:[[:space:]]*(Stage1Instances\.THM_M_0320\.)?KakutaniFixedPointTarget' \
  Stage1_Instances/THM-M-0320/GraphBridgeProof.lean
```

## Status Boundary

This is checked partial-proof and blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0320-PROOF`, authorize `[_]`, or claim audit, theorem, validation, release, or master
acceptance. Because the assigned proof phase is incomplete, `.stage1-worker-selftest.json` is
deliberately absent.

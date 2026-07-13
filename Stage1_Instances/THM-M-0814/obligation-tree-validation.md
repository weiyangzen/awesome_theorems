# THM-M-0814 obligation-tree validation

Item: `S56-M-0814-OBLIGATION_TREE`

Base revision: `27400857bccc93638c97e9c65859ddf5d5b5f4da`

Base tree: `3762537e0e5ae46cd70b086da49a69e2fd7b275c`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 33 unique obligations. The canonical ten-field projection has SHA-256
`f0ff554fe8facfa66bbdcbe9f036f7de20ebbe738b1d2cc9b4c06a899d673d7b`. The graph bundle stores
199 edges across separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. It includes 35 reciprocal proof-requirement pairs. Three parent interfaces have
named, exact conditional Lean composition certificates; fifteen deeper nonleaf relations are
explicitly marked unverified source-body decompositions and require future certificates.

The architecture follows Ford and Fulkerson's printed pages 400-402 while expanding work suppressed
by the paper: dependent-chain finiteness, coordinate transport, compact maximum attainment, convex
slack averaging, chain splicing and loop erasure, rerouting invariants, common orientation, the
left-arc construction, weak-duality double counting, and the exactly-once sum identity. No exact
Lean proof body was found or credited.

The validation reused only the automation-provided manifest-pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or other `.lake` mutation ran. The `.lake` symlink existed
before this task, so this is warm nonrelease evidence.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1,546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique ordered targets with ranks 1 through 1,546 passed |
| `python3 scripts/stage1_target.py show THM-M-0814` | 0 | rank 1,373; planned; L0/rework-required; theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `python3 Stage1_Instances/THM-M-0814/build_obligation_artifacts.py` | 0 | wrote 33 obligations and 199 typed edges; denominator `f0ff554f...3d7b` |
| repeat the generator and compare the three generated SHA-256 lines | 0 | `obligation-registry.json`, `typed-graphs.json`, and `validation-specs.json` were byte-identical |
| `python3 -B Stage1_Instances/THM-M-0814/check_obligation_tree.py` | 0 | deterministic artifacts, predecessor hashes, node schemas/anchors/ledgers, seven typed graphs, reciprocity, root reachability, plans, recipes, receipt, and false-completion boundary passed |
| `python3 -B Stage1_Instances/THM-M-0814/check_obligation_tree.py --run-lean` | 0 | temporary statement compilation and obligation elaboration passed with `--trust=0`; all three certificates were sorry-free; no `sorryAx`; output SHA-256 `e710c847...322a` |

`cutCertificate_compose`, `compose_root`, and `root_of_terminal` report only `propext`,
`Classical.choice`, and `Quot.sound`. Their substantive inputs remain named hypotheses. The check is
therefore composition evidence, not a theorem proof.

## Status boundary

This phase freezes architecture and validates conditional composition only. It accepts zero closed
obligations and leaves the root at `[H1, M3, R4]`. The predecessor statement and anchor audit and
this worker packet remain provisional pending dependency-ordered master acceptance. Primary-source
`H0`, exact proof bodies and `M0`, complete provenance/TCB, reviewed `R0`, hermetic replay,
independent verification, validation, release, `AUDIT-Z`, and theorem completion remain open.

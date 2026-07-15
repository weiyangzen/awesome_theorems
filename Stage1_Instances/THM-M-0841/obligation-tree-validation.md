# THM-M-0841 obligation-tree validation

Item: `S56-M-0841-OBLIGATION_TREE`

Base revision: `c93e664d3a7e0383b037cfa2d5e47ba14adfb2cb`

Base tree: `d8ea21a05ed52ff43d984128352a07f479aae6e6`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Frozen result

Registry version 2 freezes 53 unique obligations at denominator
`9e59690364fbc34301457900dd8ba573bce76a64a8dbeb9dca38d77e19953617`. The architecture follows
the visually inspected 1946 proof on printed pages 1087-1090: the set-family intersection lemma,
its two corollaries, the two-part high-degree base, the admissible-tolerance induction, rich-vertex
filtering, one-round and repeated deletion, and the final limiting contradiction. It separately
records the non-definitional sparse/dense complement bridge and the hidden same-part-size stability
needed on the final smaller graph.

Seven typed graphs contain 310 edges. The proof graph has 50 reciprocal requirement pairs, three
conditional composition certificates, and 25 explicitly unverified source-body decomposition
plans. All 48 required machine obligations are reachable from the root over closure-affecting proof
and refinement edges. All 53 ledgers have a stable step and a budget at most 100. No exact Lean
proof candidate is credited.

`ObligationTree.lean` elaborates exact `DenseClaim`, `DenseBase`, `DenseStep`, `DenseFamily`, and
`SparseFromDense` interfaces. Its five interface/composition declarations are sorry-free under `--trust=0`
and report only `propext`, `Classical.choice`, and `Quot.sound`. Because the three mathematical
products are explicit premises, these checks are composition evidence, not Erdos-Stone proof
evidence.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique ordered targets with ranks 1 through 1,546 passed |
| `python3 scripts/stage1_target.py show THM-M-0841` | 0 | rank 1,398; planned; L0/rework-required; theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `python3 -B Stage1_Instances/THM-M-0841/build_obligation_artifacts.py` | 0 | wrote 53 obligations, 310 typed edges, and 53 ledger steps; denominator shown above |
| repeat the generator and compare generated hashes | 0 | registry, graphs, specs, and readable tree were byte-identical |
| `python3 -B Stage1_Instances/THM-M-0841/check_obligation_tree.py` | 0 | authority hashes, schemas, denominators, ledgers, seven graphs, reciprocity, reachability, plans, recipes, receipt, and open status passed |
| `python3 -B Stage1_Instances/THM-M-0841/check_obligation_tree.py --run-lean` | 0 | temporary statement compilation and obligation elaboration passed with `--trust=0`; five declarations sorry-free; Lean output SHA-256 `2ec4662b...ae962` |
| JSON parsing, Python compilation with external pycache, scoped placeholder scan, and whitespace checks | 0 aggregate | structured files and Python parsed; no prohibited Lean construct or whitespace error |

The validation reused the automation-provided manifest-pinned Lake artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, or other `.lake` mutation ran.

## Status boundary

This phase freezes architecture and validates conditional composition only. It accepts zero closed
obligations and leaves the root at `[H1, M3, R4]`. The predecessor evidence and this worker packet
remain provisional pending dependency-ordered master acceptance. The dense base, induction step,
sparse/dense transport, all internal mathematical bodies, primary-source H0, transitive
provenance/TCB, reviewed R0, hermetic replay, independent verification, validation, release,
`AUDIT-Z`, and theorem completion remain open.

# THM-M-1065 obligation-tree validation

Item: `S56-M-1065-OBLIGATION_TREE`  
Base revision: `342d4f3073746c527586b3ea2818216ab631877c`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Frozen architecture

Registry version 1 contains 18 unique obligations. Sixteen are machine-required;
`M1065-X-SOURCE` and `M1065-X-PROVENANCE` are informational overlays and cannot earn proof
credit. The denominator digest is
`d5e21a3abc7d96576d5aeba4b8377a8ef8d92136b5ed448f9f28723f00d91ac2`.

The proof route keeps separate obligations for the common probability space, both families of
marginal laws and independence, event measurability, uniform positive constants, the quantitative
finite-block coupling, its maximal-tail upgrade, and exact witness composition. Separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs contain 75 reciprocal
typed edges. Every substantive node reaches the root in the proof graph, and every semantic ledger
has four steps, below the 100-step split threshold.

`ObligationTree.lean` kernel-checks only the exact equivalence between a named complete witness
package and the canonical ordered existential/conjunction shape. The equivalence is definitional;
it assumes no KMT result and constructs no coupling. All terminal proof-body IDs and closure
evidence remain empty.

## Commands and exact results

All Lean commands reused the existing pinned Lake closure. No dependency update, build, clone,
fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1065` | 0 | rank 507; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1065/build_obligation_artifacts.py` | 0 | built 18 obligations; printed the denominator digest above |
| `python3 Stage1_Instances/THM-M-1065/check_obligation_tree.py` | 0 | PASS; 18 obligations, 75 typed edges, open M4 root |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1065/ObligationTree.lean` | 0 | exact witness/root composition equivalence elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1065/Statement.lean \| sha256sum` | 0 | `4069871e37fe23a7b1fd1c4198307b8211e50dc521e78b1a2a9357f0d3472204  -` |
| `python3 -m json.tool Stage1_Instances/THM-M-1065/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1065/typed-graphs.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1065 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The printed-output hash is validation evidence for this run. The canonical expression fingerprint
remains the statement phase's explicit pretty-printed expression digest
`b257ceb188a0b84aab11fd389b5df322129c283dbc38f5c226900a4fec5cebd0`; these hashes intentionally
cover different byte streams.

## Status boundary

The obligation registry and typed architecture are self-tested pending master acceptance. No
obligation is closed. The conservative remaining root cut set is common-space construction,
finite-block KMT coupling, and the uniform maximal-tail upgrade. Root debt remains `M4`; primary
source pinpointing remains open at `H2`; readability remains `R4`. This packet does not claim H0,
M0, R0, audit completion, root closure, or theorem completion.

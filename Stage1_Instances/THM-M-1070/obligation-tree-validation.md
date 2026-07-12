# THM-M-1070 obligation-tree validation

Item: `S56-M-1070-OBLIGATION_TREE`  
Base revision: `4f1327c0201b7e64bed17be23fe9806cabf547e1`  
Validation date: `2026-07-12`

The registry was frozen from the exact statement and bounded anchor audit before recording closure.
It contains 13 stable obligations and separates proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. The proof graph has reciprocal `proof_requires` and `composes`
edges. The source and provenance nodes are non-proof overlays.

`ObligationTree.lean` checks only the exact conjunction transport. All six process clauses remain
explicit premises, so this phase does not prove that any arbitrary process is a Levy process. It
also supplies no existence theorem, cadlag modification, characterization, source acceptance,
audit completion, or theorem completion.

No dependency update, build, clone, fetch, or `.lake` mutation was run. Validation reused the
canonical pinned Lake dependency closure.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1070/build_obligation_artifacts.py` | 0 | wrote 13 obligations; denominator `c5866f4be491aa8209171938c78c36bde996941a27c87686d2a109d6679c5aa9` |
| `python3 Stage1_Instances/THM-M-1070/check_obligation_tree.py` | 0 | passed 13 obligations, 26 typed edges, denominator/hash/source checks, graph reciprocity and reachability, recipe coverage, closure boundary, and Lean hygiene |
| From the target directory, `LEAN_PATH=... lake env lean -o Statement.olean Statement.lean` | 1 | recorded environment limitation: no default Elan toolchain is configured |
| From `Formalizations/Lean`, `lake env lean -o ../../Stage1_Instances/THM-M-1070/Statement.olean ../../Stage1_Instances/THM-M-1070/Statement.lean` | 1 | recorded expected Lean root restriction: output source is outside the Lake package root |
| `LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)` followed by target-local `LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) "$LEAN_BIN" -o Statement.olean Statement.lean` and `LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) "$LEAN_BIN" ObligationTree.lean` | 0 | exact pinned Lean executable and Lake-derived dependency path elaborate the statement and conditional composition; axiom output is `propext`, `Classical.choice`, `Quot.sound`; temporary `Statement.olean` removed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1070/Statement.lean` | 0 | canonical statement independently elaborates through the requested pinned `lake env lean` surface |
| `python3 -m json.tool` on the registry, graph bundle, and validation specs | 0 | all structured artifacts are valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1070` | 0 | rank 512, planned lifecycle, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1070 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Closure boundary

The local conditional composition and the previously frozen definition are the only provisionally
checked nodes. Root debt remains `M3`; root, audit, and theorem completion are false. The first
critical open cut is `M1070-L-INDEPENDENT`, `M1070-L-STATIONARY`, and
`M1070-L-STOCH-CONT`. There is no accepted receipt; master acceptance is still required.

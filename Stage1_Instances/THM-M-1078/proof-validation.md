# THM-M-1078 proof-phase validation

Item: `S56-M-1078-PROOF`  
Date: `2026-07-15` (`Asia/Shanghai`)  
Base revision: `fb0fd5be494d0813177dbdc959ec911d69a72015`

## Implemented Body

`Proof.lean` closes the documented semantic obligation `M1078-T-ALLTIME`: for every
`1 < p < infinity`, terminal `MemLp (f n) p mu` for a real martingale implies
`MemLp (f k) p mu` at each `k <= n`. The proof first establishes general-exponent `MemLp`
preservation by conditional expectation using conditional Jensen for
`x |-> norm x ^ p.toReal`, then applies the martingale conditional-expectation identity.

Both declarations are placeholder-free and elaborate in the pinned environment. Their axiom
reports contain only `propext`, `Classical.choice`, and `Quot.sound`.

## Open Boundary

The exact root remains open at `M2`; no theorem-completion claim is made. The frozen
`ObligationTree.EarlierMemLpBridge` does not match the documented obligation: it concludes
`forall k, MemLp (f k) p mu`, including future times, instead of restricting to `k <= n`.
That stronger proposition is false in general, so the existing conditional root composition cannot
truthfully consume this body. A valid integration must use a process stopped at horizon `n` or
repair the conditional interface without changing the exact canonical root.

The external Burkholder body at `SmaniaD/Burkholder@afa97ef3...` is still absent from the pinned
dependency closure. Its source is approximately 980 KB across seven Lean files and targets a newer
Lean/mathlib revision. Prior scratch compilation under the pinned toolchain reached only the small
base, definitions, and `p = 2` modules; compiling a 444 KB majorant leaf was killed with exit 137
under the shared worker load. No such scratch artifact receives proof credit. The external pin,
horizon specialization, indexing, predictability, pointwise-to-a.e. bound, norm conversion, local
body, and final assembly remain open.

## Commands And Results

All commands ran in this worker clone using existing pinned Lake artifacts. No update, build,
dependency clone/fetch, or `.lake` mutation command was run.

| Command | Exit | Exact result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean --trust=0 -j1 -t0 ../../Stage1_Instances/THM-M-1078/Proof.lean` | 0 | both declarations elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean --trust=0 -j1 -t0 ../../Stage1_Instances/THM-M-1078/Statement.lean` | 0 | exact canonical statement and checked expansion transport elaborated |
| `python3 Stage1_Instances/THM-M-1078/check_obligation_tree.py` | 0 | frozen 15-obligation registry and typed graph bundle passed; pre-proof closure record remains open `M2` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1078` | 0 | rank 520; planned; L0/rework-required; theorem incomplete |
| forbidden-mechanism scan over `Proof.lean` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom/constant/unsafe declaration, oracle, or native-decision shortcut |
| `python3 -m json.tool Stage1_Instances/THM-M-1078/proof-receipt.json` | 0 | receipt JSON valid |
| `python3 Stage1_Instances/THM-M-1078/check_proof.py` | 0 | proof source, exact documented obligation, receipt hashes, axiom boundary, and open root status passed |
| `git diff --check -- Stage1_Instances/THM-M-1078 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status Boundary

This is self-tested, narrowly scoped partial proof progress for one registered semantic obligation,
pending master acceptance. It does not close the assigned proof node as a whole, the frozen proof
graph, or the exact target. `audit_complete` and `theorem_complete` remain false, and downstream
validation and release remain open.

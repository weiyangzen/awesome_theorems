# THM-M-0387 obligation-tree validation

Item: `S56-M-0387-OBLIGATION_TREE`  
Base revision: `44787231d810c8c0b31ab931e5c64f0f46fc26f6`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The validator parsed the frozen registry and graph bundle, required the full
rev-5.6 node schema, recomputed the denominator digest, checked one-to-one
registry/node identities, checked all seven graph types and reciprocal edge
indexes, rejected duplicate edges, and proved the combined proof/refinement
graph acyclic and root-reaching for all 121 required mathematical obligations.
There are 132 inventory obligations and 140 typed edges. Eleven `M0387-X*`
trust/provenance overlays are informational and cannot contribute proof credit.

The exact statement also re-elaborated under the pinned Lean toolchain. The
pre-existing untracked `Formalizations/Lean/.lake` artifact was reused and not
modified. No `lake update`, build, clone, fetch, or dependency mutation ran.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0387` | 0 | rank 1, planned, L0/rework-required, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0387/Statement.lean)` | 0 | exact target, checked identity transport, and boundary counterexamples elaborated |
| `python3 Stage1_Instances/THM-M-0387/check_statement.py` | 0 | four statement mutations killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0387/check_obligation_tree.py` | 0 | `PASS THM-M-0387 obligation tree: 132 obligations, 140 typed edges`; denominator `e934e59a...b36643`; root open M2 |
| `python3 -m json.tool Stage1_Instances/THM-M-0387/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0387/typed-graphs.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0387 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Content hashes after validation:

```text
60dde2360bacfdb05eabc88888831a67288ed3fb3e5c08e39f4364521c056f55  obligation-registry.json
6cd9a640ddcd34a23d88945bc2fde0236cb4fb09b0e9adc639bfc42eb1a100a4  typed-graphs.json
```

## Status boundary

This self-tests only the architecture freeze. Planned fingerprints are not
elaborated declarations, leaf budgets are not proof closure, and no historical
machine status is readmitted. No proof body, composition certificate, H0/R0
review, audit completion, or theorem completion is claimed. Master acceptance
is still required for the assigned scheduler item.

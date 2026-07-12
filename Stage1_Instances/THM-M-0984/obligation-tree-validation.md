# THM-M-0984 obligation-tree validation

Item: `S56-M-0984-OBLIGATION_TREE`  
Base revision: `2de0044343af8f82cca8ea26dad293408d609a39`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The registry freezes ten obligations before proof-phase credit is observed.
Its canonical projection hashes to
`7869ad0637404b744050b4cf6ded4d80ae7403c59158fea2f9aea2b8f48a1d92`.
The graph bundle contains seven separately typed graphs and fifteen edges;
every edge endpoint belongs to the registry, every proof edge has a reciprocal
composition edge, and every semantic step budget is at most 100.

`ObligationTree.lean` checks the exact root type and conditional composition
from `TerminalStrongLaw` to `Root`. The terminal is an explicit premise, so no
deep theorem body or obligation is credited by this phase. Lean reports
`propext`, `Classical.choice`, and `Quot.sound` for the composition certificate.
The root remains open at M3 with `M0984-L-TERMINAL` as the machine cut set;
the distinct Borel-versus-modern source issue remains H1.

## Commands and exact outcomes

All commands ran in this worker clone. No dependency update, build, clone,
fetch, or `.lake` mutation was performed.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0984/build_obligation_artifacts.py` | 0 | built 10 obligations; emitted denominator `7869ad0637404b744050b4cf6ded4d80ae7403c59158fea2f9aea2b8f48a1d92` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1..1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0984` | 0 | rank 264, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0984/check_obligation_tree.py` | 0 | 10 obligations and 15 typed edges passed; root reported open |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0984/ObligationTree.lean` | 0 | exact composition elaborated; axiom report was `propext`, `Classical.choice`, `Quot.sound` |
| `python3 -m json.tool Stage1_Instances/THM-M-0984/obligation-registry.json >/dev/null` | 0 | registry JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0984/typed-graphs.json >/dev/null` | 0 | graph JSON parsed |
| forbidden-token scan over obligation Lean and structured artifacts | 1 | expected ripgrep no-match; no `sorry`, `admit`, bodyless axiom, or `sorryAx` found |
| `git diff --check -- Stage1_Instances/THM-M-0984 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

## Status boundary

This phase is self-tested pending master acceptance. It freezes architecture
and checks conditional composition only. It does not claim proof closure,
source resolution, validation or release completion, or theorem completion.

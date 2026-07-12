# Statement validation record

Base revision: `b781ef440e9de69e6413b608ce5542eed8c0070e`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passes: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0989/Statement.lean` | 0 | Exact target and `statement_iff` elaborated with no diagnostics |
| `cd Formalizations/Lean && lake env lean --deps ../../Stage1_Instances/THM-M-0989/Statement.lean` | 0 | Direct project dependency is the pinned `Mathlib/Probability/CentralLimitTheorem.olean` plus Lean `Init.olean` |

The command was run from the Lean project because the repository root has no Lake project context.
The worker reused the canonical `.lake` symlink and did not update or fetch dependencies.

The frozen boundaries are deliberate: `Fin (n + 1)` excludes empty rows; per-row variance equals
one, so no zero normalizer appears; the truncation test is strict and only positive thresholds are
quantified; and the conclusion uses the standard Gaussian distribution interface. The converse,
Feller-negligibility equivalence, unnormalized scaling formulation, and variable row lengths are
not alternate claims of this node. `statement_iff` checks only the transparent presentation of the
selected target. No theorem proof or later-phase completion is claimed.

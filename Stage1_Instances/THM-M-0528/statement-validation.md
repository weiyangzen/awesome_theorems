# Statement validation record

Item: `S56-M-0528-STATEMENT`  
Base revision: `8957e7b8e92faa5c99376c8f291502ea568a7271`.

## Frozen target

`Stage1Instances.THM_M_0528.CoveringLiftUniquenessTarget` selects the general uniqueness theorem
for lifts: continuous lifts from a preconnected domain that have equal projections and agree at
one specified point are equal. This is the exact shape identified as Proposition 1.34 by the
pinned `Mathlib.Topology.Covering.Basic` source. It is neither path-lift existence nor analytic
uniformization. The only direct import is that Basic module.

The checked theorem
`coveringLiftUniquenessTarget_iff_pointwiseProjectionEncoding` transports between equality of the
two composites and pointwise equality of their projections. Primary-source page and errata
acceptance remains downstream; this node freezes the formal target without claiming `H0` or proof
closure.

## Commands and results

Commands ran in this worker clone on 2026-07-12. Lean ran from `Formalizations/Lean` against the
existing pinned `.lake` artifact; no update, fetch, build, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0528/Statement.lean` | 0 | canonical target, pointwise transport, four mutations, pinned API check, and explicit target print elaborated |
| `python3 ../../Stage1_Instances/THM-M-0528/check_statement.py` | 0 | expression SHA-256 `722b820b9322f8eba435ecaad4432c680f6301bad55f585aa73c60878ad40376`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0528/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `0011468a...1378`, `651c8acc...b1d2`, and `321626c8...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0528` | 0 | rank 585, planned, L0/rework-required, theorem incomplete |

The mutations remove preconnectedness, remove continuity of the second lift, remove the initial
agreement, or replace global equality by agreement only at the witness. They elaborate as distinct
propositions and are rejected by the expression comparison. This is statement-only evidence
pending master acceptance; dependent anchor, obligation, proof, validation, and release nodes stay
open.

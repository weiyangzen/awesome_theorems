# Statement validation record

Item: `S56-M-1171-STATEMENT`  
Base revision: `54743c8a753017ec2ce50ffebf85facec9112b95`.

## Frozen target

`Stage1Instances.THM_M_1171.CalderonZygmundEstimateTarget` fixes the whole-space scalar estimate on
`Fin n -> Real`, with product Lebesgue volume, `1 <= n`, `1 < p < infinity`, and one nonnegative
constant quantified before all smooth compactly supported functions. The Hessian is the second
Frechet derivative with its operator norm; the Laplacian is its standard-coordinate trace.
`calderonZygmundEstimateTarget_iff_expandedTarget` checks the fully expanded encoding by definitional
equality. This node does not prove the estimate.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned environment. No dependency
update, fetch, build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1171/Statement.lean` | 0 | target, definitions, definitional transport, and four mutations elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1171/check_statement.py` | 0 | expression SHA-256 `94cb9c63...2fd8`; all four structural mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1171/Statement.lean lean-toolchain lake-manifest.json` | 0 | `8fbc3048...5ae3`, `651c8acc...b1d2`, `321626c8...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1171` | 0 | rank 372, planned, theorem incomplete |

The mutations remove the dimension boundary, include `p = 1`, allow the constant to depend on the
function, or reverse the inequality. They are separately elaborated propositions and compare unequal
to the explicit kernel rendering of the root. This is statement-only evidence pending master
acceptance; source, anchor, proof, validation, and release gates remain open.

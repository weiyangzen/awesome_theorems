# Statement validation record

Item: `S56-M-0342-STATEMENT`  
Base revision: `bd0d227173ac95971603f633607751754850337e`

## Frozen target

`Stage1Instances.THM_M_0342.PlancherelTarget` quantifies over every finite dimension `n`, every
complex-valued representative `f` on `EuclideanSpace Real (Fin n)`, and its explicit
square-integrability witness `hf`. Its conclusion is exactly the equality of the `L2` norms of
`hf.toLp f` and mathlib's normalized `L2` Fourier transform of that class. The zero-dimensional
case is included. No inner-product, inversion, or surjectivity formulation receives statement
credit here.

The sole direct import is `Mathlib.Analysis.Fourier.LpSpace`. This is the narrow mathlib module that
defines the `L2` Fourier-transform instance and norm-isometry API. Existing pinned `.lake`
artifacts were used read-only; no update, build, clone, or fetch was run.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0342/Statement.lean` | 0 | target and four mutations elaborated; 33,441-byte explicit target expression printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0342/check_statement.py` | 0 | expression SHA-256 `b1a203...93e0e`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0342` | 0 | rank 835, planned, theorem incomplete |
| `python3 -m json.tool` on `statement.json` and `statement-receipt.json` | 0 | both records are valid JSON |
| placeholder/axiom scan of owned Lean files | 1 (expected) | no prohibited declaration or placeholder matched |
| `git diff --check -- Stage1_Instances/THM-M-0342` | 0 | no whitespace errors |

The mutations remove square-integrability, fix the domain to `Real`, change the function binder
from universal to existential, and exclude dimension zero. They elaborate as propositions but have
distinct fully explicit expressions, so none can silently replace the canonical target.

This is statement-only evidence pending master acceptance. The intake's primary-source pinpoint
remains unresolved, so this freezes the exact repository claim rather than asserting `H0` fidelity
to Plancherel's 1910 formulation. All downstream nodes and theorem completion remain open.

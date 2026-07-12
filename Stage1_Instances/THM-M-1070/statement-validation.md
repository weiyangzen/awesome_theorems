# Statement validation

Item: `S56-M-1070-STATEMENT`  
Base revision: `342d4f3073746c527586b3ea2818216ab631877c`  
Validation date: `2026-07-12`

The exact predicate `Stage1Instances.THM_M_1070.IsLevyProcess`, its clause-by-clause expansion,
checked definitional transport, and four deliberately changed statement shapes elaborate using the
existing pinned Lake closure. No dependency update, build, clone, or fetch was run.

The two direct imports are minimal for the exposed names. Removing
`Mathlib.Probability.Independence.Process.HasIndepIncrements` makes `HasIndepIncrements` unknown;
removing `Mathlib.Probability.IdentDistrib` makes `IdentDistrib` unknown. The latter transitively
provides `TendstoInMeasure`, so its separate direct import was removed after a successful check.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1070/Statement.lean` | 0 | exact target printed; no errors or warnings |
| import-removal probe for `HasIndepIncrements` | 1 | expected failure: unknown identifier `HasIndepIncrements` |
| import-removal probe for `IdentDistrib` | 1 | expected failure: unknown identifier `IdentDistrib` |
| `python3 -m json.tool Stage1_Instances/THM-M-1070/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1070/statement.json` | 0 | valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1070` | 0 | rank 512; L0/rework-required; planned; theorem incomplete |

## Statement boundary

This phase resolves the intake's formal encoding choices by selecting real-valued, unfiltered
processes on `NNReal`. It preserves joint rather than pairwise increment independence, includes
zero and repeated endpoints, uses almost-everywhere zero initial value, and does not silently assume
cadlag paths. The repository discovery phrase remains insufficient for `H0`: primary-edition
pinpointing, errata review, and independent source review remain open. The later proof phase must
select and prove a substantive source-backed regularization or characterization theorem; elaborating
this predicate alone supplies no root proof credit.

Status: statement self-tested, pending master acceptance; `audit_complete=false` and
`theorem_complete=false`.

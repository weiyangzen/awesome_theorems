# THM-M-0125 statement-phase blocker

Item: `S56-M-0125-STATEMENT`  
Base revision: `0fbea98f22accf2fd584a6e4691acc4d09519209`

## Verdict

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The accepted intake leaves
the source variant and normalization unresolved: Gross and Zagier (1986) contains multiple
formulations, while the repository metadata says only "elliptic-curve derivative formula." No
locally available primary-source scan, immutable source hash, theorem/page selection, transcription
of the ordered binders, or errata record selects one of those formulations.

Choosing an elliptic-curve, newform/Rankin-series, or Jacobian formulation at this point would add
mathematics not fixed by the source record. The same ambiguity affects the central point, completed
versus imprimitive L-series, Heegner hypotheses, height convention, and every period, degree,
discriminant, unit-index, conductor, and local factor in the equality. Consequently a minimal
import set cannot be certified for an exact target.

The legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_044.lean` elaborates with the pinned toolchain, but
it is not the requested target. Its principal `GrossZagierStatementData.expectedFormula` accepts a
generic complex derivative, height value, normalization factor, and bundled proposition as stored
data. This does not encode the arithmetic L-series, Heegner point, canonical height, or exact source
normalization and receives no statement credit here.

First failed gate: exact-source-statement identification. The statement node remains open with
machine status `M4`; no canonical declaration, expression fingerprint, checked transport, or
theorem-completion evidence is claimed. Reopen the node only after an immutable primary source is
available and one theorem or corollary is selected with a page locator, exact transcription,
convention ledger, and errata audit.

## Commands and results

All commands ran in this worker clone. The Lean commands used the already materialized pinned Lake
environment; no dependency state was changed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard projection passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0125` | 0 | Rank 44, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_044.lean` | 0 | Legacy abstract interface elaborated; this is negative boundary evidence, not exact-target evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_044.lean` | 0 | SHA-256 values `651c8a...1d2`, `321626...d81`, and `30198b...f52` respectively |

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked rather
than self-tested.

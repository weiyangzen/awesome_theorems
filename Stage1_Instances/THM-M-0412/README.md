# THM-M-0412 Intake Dossier

## Status

- Lifecycle: `planned`
- Baseline: `L0 / rework_required`
- Intake item: `S56-M-0412-INTAKE`
- Audit complete: no
- Theorem complete: no
- Provisional root vector: `H5 / M4 / R4`

This dossier freezes only the metadata-level scope discoverable in the repository. The source does
not identify an exact theorem. In particular, the label "Pierce conjecture", attribution to Trygve
Nagell, year 1948, and gloss "integer points on certain cubic curves" do not uniquely determine a
claim. No convenient Nagell-Lutz or Markov-equation theorem is substituted for it.

## Frozen Intake

| Field | Value |
|---|---|
| Theorem ID | `THM-M-0412` |
| Execution rank | 21 |
| Legacy slot | `S1-M-021` (discovery only) |
| Repository name | `皮尔斯猜想` (Pierce conjecture) |
| Repository attribution | Trygve Nagell |
| Repository year | 1948 |
| Repository gloss | Certain cubic curves' integer points |
| Category | Number theory / Diophantine equations |
| Target system | Lean 4 + mathlib |
| Lane | `hard_mathlib_anchor_and_wrapper` |

The domains, curve equation or family, quantifier order, hypotheses, conclusion, boundary cases,
primary-source theorem number, and primary-source page are all unresolved. Consequently the exact
canonical Lean target, universe profile, foundation/TCB profile, and computation profile remain open
for the statement phase.

## Intake Boundary

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_021.lean` is discovery input only.
Its abstract `NagellLutzBranchData` predicates and conditional `StatementShape` neither identify nor
prove the source theorem. Its narrative identity correction has no primary-source evidence in the
repository, so it receives no rev-5.6 statement or proof credit.

See [scope-map.md](scope-map.md) and [source-statement-crosswalk.md](source-statement-crosswalk.md).

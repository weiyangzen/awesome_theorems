# Statement validation record

Item: `S56-M-0452-STATEMENT`  
Base revision: `350ffc25f193b3d2ac0fcc9f4d760879cfae0f58`

## Frozen target

`Stage1Instances.THM_M_0452.NeronTatePairingTarget` is the exact target selected by the intake. It
quantifies over an elliptic Weierstrass curve over every number field. The package retains the
normalized canonical-height limit and comparison, the one-half polarization, symmetry, additivity
and integer scalar laws in both arguments, the self-pairing identity, nonnegative diagonal and
torsion kernel, and a positive-definite pairing on the quotient by `AddCommGroup.torsion`.

The only direct imports are `Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point` and
`Mathlib.NumberTheory.Height.NumberField`. The structure declares the proposition to be proved; no
value inhabiting it is supplied.

## Commands and results

All commands ran in this worker clone. Lean reused the existing canonical `.lake` symlink; no
dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0452/Statement.lean` | 0 | exact target, four mutations, quotient encoding, and identity convention elaborated; explicit target printed |
| `python3 Stage1_Instances/THM-M-0452/check_statement.py` | 0 | expression SHA-256 `c57affc6c695e804883b40a8d9ad148b9fdb19a42bfac04e5f9b68acee7198d9`; all mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0452/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `5098fa...4bff`, `651c8a...b1d2`, and `321626...5b2d`, matching `statement.json` |
| `python3 -m json.tool Stage1_Instances/THM-M-0452/statement.json >/dev/null` | 0 | statement JSON parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard projection passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-0452` | 0 | rank 301, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)' Stage1_Instances/THM-M-0452 -g '*.lean'` | 1 | expected no-match result; no prohibited Lean declaration |
| `git diff --check -- Stage1_Instances/THM-M-0452 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The validator distinguishes removal of the number-field domain, a changed polarization factor,
restriction from integer to natural scalars, and omission of the positive-definite torsion
quotient. These are statement-identity checks, not claims that the mutations are mathematically
false.

This is statement-only evidence pending master acceptance. The theorem remains unproved and
incomplete; all later phases and theorem-completion gates remain open.

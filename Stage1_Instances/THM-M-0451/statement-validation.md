# Statement validation record

Item: `S56-M-0451-STATEMENT`  
Base revision: `a447e0707c423654e3a2bcc5258f7b314cb70a64`

## Frozen target

`Stage1Instances.THM_M_0451.NeronTateCanonicalHeightTarget` is the exact package selected by the
intake dependency. It quantifies over an elliptic Weierstrass curve over an arbitrary number field.
Its `Nonempty` conclusion retains the normalized limiting formula, uniform bounded comparison with
half the projective x-height, quadraticity for all integer scalars, the parallelogram law,
nonnegativity, and the torsion iff zero-height kernel. The point at infinity is handled by mathlib's
checked `xRep = [1, 0]` convention.

The only direct imports are `Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point` and
`Mathlib.NumberTheory.Height.NumberField`. The structure declares the proposition to be proved; no
value inhabiting it is supplied.

## Commands and results

All commands ran in this worker clone. Lean used the existing canonical `.lake` symlink; no
dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0451/Statement.lean` | 0 | exact target, four mutations, and identity convention elaborated; explicit target printed |
| `python3 Stage1_Instances/THM-M-0451/check_statement.py` | 0 | expression SHA-256 `76392071dc0670ad9c58f8eabc2195eecd990545084cfce9d6ecb13696803ed8`; all mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0451/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `f288b8...6c52`, `651c8a...b1d2`, and `321626...5b2d`, matching `statement.json` |
| `python3 -m json.tool Stage1_Instances/THM-M-0451/statement.json >/dev/null` | 0 | statement JSON parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard projection passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-0451` | 0 | rank 93, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0451` | 0 | no whitespace errors |

The validator distinguishes removal of the number-field domain, restriction from integer to
natural scalar quadraticity, weakening the torsion equivalence, and omission of the defining
limit. These are statement-identity checks, not claims that the mutations are mathematically false.

This is statement-only evidence pending master acceptance. The theorem remains unproved and
incomplete; all later phase evidence remains open.

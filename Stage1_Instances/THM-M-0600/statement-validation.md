# Statement validation record

Item: `S56-M-0600-STATEMENT`  
Base revision: `f81c1e19458336143e9cf1179bdb9eb3121566b2`

## Frozen target

`Stage1Instances.THM_M_0600.MorseLemmaTarget` freezes the finite-dimensional, boundaryless real
smooth-manifold claim from intake. A `SmoothLocalCoordinates` witness contains only a local smooth
equivalence centered at the point, never the requested normal-form equality. Criticality and Hessian
nondegeneracy are computed in an arbitrary centered base coordinate system. The conclusion produces
new centered smooth coordinates and exact equality throughout their open target neighborhood.

The negative directions are precisely the coordinates `i < index`, with `index <= n`. Thus dimension
zero, index zero, and index `n` are not silently excluded. The sole direct import is
`Mathlib.Geometry.Manifold.ContMDiff.NormedSpace`.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned Lake artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0600/Statement.lean` | 0 | target, checked definitional transport, and four structural mutations elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0600/check_statement.py` | 0 | expression SHA-256 `6ba927d7712fa05ea04ff656eefe32d16a57a2c45f4aa49a30695b263b04911d`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0600/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `40dced...97dc`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |

This is statement-only evidence pending master acceptance. It supplies no proof and does not advance
anchor-audit, obligation-tree, proof, validation, or release nodes.

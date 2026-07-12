# Statement validation record

Item: `S56-M-1056-STATEMENT`  
Base revision: `8f25592ee68e5a24d7d50cc5785bd684414fc8ac`

`Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget` freezes the exact intake-selected
finite-dimensional real invertible ergodic-cocycle variant. Measurable complementary projections
encode the direct-sum subspaces and make equivariance and simultaneous vector growth explicit.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1056/Statement.lean` | 0 | canonical target, splitting package, and four mutations elaborated; explicit target printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-1056/check_statement.py` | 0 | expression SHA-256 `8e1a96a304ce3dd43838f934406d58ac3594b9d34c6e1617461abc17e65d403b`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1056/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match `statement.json` |

The mutations remove inverse integrability, change the scalar domain, alter cocycle binder scope,
and admit the excluded zero-dimensional boundary. This evidence elaborates only the proposition; it
does not prove Oseledets or advance any dependent node.

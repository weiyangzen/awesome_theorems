# Statement validation record

Item: `S56-M-0112-STATEMENT`  
Base revision: `0f142dc81233343d6cad44f3c6dfbe9240e15606`

## Frozen target

`Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget` freezes the selected weak topological
Lefschetz claim. The target quantifies over connected smooth complex projective ambient data and a
smooth hyperplane-section inclusion with a compatible basepoint. It requires the inclusion-induced
map on `HomotopyGroup.Pi k` to be bijective for `k < n - 1` and surjective for `k = n - 1`.

The sole direct import is `Mathlib.Topology.Homotopy.HomotopyGroup`. The pinned snapshot does not
provide complex analytification or a canonical algebraic hyperplane-section predicate. The local
`LefschetzHyperplaneData` therefore types those missing interface propositions and the induced map;
it does not contain any injectivity, surjectivity, or weak-Lefschetz conclusion. Native future APIs
will require checked transports and receive no credit from this statement node.

## Commands and results

All commands ran inside this worker clone. Lean ran from `Formalizations/Lean` with the existing
pinned Lake environment; no dependency was fetched, updated, or built.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0112` | 0 | rank 35, planned, L0/rework-required, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0112/Statement.lean` | 0 | exact target, `Iff.rfl` expansion, four mutation fixtures, and explicit expression elaborated |
| `python3 Stage1_Instances/THM-M-0112/check_statement.py` | 0 | expression SHA-256 `1daee7f6d7814d04bb7cefe87b3487fc78a862bedafbf8dc283bd6cf1a5eb654`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0112/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `35bd5c...2dff`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 -m json.tool Stage1_Instances/THM-M-0112/statement.json >/dev/null` | 0 | structured statement artifact is valid JSON |
| forbidden-term scan of `Statement.lean` and `check_statement.py` | 1 | no `sorry`, `axiom`, `admit`, or `placeholder` token found; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-0112 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation and boundary record

The validator separately elaborates and serializes mutations that remove projectivity, change the
dimension comparison domain from truncated naturals to integers, move the degree binder outside the
geometric data and retain only a fixed-degree conclusion, and require bijectivity at the boundary.
None serializes to the canonical expression. These are structural statement-kill checks, not proofs
that every broadened mathematical mutation is false.

Natural subtraction is frozen intentionally. At complex dimension zero or one, `n - 1 = 0`, so the
strict lower range is empty and the boundary assertion is surjectivity on `pi_0`. At larger
dimensions, bijectivity stops strictly below `n - 1`; the boundary receives only surjectivity.

This is statement-only evidence pending master acceptance. The theorem remains unproved and
incomplete; anchor audit, obligation tree, proof, full validation, and release phases remain open.

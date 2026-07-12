# Exact-statement gate: blocked

Item: `S56-M-1281-STATEMENT`  
Theorem: `THM-M-1281`  
Base revision: `6bcd5f977dc26298be5f77327a2616e726454eb7`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the name "Aubin theorem", the year 1976, and the gloss "Yamabe problem
(non-conformally-flat)". The accepted intake dependency deliberately labels its strict
Yamabe-constant comparison as provisional and leaves the primary-source theorem and page
unselected. A bibliographic candidate is identified, but its exact statement has not been
inspected and frozen.

The missing source choices affect the proposition itself:

- whether the root is a strict comparison with the round sphere, attainment of the Yamabe
  functional, existence of a constant-scalar-curvature conformal metric, or a combined result;
- the dimension threshold and whether the result is stated dimension by dimension;
- compactness, boundarylessness, connectedness, and smoothness assumptions;
- whether the geometric hypothesis is failure of local conformal flatness or existence of a point
  where the Weyl tensor is nonzero, and the hypotheses needed to identify those formulations;
- the normalization of the Yamabe functional, conformal Laplacian, scalar curvature, volume, and
  sharp spherical constant;
- whether the constant belongs to a metric's conformal class or is a manifold-level invariant;
- treatment of disconnected manifolds, dimensions below the source threshold, conformally flat
  metrics, and vanishing Weyl curvature.

These alternatives change the domains, ordered binders, hypotheses, conclusion, and boundary
policy. Selecting one from general mathematical memory would invent missing mathematics. Encoding
an abstract structure that assumes a Yamabe constant, sphere comparison, or desired inequality
would likewise be a substituted interface rather than the exact source theorem. No Lean
declaration, axiom, assumed result, broadened theorem, or weakened special case was introduced.

The first failed gate is therefore canonical human-claim identity, before minimal imports,
expression serialization, checked transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations can be established. Machine state remains `M4`; statement
acceptance and theorem completion are false.

## Pinned environment and searches

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). The existing `.lake` closure
was read only; no update, build, clone, or fetch command was used.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1281` | 0 | Rank 452, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| repository `rg` search for Aubin, Yamabe, non-conformal-flatness, Weyl curvature, and conformal Yamabe terminology | 0 | Found only underspecified catalog metadata, provisional intake material, adjacent separately owned targets, and unrelated Aubin-Lions references; no exact source-frozen proposition or Lean declaration |
| pinned-mathlib `rg` search for Yamabe, conformal Laplacian/scalar-curvature transformation, Weyl curvature, and local conformal flatness | 0 | Found only general conformal-map APIs; no theorem-specific Yamabe geometry interface or exact Aubin target |

There is no applicable `lake env lean <target>.lean` command: the exact expression required by the
assigned phase does not exist. Elaborating a made-up proxy would be false evidence rather than the
smallest real validation.

## Retry condition

An accountable source audit must select an immutable edition of Aubin's 1976 paper, record the
exact theorem and page plus errata disposition, and freeze every scope and normalization choice
listed above. It must crosswalk the strict-comparison and existence formulations and distinguish
this root from the full Yamabe theorem and the separately scheduled Schoen branch. A later
statement run can then choose real Lean interfaces, minimize imports, elaborate and fingerprint
the exact expression, compile any credited transports, and execute the four required mutation
classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

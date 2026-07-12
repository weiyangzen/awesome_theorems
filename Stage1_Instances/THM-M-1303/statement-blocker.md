# Exact-statement gate: blocked

Item: `S56-M-1303-STATEMENT`  
Theorem: `THM-M-1303`  
Base revision: `d106a271df55889c00fab33c3ecbdcc7f1d21bd1`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is "paraproduct decomposition of functions" (`函数的仿积分解`). That
phrase does not select one proposition and does not fix:

- whether the root is Bony's product decomposition, a bilinear continuity estimate for one
  paraproduct, or a decomposition-plus-estimates package;
- the Euclidean or periodic domain, dimension, scalar field, and functions versus distributions;
- a homogeneous or inhomogeneous dyadic resolution, its cutoffs, index ranges, and normalization;
- the exact low-high, high-low, and comparable-frequency operators;
- the input function spaces and regularity indices, including endpoint exclusions;
- the topology or distributional sense in which the series and recomposition equality hold.

These choices alter the domains, ordered binders, hypotheses, and conclusion. In addition,
`THM-M-1301` is separately catalogued as "Bony paraproduct decomposition" and has the same leading
candidate identity. The repository provides no source-level distinction between that target and
this one. Reusing the neighboring candidate, selecting a convenient algebraic finite-sum identity,
or assuming abstract operators with the desired identity would merge, weaken, or substitute the
unknown claim.

The Bony 1981 paper and DOI recorded by intake remain discovery anchors only: the repository has no
immutable primary copy, exact theorem/display/page selection, assumption crosswalk, or errata
decision for this target. Consequently the canonical human claim fails before a minimal import,
Lean expression, normalized-expression hash, checked alternate transport, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations can be produced. No
Lean declaration, axiom, placeholder, or broadened proxy was introduced. Machine state remains
`M4`; statement acceptance and theorem completion are false.

## Pinned environment and checks

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The existing canonical `.lake` artifacts were read only; no
update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1303` | 0 | Rank 471, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, Chinese wording, `paraproduct`, and Bony material | 0 | Found the underspecified catalogue/intake records, the colliding `THM-M-1301` intake, and an abstract legacy object model; no source-frozen target |
| pinned-mathlib `rg` search for `paraproduct`, Bony decomposition, resonant product, and Littlewood-Paley paraproduct namespaces | 1 | No matching paraproduct API (exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_182.lean` | 0 | The legacy discovery module elaborated, but its paraproduct operation and continuity claim are caller-supplied structure fields, not the target |
| `git diff --check -- Stage1_Instances/THM-M-1303` | 0 | No whitespace errors |

The legacy elaboration is only a boundary check. In
`AwesomeTheorems.Stage1.S1_M_182.ParaproductCommutatorEstimates`, `paraproduct` is an unconstrained
binary function and `paraproductContinuity` is an unconstrained `Prop`; the module neither defines
a dyadic paraproduct nor states a recomposition theorem. It receives no statement or proof credit.
There is no applicable `lake env lean <canonical-target>.lean` check because no exact expression can
be selected without inventing mathematics.

## Retry condition

An accountable source review must select and pin an immutable primary statement, identify its exact
theorem/display/page and errata status, freeze all domain, dyadic-resolution, operator, regularity,
and convergence conventions above, and resolve the identity boundary with `THM-M-1301`. A later
statement run can then encode that exact claim, minimize imports, fingerprint elaboration, compile
checked transports, and execute all four required mutation classes.

First failed gate: rev-5.6 section 5 exact-statement identity. The assigned phase is not genuinely
self-tested to its completion gate, so no `.stage1-worker-selftest.json` is emitted.

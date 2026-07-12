# Exact-statement gate: blocked

Item: `S56-M-1106-STATEMENT`  
Theorem: `THM-M-1106`  
Base revision: `8c0f75b6729905650deba42603ef9f59f6b37e2c`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record identifies the Marchenko-Pastur law, attributes it to Marchenko and Pastur in 1967, and says
only "eigenvalues of sample covariance matrices." The accepted intake identifies the original
paper as a discovery anchor but explicitly leaves its numbered theorem, page, complete assumptions,
translation differences, and errata uninspected.

The label denotes a family of inequivalent limit theorems. The available record does not freeze:

- real or complex entries, their independence, centering, variance, or moment/tail assumptions;
- rectangular dimensions, covariance orientation, normalization, or population covariance;
- whether the aspect parameter is rows/columns or its reciprocal, and its endpoint regime;
- which Gram matrix supplies the empirical measure and how forced zero eigenvalues are counted;
- the exact density, support, and atom at zero of the limiting measure;
- almost-sure, in-probability, or another convergence mode, and its topology or test functions.

These choices change domains, binders, hypotheses, and the conclusion. In particular, swapping the
dimension ratio or Gram-matrix orientation changes the zero-atom convention; it is not a harmless
notation choice. Selecting a familiar modern iid finite-variance formulation would therefore
substitute an unaudited theorem for the attributed source claim. Hiding the missing mathematics
behind opaque predicates or assuming the desired convergence would be placeholder evidence.

Consequently there is no canonical human proposition on which to minimize imports, serialize an
elaborated expression, check alternate transports, or run meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations. No Lean declaration, axiom, `sorry`,
weakened special case, or broadened theorem was introduced. Machine state remains `M4`; statement
acceptance and theorem completion are false.

## Pinned environment and search

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` directory
was read only; no update, build, clone, fetch, or dependency mutation was run.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1106` | 0 | rank 546, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for Marchenko-Pastur and sample-covariance spectral wording | 1 outside the owned dossier | no exact source-frozen proposition or historical Lean candidate found |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C` canonical pinned mathlib `rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| pinned-mathlib `rg` search for Marchenko, Pastur, sample covariance, and empirical spectral distribution | 0 only for generic wording | found only two generic covariance-matrix comments in the multivariate Gaussian module; no Marchenko-Pastur statement or supporting spectral-limit API |

There is no applicable `lake env lean <canonical-target>.lean` check: the exact proposition needed
to create that file has not been identified. Elaborating an invented abstract interface would not
validate the assigned target.

## Retry condition

An accountable source review must preserve an immutable primary-source edition, record its content
hash, exact theorem/page and referenced definitions, audit translation differences and errata, and
independently approve a binder-by-binder crosswalk. It must freeze every entry-distribution,
dimension, normalization, ratio, empirical-measure, zero-atom, and convergence convention above.
A later statement run can then encode the real claim, minimize pinned imports, fingerprint the
elaborated expression and environment, check transports, and run all four mutation classes.

This is the first failed gate and does not complete this node or any later node. The assigned phase
is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.

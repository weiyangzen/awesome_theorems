# Exact-statement gate: blocked

Item: `S56-M-0179-STATEMENT`

Theorem: `THM-M-0179`

Base revision: `bcb28c5ba8db59ba986fdca6d4669097b6c98b3e`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository evidence currently
available. The authoritative source trace supplies only the Chinese label "Yau estimate"
(`丘成桐估计`), attribution to Shing-Tung Yau, the year 1978, and the gloss "lower-bound
estimate for the first eigenvalue." It supplies no bibliography, immutable source edition,
theorem/page locator, formula, or assumption list. The intake therefore correctly leaves both
`canonical_statement` and `canonical_formal_target.declaration_or_expression` unset.

The gloss does not determine any one proposition. In particular, it leaves open:

- the operator, its sign, and its normalization;
- whether "first" denotes the bottom eigenvalue, the first positive eigenvalue, or a Dirichlet or
  Neumann eigenvalue;
- whether the setting is a closed manifold, a complete noncompact manifold, or a bounded domain;
- dimension, connectedness, boundary conditions, and regularity assumptions;
- the required Ricci or other curvature bound and any diameter, volume, or normalization inputs;
- the exact lower-bound constant, strictness, equality cases, and degenerate cases.

These choices alter the domains, ordered binders, hypotheses, and conclusion. The repository also
contains a separate 1975 PDE entry with the same Chinese title (`THM-M-1319`) and separately
scheduled Li-Yau, Zhong-Yang, and Yau-conjecture records. Name similarity cannot select among these
results. Choosing a familiar eigenvalue inequality, adding convenient hypotheses, or introducing
an abstract predicate called an eigenvalue would broaden or substitute the scheduled theorem.

There is consequently no canonical expression for import minimization, elaborated-expression
hashing, checked alternate transports, or the required removed-hypothesis, changed-domain,
binder-scope, and boundary mutations. No Lean declaration or proof-like artifact was added.
Machine debt remains `M4`; the statement gate, audit completion, and theorem completion remain
open.

## Pinned environment and validation

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The canonical `.lake` directory was used read-only; no
update, build, clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0179` | 0 | Rank 670, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese title, English label, and first-eigenvalue lower-bound gloss | 0 | Found only underspecified metadata, the two intakes, and separately scheduled neighboring results; no source-frozen target |
| pinned-mathlib `rg` search for Yau estimates, first eigenvalues, Laplace-Beltrami operators, and eigenvalue/Ricci combinations | 1 | No matching theorem-specific API (`rg` exit 1 means no match) |

There is no honest `lake env lean <target>.lean` command to run because an exact target does not
exist. Elaborating a guessed or generic proposition would not validate this phase.

## Retry condition

An accountable source review must identify an immutable primary-source edition and exact
theorem/page, check errata, and freeze the operator, eigenvalue indexing, geometric setting,
ordered hypotheses, normalization, constant, conclusion, and boundary cases. It must distinguish
the result from `THM-M-1319` and the nearby Li-Yau, Zhong-Yang, and Yau-conjecture targets. A later
statement run can then encode the exact proposition, minimize pinned imports, fingerprint the
elaborated expression, add checked transports, and execute the structural mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

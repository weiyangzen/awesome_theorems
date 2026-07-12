# Exact-statement gate: blocked

Item: `S56-M-1319-STATEMENT`

Theorem: `THM-M-1319`
Base revision: `6fe4239145678f2a649a57e6610ba40dc8a9cd83`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the label "Yau estimate" (`丘成桐估计`), attribution to Shing-Tung Yau, the
year 1975, and the gloss "lower bound for the first eigenvalue." It supplies no primary-source
paper, immutable edition, theorem/page, formula, or assumption list. The accepted intake therefore
correctly left `canonical_statement` and the formal declaration unset.

The gloss does not determine a proposition. In particular it does not fix:

- the operator or its sign and normalization;
- whether "first" means the bottom eigenvalue, the first positive eigenvalue, or a Dirichlet or
  Neumann eigenvalue;
- whether the space is a closed manifold, a complete noncompact manifold, or a bounded domain;
- dimension, connectedness, boundary conditions, and regularity assumptions;
- Ricci or other curvature bounds, diameter, volume, or further geometric inputs;
- the exact constant, strictness, equality cases, and degenerate or boundary cases.

These choices change the domains, ordered binders, hypotheses, and conclusion. The repository also
contains a separate 1978 entry with the same Chinese title (`THM-M-0179`) and adjacent but distinct
Li-Yau, Zhong-Yang, and Yau-conjecture records. Name similarity cannot choose among those results.
Selecting a familiar eigenvalue inequality, strengthening assumptions to obtain a convenient
theorem, or encoding an abstract relation called an eigenvalue would substitute invented
mathematics for the scheduled target.

Consequently there is no canonical expression on which to minimize imports, compute an elaborated
expression hash, check alternate encodings, or run removed-hypothesis, changed-domain,
binder-scope, and boundary mutations. No Lean declaration or proof-like artifact was introduced.
Machine debt remains `M4`; statement acceptance and theorem completion are false.

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
| `python3 scripts/stage1_target.py show THM-M-1319` | 0 | Rank 481, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese title, English label, and first-eigenvalue lower-bound gloss | 0 | Found only underspecified metadata, this intake, a duplicate title, and separately scheduled neighboring results; no source-frozen target |
| pinned-mathlib `rg` search for Yau estimates, first eigenvalues, Laplace-Beltrami operators, and eigenvalue/Ricci combinations | 1 | No matching theorem-specific API (`rg` exit 1 means no match) |

There is no honest `lake env lean <target>.lean` check to run: the exact target does not exist.
Elaborating a guessed or generic proposition would not validate this statement phase.

## Retry condition

An accountable source review must identify an immutable primary-source edition and exact
theorem/page, check errata, and freeze the operator, eigenvalue indexing, geometric setting,
ordered hypotheses, normalization, constant, conclusion, and boundary cases. It must distinguish
the selected result from `THM-M-0179` and the nearby Li-Yau, Zhong-Yang, and Yau-conjecture targets.
A later statement run can then encode the exact proposition, minimize pinned imports, fingerprint
the elaborated expression, add checked transports, and execute structural mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

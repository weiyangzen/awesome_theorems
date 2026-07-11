# Exact-statement gate: blocked

Item: `S56-M-1189-STATEMENT`  
Base revision: `b0f46ce08e1b6a797d65cf735b0ccf96bd57ddcb`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire source wording is `抛物型方程的正则性` ("regularity of parabolic equations"), under the
title "Schauder estimate for the heat equation". It gives no primary-source theorem, edition,
page, or formula. In particular, it does not determine:

- an interior, boundary, initial-boundary, or global estimate;
- a forward, backward, or two-sided cylinder and its relation to the parabolic boundary;
- the classical or weak solution notion, coefficient class, and forcing convention;
- the precise parabolic Holder spaces, seminorm normalization, and range of `alpha`;
- whether the estimate contains a lower-order norm of `u`, initial/boundary data, or both;
- the dependence of the constant on dimension, radii, domain geometry, time interval, and
  coefficient ellipticity/regularity;
- compatibility conditions and endpoint or degenerate-cylinder policy.

These choices give inequivalent theorems. Selecting one from general mathematical knowledge or
combining conventions from the candidate books in `source-statement-crosswalk.md` would invent
missing mathematics rather than elaborate the exact repository target. Neither book candidate has
yet been inspected at a fixed theorem/page, and a bibliography-level discovery anchor is not a
canonical statement.

The intake correctly leaves the exact variant open. Therefore this phase fails at canonical
human-claim identity, before minimal imports, an elaborated expression fingerprint, checked
transports, or meaningful removed-hypothesis/domain/binder-scope/boundary mutations can be
established. No statement acceptance, proof credit, audit completion, or theorem completion is
claimed.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_152.lean` was inspected and elaborated only as
unaccepted discovery material. It defines useful expression-level objects such as parabolic
cylinders, an anisotropic Holder-bound predicate, and a formal heat operator. Its prospective
Schauder interface stores the estimate constants and hypotheses in structure data; it is not a
transcription of an identified primary-source theorem. The module itself says that it normalizes a
statement shape and does not claim the terminal PDE result.

The legacy module elaborates with six broad direct mathlib imports in the pinned environment and
prints several queried mathlib declaration types. This establishes syntax and type correctness of
that abstract boundary only. It neither establishes a minimal import for an exact target nor
resolves the source ambiguity, so it receives no rev-5.6 statement credit.

## Required unblock

An accountable source reviewer must inspect one stable primary source and record its edition,
theorem/page, exact formula, incorporated definitions, and errata status. The review must freeze the
operator, solution notion, domain and boundary conventions, Holder norm normalization, all
hypotheses, the quantitative conclusion, constant dependencies, and degenerate cases. A later
statement worker can then encode that one claim without substitution, minimize its pinned imports,
serialize the elaborated expression, and run all four required mutation classes.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. No `lake update`, build, dependency fetch,
or mutation of `.lake` was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1189` | exit 0; rank 152, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_152.lean)` | exit 0; legacy abstract module elaborated and printed the queried `deriv`, `fderiv`, `iteratedFDeriv`, `Laplacian.laplacian`, Holder, and smoothness declaration types |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transport, and mutation tests. The
assigned phase is therefore not self-tested or complete, and no `.stage1-worker-selftest.json` is
emitted.

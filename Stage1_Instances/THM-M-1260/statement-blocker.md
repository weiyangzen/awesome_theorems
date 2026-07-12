# Exact-statement gate: blocked

Item: `S56-M-1260-STATEMENT`  
Theorem: `THM-M-1260`  
Base revision: `9144fc9aa3522671a4cda7de9d460d01f382367a`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the title "pseudodifferential operators", the gloss "generalization of
differential operators", the date 1965, and the names Joseph Kohn, Louis Nirenberg, and Lars
Hormander. It supplies no publication, edition, theorem/page, formal proposition, ordered binders,
hypotheses, or conclusion. The accepted intake therefore correctly leaves the canonical statement
null and classifies exact statement identification as blocked.

The label names a class of operators rather than a unique truth-valued theorem. At least the
following inequivalent targets fit the metadata:

- differential operators of a fixed order embed into a specified pseudodifferential symbol class;
- two pseudodifferential operators compose, with an asymptotic expansion for the resulting symbol;
- a pseudodifferential operator of order `m` maps between specified Sobolev spaces;
- ellipticity gives a parametrix or a microlocal regularity conclusion.

Even the closest reading, the first target, does not fix the Euclidean or manifold setting,
scalar or bundle coefficients, regularity of coefficients, symbol class and type, quantization,
Fourier normalization, order convention, proper-support condition, or function/distribution
spaces. Those choices alter domains, quantifiers, assumptions, and conclusions. Selecting one,
combining several, or encoding an abstract interface that assumes the desired analytic properties
would substitute invented mathematics for the source claim.

Consequently there is no canonical expression on which to minimize imports, compute an elaborated
expression fingerprint, check alternate encodings, or run the required removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. No Lean declaration or theorem surrogate was
introduced. Machine state remains `M4`; statement acceptance, audit completion, and theorem
completion remain false.

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

Commands ran inside this worker clone. Lean used the existing canonical `.lake` artifacts through
the worker symlink; no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1260` | 0 | Rank 437, planned, `L0/rework_required`, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for `pseudodifferential`, `pseudo-differential`, `伪微分`, `Kohn-Nirenberg`, and `Hormander` | 0 | Found the underspecified metadata and other targets' discovery material, but no source-frozen proposition for `THM-M-1260` |
| pinned-mathlib `rg` search for pseudodifferential operators, Kohn-Nirenberg, symbol classes, and oscillatory integrals | 1 | No matching pseudodifferential-calculus source in pinned mathlib; exit 1 means no match |

There is no applicable `lake env lean <target>.lean` command: the canonical proposition needed to
create that file is precisely what the source record fails to identify. Compiling a convenient
proxy would not validate the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, account for errata, and crosswalk every binder, hypothesis, convention, and
conclusion. It must distinguish the selected result from the composition, mapping, parametrix, and
microlocal-regularity families above. A later statement run can then encode that exact claim,
minimize pinned imports, preserve its elaborated expression and environment fingerprints, compile
any credited transports, and run all four mutation classes.

This assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

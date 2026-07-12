# Exact-statement gate: blocked

Item: `S56-M-1062-STATEMENT`
Theorem: `THM-M-1062`
Base revision: `2258ea568eef0aa1e38a1124909098ee19b8b0e9`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is `随机扰动动力系统` ("randomly perturbed dynamical systems") under
the name "Freidlin-Wentzell theory." This names a theory containing multiple inequivalent theorem
families, not one proposition. The intake identifies a finite-horizon sample-path large-deviation
principle as a candidate only and expressly leaves the primary theorem selection open.

The record does not fix:

- a sample-path large-deviation theorem rather than an exit-time, exit-location, quasipotential,
  metastability, or invariant-measure theorem;
- the finite- or infinite-dimensional state space, the time horizon, or the path-space topology;
- the stochastic equation, initial-condition quantifiers, coefficient regularity, and existence or
  uniqueness hypotheses;
- additive versus multiplicative noise, nondegenerate versus degenerate diffusion, and the role of
  a diffusion matrix or its inverse;
- the small-noise normalization (`epsilon` versus `sqrt epsilon`) and corresponding LDP speed;
- pointwise versus uniform initial conditions and the precise open-set lower and closed-set upper
  bounds;
- the controlled-path or inverse-covariance definition of the action, its extended-real value on
  inadmissible paths, compact level-set assumptions, and exponential-tightness requirements.

These choices change domains, ordered binders, hypotheses, and the conclusion. Selecting a familiar
sample-path theorem, encoding an abstract large-deviation principle as an assumption, or proving a
finite-dimensional special case would invent or substitute mathematics. The only bibliographic
lead is the Freidlin-Wentzell monograph, but the dossier has no pinned edition artifact, exact
theorem/page, verbatim statement, definitions incorporated by reference, or errata crosswalk. The
upstream intake dependency is also only provisional (`[_]`), not master accepted.

Consequently the canonical human-claim identity gate fails before minimal imports, ordered Lean
binders, expression serialization, checked alternate transports, or meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations can be established. No `Statement.lean`
file, assumed interface, placeholder, axiom, weakened target, or broadened target was introduced.
Machine state remains `M4`; statement acceptance and theorem completion are false.

## Pinned environment and discovery boundary

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

The repository search found only the terse source metadata and the fail-closed intake candidate.
A read-only search of pinned mathlib found no declaration mentioning Freidlin or Wentzell and no
large-deviation API that could identify the intended claim. This is discovery evidence only, not
the downstream anchor audit. Existing canonical `.lake` artifacts were reused; no dependency was
updated, built, cloned, or fetched.

## Narrow validation evidence

All commands ran inside this worker clone.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1062` | 0 | rank 505; planned; legacy artifacts unaccepted; theorem incomplete |
| `git rev-parse HEAD` | 0 | produced the base revision recorded above |
| `cd Formalizations/Lean && lake env lean --version` | 0 | produced the Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | produced the Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for `Freidlin`, `Wentzell`, and `随机扰动动力系统` | 0 | found only underspecified metadata and the intake artifacts; no source-frozen proposition |
| pinned-mathlib `rg` search for Freidlin-Wentzell and large-deviation APIs | 1 | no theorem-specific match (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` command because the exact expression required
by this phase cannot be identified. Elaborating a freely chosen nearby result or an abstract
structure that assumes the desired LDP would be fake statement evidence, not validation.

## Retry condition

An accountable source reviewer must pin and inspect a stable primary-source edition, exact
theorem/page, definitions, assumptions, and errata. The review must select one theorem family and
freeze every state-space, time, topology, equation, coefficient, noise, initial-condition, speed,
rate-function, compactness, bound, and degenerate-case convention listed above. A later statement
worker can then encode that exact claim, minimize its pinned imports, serialize and hash its
elaborated expression and environment, compile checked transports, and run all four required
mutation classes.

First failed gate: section 5 exact source-statement identity. The assigned phase is not genuinely
self-tested to completion, so no `.stage1-worker-selftest.json` is emitted. No downstream-node,
audit-completion, proof, or theorem-completion credit is claimed.

# Exact-statement gate: blocked

Item: `S56-M-1020-STATEMENT`  
Theorem: `THM-M-1020`  
Base revision: `f552b1fbe91904b0d46dad9e5e29e9075fc93c1e`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is `特征函数的积分恒等式` ("an integral identity for characteristic
functions") under the name "Parseval identity". It supplies no formula or primary-source locator.
In particular, it does not determine:

- whether the objects are probability measures, densities, random variables, or arbitrary
  square-integrable functions;
- whether the identity is a norm equality or a bilinear/sesquilinear inner-product identity;
- the domain and codomain, including the real line versus a higher-dimensional or abstract group;
- the Fourier transform and characteristic-function sign and normalization conventions;
- the reference measures, complex conjugation placement, and multiplicative constant;
- the integrability, square-integrability, absolute-continuity, or density hypotheses;
- whether equality is pointwise, almost everywhere, or an equality of extended integrals;
- the treatment of zero measures, absent densities, and infinite integrals.

These choices yield inequivalent propositions. A general characteristic function is bounded but
need not be integrable or square-integrable. Choosing the classical Fourier-series Parseval
identity, Plancherel for an `L2` function, or a density inner-product formula would therefore
substitute an invented theorem for this target. The intake dependency records precisely the same
ambiguity and does not select a canonical claim.

Consequently the canonical human-claim identity gate fails before minimal imports, ordered Lean
binders, an elaborated expression fingerprint, checked alternate transports, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutations can be established. No
Lean declaration, opaque interface, axiom, placeholder, weakened special case, or broadened target
was introduced. Machine state remains `M4`; statement acceptance and theorem completion are false.

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

The pinned mathlib search found several nearby but non-identifying theorem families: polynomial
Parseval, additive-circle and torus Fourier-series Parseval, Schwartz-space Plancherel, and `L2`
Fourier Plancherel. It also found the probability `charFun` API. None of those declarations fixes
which identity the repository phrase intends, so none receives statement credit. This was only
discovery against existing read-only `.lake` artifacts; no update, build, clone, or fetch ran.

## Narrow validation evidence

All commands ran inside this worker clone.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1020` | 0 | Rank 496, planned, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD` | 0 | Produced the base revision recorded above |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Produced Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Produced Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese title and gloss plus English Parseval/characteristic-function combinations | 0 | Found only the underspecified metadata and its generated projections; no source-frozen proposition |
| pinned-mathlib `rg` search for `parseval`, `plancherel`, and characteristic-function APIs | 0 | Found the neighboring families described above, but no evidence selecting one as this target |
| `git diff --check -- Stage1_Instances/THM-M-1020` | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Confirmed that this blocked phase did not emit a completion manifest |

There is no applicable `lake env lean <target>.lean` command: the exact expression required by the
assigned phase does not exist. Elaborating a freely chosen nearby theorem or a structure that
assumes the desired equality would be fake evidence rather than validation.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, check errata, and freeze the displayed formula, all domains and ordered quantifiers,
Fourier convention, reference measures, hypotheses, equality notion, constants, and degenerate
cases. A later statement run can then encode that exact claim, minimize pinned imports, serialize
and hash its elaborated expression and environment, compile checked transports, and run all four
required mutation classes.

First failed gate: section 5 exact source-statement identity. The assigned phase is not genuinely
self-tested to completion, so no `.stage1-worker-selftest.json` is emitted. No downstream-node,
audit-completion, proof, or theorem-completion credit is claimed.

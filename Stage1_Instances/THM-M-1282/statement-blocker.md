# Exact-statement gate: blocked

Item: `S56-M-1282-STATEMENT`  
Theorem: `THM-M-1282`  
Base revision: `883205204cea57181965a9de9620f3c150aaf2e8`

## Decision

The exact Lean 4 statement cannot be truthfully elaborated from the authoritative repository
record. That record supplies only the name "Schoen theorem", the year 1984, and the gloss "Yamabe
problem (conformally flat)". The intake preserves a plausible provisional scope, but explicitly
leaves the exact source theorem and its conventions unresolved. The cited Schoen paper is only a
bibliographic discovery anchor: no immutable source copy, exact theorem/page, or reviewed
source-to-binder crosswalk is present in this clone.

In particular, the available record does not determine all proposition-changing choices:

- whether the root is the complete Yamabe existence theorem or only the remaining locally
  conformally flat branch after the Aubin/Trudinger reductions;
- connectedness, dimension restrictions, and any exceptional spherical case;
- the precise smoothness, compactness, boundary, and local-conformal-flatness conventions;
- whether the conclusion is stated as a conformal metric, a positive conformal factor solving the
  Yamabe equation, or attainment of the Yamabe functional;
- the exponent, Laplacian sign, scalar-curvature constants, normalization, and regularity in an
  analytic formulation;
- which positive-mass theorem hypotheses, including dimension or spin qualifications, occur in
  the selected historical statement rather than only in a proof route.

These alternatives are not definitionally interchangeable and can change domains, binders,
hypotheses, and conclusions. Choosing among them from the short metadata would invent, broaden, or
substitute mathematics. It would also violate the intake's explicit retry condition that
`SRC-1282-1` first be resolved by a pinpoint primary-source statement.

The pinned mathlib snapshot has manifold Riemannian-metric infrastructure, but the scoped search
found no scalar-curvature, Yamabe, conformal-metric, or locally-conformally-flat API from which this
root could currently be encoded without introducing substantial new definitions. Its
`ConformalGroupoid` concerns conformal maps on normed-model spaces and is not a Riemannian conformal
metric or Yamabe interface. This library boundary is secondary to the source ambiguity: even an
abstract local interface would not identify the exact theorem.

Consequently there is no canonical Lean expression, minimal import set, expression fingerprint,
checked alternate-form transport, or meaningful removed-hypothesis/domain/binder-scope/boundary
mutation suite. No Lean declaration, assumed theorem interface, axiom, placeholder, weakened case,
or broadened target was introduced. Machine debt remains `M4`; statement acceptance and theorem
completion are false.

## Pinned environment and validation

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` directory
was used read-only through the clone's existing symlink. No update, build, dependency clone, or
fetch command was run.

- Lean toolchain pin: `leanprover/lean4:v4.29.0`.
- Lean executable: Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1282` | 0 | Rank 453, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the title and conformally-flat Yamabe wording | 0 | Found only short metadata, this provisional intake, and related target boundaries; no source-frozen exact proposition |
| pinned-mathlib `rg` search for scalar curvature, Yamabe, conformal metrics, and locally conformally flat geometry | 1 | No matching API (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check because no exact target exists. Compiling
a newly invented proposition or a structure that assumes the desired conclusion would be fake
statement evidence rather than validation of the assigned deliverable.

## Retry condition

An accountable source review must provide an immutable primary-source edition and pinpoint the
exact theorem/page, all assumptions, definitions, and errata. It must resolve the distinction
between the conformally flat branch and the unrestricted Yamabe theorem and decide every convention
listed above. A later statement run can then implement the necessary geometry interfaces, minimize
the imports, serialize the elaborated expression and environment fingerprint, compile checked
transports, and execute all four required mutation classes.

This phase is not genuinely self-tested to its completion gate. No
`.stage1-worker-selftest.json` is emitted, and no receipt or state transition is claimed.

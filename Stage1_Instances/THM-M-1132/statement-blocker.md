# Exact-statement gate: blocked

Item: `S56-M-1132-STATEMENT`  
Theorem: `THM-M-1132`  
Base revision: `5616162cb70eb9714202c5cfe98baa99a30e95a3`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
entire mathematical statement is the phrase "heat kernel or Gaussian kernel". The record gives no
primary source, edition, theorem/page, formula, or indication of which property of a heat kernel is
the asserted theorem. The predecessor intake is only provisional (`[_]`) and supplies no accepted
source-selection receipt.

The phrase leaves proposition-changing choices unresolved:

- Euclidean space, a manifold, a bounded domain, or another state space;
- spatial dimension and scalar field;
- the sign of the Laplacian and the diffusivity convention in the heat operator;
- the time domain and treatment of `t = 0`;
- the Gaussian exponent, prefactor, norm, and reference measure;
- whether "fundamental solution" means the positive-time PDE identity, unit mass and positivity,
  distributional convergence to a Dirac mass, convolution representation, semigroup behavior, or
  uniqueness in a specified class;
- regularity, integrability, initial-data, and uniqueness hypotheses.

These are not alternate notations for one proposition. For example, proving that a selected
Gaussian has mass one would not establish its distributional initial condition, its heat-equation
identity, or uniqueness. Choosing one familiar formula or combining several standard properties
would therefore substitute invented mathematics for the repository claim.

The canonical human statement consequently fails before minimal imports can be determined. There
is no exact expression to elaborate or fingerprint and no meaningful removed-hypothesis,
changed-domain, binder-scope, or boundary-case mutation suite. No Lean declaration, axiom,
placeholder, weakened special case, or broadened target was introduced. Machine state remains
`M4`; statement acceptance, audit completion, and theorem completion remain false.

## Pinned environment and checks

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
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
| `python3 scripts/stage1_target.py show THM-M-1132` | 0 | Rank 337, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese title, literal claim, and English heat/Gaussian-kernel terms | 0 | Found only the underspecified metadata, this intake dossier, and unrelated heat-kernel mentions; no source-frozen proposition for this target |
| pinned-mathlib `rg` search for `heat kernel`, `gaussian kernel`, `heat equation`, `HeatKernel`, and `GaussianKernel` | 1 | No matching declaration or source text (`rg` exit 1 means no match) |

There is no honest `lake env lean <target>.lean` check: an exact target does not exist. Elaborating a
hand-selected Gaussian identity or an abstract interface that assumes heat-kernel semantics would
be false evidence for the assigned exact-statement deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, handle errata, and freeze all domains, ordered binders, operator conventions,
hypotheses, conclusions, and boundary cases listed above. After the intake dependency receives
master acceptance, a later statement run can encode that exact claim, minimize pinned imports,
serialize the elaborated expression and environment fingerprint, check alternate transports, and
run all four mutation classes.

This phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

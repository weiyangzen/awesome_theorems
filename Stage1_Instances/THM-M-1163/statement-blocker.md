# Exact-statement gate: blocked

Item: `S56-M-1163-STATEMENT`  
Theorem: `THM-M-1163`  
Base revision: `5deb8c587c4f4bde14e6c99658fe76c173180019`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording for this target is `边值问题的积分核` ("integral kernel for
boundary-value problems"), under the title "Green function". The record does not supply a primary
source, theorem/page, quotation, or any of the data needed to select one proposition:

- the differential operator, sign convention, coefficients, and scalar field;
- the ambient dimension, domain, boundary regularity, and boundary condition;
- the function, measure, or distribution spaces and the solution concept;
- whether the claim is a definition, existence theorem, uniqueness theorem, inverse-kernel
  identity, or representation formula;
- normalization, integrability, singularity, diagonal, and degenerate-domain conventions; or
- the ordered quantifiers and hypotheses under which the asserted conclusion holds.

These choices give inequivalent Green-function theorems. In particular, a Laplace Dirichlet Green
function, a Sturm--Liouville Green function, a heat kernel, and an abstract resolvent kernel are not
interchangeable. Selecting one because it is convenient to encode would substitute mathematics,
not elaborate the exact source target. The separately scheduled ODE entry `THM-M-1392` and the
adjacent symmetry and eigenfunction-expansion entries do not resolve this target's ambiguity.

The intake dependency reaches the same fail-closed result and assigns `[H4, M4, R4]`. Stage0 also
marks the precise definitions, hypotheses, proof, equivalent formulations, dependencies, and
machine artifact as still to be supplied. The metadata value `已验证` is not a source or kernel
receipt.

Consequently this phase fails at canonical human-claim identity, before minimal imports, an
elaborated expression fingerprint, checked transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary-case mutations can be established. No Lean declaration,
axiom, assumed representation identity, abstract structure containing the desired conclusion,
weakened special case, or broadened theorem was introduced. Statement acceptance and theorem
completion remain false.

## Pinned environment and scoped search

Commands were run inside this worker clone on 2026-07-12 (Asia/Shanghai). Existing `.lake`
artifacts were only read; no update, build, clone, or fetch command was used.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1163` | 0 | Rank 366, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the title and both repository glosses | 0 | Found only underspecified source metadata, its Stage0 projection, this intake, and distinct related targets; no source-frozen proposition for `THM-M-1163` |
| pinned mathlib `rg` search for Green functions, Green kernels, boundary-value problems, and integral kernels | 0 | Found generic probability-kernel integration APIs but no identified PDE Green-function theorem matching the unresolved source claim |

There is no applicable `lake env lean <target>.lean` elaboration check: no exact expression exists.
Elaborating a proposition chosen from one Green-function family, or an abstract interface that
assumes the desired identity, would be fake statement evidence rather than the assigned
deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, dispose of corrections and errata, and freeze every operator, domain, boundary,
space, normalization, singularity, quantifier, hypothesis, conclusion, and degenerate-case choice
listed above. A later statement run can then crosswalk that claim row by row, encode the exact Lean
expression, minimize its pinned imports, fingerprint the elaboration and environment, and execute
the four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

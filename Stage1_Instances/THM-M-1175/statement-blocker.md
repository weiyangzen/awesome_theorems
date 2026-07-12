# Exact-statement gate: blocked

Item: `S56-M-1175-STATEMENT`  
Theorem: `THM-M-1175`  
Base revision: `54743c8a753017ec2ce50ffebf85facec9112b95`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
entire mathematical statement is the gloss "Harnack inequality for divergence-form elliptic
equations". The record gives no primary-source theorem/page and does not select an equation,
solution notion, or comparison geometry. The intake therefore correctly leaves
`canonical_statement` and the canonical formal declaration unset.

In particular, the record does not determine:

- whether the equation is homogeneous or has lower-order/source terms, nor the scalar or system
  coefficient model;
- coefficient measurability, symmetry, boundedness, and the precise uniform-ellipticity inequalities;
- the dimension, ambient domain, weak Sobolev space, weak formulation, or representative of the
  solution;
- nonnegative versus strictly positive solutions and the treatment of the identically-zero case;
- balls versus general compactly contained regions, their nesting/radius restrictions, and boundary
  distance;
- ordinary versus essential supremum and infimum, and the exact structural dependencies of the
  Harnack constant.

These are proposition-changing choices. Selecting a familiar Moser theorem, a harmonic special
case, an abstract predicate that assumes the desired estimate, or the nearby external De Giorgi
formalization would invent or substitute mathematics. Moser's 1961 paper remains only the intake's
discovery anchor because no immutable edition, theorem/page, assumptions, or errata crosswalk has
been accepted. Consequently there is no meaningful minimal-import claim, elaborated-expression
fingerprint, checked transport, or removed-hypothesis/domain/scope/boundary mutation suite.

No Lean declaration, proof device, assumed Harnack property, weakened special case, or broadened
target was introduced. Machine debt remains `M4`; `statement_elaborated`, theorem completion, and
all dependent-node gates remain false.

## Environment and searches

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The existing `.lake` artifacts were read only; no update,
build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1175` | 0 | Rank 375, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for divergence-form Harnack and Moser Harnack wording | 0 | Found the underspecified metadata and adjacent historical audit notes, but no source-frozen proposition for `THM-M-1175` |
| pinned-mathlib `rg` search for `Harnack`, `weak_harnack`, `harnack_on_ball`, `De Giorgi`, and `Moser` in `Mathlib/**/*.lean` | 1 | No match; exit 1 is `rg`'s no-match result |

There is no applicable `lake env lean <target>.lean` check because the exact target required by the
node does not exist. Creating a generic interface whose hypotheses encode the conclusion would be
fake elaboration evidence rather than validation.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact theorem/page,
dispose of errata, and freeze every operator, coefficient, ellipticity, weak-solution, sign,
dimension, domain, comparison-region, extrema, constant-dependency, and degenerate-case convention
listed above. It must also distinguish this root from harmonic, parabolic, non-divergence, boundary,
and regularity-only Harnack results. A later statement run can then encode that proposition, minimize
its pinned imports, fingerprint the elaborated expression, provide checked transports, and run
structural mutations and boundary checks.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

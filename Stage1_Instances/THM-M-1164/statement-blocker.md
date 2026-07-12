# Exact-statement gate: blocked

Item: `S56-M-1164-STATEMENT`

Theorem: `THM-M-1164`

Base revision: `1606d531758dba438f0601f56c38fb4b651aa258`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository source record. Its entire
mathematical wording is the title `Green函数的对称性` (symmetry of the Green function) and the
phrase `自伴算子的Green函数` (Green function of a self-adjoint operator). The attribution is only
"many mathematicians, nineteenth century"; there is no primary source, edition, theorem/page,
formula, proof, or errata record. The historical `已验证` label is untrusted metadata, not source or
kernel evidence.

The intake usefully proposes the standard resolvent/inverse family, but deliberately leaves the
formal module and expression open. It also exposes choices that still change the proposition:

- the Hilbert space, scalar field, operator realization, domain, and boundary conditions;
- whether the Green object is an inverse at zero, a resolvent at a spectral parameter, or a
  generalized inverse when zero modes occur;
- whether the conclusion concerns self-adjointness of a bounded Green operator or symmetry of a
  representing integral kernel;
- the underlying measure space, kernel representation and uniqueness hypotheses, and whether the
  kernel is a function, an almost-everywhere class, or a distribution;
- Hermitian symmetry `K x y = conj (K y x)` versus real symmetry, and almost-everywhere versus
  pointwise equality;
- regularity and exceptional-set hypotheses needed to upgrade an almost-everywhere identity.

These are inequivalent theorem statements. In particular, self-adjointness of a bounded inverse is
not itself an integral-kernel symmetry theorem, a real pointwise symmetry statement is stronger
than complex almost-everywhere Hermitian symmetry, and a generalized inverse has a different
zero-mode boundary. Selecting one convenient bounded-operator theorem or inventing an abstract
kernel representation would therefore substitute for the unidentified root rather than elaborate
it exactly.

Consequently the canonical human-claim identity gate fails before minimal imports, fixed binders,
an elaborated expression fingerprint, checked transports, or meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations can be established. No Lean target,
axiom, placeholder, assumed interface, or broadened special case was introduced. Machine debt
remains `M4`; statement acceptance and theorem completion are not claimed.

## Pinned API boundary

Pinned mathlib does provide partially defined operators and their adjoints in
`Mathlib.Analysis.InnerProductSpace.LinearPMap`: `LinearPMap.IsFormalAdjoint`,
`LinearPMap.adjoint`, the characterization `LinearPMap.isSelfAdjoint_def`, and the dense-domain
consequence `IsSelfAdjoint.dense_domain`. Those definitions are useful substrate for one possible
operator formulation, but they do not choose an inverse/resolvent, kernel representation,
uniqueness theorem, equality mode, or PDE boundary realization.

A search of the pinned mathlib source for “Green function”, “Green kernel”, and “integral kernel”
found no theorem-specific Green-kernel API. Repository-wide discovery found only the short source
catalogue, generated target projections, and neighboring dossiers. These negative searches do not
repair the absent source proposition. There is no applicable `lake env lean <target>.lean` command:
the exact expression such a file would elaborate is the missing deliverable, and elaborating a
freely selected proxy would be fake evidence.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake`
artifacts were read only; no update, build, clone, fetch, or dependency mutation was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1164` | 0 | Rank 367, planned lifecycle, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision above |
| repository `rg` search for the theorem ID, Chinese title and wording, and English symmetry terms | 0 | Found only underspecified catalogue/generated metadata and neighboring dossier references; no exact source proposition |
| pinned-mathlib `rg` search for Green functions, Green kernels, and integral kernels | 0 | No theorem-specific Green-function or integral-kernel API; two unrelated probability-kernel lines matched “integral” and “kernel” separately |
| pinned-mathlib `rg` inspection of `Mathlib.Analysis.InnerProductSpace.LinearPMap` | 0 | Confirmed unbounded-operator adjoint substrate only; no inverse/resolvent or Green-kernel statement selected |

## Retry condition

An accountable source reviewer must pin an immutable primary or authoritative scholarly source by
edition and exact theorem/page, check errata, and freeze the Hilbert/scalar setting, operator and
boundary realization, inverse/resolvent or generalized-inverse convention, spectral parameter and
zero-mode policy, kernel representation and uniqueness assumptions, measure, quantifier order,
Hermitian/real convention, equality mode, and regularity or exceptional cases. A later statement
worker can then transcribe that proposition, minimize pinned imports, serialize the elaborated
expression and environment, compile any credited transports, and execute all four required
mutation classes.

The assigned phase is not genuinely self-tested to its completion gate. Therefore no
`.stage1-worker-selftest.json` is emitted.

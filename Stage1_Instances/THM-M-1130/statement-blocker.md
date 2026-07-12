# Exact-statement gate: blocked

Item: `S56-M-1130-STATEMENT`  
Theorem: `THM-M-1130`  
Base revision: `f756a5a3b3e172050802423f4b98d5910b56dbb5`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
Its entire mathematical content is the title "heat equation" and the gloss "mathematical model of
heat conduction". An equation or model family is not by itself a theorem, and the record supplies
no truth-valued conclusion. It also supplies no primary-source theorem/page that could select one.

Even a choice to encode the familiar display `partial_t u = alpha * Delta u` would leave material
choices unresolved:

- the spatial dimension and whole-space, bounded-domain, or manifold setting;
- the time domain, initial data, and Dirichlet, Neumann, Robin, or no boundary data;
- constant isotropic diffusivity versus variable or anisotropic coefficients, the sign convention,
  and the presence of a source term;
- classical, weak, distributional, mild, or semigroup solutions and their regularity;
- whether the intended conclusion is derivation, existence, uniqueness, characterization,
  representation, or a qualitative property of solutions.

These choices yield inequivalent propositions. Restating a selected PDE as both hypothesis and
conclusion would be a tautological proxy, not the catalog claim. Selecting a fundamental-solution
or maximum-principle result would substitute the separately scheduled targets `THM-M-1132` or
`THM-M-1133`; selecting a physical derivation would overlap `THM-M-1131`. The historical Fourier
citation in the intake is only a discovery lead: no edition passage, exact claim, assumptions,
translation, or errata review has been accepted.

The canonical human claim therefore fails before ordered binders, minimal imports, an elaborated
expression fingerprint, checked transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary-case mutations can be established. No Lean declaration, `sorry`, axiom,
opaque heat-equation predicate, weakened special case, or broadened theorem was introduced.
Machine state remains `M3`, as recorded by the accepted intake dependency: the exact target is
blocked on source-statement selection rather than claimed absent from all possible formalizations.

## Pinned environment and search

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The canonical `.lake` symlink and its existing pinned
artifacts were read only; no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1130` | 0 | Rank 335, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for `heat equation`, `heat conduction`, `热方程`, and `热传导` | 0 | Found only the underspecified catalog text, adjacent targets, and unrelated or legacy discovery artifacts; no source-frozen proposition for this target |
| pinned-mathlib `rg` search for `heat equation`, `HeatEquation`, and heat-equation/Laplacian APIs | 1 | No theorem-specific heat-equation declaration was found (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check: no exact target expression exists.
Elaborating a freely chosen PDE predicate or an interface that assumes the desired property would
be fake statement evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, dispose of translation and errata issues, and freeze the domain, coefficient and sign
conventions, data, regularity, solution notion, ordered hypotheses, conclusion, and boundary cases.
It must also explain the boundary with `THM-M-1131`, `THM-M-1132`, and `THM-M-1133`. A later
statement run can then encode that claim exactly, minimize its pinned imports, fingerprint the
elaborated expression, provide checked transports for alternate encodings, and run structural
mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted. Statement acceptance, all downstream credit, and theorem
completion remain false.

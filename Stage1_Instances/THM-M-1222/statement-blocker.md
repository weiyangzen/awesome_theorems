# Exact-statement gate: blocked

Item: `S56-M-1222-STATEMENT`  
Theorem: `THM-M-1222`  
Base revision: `f4b142975b0cf41e1c092e006544346545ed8b8c`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
Its complete mathematical wording is the label "Ginibre-Velo NLW theorem" and the phrase
`NLW的局部适定性` (local well-posedness of NLW), attributed to Jean Ginibre and Giorgio Velo in
1985. The record provides no publication, immutable edition, theorem/page, quotation, displayed
equation, or imported definitions. The accepted intake dependency accordingly freezes only a
theorem family at `[H3, M4, R4]`, not a canonical proposition.

The missing choices are mathematically substantive:

- nonlinear wave versus nonlinear Klein-Gordon, including the mass term and sign conventions;
- spatial dimension, real or complex scalar field, and the precise nonlinearity and exponent
  range;
- homogeneous or inhomogeneous Sobolev/energy data spaces and any compatibility, smallness,
  symmetry, or decay assumptions;
- weak, mild, strong, or classical solution notion, its spacetime regularity, and the time
  interval or maximal-lifespan convention;
- the uniqueness class and the topology and quantitative strength of continuous dependence; and
- whether persistence of regularity, a blow-up alternative, conservation, or endpoint and
  degenerate-data cases are part of the conclusion.

These choices yield inequivalent local well-posedness theorems. In particular, silently treating a
nonlinear Klein-Gordon result as NLW, choosing a convenient power nonlinearity, or encoding an
abstract problem whose fields assume existence and uniqueness would substitute mathematics rather
than elaborate the exact source claim. The neighboring Segal, Shatah-Struwe, Grillakis, and Tao
targets do not disambiguate this one. The repository's `已验证` value is untrusted discovery
metadata, not a source or kernel receipt.

Consequently this phase fails at canonical human-claim identity, before minimal imports, fixed
ordered binders and universes, an elaborated-expression fingerprint, checked transports, or the
required removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations can be
defined. No Lean declaration, axiom, placeholder, assumed well-posedness structure, weakened
special case, or broadened theorem was introduced. The statement node remains open at `M4`; no
statement acceptance, proof credit, audit completion, or theorem completion is claimed.

## Pinned environment and scoped search

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). Existing `.lake` artifacts
were read only; no update, build, clone, fetch, or dependency mutation was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1222` | 0 | Rank 413, planned lifecycle, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for Ginibre-Velo, NLW local well-posedness, nonlinear wave, and nonlinear Klein-Gordon | 0 | Found only underspecified catalogue metadata, its generated projections, separately owned neighboring dossiers, and unrelated legacy modules; no source-frozen proposition or target-specific Lean module |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| pinned-mathlib `rg` search for Ginibre, nonlinear wave/Klein-Gordon, local well-posedness, and Cauchy-problem terminology | 0 | Only the unrelated Fortuin-Kastelyn-Ginibre inequality matched; no relevant PDE target was identified |

There is no applicable `lake env lean <target>.lean` elaboration check: the exact expression to put
in that file is precisely what the source record does not determine. Elaborating a freely selected
PDE variant or an interface that assumes the desired result would be fake statement evidence, not
the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, resolve the NLW/Klein-Gordon and 1985 attribution, dispose of errata, and freeze every
equation, dimension, nonlinearity, space, solution, lifespan, uniqueness, dependence, endpoint,
quantifier, hypothesis, conclusion, and degenerate-case choice listed above. A later statement run
can then crosswalk that claim row by row, encode the exact Lean expression, minimize its pinned
imports, fingerprint the elaboration and environment, and execute all four structural mutation
classes.

The assigned phase is not genuinely self-tested to its completion gate. Therefore no
`.stage1-worker-selftest.json` is emitted.

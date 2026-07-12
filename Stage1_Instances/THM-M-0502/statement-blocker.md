# Exact-statement gate: blocked

Item: `S56-M-0502-STATEMENT`  
Theorem: `THM-M-0502`  
Base revision: `d35402671f48a935ddbe17b2e5a2b5ebb8b9cfe4`

## Decision

The exact Page/Landau-Page proposition cannot be truthfully recovered from the authoritative
repository record. `Docs/researches/math_theorems.md` supplies only A. Page, 1935, and the Chinese
gloss "existence of real zeros of L-functions." That gloss is not the usual at-most-one
exceptional-zero conclusion and does not identify a theorem or page in Page's paper. The intake's
two citations are explicitly discovery anchors: neither source text, a stable scan hash, pinpoint
statement, errata disposition, nor premise-by-premise review is present in this clone.

The missing choices are proposition-changing rather than notational:

- the family of primitive characters and whether the uniform bound is on each conductor, a
  product of two conductors, or another parameter;
- whether characters must be real, nonprincipal, quadratic, or primitive representatives of
  induced characters;
- the lower threshold on the family parameter and the absolute constant's quantifier order;
- the exact zero region, including logarithm normalization, strict endpoints, and whether it is a
  real interval or a complex rectangle;
- whether uniqueness concerns a character, a primitive representative, a zero, or a
  character-zero pair;
- whether reality, simplicity, or another property of the exceptional zero belongs to the root
  conclusion.

Choosing values for these fields from general mathematical memory would silently replace the
source claim. Conversely, formalizing only the repository's existential gloss would substitute a
different theorem: Page's theorem permits no exceptional zero. The available mathlib APIs do not
resolve the ambiguity. The pinned environment contains `DirichletCharacter.LFunction`,
`DirichletCharacter.IsPrimitive`, and the neighboring nonvanishing theorem on `re s >= 1`, but no
repo-local Landau-Page declaration or source-frozen target was found.

Therefore no canonical Lean expression, minimal-import claim, expression fingerprint, checked
alternate encoding, or meaningful removed-hypothesis/domain/binder/boundary mutation suite can be
produced. No abstract predicate, assumed Page theorem, `sorry`, axiom, placeholder, weakened case,
or broadened theorem was introduced. The statement node remains blocked at `M4`; audit completion
and theorem completion remain false.

## Pinned environment and validation

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. Existing `.lake` artifacts were read only; no update,
build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0502` | 0 | rank 682; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese title, English gloss, Page 1935, and the paper title | 0 | found only the underspecified source metadata and this intake dossier; no exact proposition |
| pinned-mathlib `rg` search for Landau-Page, Page's theorem, and exceptional real zeros/characters | 1 | no theorem-specific match; exit 1 is ripgrep's no-match result |
| pinned-mathlib `rg` search for Dirichlet-character conductor, primitivity, and L-function APIs | 0 | nearby substrate exists, but it does not select an exact Page statement |

There is no applicable `lake env lean <statement>.lean` check: the required exact expression is
what the missing source decision prevents. Re-running `IntakeProbe.lean` would only recheck nearby
APIs and cannot validate this phase's deliverable.

## Retry condition

An accountable source review must select an immutable edition or scan of Page's primary paper (or
explicitly authorize a precisely cited modern formulation), give the theorem/page and exact
wording, resolve errata, and freeze every family, conductor, constant, region, endpoint, and
uniqueness choice above. A later statement run can then encode that exact proposition, determine
the minimal pinned imports, preserve its elaborated expression and environment fingerprint, add
checked transports, and perform the four required structural mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

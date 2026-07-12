# Exact-statement gate: blocked

Item: `S56-M-0174-STATEMENT`

Theorem: `THM-M-0174`

Base revision: `c5e497a7dda44b669ff85eaf30ad2ec5da8085c3`

## Decision

No exact Lean 4 target can yet be truthfully elaborated. The accepted input is only a provisional
intake whose conventional human scope says that, for a closed oriented smooth `4k`-manifold, the
signature of the middle-dimensional intersection pairing equals evaluation of the top-degree
Hirzebruch `L`-class on the fundamental class. The intake explicitly leaves the pinpoint source,
incorporated definitions, and exact conventions open.

Those open choices change the proposition: connectedness and empty-manifold conventions;
cohomology coefficients; the intersection-form sign; the orientation and fundamental-class model;
Pontryagin-class and `L`-polynomial normalization; the rational-to-integer bridge; the `k = 0`
case; and binder order are all unfrozen. Selecting them without source review would invent the
canonical statement rather than elaborate it.

The pinned Lean closure also does not provide the concrete interfaces needed to express that claim
non-tautologically. It has `BoundarylessManifold` and algebraic quadratic-form invariants
`sigPos` and `sigNeg` for quadratic forms, but the scoped search found no Hirzebruch
signature theorem, Pontryagin-class or Hirzebruch `L`-class package, closed-oriented-manifold
fundamental-class evaluation, Poincare duality, or canonical manifold intersection form. An
abstract record supplying either side or their equality would be a prohibited substitution.

Consequently there is no canonical declaration/expression, normalized expression hash, minimal
import set, checked alternate transport, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutation suite. Machine state remains `M4`; no statement, proof, audit,
or theorem-completion credit is claimed. `StatementProbe.lean` checks only the two available
substrate families and is explicitly not a theorem statement.

## Pinned environment and validation

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The reused `.lake` tree was read only; no update, build,
clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0174` | 0 | Rank 668, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| exact repository and pinned-mathlib `rg` searches for the theorem, Pontryagin classes, `L`-class, fundamental-class, Poincare-duality, and intersection-form APIs | mixed 0/1 | Only adjacent repo audit notes and unrelated uses were found; no concrete target surface was located (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0174/StatementProbe.lean` | 0 | Both minimal imports elaborated; printed the checked boundaryless-manifold and quadratic-signature declarations |
| `python3 -m json.tool Stage1_Instances/THM-M-0174/statement-blocker.json` | 0 | Blocker record is valid JSON |
| direct placeholder and trailing-whitespace assertions over the three statement artifacts | 0 | No forbidden proof placeholder and no trailing whitespace found |
| `git diff --check -- Stage1_Instances/THM-M-0174` | 0 | No whitespace errors |

## Retry condition

An accountable review must select and hash an immutable primary-source edition, transcribe the
exact theorem and incorporated definitions, resolve all conventions and degenerate cases above,
audit errata, and independently approve the mapping. The missing concrete Lean interfaces must
then be implemented or supplied by pinned imports without assuming the desired equality. A later
statement run can minimize imports, elaborate and fingerprint the exact target, check alternate
transports, and run all four mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

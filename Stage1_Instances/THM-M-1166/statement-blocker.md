# Exact-statement gate: blocked

Item: `S56-M-1166-STATEMENT`  
Theorem: `THM-M-1166`  
Base revision: `26c19e81aed0ce63fa6787c9db5d397a36f0fb4c`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical wording is the title `椭圆型方程` (elliptic equations) and the phrase
`二阶椭圆型方程的理论` (the theory of second-order elliptic equations). This names a field rather
than one truth-valued theorem. No primary source, edition, theorem/page, formula, or quantified
claim is identified, and the Stage0 record explicitly leaves the proof or observation to be
supplied.

The missing choices change the proposition rather than merely its notation:

- linear, quasilinear, scalar, or system operator, and divergence or non-divergence form;
- ambient dimension, domain and boundary regularity, and coefficient class;
- ellipticity notion and constant, including whether degeneracy is excluded;
- weak, strong, viscosity, or classical solution notion, forcing, and boundary data;
- existence, uniqueness, maximum principle, regularity, representation, or quantitative estimate
  as the conclusion, with its spaces, exponents, constants, and endpoint cases.

These alternatives are inequivalent. In particular, choosing a maximum principle or a Dirichlet
solvability theorem would substitute one result from the named theory, while choosing Schauder
estimates would also absorb the separately scheduled `THM-M-1167`. The accepted intake dependency
therefore correctly leaves the canonical human claim null and classifies the statement as
source-blocked.

Consequently this phase fails at canonical claim identity, before minimal imports, ordered Lean
binders, fixed universes and typeclass context, an elaborated expression fingerprint, checked
alternate encodings, or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be established. No arbitrary abstract predicate, axiom, placeholder,
or convenient special theorem was introduced. The statement node remains open at `M4`; no
statement or theorem completion is claimed.

## Discovery boundary

Repository-wide discovery found only the same catalogue phrase in
`Docs/researches/math_theorems.md` and its Stage0 projection. The target manifest and generated
checklist repeat metadata but do not supply mathematical content. A terminology search of the
pinned mathlib Lean sources found no match for `elliptic equation`, `elliptic operator`, `elliptic
PDE`, `uniformly elliptic`, or `strong maximum principle`. This negative search is discovery
evidence only: even a library candidate could not select which source theorem this target means.

There is no applicable `lake env lean <target>.lean` elaboration check because the expression such
a file would contain is exactly what the source fails to determine. Elaborating a freely selected
proxy would be fake statement evidence, not validation of the assigned deliverable.

## Pinned environment and validation

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). Existing canonical `.lake`
artifacts were read only; no update, build, clone, fetch, or dependency mutation was performed.

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
| `python3 scripts/stage1_target.py show THM-M-1166` | 0 | Rank 369, planned lifecycle, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the theorem ID, Chinese title, and catalogue phrase | 0 | Only the underspecified catalogue source and Stage0 projection supplied mathematical wording |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| pinned-mathlib `rg` search for elliptic equations, operators, PDEs, uniform ellipticity, and the strong maximum principle | 0 | No matching Lean source was found |

## Retry condition

An accountable source reviewer must pin an immutable primary or authoritative scholarly source by
edition and exact theorem/page, then freeze one displayed theorem with its operator, dimension,
domain, coefficient and ellipticity assumptions, solution notion, data, ordered quantifiers,
conclusion, constants, and boundary or degenerate cases. The selection must be cross-checked against
neighboring targets, especially `THM-M-1167`, and record relevant errata. A later statement worker
can then encode that exact proposition, minimize its pinned imports, serialize and hash the
elaborated expression and environment, compile any credited transports, and execute all four
required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate. Therefore no
`.stage1-worker-selftest.json` is emitted.

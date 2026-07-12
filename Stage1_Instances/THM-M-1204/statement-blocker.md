# Exact-statement gate: blocked

Item: `S56-M-1204-STATEMENT`  
Theorem: `THM-M-1204`  
Base revision: `446f3e80e7a93deeca70150fa80d9ee079ee0586`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
complete target metadata is the title "Kruzkov theorem", the gloss "entropy solutions of
multidimensional conservation laws", the attribution Stanislav Kruzkov, and the year 1970. The
intake identifies Kruzkov's 1970 paper as a discovery source, but no immutable source copy,
theorem/page pinpoint, inspected wording, translation, or errata record is present. In particular,
the record does not fix:

- whether the root is existence, uniqueness, a comparison/stability estimate, or a packaged
  well-posedness theorem;
- the spatial dimension, time-space domain, scalar flux and its precise regularity;
- the initial-data space, boundedness or integrability assumptions, and representative/equality
  convention;
- the weak/distributional equation, test-function class, entropy inequalities and their signs;
- the initial-trace and time-continuity formulation;
- whether the contraction estimate is global or local with finite propagation; or
- ordered binders, every premise, the exact conclusion, and degenerate boundary cases.

These choices distinguish materially different propositions. Selecting a familiar modern
formulation, narrowing the result to uniqueness, or packaging an assumed `EntropySolution`
predicate with the desired result as a field would substitute or assume the theorem rather than
elaborate the exact source claim.

The canonical human-claim identity therefore fails before minimal imports, elaborated-expression
fingerprinting, checked transports, or removed-hypothesis, changed-domain, binder-scope, and
boundary-case mutations can be meaningful. No Lean declaration, axiom, proof placeholder,
weakened special case, or broadened theorem was introduced. Machine debt remains `M4`; statement
acceptance and theorem completion are false.

## Pinned environment and scoped checks

Commands were run inside this worker clone on 2026-07-12 (Asia/Shanghai). The clone's
`Formalizations/Lean/.lake` is a pre-existing symlink to the canonical pinned artifacts and was
used read-only. No update, build, dependency clone, or fetch was run.

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
| `python3 scripts/stage1_target.py show THM-M-1204` | 0 | Rank 398, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the target ID, Chinese title/gloss, English gloss, and Kruzkov spellings | 0 | Found only underspecified metadata, this intake, and unrelated legacy discovery mentions; no source-frozen proposition for this target |
| pinned-mathlib `rg` search for Kruzkov spellings, entropy solutions/conditions, conservation laws, and weak solutions | 0 | Found only a generic documentation mention of weak PDE solutions; no matching conservation-law target |

There is no applicable `lake env lean <target>.lean` elaboration command because no exact expression
exists. Compiling one arbitrarily selected interpretation would be false statement evidence, not
the assigned deliverable.

## Retry condition

An accountable source review must select an immutable edition of Kruzkov's primary paper and an
exact theorem/page, inspect and record errata, provide the exact wording and translation, and freeze
every equation, domain, flux, solution-space, entropy, trace, quantifier, premise, conclusion, and
boundary choice listed above. A later statement run can then encode that exact Lean expression,
minimize pinned imports, fingerprint the elaboration and environment, compile checked transports,
and execute all four mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

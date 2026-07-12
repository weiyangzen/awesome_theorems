# Exact-statement gate: blocked

Item: `S56-M-1201-STATEMENT`  
Theorem: `THM-M-1201`  
Base revision: `bffb5c63a3a8b89fc36a28a72eed61be8fc4d16a`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
complete target metadata is the title "entropy condition", the gloss "condition for uniqueness of
weak solutions", the attribution Peter Lax, and the year 1971. It supplies no primary-source
theorem/page or exact mathematical wording. In particular, it does not fix:

- a scalar conservation law or a system, the spatial dimension, the flux, or its regularity;
- the time-space domain, initial or boundary data, and the weak-solution function space;
- a distributional formulation and initial-trace convention;
- an entropy/entropy-flux pair, quantification over entropies or constants, or an admissibility
  inequality;
- whether the claimed root is an individual-shock criterion, uniqueness in an entropy class, an
  `L1` contraction/comparison estimate, or a full existence-and-uniqueness result; or
- ordered binders, every hypothesis, the equality notion, and boundary or degenerate cases.

The intake identifies two incompatible readings. Lax's 1971 *Shock waves and entropy* is only a
bibliographic discovery candidate and may concern shock admissibility for hyperbolic systems.
Kruzkov's 1970 scalar theory is a closer match to the uniqueness gloss, but conflicts with the
recorded author and year. Neither citation is pinpointed to an inspected theorem. Moreover, the
repository schedules Lax shock admissibility, Oleinik's scalar condition, and Kruzkov's theorem as
the separate targets `THM-M-1202`, `THM-M-1203`, and `THM-M-1204`. Selecting any of them here would
broaden, duplicate, or substitute the assigned theorem.

The canonical human-claim identity therefore fails before minimal imports, elaboration, expression
fingerprinting, checked transports, or the required removed-hypothesis, changed-domain,
binder-scope, and boundary-case mutations can be meaningful. No Lean declaration, axiom,
placeholder, assumed uniqueness field, weakened special case, or broadened theorem was introduced.
Machine debt remains `M4`; statement acceptance and theorem completion are false.

## Pinned environment and scoped checks

Commands were run inside this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake`
directory was used read-only. No update, build, clone, fetch, or other dependency mutation was run.

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
| `python3 scripts/stage1_target.py show THM-M-1201` | 0 | Rank 395, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the target ID, Chinese title/gloss, English gloss, entropy-condition terms, Lax, and Kruzkov | 0 | Found only underspecified metadata, this intake, legacy discovery notes, and separately owned neighboring targets; no source-frozen proposition for this target |
| pinned-mathlib `rg` search for entropy solutions/conditions, weak solutions, conservation laws, Kruzkov, and Lax shocks | 0 | Found only a generic documentation mention of weak PDE solutions; no theorem-specific conservation-law target matching the unresolved claim |

There is no applicable `lake env lean <target>.lean` elaboration command because no exact
expression exists. Elaborating one selected interpretation or an abstract interface that assumes
the desired uniqueness would be fake statement evidence, not the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, inspect and record errata, and freeze every PDE, flux, domain, solution-space,
entropy, trace, quantifier, hypothesis, conclusion, and boundary choice listed above. It must also
resolve the conflict between the Lax attribution and the Kruzkov-like uniqueness gloss and explain
the boundary with `THM-M-1202` through `THM-M-1204`. A later statement run can then encode the exact
Lean expression, minimize pinned imports, fingerprint the elaboration and environment, compile
checked transports, and execute all four mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

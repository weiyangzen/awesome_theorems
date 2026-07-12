# Exact-statement gate: blocked

Item: `S56-M-1126-STATEMENT`  
Theorem: `THM-M-1126`  
Base revision: `df2787679a822d5d86d0142bb5f14f3d6691e66d`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository's source record. The only
mathematical wording is "solution of the one-dimensional wave equation", accompanied by the title
"wave equation", attribution to Jean le Rond d'Alembert, and the year 1746. No primary-source
edition, theorem/page, exact equation, assumptions, or conclusion is identified.

The phrase does not determine:

- the equation, sign convention, wave speed, scalar field, or spatial and temporal domains;
- the classical, strong, weak, or distributional solution notion and required regularity;
- initial or boundary data, compatibility conditions, and the time interval;
- whether the claimed result is existence, uniqueness, representation, energy conservation,
  regularity, or finite propagation;
- the treatment of zero wave speed, endpoints, zero/constant data, or time orientation.

These choices change the domains, binders, hypotheses, and conclusion. Choosing the Cauchy problem
on `Real`, a bounded or periodic problem, a uniqueness theorem, or a formula would therefore invent
or substitute mathematics. In particular, the immediately adjacent `THM-M-1127` is separately
named "d'Alembert formula" and described as the general solution of the one-dimensional wave
equation. Importing that formula as this target would collapse two repository IDs contrary to the
intake's frozen exclusion.

The metadata label `已验证` is untrusted and supplies neither a human source nor kernel evidence.
Consequently the canonical human claim fails before minimal imports, an elaborated expression
fingerprint, checked transports, or meaningful removed-hypothesis, changed-domain, binder-scope,
and boundary mutations can be produced. No Lean declaration, axiom, placeholder, broadened target,
or weakened special case was introduced. Machine state remains `M4`; statement acceptance and
theorem completion are false.

## Pinned environment and narrow validation

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). The canonical shared `.lake`
artifacts were read only; no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1126` | 0 | Rank 331, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for the Chinese/English title, source wording, and d'Alembert formula | 0 | 49 metadata and related-target matches; none supplies a source-frozen proposition for `THM-M-1126` |
| pinned-mathlib `rg` search for wave-equation and d'Alembert-formula names | 1 | No matches (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check: an exact target expression does not
exist. Elaborating an arbitrary PDE interface or assuming a solution predicate would be fake
statement evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact theorem/page,
resolve relevant errata, and freeze every equation, domain, regularity, data, compatibility,
solution, conclusion, and boundary choice above. It must also explain the boundary with
`THM-M-1127`. A later statement run can then encode that exact claim, minimize pinned imports,
fingerprint the elaborated expression, add checked transports, and run the four structural mutation
classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.

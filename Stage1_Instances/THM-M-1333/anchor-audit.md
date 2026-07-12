# Anchor audit

Cutoff: 2026-07-12 (Asia/Shanghai). The target is the exact continuity-only proposition frozen in
`Statement.lean`. Searches followed the rev-5.6 order: repo-local Lean, pinned mathlib, then public
external discovery. The structured inventory and exact query limitations are in
`anchor-audit.json`.

## Result

No exact Lean 4 proof candidate was found. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the closest declarations are
`IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt` and its zero-radius variant in
`Mathlib.Analysis.ODE.PicardLindelof`. They produce the right general shape of differential
conclusion on a closed interval, but their `IsPicardLindelof` input contains a uniform spatial
`LipschitzOnWith` premise, separate time continuity, a norm bound, and a quantitative lifespan
condition. Joint continuity on an open neighborhood does not supply the Lipschitz premise. Using
either candidate would therefore substitute Picard-Lindelof for Peano and is ineligible.

`AnchorAudit.lean` checks the declarations, prints their kernel dependency reports, and checks a probe
that exposes the extra Lipschitz field. The reports are `propext`, `Classical.choice`, and
`Quot.sound`; these are recorded as foundation dependencies, not placeholders. No local wrapper or
proof of `PeanoExistenceTarget` was found.

## External boundary

Anonymous GitHub repository search was replayed for Peano, Cauchy-Peano, and ODE aliases and
returned zero repositories. This is weak discovery evidence because repository search does not
search all code. The two grep.app code-search requests were rejected with HTTP 429. That access
failure is recorded rather than converted into a false negative. Consequently this audit claims a
classified bounded inventory, not exhaustive global discovery.

The truthful machine classification remains `M4`: the exact target elaborates, but no exact proof
candidate is integrated or independently checkable. The theorem is not proved or complete.

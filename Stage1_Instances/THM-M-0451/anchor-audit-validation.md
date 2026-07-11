# Anchor-audit validation

Item: `S56-M-0451-ANCHOR_AUDIT`  
Base revision: `9d8b8be1a0c1e013c78877b464b9999df60cc910`  
Audit cutoff: 2026-07-12 (Asia/Shanghai)

## Result

All four candidates in the frozen audit inventory are classified. The exact local declaration is
only a proposition definition. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the rational-point group, `xRep`, global
number-field logarithmic height, height nonnegativity, and the torsion predicate. The checked probes
in `AnchorAudit.lean` confirm those types and the identity-point coordinate convention, but mathlib
contains no terminal Neron-Tate or elliptic canonical-height declaration.

The strongest credible external Lean 4 source is
`MichaelStollBayreuth/Heights@688bdb63259556fab4b0f699ce0d10bd2dce23f6`. Its immutable archive
and `Heights/EllipticCurve.lean` were previously content-addressed as
`09e8bd85...33d27` and `1c7a36c8...c2a3`. The source supplies `Point.naiveHeight`, an approximate
parallelogram estimate, finite-height infrastructure, and conditional Mordell-Weil descent. Its
recorded term audit found no `NeronTate`, `canonicalHeight`, `canonical height`, or `Tate height`
surface. It targets Lean `v4.30.0-rc2` and mathlib `6f66e004...d940`, is not a pinned dependency,
and does not prove the exact package in any case.

Consequently the root remains `[H1, M3, R3]`. This is a bounded formal-anchor audit, not theorem
completion and not proof that no Lean implementation exists anywhere. A fresh GitHub immutable
archive request timed out after 30 seconds, so global public-search saturation is explicitly not
claimed.

## Commands and exact results

All repository commands ran in this worker clone. Lean reused the existing canonical `.lake`
artifacts read-only; no update, fetch, clone, dependency build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0451` | 0 | rank 93, planned, rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386...`, tree `bdc39a3...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib grep -n -i -E 'n[eé]ron\|neron\|canonical.?height\|hat.?height\|height.*elliptic\|elliptic.*height' HEAD -- '*.lean'` | 0 | only unrelated order-theory text about finite height; no terminal candidate |
| `rg` with the same alias family over all installed pinned Lake dependencies | 1 | no relevant terminal candidate; exit 1 is the expected no-match result |
| `curl -I -L --max-time 30 https://github.com/MichaelStollBayreuth/Heights/archive/688bdb63259556fab4b0f699ce0d10bd2dce23f6.tar.gz` | 28 | connection timed out; recorded as access limitation, not negative discovery evidence |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0451/AnchorAudit.lean` | 0 | six pinned substrate probes and two checked wrappers elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0451/Statement.lean` | 0 | exact statement re-elaborated; no package inhabitant introduced |
| `python3 Stage1_Instances/THM-M-0451/check_anchor_audit.py` | 0 | 4/4 inventory rows, local statement hash, three mathlib hashes, pin, and probe coverage agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-0451/anchor-audit.json >/dev/null` | 0 | structured audit parsed |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)' Stage1_Instances/THM-M-0451` | 1 | no prohibited Lean declarations; exit 1 means no match |
| `git diff --check -- Stage1_Instances/THM-M-0451 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open integration gate

Reopen the candidate inventory when a concrete Lean 4 canonical-height implementation is located
with an immutable revision, toolchain, license, module, terminal proof body, exact normalized type,
and an adapter to the frozen `xHeight / 2` normalization. Until it is pinned/imported and checked,
neither adjacent height infrastructure nor the historical statement surface earns `M1` or `M0`.

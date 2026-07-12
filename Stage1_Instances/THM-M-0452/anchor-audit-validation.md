# Anchor-audit validation

Item: `S56-M-0452-ANCHOR_AUDIT`  
Base revision: `3699e5855e919efdcfc83019c12ef3b883b026f2`  
Audit cutoff: 2026-07-12 (Asia/Shanghai)

## Result

All four candidates in the frozen formal-anchor inventory are classified. The exact local
declaration is only a proposition definition. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides elliptic rational points, the selected
logarithmic x-height, its nonnegativity, the torsion subgroup, and the quotient constructor. The
checked probes in `AnchorAudit.lean` confirm these types, torsion membership, and the identity-point
coordinate convention. They do not provide the canonical height or its pairing.

The historical `NeronTateHeightPairingAPI` is a weaker interface whose wrappers assume an instance.
The strongest credible external Lean 4 source audited is
`MichaelStollBayreuth/Heights@688bdb63259556fab4b0f699ce0d10bd2dce23f6`. A fresh immutable
archive download reproduced SHA-256 `09e8bd85...33d27`, and its `Heights/EllipticCurve.lean`
reproduced `1c7a36c8...c2a3`. The source supplies `Point.naiveHeight`, an approximate parallelogram
estimate, finite-height infrastructure, and conditional Mordell-Weil descent. The complete alias
search found no Neron-Tate, canonical-height, height-pairing, or Tate-height surface. It also targets
Lean `v4.30.0-rc2` and mathlib `6f66e004...d940`, rather than this repository's pinned stack.

Consequently the root remains `[H1, M3, R3]`. This is a bounded candidate audit, not theorem
completion and not proof that no Lean implementation exists anywhere. No exhaustive public code
search is claimed.

## Commands and exact results

All repository commands ran in this worker clone. Lean reused the existing canonical `.lake`
artifacts read-only; no update, fetch, clone, dependency build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0452` | 0 | rank 301, planned, rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386...`, tree `bdc39a3...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib grep -n -i` with the frozen alias family at `HEAD -- '*.lean'` | 1 | expected no-match result; no terminal candidate |
| `rg` with the alias family over all installed pinned Lake dependencies | 1 | expected no-match result for a terminal candidate |
| `curl -L --fail --max-time 60` for the immutable Heights commit archive, then `sha256sum`, extraction, alias search, and targeted declaration inspection in a temporary directory | 0 | archive and file hashes reproduced; adjacent declarations found; no terminal alias; temporary directory removed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0452/AnchorAudit.lean` | 0 | ten pinned declarations/wrappers elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0452/Statement.lean` | 0 | exact statement re-elaborated; no package inhabitant introduced |
| `python3 Stage1_Instances/THM-M-0452/check_anchor_audit.py` | 0 | 4/4 candidates, statement hash, four mathlib source hashes/blobs, pin, and probe coverage agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-0452/anchor-audit.json >/dev/null` | 0 | structured audit parsed |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)' Stage1_Instances/THM-M-0452` | 1 | expected no-match result; no prohibited Lean declarations |
| `git diff --check -- Stage1_Instances/THM-M-0452 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open integration gate

Reopen the inventory when a concrete Lean 4 implementation is located with an immutable revision,
toolchain, license, module, terminal body, exact normalization, and an adapter to the frozen package.
Until it is pinned/imported and checked, neither a statement interface nor adjacent height
infrastructure earns `M1` or `M0`.

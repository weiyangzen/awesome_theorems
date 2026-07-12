# Anchor-audit validation record

Item: `S56-M-0468-ANCHOR_AUDIT`  
Base revision: `afa4c955de308129aa8a2e0882fa02fde43fedbe`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The exact frozen target remains only the proposition
`Stage1Instances.THM_M_0468.BogomolovTarget`. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides genuine early
abelian-variety infrastructure in `Mathlib.AlgebraicGeometry.Group.Abelian`:
the checked theorem says a proper geometrically integral group scheme over a
field is commutative. It does not provide canonical heights, small-point
loci, special subvarieties, or the Bogomolov conclusion. A bounded scan of
repo-local and all materialized pinned Lean sources found no terminal candidate.

Public Sourcegraph search found no `Bogomolov` Lean match. It did locate
Neron-Tate work in `facebookresearch/atlas-lean` at immutable indexed commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`; direct immutable-source inspection
found only elliptic-curve height infrastructure, and its named parallelogram
theorem ends in `sorry`. The separately audited
`MichaelStollBayreuth/Heights@688bdb63259556fab4b0f699ce0d10bd2dce23f6`
has checked naive-height and conditional Mordell-Weil support, but no canonical
height or Bogomolov theorem and a different toolchain. Neither is an exact
proof candidate. GitHub code search was credential/rate-limit blocked, so no
negative result is claimed for that lane.

The exact root therefore remains `M4` formalization debt. This completed,
bounded anchor inventory does not claim exhaustive global discovery, audit
completion, or theorem completion.

## Commands and results

All Lean commands used the existing pinned `.lake` artifacts. No dependency
update, build, clone, fetch, or installation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0468/AnchorAudit.lean` | 0 | pinned abelian-variety support theorem and four related interfaces elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0468/Statement.lean` | 0 | exact frozen target and statement transport re-elaborated |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | target fingerprint, manifest pin, installed mathlib HEAD, module hash, four candidates, and fail-closed boundary agreed |
| `rg -n -i --glob '*.lean' 'Bogomolov|Neron.?Tate|canonical.?height|small.?points|equidistribution' ...` | 0 | repo-local statement boundaries and height-related support found; no exact Bogomolov proof body in materialized pinned dependencies |
| Sourcegraph public searches for `Bogomolov`, `NeronTate`, and `canonicalHeight` in Lean | 0 | zero Bogomolov matches; one external project for Neron-Tate/canonical height; response hashes recorded in `anchor-audit.json` |
| immutable raw-file inspection of `facebookresearch/atlas-lean@34ffed3...` | 0 | Lean v4.29.0 and same mathlib pin; height module SHA-256 `8a34a66b...b6068`; named parallelogram result is admitted |
| immutable raw-file inspection of `MichaelStollBayreuth/Heights@688bdb6...` | 0 | Lean v4.30.0-rc2, mathlib `6f66e004...`; module SHA-256 `1c7a36c8...c2a3`; naive-height support only |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | rank 314; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0468/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0468 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open integration gate

Reopen integration only for a concrete Lean 4 candidate with repository URL,
immutable commit, toolchain and dependency graph, module, exact declaration and
normalized type, license, terminal body provenance, and a successful local
wrapper check. Until then, neither external anchor is proof credit and no
`M0`, full-audit, or theorem-completion claim is valid.

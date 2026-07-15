# THM-M-0034 proof-phase recheck at `fd020d65`

Item: `S56-M-0034-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `fd020d65a412e2c870f4bac1fefb9ea4ed5f5fd8`

Base tree: `5fce2f82823f95e5aa2ce97bd08b22091f96aeda`

## Verdict

`blocked`. A real Lean proof of the exact frozen target exists and was replayed, but no legal
repo-local proof integration can be made from the selected external source. The immutable
`edmund-ukaisi/QuillenSuslin` revision
`e8d85a6f6fa210ba0be12bd02aa22009699f0c35` contains no `LICENSE`, `LICENCE`, `COPYING`, `NOTICE`,
repository license metadata, or other permission grant. It is also absent from the pinned Lake
dependency graph. Copying its proof closure into the owned path would therefore violate the
supply-chain gate rather than complete it.

The exact external theorem is `QuillenSuslin.quillenSuslin` from
`QuillenSuslin.Theorem`. It has the same field, `Fin n`, finite-projective module, independent
universe, and `Module.Free` conclusion as the canonical target, and is stronger only by including
`n = 0`. Its exact checked adapter is:

```lean
theorem quillenSuslinTarget : QuillenSuslinTarget.{u, v} := by
  intro k _ n _ P _ _ _ _
  exact QuillenSuslin.quillenSuslin n P
```

A fresh 53-module source replay against the canonical Lean 4.29.0 and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` artifacts succeeded. The terminal theorem and exact
adapter both report only `propext`, `Classical.choice`, and `Quot.sound`. The replayed terminal
object has SHA-256 `792186c7df750895f1e76f58c432799b02e36f91f5c7b46e30d4afb620fbd3ea`,
and the two-line axiom output has SHA-256
`cb19136bb2f69b9ab349230a647ade69be6e72a94d5792e0988f24a382e35e8c`. The external project's
lexer-aware scan reports zero live `sorry`, `#exit`, `native_decide`, or `axiom` tokens across all
76 production files.

This is technical `M1` evidence, not licensed repo-local closure. No external source, proof body,
dependency, wrapper, registry, typed graph, or accepted receipt was added. The item remains `[ ]`,
the lifecycle remains `planned`, and the accepted root remains `[H1, M3, R4]`. Audit completion,
theorem completion, validation, release, and master acceptance are not claimed. Because the proof
phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Current Upstream Recheck

The current public default branch is still `dev`. Its codeload archive has SHA-256
`2678e001a8dcc331ad0c98f4b2562c8aea19a0bed81986a9e96e173d682ff9e1`; the theorem source remains
byte-identical at SHA-256 `15496d2272b3d481d0158a0c18cf4444d03376dc24edd085d797f29b4317cd4c`,
the toolchain remains `leanprover/lean4:v4.29.0`, and a recursive scan again found zero license
artifacts. Repository metadata still reports no license. The prior reopen condition has therefore
not occurred.

The first failed gate is `M0034-X-LICENSE`. The immediate root cut set remains
`M0034-X-LICENSE` and `M0034-X-EXTERNAL-BODY`. Reopen after an explicit compatible license grant
allows immutable pinning or vendoring of the audited revision, then place its 53-module theorem
closure in the repository validation closure and replay the exact adapter. An independently
implemented repo-local proof that does not copy the unlicensed source is the other valid route.

## Validation

All repository checks ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts. No `lake update`,
`lake build`, dependency clone/fetch, checkout, or `.lake` repair was run. Network use was limited
to read-only upstream metadata and codeload rechecking; it did not acquire or install a dependency.
The dirty symlink and external replay make this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0034` | 0 | Rank 1078; planned; `L0/rework_required`; theorem incomplete. |
| Fresh 53-module `lake env lean` replay and exact adapter | 0 | Terminal theorem and canonical adapter elaborated; each reports exactly `[propext, Classical.choice, Quot.sound]`. |
| Current `dev` codeload hash/source/toolchain/license scan | 0 | Archive `2678e001...ff9e1`; theorem `15496d22...d4c`; Lean v4.29.0; zero license artifacts. |
| Fresh temporary `Statement.olean`, then `lake env lean --trust=0 -t0` on `ObligationTree.lean` | 0 | The exact statement and conditional composition declarations elaborated; this is interface evidence only, with no root-body credit. |
| `python3 -B Stage1_Instances/THM-M-0034/check_obligation_tree.py` | 1 | Known stale-validator failure: `instance.json.owned_artifacts` omits the already integrated `proof-blocker.json` and `proof-validation.md`, so the exact file-set assertion at line 247 fails. |
| Scoped prohibited-declaration scan over owned Lean files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, bodyless axiom, or unsafe declaration. |
| `python3 -m json.tool Stage1_Instances/THM-M-0034/proof-recheck-2026-07-15-head-fd020d65-slot49.json` | 0 | The current-base blocker packet is valid JSON. |
| Scoped whitespace checks | 0 | No whitespace diagnostics in either new owned artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion packet. |

The obligation-tree validator failure is pre-existing reconciliation debt, not proof evidence. Its
exact owned-file assertion became stale when the earlier blocker pair was integrated. The frozen
typed graph also predates the successful technical replay and still describes the candidate as
locally unreplayed. This proof-only recheck does not rewrite prerequisite authority artifacts to
make them agree with a failed proof phase; the integration lane must reconcile them before future
node acceptance.

The checked inputs include `Statement.lean` SHA-256
`cfdfeabe825f5b7936905cee310c2306dba8b18a4b25281fb09c7d10719b79e8`, obligation-registry
SHA-256 `de388aac08659553285062670f11ef3c68d0fa5539c6c575e6e8744fa1a1e133`, typed-graphs SHA-256
`fa5cfa00873556291a783b7376d3cb0d949cfc36b4d6a9bcf34e8c96d90e3c0b`, and Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

This is durable blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0034-PROOF` and does not support a provisional or accepted item state.

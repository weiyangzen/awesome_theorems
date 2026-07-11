# Anchor-audit validation record

Item: `S56-M-0107-ANCHOR_AUDIT`  
Base revision: `bca606e3b3f7a0638b9d257751458c87a1ee5368`

## Verdict

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains two genuine partial
anchors for the frozen existential factorization target. The ZMT instance proves
`IsOpenImmersion f.toNormalization` under the four frozen hypotheses, and
`Scheme.Hom.toNormalization_fromNormalization` proves the required composition equation. The
source files have SHA-256 digests recorded in `anchor-audit.json`.

This is not exact root closure. An exploratory Lean check of
`IsFinite f.fromNormalization` under all four root hypotheses failed typeclass synthesis. The
pinned normalization is integral, but the audited API does not make its second map finite in this
generality. The old `S1_M_031.zariskiMain_mathlib_wrapper` wraps the related `03GW` theorem rather
than this root. No credible separate Lean repository was returned by the two GitHub repository
searches; unauthenticated GitHub code search was unavailable (HTTP 401). These limitations are
recorded rather than converted into a claim that no external formalization exists.

## Commands and results

Commands ran in this clone on 2026-07-12. Lean ran from `Formalizations/Lean` using the existing
pinned Lake environment. No dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0107` | 0 | Rank 31, planned, rework required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum .../ZariskisMainTheorem.lean .../Normalization.lean` | 0 | `73c910...4715` and `e14225...0122` |
| `lake env lean ../../Stage1_Instances/THM-M-0107/AnchorAudit.lean` | 0 | Printed the three exact candidate types; checked the open-immersion instance and composition equation |
| temporary `#print axioms` probe via `lake env lean` | 0 | Both named declarations report `propext`, `Classical.choice`, and `Quot.sound` |
| exploratory `example ... : IsFinite f.fromNormalization := by infer_instance` | 1 | Failed to synthesize `IsFinite f.fromNormalization`; removed from the passing audit module and retained as the actionable blocker |
| GitHub repository API searches for exact phrase and `zariskismain`, language Lean | 0 | Both returned `total_count 0` |
| unauthenticated GitHub code-search API query | 1 | HTTP 401; search limitation, not negative evidence |

The passing Lean module contains no proof of the root and no placeholder. Anchor audit is
self-tested, but master acceptance, obligation-tree, proof, validation, release, and theorem
completion remain open.

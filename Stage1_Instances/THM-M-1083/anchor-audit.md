# THM-M-1083 anchor audit

## Result

The pinned mathlib revision provides the exact Kolmogorov-condition substrate but no terminal
continuity theorem. A positive external Lean 4 candidate exists at immutable commit
`91885e6172648ea7f9c6a16b3a7069f92c88e023` in
`RemyDegenne/brownian-motion`: `ProbabilityTheory.exists_modification_holder` constructs one
fixed-time modification with every Holder exponent below `(q-d)/p`.

This is classified `M3`, not completion. Specializing it to the frozen target requires a checked
covering-number witness for the compact interval subtype, `p = alpha`, `q = 1 + beta`, `d = 1`,
and checked transports from `HolderOnWith ... univ` to `HolderWith`. More importantly, the project
uses Lean `v4.30.0-rc1` and mathlib `f233061...`, while this repository pins Lean `v4.29.0` and
mathlib `8a178386...`; the external module is not in the local Lake closure. Its body and
transitive axiom closure were therefore not kernel-checked here.

The complete structured inventory, statement comparisons, immutable hashes, query families, and
access limitations are in `anchor-audit.json`. No exhaustive global-discovery claim is made because
the unauthenticated GitHub tree/code-search surface returned HTTP 403.

## Validation

Commands below were run from the repository root on 2026-07-12. Exact outputs are summarized
without upgrading the theorem state.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1083/AnchorAudit.lean` (from `Formalizations/Lean`) | 0 | all six pinned-mathlib declarations elaborated; four axiom reports printed `Classical.choice`, `propext`, and `Quot.sound` only |
| `python3 -m json.tool Stage1_Instances/THM-M-1083/anchor-audit.json >/dev/null` | 0 | structured inventory valid JSON |
| `rg -n 'sorry|admit|axiom' /tmp/kc-jsdelivr` | 1 | no defensive placeholder token in the complete 81,626-byte immutable external source |
| `sha256sum /tmp/kc-jsdelivr /tmp/bm-manifest.json` | 0 | source `ce2b9dc...578a9`; manifest `23013991...07e02` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 blueprint/manifest standard passed |
| `python3 scripts/stage1_target.py check` | 0 | target manifest and Markdown projection passed |
| `python3 scripts/stage1_target.py show THM-M-1083` | 0 | rank 525; planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1083 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Status boundary: the anchor-audit phase is self-tested and awaits master acceptance. It supplies no
proof, obligation-tree, release, `AUDIT-Z`, or `THEOREM-Z` evidence.

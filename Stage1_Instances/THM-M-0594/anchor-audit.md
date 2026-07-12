# Anchor audit

Item: `S56-M-0594-ANCHOR_AUDIT`. Audit date: 2026-07-12. Worker base
revision: `ef4b7fa8a178497a72e8409648876ceefeb811f8`.

## Pinned mathlib result

The Lake manifest pins `leanprover-community/mathlib4` at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` under Lean 4.29.0. At that exact
revision, `Mathlib.Geometry.Manifold.WhitneyEmbedding` defines
`exists_embedding_euclidean_of_compact`. Its source requires `[CompactSpace M]`
and returns a smooth closed embedding with pointwise injective `mfderiv`.
The module header explicitly leaves the sigma-compact weak Whitney theorem as
a TODO.

`AnchorAudit.lean` checks a wrapper from this theorem to the checked expanded
form of `WhitneyEmbeddingTarget` after adding `CompactSpace M`. The only conclusion
transport is `IsClosedEmbedding.isEmbedding`. This proves that the candidate is
a genuine compact specialization, but also makes the failed root match
decisive: compactness is not a hypothesis of the canonical target.

The historical `S1_M_255.lean` wrapper has the same terminal mathlib body. It
is discovery evidence, not a second proof and not accepted rev-5.6 root credit.

## External Lean 4 result

Repository-local sources, pinned mathlib, and GitHub repository plus issue/PR
searches were checked for `Whitney embedding` and `WhitneyEmbedding`. No
credible external Lean 4 terminal proof of the unrestricted canonical target
was identified. GitHub search exposed `leanprover/lean-eval` PR 353, described
as a strong-Whitney *evaluation problem*; a benchmark prompt is not a checked
proof candidate. Since no external proof with an inspectable declaration and
immutable revision was found, none is recorded as anchor-only closure.

This is a reproducible bounded search result, not a universal claim that no
such project exists. A later candidate must supply an immutable commit, exact
declaration and type, toolchain, dependency/license feasibility, placeholder
and axiom audit, and terminal proof-body provenance before receiving credit.

## Validation record

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard agrees on 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | Rank 255, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0594/AnchorAudit.lean` | 0 | Exact compact wrapper elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]` |
| `rg -n '\\b(sorry|admit|axiom|proof_wanted)\\b' .../WhitneyEmbedding.lean Stage1_Instances/THM-M-0594/AnchorAudit.lean` | 1 (expected) | No prohibited marker in the upstream terminal source file or local audit wrapper |
| `python3 -m json.tool Stage1_Instances/THM-M-0594/anchor_candidates.json` | 0 | Structured candidate inventory is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0594 .stage1-worker-selftest.json` | 0 | No whitespace errors |

No `.lake` content was updated, built, fetched, cloned, or edited. The existing
pinned artifacts were used read-only.

## Verdict boundary

The anchor-audit phase is self-tested and pending master acceptance. The root
remains `[H1, M3, R3]`, `not_repo_local_closed`, with formalization debt. Audit
of candidates does not prove the theorem, and no theorem-completion or later
phase claim is made.

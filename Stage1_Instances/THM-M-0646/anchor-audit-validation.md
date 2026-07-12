# Anchor-audit validation

Item: `S56-M-0646-ANCHOR_AUDIT`  
Base revision: `83f5974d31f82ec4ad3b558c2e1c5078e070e986`  
Validation date: 2026-07-12

Commands were run in this worker clone using only the existing pinned Lake artifacts. No Lake
update/build, dependency fetch/clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, and execution skill passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0646` | 0 | Rank 692, planned lifecycle, theorem incomplete. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0646/Statement.lean` | 0 | Frozen target and existing checked transports re-elaborated. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0646/AnchorAudit.lean` | 0 | Four pinned declarations and two local witnesses elaborated; all printed axiom sets were `[propext, Classical.choice, Quot.sound]`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the manifest pin. |
| `rg -n 'exists_elementary(Embedding_card_eq_of_ge|Embedding_card_eq|ilyEquivalent_card_eq|Substructure_card_eq)' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Located the upward exact/stronger family and downward disambiguation theorem in pinned source. |
| `rg -n '\bsorry\b|\badmit\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib/ModelTheory/Satisfiability.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/ModelTheory/Skolem.lean` | 1 | Expected no-match result: no placeholder token in either pinned source module. |
| `curl ... sourcegraph.com/.api/search/stream ...` | 0 | Completed with six indexed matches across two repositories; response SHA-256 `a4b07421ee5bd7521550c7715e171412b0933c62f4a3e299f952077e199afde0`. |
| `curl ... api.github.com/search/repositories?q=...` | 0 | Quoted ASCII query returned `total_count=0`, complete; response SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2`. |
| `curl ... api.github.com/search/code?q=...` | 0 | HTTP 403 rate-limit response captured; SHA-256 `ff4efb0ee22ebccbed9a17ab9cd85163b6c2c7647b75dcb6d10241d5b357a6b4`; no negative result claimed. |
| `curl ... Foundation/archive/c28942b7...tar.gz` and source scan outside the repository | 0 | Immutable archive SHA-256 `477e6268...e935975`; only downward set-theory/countable-hull results, no matching upward target. |
| `git diff --check -- Stage1_Instances/THM-M-0646` | 0 | No whitespace errors. |

The exact mathlib candidate is eligible for `M0-W`, but this anchor-audit receipt does not accept
that machine state. The first remaining gate is the frozen obligation/provenance graph, followed by
proof, trust, validation, and master acceptance.

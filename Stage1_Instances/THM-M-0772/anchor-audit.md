# Formal candidate anchor audit

Item: `S56-M-0772-ANCHOR_AUDIT`  
Audit cutoff: 2026-07-12 (Asia/Shanghai)  
Repository base revision: `9c62e277cad936290d63af79d788d97dd17bf4cf`

## Frozen query scope

The exact target is the statement-phase proposition
`Stage1Instances.THM_M_0772.HausdorffMaximalPrinciple`: for every `P : Type u` with
`PartialOrder P`, there exists `c : Set P` satisfying `IsMaxChain (· ≤ ·) c`. Searches used
`Hausdorff maximal principle`, `Hausdorff maximality principle`, `maxChain`, `maxChain_spec`, and
`IsMaxChain`, including the common stronger formulation for an arbitrary binary relation.

Search order and surfaces were: this target's repo-local files; every installed pinned package
under `Formalizations/Lean/.lake/packages`; pinned mathlib source; then unauthenticated GitHub
repository and code search for public Lean projects. No dependency was fetched or updated.

## Frozen inventory and classification

| ID | Origin and immutable identity | Candidate | Exactness and provenance | Result |
|---|---|---|---|---|
| `C-LOCAL-01` | awesome_theorems tree at base revision above | `Statement.lean` | Statement and boundary checks only; it intentionally has no general proof body. | `M4`, not a closure candidate |
| `C-MATHLIB-01` | `leanprover-community/mathlib4`, commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, clean package tree; Git blob `b10b8b938ecff5db9c3c70cab7948746b06fefcd` | `Mathlib.Order.CompleteLattice.Chain.maxChain_spec` | Has type `IsMaxChain r (maxChain r)` for arbitrary `r`, hence specializes exactly to the frozen partial-order target. The terminal body is the theorem at source lines 107-110, built from `ChainClosure`, `SuccChain`, and classical selection used in the imported chain API. Source SHA-256: `074d91a7eb6be7f846e9fe468f9ff6a05f4e70cb2f04a13a6ba381ab726972a8`. Apache-2.0 via mathlib's repository license. | Eligible pinned mathlib anchor; direct adapter elaborates; provisional `M0-W` candidate, pending downstream proof/provenance acceptance |
| `C-MATHLIB-02` | same mathlib commit | `Mathlib.Order.Zorn.IsChain.exists_maxChain` | Produces a maximal chain containing an input chain, but its proof invokes `maxChain_spec`; it is a downstream wrapper/alias, not an independent terminal body. | Deduplicated under `C-MATHLIB-01` |
| `C-EXT-01` | public GitHub search as of cutoff | No distinct Lean 4 project discovered | Both exact-phrase repository queries returned zero repositories. Code search for `maxChain_spec` returned HTTP 403 due the unauthenticated API rate limit, so no exhaustive external-negative claim is made. | Access-limited negative result; no external candidate credited |

The mathlib source itself records that the construction was originally ported from Isabelle/HOL's
`HOL/Zorn.html`. That is useful historical provenance, but it is neither a distinct Lean 4
candidate nor repo-local Lean closure and receives no machine-proof credit here.

## Statement comparison and trust boundary

`maxChain_spec` is stronger than the target only in generality: it assumes no order laws on `r`.
Instantiating `r := (· ≤ ·)` supplies exactly the target witness and does not add, remove, or
reorder any target hypothesis. `AnchorAudit.lean` checks that adapter at the universe-polymorphic
target type. Both `#print axioms maxChain_spec` and `#print axioms ...mathlib_maxChain_spec_candidate`
report `[propext, Classical.choice, Quot.sound]`; no new axiom is introduced by the adapter. These
are ordinary mathlib classical-foundation dependencies, not proof placeholders. Full transitive
declaration/body hashes, TCB acceptance, and proof integration remain downstream gates.

The terminal source contains a concrete theorem body, not `sorry`, `axiom`, `unsafe`, or an external
oracle. A scoped text scan of the exact source file found no `sorry`, `admit`, `axiom`, or `unsafe`
token. This parser-adjacent inspection plus kernel elaboration is sufficient for anchor-audit
classification, but is not a release-grade transitive placeholder/provenance proof.

## Commands and exact results

All commands ran in this worker clone without modifying `.lake`.

| Command | Exit | Result |
|---|---:|---|
| `git rev-parse HEAD` | 0 | `9c62e277cad936290d63af79d788d97dd17bf4cf` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output (clean) |
| `git -C Formalizations/Lean/.lake/packages/mathlib ls-tree HEAD Mathlib/Order/CompleteLattice/Chain.lean` | 0 | blob `b10b8b938ecff5db9c3c70cab7948746b06fefcd` |
| `lake env lean ../../Stage1_Instances/THM-M-0772/AnchorAudit.lean` (from `Formalizations/Lean`) | 0 | exact adapter elaborated; terminal and adapter axiom sets both `[propext, Classical.choice, Quot.sound]` |
| `rg -n '\\b(sorry|admit|axiom|unsafe)\\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Order/CompleteLattice/Chain.lean` | 1 | no matching placeholder/trust-boundary token |
| GitHub repositories query for `"Hausdorff maximal principle" language:Lean` | 0 | HTTP 200 JSON, `total_count: 0`, response SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| GitHub repositories query for `"Hausdorff maximality principle" language:Lean` | 0 | HTTP 200 JSON, `total_count: 0`, same response SHA-256 |
| GitHub code query for `maxChain_spec language:Lean` | 0 (curl capture) | HTTP 403 rate-limit response; SHA-256 `ff4efb0ee22ebccbed9a17ab9cd85163b6c2c7647b75dcb6d10241d5b357a6b4` |
| Sourcegraph global archived/fork search for both names and `maxChain_spec`, `lang:Lean`, count 100 | 28 (curl timeout) | before the 30-second timeout it reported 9 matches: 6 in mathlib commit `12b4b4ad...` and 3 copied lines in Pygments test data commit `f1a91515...`; no distinct formal candidate. Partial response SHA-256 `0837af049a7d06e0594c7e8f6825e1f48c2e45f8c9c50ce6e6825413550d169a`; saturation not claimed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard OK: 15 groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `git diff --check -- Stage1_Instances/THM-M-0772` | 0 | no whitespace errors |

## Status boundary

The frozen four-entry inventory is fully classified, and the pinned mathlib candidate has a real
kernel elaboration receipt. This completes only the assigned anchor-audit proposal, pending master
acceptance. It does not complete the obligation-tree, proof, validation, or release phases; it does
not establish `AUDIT-Z` or `THEOREM-Z`; and it does not upgrade the instance's authoritative root
vector or lifecycle. The external search limitation is recorded rather than concealed, and no
distinct external candidate is credited.

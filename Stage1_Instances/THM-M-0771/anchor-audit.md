# THM-M-0771 anchor audit

Item: `S56-M-0771-ANCHOR_AUDIT`  
Intent: audit only  
Immutable mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`

## Scope and method

The audit is keyed to the statement-phase expression digest
`adeed39bf6f748a2f9deb3f75399b41e073f2edb84be65dad243c1aae11dfecd`. It searched the
existing pinned Lake package sources, without fetching or changing dependencies. The search terms
were `exists_wellOrder`, `WellOrderingRel`, `IsWellOrder.subtype_nonempty`, and the hyphenated and
unhyphenated English theorem name. All 11 package Git checkouts were recorded at their existing
revisions; only mathlib contained a defining candidate. Hits elsewhere merely consume mathlib's
declarations and therefore are not independent proof bodies.

## Candidate inventory

| ID | Immutable source anchor | Exact type and fit | Body provenance | Disposition |
|---|---|---|---|---|
| A1 | mathlib `Mathlib/SetTheory/Cardinal/Order.lean:524`, blob `c89ff6ad83317b9bb03929693ee47e668bc78c88` | `IsWellOrder.subtype_nonempty` gives the exact conclusion for arbitrary `alpha`; `mathlib_relation_candidate` checks its universal closure | packages `WellOrderingRel` with `WellOrderingRel.isWellOrder`; the relation pulls cardinal `<` back along the classically chosen `embeddingToCardinal` | preferred exact anchor |
| A2 | same module, line 529 and blob | `exists_wellOrder alpha` gives the exact bundled alternate frozen by the statement phase | constructs `linearOrderOfSTO WellOrderingRel` and supplies `WellOrderingRel.isWellOrder.toIsWellFounded` | secondary transport anchor |

The pinned source bodies contain no `sorry`, `admit`, new axiom declaration, or `unsafe`
declaration. Kernel reporting gives both wrappers and both upstream endpoints the same foundation
profile: `propext`, `Classical.choice`, and `Quot.sound`. This is expected classical choice, rather
than a placeholder-free constructive proof of choice.

## External result

No independent exact Lean 4 candidate was found in the other ten already-pinned package checkouts.
This is a bounded, reproducible dependency-closure audit, not a claim that every public Lean
repository has been exhaustively searched. No moving external dependency was fetched. Mathlib is
already pinned by `Formalizations/Lean/lake-manifest.json`, so A1 is dependency-feasible for a later
repo-local wrapper.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `git rev-parse HEAD` | 0 | `9864b47f2fbf53d0b642c54f12039877d4635056` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard OK; 1546 targets |
| `python3 scripts/stage1_target.py check` | 0 | manifest OK; ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0771` | 0 | rank 780; L0/rework required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned revision matched the Lake manifest |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD:Mathlib/SetTheory/Cardinal/Order.lean` | 0 | blob `c89ff6ad83317b9bb03929693ee47e668bc78c88` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0771/AnchorAudit.lean` | 0 | both exact candidate wrappers elaborated; all four axiom reports matched |
| `python3 -m json.tool Stage1_Instances/THM-M-0771/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0771 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The audit phase is self-tested and awaits master acceptance. It does not advance the root beyond
`[H1, M3, R4]`: the obligation registry is not frozen, no proof-phase wrapper is credited, and the
validation and release gates remain open. Theorem completion is false.

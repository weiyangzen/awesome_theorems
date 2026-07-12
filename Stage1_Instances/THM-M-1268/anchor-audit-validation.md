# Anchor-audit validation

Item: `S56-M-1268-ANCHOR_AUDIT`  
Base revision: `ad0567008a38fc8c39deda009ab34e4ca9910f46`

## Result

The bounded search found no exact terminal Lean theorem. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` does contain the two principal proof supports:
`Convex.toWeakSpace_closure` identifies norm and weak closures of transported convex sets, while
`lowerSemicontinuous_iff_isClosed_preimage` characterizes lower semicontinuity by closed sublevel
sets. `AnchorAudit.lean` binds these declarations to the materialized immutable revision.

Neither support declaration has the frozen functional type. A future proof must still derive
convexity of every `EReal` sublevel from the dossier's explicit Jensen predicate, transport closed
sublevels through `toWeakSpace`, and prove the converse topology direction. Thus the exact root
remains `M4` with `formalization_debt`; there is no exact external closure and hence no discovered
repo-local integration debt.

The public repository search returned no candidates, while public code search was rate-limited.
Those are bounded discovery results, not a claim of global absence. No dependency was cloned,
fetched, installed, updated, or built.

## Commands and results

Commands ran on 2026-07-12. Lean reused only the existing pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1268` | 0 | rank 444, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1268/Statement.lean` | 0 | exact canonical target and checked expanded transport re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1268/AnchorAudit.lean` | 0 | five pinned mathlib support declarations elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, matching the manifest pin |
| `rg -n -i 'lowersemicontinuous\|lower semicontinu\|weak.*closed\|closed.*weak\|convex.*closed\|closed.*convex' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology` | 0 | located the closure and sublevel bridges; no exact functional theorem |
| repository-local search for weak-lower-semicontinuity aliases in Lean and Markdown | 0 | only this dossier and descriptive neighboring references; no proof candidate |
| GitHub REST repository searches for the three aliases recorded in `anchor-audit.json` | 0 | zero complete metadata results; each response SHA-256 `08c082...2600` |
| GitHub REST code search for `"weak lower semicontinuity" language:Lean` | 0 | HTTP 403 rate-limit response; SHA-256 `1db366...386e`; no negative claim |
| `python3 -m json.tool Stage1_Instances/THM-M-1268/anchor-audit.json` | 0 | audit artifact is valid JSON |

## Open proof gate

The next phase must freeze separate obligations for convex sublevels, norm-closed sublevels,
weak-closure transport, image/preimage identities, the weak-lower-semicontinuity direction, and the
continuous-transport converse. Exact proof credit additionally requires terminal-body provenance,
transitive trust inspection, and kernel checking; none is claimed here.

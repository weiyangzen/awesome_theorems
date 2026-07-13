# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md:4699-4704` is the complete repository research record. It gives
the title `介值定理`, Bernard Bolzano, 1817, the exact gloss
`连通空间上连续函数的值域`, importance "high," and `已验证`. Git history traces all six
uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. This establishes
repository provenance, not a theorem-level primary source or a binder-complete proposition.

`Docs/Stage0_Blueprint.md:17341-17366` repeats that gloss while explicitly leaving precise
definitions and premises, proof route, dependencies, equivalent formulations, axioms,
machine-checked status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

No repository-local exact quotation, theorem/page locator, incorporated definition chain,
assumption list, proof boundary, translation review, correction or errata disposition, or
independent source review was found for this target.

## Primary-source lead

The catalog attribution and date point to Bernard Bolzano's 1817 work commonly cited under the
title *Rein analytischer Beweis des Lehrsatzes, dass zwischen je zwey Werthen, die ein
entgegengesetztes Resultat gewahren, wenigstens eine reelle Wurzel der Gleichung liege*. This
intake records that only as a bibliographic discovery lead. No immutable edition, exact page or
proposition, transcription, incorporated definitions, translation, proof passage, corrections,
errata, or independent review has been admitted. The lead therefore does not establish H0 or fix
the repository's more topological wording.

## Phrase crosswalk

| Repository phrase | Candidate mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `介值定理` | ordered intermediate-value theorem family | `IsPreconnected.intermediate_value` or a specialization | family name, not exact identity |
| `连通空间` | connected or preconnected whole space, or a connected/preconnected subset | `ConnectedSpace`, `PreconnectedSpace`, `IsConnected`, or `IsPreconnected` | carrier and nonemptiness convention absent |
| `连续函数` | globally continuous function or function continuous on a carrier | `Continuous f` or `ContinuousOn f s` | continuity domain absent |
| `值域` | connected image, order-convex image, interval inclusion, or existential preimage | `IsConnected (f '' s)`, `Icc _ _ \u2286 f '' s`, `Icc _ _ \u2286 range f`, or `Exists` | predicate and conclusion absent |
| Bolzano / 1817 | historical identity and root-existence context | source provenance only | primary edition and exact relationship open |
| `已验证` | inherited catalog status | no Lean proposition or proof object | explicitly rejected as evidence |

## Candidate-form crosswalk

| Candidate form | Pinned declaration | Relationship to received wording | Credit boundary |
|---|---|---|---|
| continuous image of a connected set is connected | `IsConnected.image` | literal reading of the gloss, but separately owned by `THM-M-0626` | candidate only; no shared state or proof credit |
| between-values theorem on a preconnected set | `IsPreconnected.intermediate_value` | strongest direct match to a set-based ordered reading | codomain order and exact binders are absent from the source |
| between-values theorem on a preconnected space | `intermediate_value_univ` | direct whole-space candidate | connected/preconnected and range conventions remain open |
| oriented closed-interval theorem | `intermediate_value_Icc` / `intermediate_value_Icc'` | familiar analysis specialization | interval domain and orientation are not stated |
| unordered closed-interval theorem | `intermediate_value_uIcc` | packages both endpoint orders | still a specialization selected by convention |
| sign-change root theorem | future checked corollary of an interval theorem | close to the historical Bolzano lead | zero, signs, real codomain, and interval hypotheses are absent |

The pinned declarations were inspected only as intake discovery surfaces. Their source comments and
types do not decide which one is source-identical, and the scheduled anchor audit must later check
terminal bodies, dependencies, axioms, licenses, and provenance at immutable revisions.

## Gate to statement work

Before H0 or the statement gate can pass, accountable reviewers must preserve an immutable primary
or authoritative source; identify the exact proposition and incorporated definitions by stable
locator; map every domain, codomain, connectedness, order, continuity, endpoint, orientation,
conclusion, and boundary clause; reconcile `THM-M-0626`; audit translation, corrections, and
errata; and independently approve the crosswalk.

Only then may a statement worker encode that same claim, minimize pinned imports, serialize the
elaborated expression and environment, compile credited transports, and run the required statement
mutations. Selecting the familiar real-interval or zero form now would narrow or substitute the
received target rather than faithfully elaborate it.

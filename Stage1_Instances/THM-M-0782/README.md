# THM-M-0782 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the catalogue item named "Dongpa theorem"
(`东帕定理`). The received metadata attributes it to Patrick Dehornoy in 1989 and describes only
"large cardinals and the axiom of determinacy." That is not an identifiable theorem statement.

The attribution does identify a strong discovery lead: Dehornoy's 1989 Bourbaki expose *La
determination projective*, a survey of the Martin-Steel projective-determinacy results. It does not
establish that there is an eponymous "Dehornoy theorem," nor does it choose one theorem from the
finite-level and full projective-determinacy results discussed by that source. The dossier therefore
preserves the received claim while refusing to invent an exact root.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Claim identity | A theorem relating large-cardinal hypotheses to determinacy, as indicated by the received metadata | The name "Dongpa theorem" is not accepted as an established eponym |
| Historical lead | Patrick Dehornoy, *La determination projective*, Seminaire Bourbaki, expose 710, 1989, pp. 261-276 | This is an expository source, not yet an exact root statement |
| Candidate theorem family | Martin-Steel implications from Woodin-cardinal hypotheses (with an appropriate measurable cardinal above in finite-level forms) to projective determinacy | Finite-level determinacy and full PD are distinct claims; neither is frozen as canonical |
| Games | Perfect-information games of length omega on natural numbers, with projective payoff sets | Coding of plays, strategies, payoff classes, and winning must be selected and checked |
| Large cardinals | Woodin-cardinal hypotheses and any required measurable-above condition | Exact number, ordering, ambient model, and background theory remain open |
| Formal target | A Lean 4 model-theoretic/set-theoretic implication after a source theorem is selected | No declaration, expression hash, import set, or foundation profile is credited |
| Exclusions | Borel determinacy, the axiom of determinacy for all sets of reals, converse consistency-strength results, and unrelated Dehornoy algebra/order results | None may substitute for the source-selected root |

## Planned boundary

The intake freezes the ambiguity rather than a guessed theorem. `intake.json` records the scope,
open decisions, and task DAG. `source_statement_crosswalk.md` distinguishes the repository wording,
the Dehornoy expose, and candidate Martin-Steel results.

The initial root vector is `[H5, M4, R3]`: no primary proof statement with page-level assumptions
has been accepted, no exact Lean proposition has been selected, and no reviewed reconstruction
exists. No proof body, assumed axiom, or broadened determinacy assertion is introduced.

## Status

Lifecycle is `planned`. Audit completion and theorem completion are false. Master acceptance is
pending, and this intake claims no later phase or checklist state.

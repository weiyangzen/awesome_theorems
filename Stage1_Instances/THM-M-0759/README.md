# THM-M-0759 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `自动机理论`
("automata theory"). The repository attributes it collectively to many mathematicians in the
twentieth century and supplies only the gloss `有限自动机的理论` ("the theory of finite
automata"). Its `已验证` ("verified") label is untrusted metadata and gives no human-source or
Lean proof credit.

The gloss names a subject, not a truth-valued, binder-complete proposition. It does not select a
machine model, its input and behavior semantics, finiteness assumptions, or a conclusion.
Finite-word DFA/NFA results, finite-state transducers, tree and infinite-word automata, and other
finite-state families all require source selection. Even within the word-language reading,
DFA/NFA equivalence, closure, pumping, Myhill-Nerode, Kleene's theorem, minimization, and decision
procedures are distinct results. The repository survey and neighboring Stage1 targets list several
separately, so intake may not silently substitute one result or conjoin the field into an omnibus
theorem.

The canonical mathematical and Lean statements therefore remain null. The provisional vector is
`[H5, M4, R4]`: `H5` classifies only the received catalog wording as an ill-posed, unstable
proposition; no usable source-identical formal artifact is selected; and no source-faithful proof
reconstruction can attach to an absent root. It does not classify finite-automata mathematics as
false or open.

`instance.json` is the structured scope authority. `scope-map.md` freezes the subject boundary and
prohibited substitutions. `source-statement-crosswalk.md` maps the catalog wording to unresolved
source and formal choices. All six downstream phases remain open in `task-dag.json`.
`IntakeProbe.lean` authenticates adjacent APIs in pinned mathlib but declares no target theorem.
No H0, M0, R0, accepted state, audit completion, theorem completion, or master acceptance is
claimed.

# THM-M-0766 rev-5.6 intake

`THM-M-0766` is the catalog item "linear-bounded automaton." The source record gives only the
gloss "context-sensitive languages," attributes it to Seymour Ginsburg and Sheila Greibach in
1963, and labels it `verified`. A machine model and a language family do not by themselves form a
truth-valued theorem with binders, hypotheses, and a conclusion.

## Intake result

This directory records a fail-closed `planned` instance. The repository separately names the
equivalence between context-sensitive languages and linear-bounded automata as a Kuroda 1964
computer-science target. Primary bibliographic evidence and a contemporary review support the
nondeterministic LBA equivalence as a plausible correction, while Landweber's 1963 Theorem 3 gives
only the deterministic LBA-to-type-1-language direction. Neither result may be silently substituted
for this item's unstable wording and unsupported author/year attribution.

The provisional root vector is `[H5, M4, R4]`: the received target is not yet one stable
proposition; the bounded intake search located only adjacent formal-language and Turing-machine
interfaces, not a source-identical usable formal artifact; and no source-faithful proof route can be
reconstructed before the root is selected. A master-approved target correction could later move a
specific proposition into ordinary source and statement review.

## Formal boundary

Pinned mathlib defines `Language`, deterministic Turing-machine tapes, machines, configurations,
steps, reachability, evaluation, and finite bundled `TM2` machines. It does not expose a
linear-bounded-automaton or context-sensitive-grammar interface in the bounded query. The
`IntakeProbe.lean` file authenticates adjacent APIs only. It declares no theorem and receives no
statement or proof credit.

All six downstream tasks remain open. `validation.md` records the exact nonrelease worker checks.
Neither audit completion nor theorem completion is claimed.

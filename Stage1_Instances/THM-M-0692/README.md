# THM-M-0692 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "cut
elimination theorem". The inventory supplies only the gloss "cut elimination in sequent
calculus", an attribution to Gerhard Gentzen, and the year 1934. It does not select a calculus or
state a proposition.

Cut elimination is a family of metatheorems. Classical `LK` and intuitionistic `LJ`, propositional
and first-order syntax, one- and two-sided sequents, set/list/multiset contexts, and calculi with
different structural and equality rules have materially different derivability judgments and
normalization claims. Selecting one without an exact source passage would substitute an invented
target for the repository record.

The intake therefore freezes this ambiguity and the exclusion boundary rather than a canonical
Lean proposition. The root remains `[H3, M4, R4]`. A pinned Lean probe checks only generic syntax
containers and well-founded recursion ingredients that could support a later encoding; it is not a
sequent calculus, cut-elimination statement, or proof. Commands and results are in `validation.md`.


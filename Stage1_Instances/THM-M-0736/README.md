# THM-M-0736 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "proof
complexity lower bounds". The source inventory supplies only the gloss "lower bounds on proof
length", attributes the topic to many mathematicians, and dates it to the 1980s. It does not name
a proof system, a family of tautologies, a size measure, an asymptotic bound, or a theorem.

Those omissions are material. Lower bounds for resolution, cutting planes, bounded-depth Frege,
and other proof systems are different propositions, while strong lower bounds for unrestricted
Frege or extended Frege systems cannot silently be substituted. The adjacent repository records
for Frege lower bounds and extended Frege also make a Frege-specific interpretation unsafe.

The intake therefore freezes the ambiguity and exclusion boundary instead of inventing a theorem.
The root remains `[H3, M4, R4]`. A pinned Lean probe confirms only that basic finite encodings and
length/cardinality measures elaborate; it is not a propositional proof-system model, lower-bound
statement, or proof. Exact commands and results are recorded in `validation.md`.

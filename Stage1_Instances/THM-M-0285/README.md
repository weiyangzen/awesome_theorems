# THM-M-0285 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Borel-Cantelli lemma. The repository gives only the gloss "the probability of an infinite sequence
of events," attributes the result to Emile Borel and Francesco Cantelli in 1909, and labels it
verified. Under rev-5.6 that label is untrusted inventory metadata, not a source audit, an exact
Lean proposition, or proof evidence.

The title names a standard two-part theorem family, but the gloss does not choose the first lemma
(summable event measures imply a null limsup), the second lemma (independent measurable events with
divergent total measure imply a full-measure limsup), both parts as a paired target, or a more
general form. Those choices change the domain, hypotheses, and conclusion, so intake does not fill
them in from memory.

Pinned mathlib has exact-topic declarations for both customary directions:
`MeasureTheory.measure_limsup_atTop_eq_zero` and
`ProbabilityTheory.measure_limsup_eq_one`. It also contains Levy's generalized Borel-Cantelli
theorem. `IntakeProbe.lean` authenticates these interfaces. The declarations are strong formal
candidates, but the catalog supplies no source statement from which to select one and no reviewed
transport. They therefore receive no target or proof credit at intake.

The provisional vector is `[H1, M3, R4]`: the recognizable human theorem family still lacks an
accepted pinpoint source and clause mapping; usable exact-topic formal interfaces exist but no
canonical target has been selected or checked against them; and no source-faithful readable proof
has been reconstructed. `instance.json` is the structured scope authority and `task-dag.json` keeps
all six downstream phases open. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.

# THM-M-0264 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Bolzano-Weierstrass theorem.
The repository catalog gives the attribution Bernard Bolzano/Karl Weierstrass, the year 1817, and
the gloss `有界数列必有收敛子列` (every bounded sequence has a convergent subsequence). It does
not cite a source or state the sequence's codomain, boundedness convention, topology, subsequence
encoding, or exact conclusion.

The real-analysis category and classical name strongly suggest real-valued sequences. Pinned
mathlib contains `tendsto_subseq_of_bounded`, explicitly documented as Bolzano-Weierstrass for
bounded sequences in proper metric spaces. Specializing it to `Set.range x` and `X := Real` is a
credible route to the conventional real-sequence theorem, but intake does not silently turn that
conventional interpretation into the source-exact root. The separate target `THM-M-0619` owns the
compact-metric-space sequence formulation and supplies no statement or proof credit here.

The provisional vector is `[H1, M3, R4]`: an established published theorem family is identified,
but no pinpoint primary proposition or independent source review is admitted; a direct pinned Lean
interface is authenticated without a frozen root or proof credit; and no source-faithful readable
proof reconstruction exists.

`instance.json` is the structured scope authority. The scope map and source-statement crosswalk
freeze the unresolved choices, `task-dag.json` leaves all six downstream phases open, and
`IntakeProbe.lean` checks candidate APIs only. No exact statement, H0, M0, R0, accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.

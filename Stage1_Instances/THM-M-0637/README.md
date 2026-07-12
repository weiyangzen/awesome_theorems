# THM-M-0637 rev-5.6 intake

`THM-M-0637` is the point-set-topology catalog entry for the Schauder fixed-point theorem. The
repository supplies Juliusz Schauder, the year 1930, and the gloss "a fixed point of a compact map
on a Banach space." The inherited `verified` label is untrusted. This dossier records a fail-closed
`planned` intake and does not promote that short gloss to a canonical proposition or proof.

## Intake result

The publisher scan of Schauder's 1930 paper was inspected. `Satz II` on printed page 175 states the
relevant family: a continuous self-map of a closed convex subset `H` of a `B`-space has a fixed
point when `F(H)` is compact. The paper identifies the normed complete spaces studied by Banach as
`B`-spaces. This strongly distinguishes the catalog's "compact map" wording from the compact-domain
form, but source preservation, incorporated definitions, nonemptiness, translation, corrections,
errata, proof boundary, and independent review are not accepted. The candidate therefore remains
an `H1` source lead, not `H0`.

The repository separately schedules `THM-M-0318` with the same theorem name under functional
analysis. Its dossier chooses a nonempty compact convex domain in a real normed space, closer to the
paper's `Satz I` than the present compact-image wording. That work is valuable discovery evidence,
but it transfers no statement, lifecycle, receipt, proof, or completion credit. Integration must
decide whether the IDs intentionally represent the compact-domain and compact-image forms.

## Formal boundary

`IntakeProbe.lean` elaborates pinned Banach-space, closedness, convexity, continuity, invariance,
compactness, compact-operator, and fixed-point vocabulary. It declares no target theorem and no
proof body. In particular, mathlib's `IsCompactOperator` is a (semi)linear operator interface and
is not silently equated with Schauder's nonlinear, domain-relative compact-image premise.

The provisional vector is `[H1, M4, R4]`. The exact mathematical statement, exact Lean expression,
minimal imports, transports, and statement fingerprint remain for the dependent statement node.
All six downstream tasks are open. Neither audit completion nor theorem completion is claimed.

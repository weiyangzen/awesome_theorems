# THM-M-0963 rev-5.6 intake

`THM-M-0963` is the counting-combinatorics catalog item "Ray-Chaudhuri-Wilson
theorem." The repository gives the gloss "an upper bound for an L-intersecting family,"
the authors, the year 1975, and an untrusted `verified` label. Those fields identify a
classical theorem family, but do not supply a binder-complete proposition or a source.

## Intake result

This dossier records a fail-closed `planned` instance. The primary bibliographic lead is
D. K. Ray-Chaudhuri and R. M. Wilson, *On t-designs*, *Osaka Journal of Mathematics* 12
(1975), 737-744. Its bibliographic identity is independently corroborated, but the primary
text could not be retrieved from the publisher or repository during this worker intake.
Two immutable secondary sources restate the familiar uniform theorem, and a third independently
corroborates its definition, bound, citation, and tight example: a family of
`k`-subsets of an `n`-set whose distinct pairwise intersection sizes lie in an `s`-element
set `L` has at most `choose n s` members, under `0 < s <= k <= n`. That restatement is a
strong candidate root, not an accepted canonical claim. The exact primary wording,
definition chain, endpoint assumptions, proof boundary, corrections, and independent
source review remain open, so the dossier records `H1`, not `H0`.

## Formal boundary

Pinned mathlib supplies finite sets, pairwise relations, intersection cardinalities,
fixed-cardinality powersets, and `Nat.choose`. A bounded repository and pinned-mathlib
search found no Ray-Chaudhuri-Wilson or L-intersecting declaration under the recorded
terms. `IntakeProbe.lean` elaborates only these adjacent APIs and a source-guided candidate
proposition shape. The shape is a definition of a proposition, not a theorem, proof,
canonical target, or statement-gate fingerprint.

The planned root vector is `[H1, M3, R4]`: a published primary source and precise
secondary restatements are located but the primary passage and exact source mapping are not
admitted; only an unproved candidate Lean shape and adjacent interfaces elaborate; and no
source-faithful proof reconstruction exists. All six downstream tasks remain open. No exact
statement, proof state, audit completion, theorem completion, or master acceptance is claimed.

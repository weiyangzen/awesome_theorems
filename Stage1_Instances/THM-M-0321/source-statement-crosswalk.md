# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the name, attributes it to Andrey Markov and Shizuo
Kakutani, gives the year 1936, and glosses the statement as "a fixed point of a commuting family of
operators". That wording does not specify the ambient space, compact convex set, continuity,
affinity, commutation quantifiers, or common-fixed-point conclusion. Its `verified` metadata is
untrusted under rev-5.6.

## Candidate primary sources

- A. Markov, "Quelques theoremes sur les ensembles abeliens", *Comptes Rendus (Doklady) de
  l'Academie des Sciences de l'URSS*, new series 1 (1936), 311-313. This is the historical 1936
  discovery anchor; the original text and its exact hypotheses have not yet been inspected here.
- Shizuo Kakutani, "Two fixed-point theorems concerning bicompact convex sets", *Proceedings of
  the Imperial Academy* 14 (1938), 242-245. This is a historical discovery anchor for Kakutani's
  contribution; the relevant numbered result and terminology must be checked from a stable scan.

These bibliographic anchors are not `H0` evidence. The statement phase must inspect stable copies,
select the authoritative formulation, record theorem/page boundaries and corrections, and obtain
independent review. In particular, the repository's single year must not silently collapse the
distinct historical sources.

## Claim crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "commuting family" | pairwise commuting, possibly infinite family | index type and equality of both compositions on `K` | included; encoding open |
| "operators" | continuous affine self-maps, not arbitrary linear operators | `ContinuousAffineMap` on a subtype or invariant ambient maps | included; representation open |
| fixed point | one point fixed by every map | `Exists fun x : K => Forall fun i => f i x = x` | included; exact expression open |
| compact convex domain | nonempty compact convex subset | `Set.Nonempty`, `IsCompact`, and `Convex Real` | included |
| ambient geometry | locally convex real topological vector space | topological additive/module structures and `LocallyConvexSpace Real E` | included; exact classes open |

## Lean discovery boundary

A scoped name search of pinned mathlib found the unrelated Riesz-Markov-Kakutani representation
modules but no Markov-Kakutani common-fixed-point declaration. `IntakeProbe.lean` checks that the
generic types needed to state a future target elaborate. It neither asserts the theorem nor proves
that no usable anchor exists under another name. A full immutable-revision candidate and terminal
body audit belongs to `S56-M-0321-ANCHOR_AUDIT` after the exact statement is frozen.

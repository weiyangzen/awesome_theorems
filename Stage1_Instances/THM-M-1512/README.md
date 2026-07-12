# THM-M-1512 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository target
`纳什存在性定理` (Nash existence theorem). The catalog supplies only the gloss `纳什均衡的存在性`
(existence of Nash equilibrium), attributes it to John Nash in 1950, and labels it `已验证`.
That status is untrusted and provides no human-source or Lean proof credit.

An inspected primary-source lead, Nash's 1950 *Equilibrium Points in N-Person Games*, describes a
finite normal-form game: every player has finitely many pure strategies, every pure strategy
profile has a payment vector, mixed strategies are probability distributions, and equilibrium is
a self-countering mixed profile. Nash concludes that such an equilibrium exists via Kakutani's
fixed-point theorem. This identifies the intended historical theorem family, but the repository
does not cite that paper or state its proposition. In particular, it omits the player index,
nonemptiness and finiteness assumptions, payoff codomain, mixed-versus-pure convention,
best-response definition, and the treatment of degenerate games. The downstream statement phase
must select and independently review the exact source proposition rather than importing these
choices silently.

The intake therefore freezes the family and ambiguity boundary, not a canonical mathematical or
Lean proposition. The root is provisionally `[H1, M4, R4]`: a complete human theorem and proof route
are located in the primary lead but have not passed the pinpoint assumption/errata/translation and
independent-review gate; no usable Nash-equilibrium formal artifact was found in the bounded
repo-local and pinned-mathlib search; and no source-faithful readable reconstruction exists.

`IntakeProbe.lean` checks only adjacent pinned APIs for finite probability simplices, compactness,
convexity, and correspondences. It does not define a game, state Nash equilibrium, invoke
Kakutani, or prove this target. The lifecycle remains `planned`; every downstream task is open,
and no accepted execution state, audit completion, or theorem completion is claimed.

The intake also records one immutable external Lean 4.31 source candidate with an
`ExistsNashEq` declaration. It was neither integrated nor built in the pinned Lean 4.29 closure,
and its statement, axioms, dependencies, and proof-body provenance remain for anchor audit. It
therefore supplies no machine-status upgrade.

See `scope-map.md`, `source-statement-crosswalk.md`, and `validation.md` for the exact boundary and
self-test evidence.

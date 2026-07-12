# Source-statement crosswalk

## Repository record

`Docs/Stage0_Blueprint.md:14739-14764` names the Eilenberg-Steenrod axioms and gives only "an axiom
system for homology theory" as content. It attributes the item to Samuel Eilenberg and Norman
Steenrod and dates it 1945, but supplies no publication, theorem, edition, page, definitions, or
proof. `Docs/researches/math_theorems.md:3988-3993` repeats the same metadata. The manifest's
`已验证` value is explicitly untrusted under rev-5.6 and provides neither H nor M credit.

The adjacent `THM-M-0537` record says "axiomatization of homology theory" and appears semantically
duplicative. Intake preserves both IDs and flags the overlap for master/source review; it does not
merge targets or transfer evidence.

## Primary-source candidate

Samuel Eilenberg and Norman Steenrod, *Foundations of Algebraic Topology*, Princeton University
Press, 1952, is the primary bibliographic candidate. Its axiomatic treatment of homology theory
must be inspected at a stable edition to locate the exact definitions/axioms, determine the role of
additivity, and decide whether a theorem rather than a definition is intended. The repository's
1945 date must be reconciled against primary publication history. Exact chapter, section, page,
wording, assumptions, errata, and an independent reviewer remain open, so this lead is not H0.

## Crosswalk

| Repository phrase | Classical mathematical component | Required formal component | Intake status |
|---|---|---|---|
| "homology theory" | graded covariant functors on spaces or pairs, plus boundary maps | a concrete category/functor family and natural transformations | included; encoding and coefficients open |
| "axiom system" | homotopy invariance | equality of maps induced by homotopic maps, at the selected domain | included; exact law open |
| "axiom system" | exactness | the long exact sequence of a pair with its degree shift | included; indexing and maps open |
| "axiom system" | excision | isomorphism under the source's precise excisive-subpair hypotheses | included; hypotheses open |
| "axiom system" | dimension | homology of a point concentrated in degree zero, with fixed coefficients | included; reduced/unreduced convention open |
| possible extra convention | additivity/disjoint unions | preservation statement for the selected class of coproducts | source-dependent; not yet included as a root law |
| theorem status | definition, concrete-model theorem, or uniqueness result | exact `Prop` or structure declaration and checked relationship | unresolved hard statement blocker |

## Debt boundary

The source family and likely primary book are identified, but the repository does not state a
proposition and the primary text has not yet been pinpointed and independently reviewed. `H2`
records this ill-posed/conditional statement debt rather than claiming a complete source proof.
Until the statement fork is resolved there is no canonical Lean target, so `M4` is mandatory.

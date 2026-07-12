# THM-M-0028 rev-5.6 dossier

`THM-M-0028` is the catalog item named "Noetherian ring structure theorem." The repository gloss
says that it concerns the ascending chain condition for ideals, attributes it to Emmy Noether in
1921, and labels it verified. That label is untrusted metadata, not source or machine evidence.

## Planned scope

The dossier selects the source-matched chain theorem: for every
commutative ring `R` in which every ideal is finitely generated, every ascending sequence of ideals
eventually stabilizes. A chain stabilizes when some index `n` has the same ideal at every later
index. The modern Lean candidate uses a unital `CommRing`; no `Nontrivial`, domain, characteristic,
or countability premise is added, so the zero ring remains in that planned encoding.

The catalog does not say whether its title denotes a definition, an equivalence theorem, or only
the ACC direction. Noether's named Satz I states the finite-generation-to-chain direction and then
notes the converse; the selected root follows the named theorem rather than silently strengthening
it to a biconditional. The statement phase must ratify the modern unital specialization and record
the converse as a checked related form rather than inherit either as accepted fact.
Noncommutative left/right variants, descending chains, Artinian rings, Hilbert's basis theorem, and
Noether normalization are distinct statements and cannot silently replace this target.

## Source boundary

An observed digest-bound scan of Emmy Noether's 1921 paper *Idealtheorie in Ringbereichen* was
inspected at
printed pages 29-31. Section 1 defines ideals and finite ideal bases; Satz I on pages 30-31 derives
eventual stabilization from that finiteness condition and notes the converse. The historical ring
is commutative but need not have a multiplicative identity, whereas Lean's planned `CommRing`
specialization is unital. The Stacks Project, Section 10.31 (tag `00FM`), was inspected as an
authoritative modern secondary cross-check. Neither source is accepted as an `H0` packet here;
complete terminology/premise/proof mapping, errata review, and independent review remain open.

## Formal boundary

The statement phase freezes the modern unital specialization as
`Stage1Instances.THM_M_0028.IdealAscendingChainTarget`. It elaborates with the sole import
`Mathlib.RingTheory.Finiteness.Defs`, strictly below the module containing the adjacent
Noetherian chain theorem. Checked iff transports cover the regular-submodule carrier and the
function-plus-monotonicity source spelling, four structural mutations are distinguished, and a
subsingleton boundary plus a concrete `PUnit` probe confirm that the target does not silently add
`Nontrivial`.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.RingTheory.Noetherian.Defs` contains an exact type for the adjacent candidate
`monotone_stabilizes_iff_noetherian` and the finite-generation characterization
`isNoetherianRing_iff_ideal_fg`. Their terminal bodies, provenance, dependencies, and trust closure
remain for the later anchor audit and receive no proof credit here.

The planned vector is `[H1, M3, R3]`: a stable conventional claim plus source leads support `H1`;
exact pinned formal interfaces support only `M3` until anchor-audit and proof gates run; and
the dossier maps scope without providing a reviewed proof reconstruction. The statement proposal
is self-tested pending master acceptance, and all five later tasks remain open. No accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.

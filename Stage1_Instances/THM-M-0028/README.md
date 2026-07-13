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

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the fresh anchor
audit composes `isNoetherianRing_iff_ideal_fg` with
`monotone_stabilizes_iff_noetherian` behind a literal exact-target adapter. Lean prints both bodies,
reports both terminals and the adapter sorry-free, and reports only `propext`,
`Classical.choice`, and `Quot.sound` for the adapter. This is a self-tested `M0-W / E2`
candidate, not accepted proof state.

The immutable Atlas project also contains the exact biconditional `noetherian_fg_iff_acc` at
revision `34ffed396f376454c1a9b297f3fd74c5c801fb50`. It elaborates against the same pinned
Lean/mathlib environment, but it is outside the dependency closure, reduces to the same mathlib
route, and has a restrictive noncommercial/no-training license. It is classified `M1 / E2`
corroboration and is not integrated. Atlas describes this corpus as LLM-autoformalized; its
automated report is recorded as provenance, not as independent human review.

The planned vector is `[H1, M3, R3]`: a stable conventional claim plus source leads support `H1`;
an exact pinned formal route is an unaccepted `M0-W / E2` candidate while the accepted root remains
`M3` until proof, composition, provenance/trust, validation, and master-acceptance gates run; and
the dossier maps scope without providing a reviewed proof reconstruction. The statement proposal
and anchor inventory are self-tested pending master acceptance, and all downstream tasks remain open. No accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.

## Frozen obligation architecture

Registry `THM-M-0028-OBLIGATIONS-v1` freezes 25 canonical obligations before candidate status is
credited. Separate proof, refinement, provenance, evidence, trust, documentation, and workflow
graphs expand the two distinct pinned terminal bodies through their Noetherian-class, compactness,
complete-lattice, and monotone-chain dependencies. `ObligationTree.lean` checks both child-to-parent
compositions while keeping finite-generation-to-Noetherianity and Noetherianity-to-chain-
stabilization as explicit premises. The architecture installs no proof and leaves the accepted
root at `[H1, M3, R3]` pending master acceptance and every downstream gate.

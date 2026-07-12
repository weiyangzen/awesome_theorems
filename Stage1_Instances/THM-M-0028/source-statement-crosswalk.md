# THM-M-0028 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:221-226` names `诺特环结构定理`, attributes it to Emmy Noether
in 1921, and states `诺特环的理想升链条件`: the ascending chain condition for ideals of a
Noetherian ring. `Docs/Stage0_Blueprint.md:884-909` repeats the gloss while leaving exact
definitions, premises, proof route, equivalent formulations, logical foundation, and machine
artifact open. All six catalog fields originated at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The manifest preserves `已验证` only as
untrusted source metadata.

The wording does not itself distinguish a definition from a theorem, select a unital convention,
or say whether the intended theorem is one implication or the standard equivalence. This intake
records that ambiguity and selects the direction of Noether's named chain theorem provisionally:
finite generation of every ideal implies stabilization of every ascending ideal chain.

## Human sources

Crossref metadata identifies Emmy Noether, *Idealtheorie in Ringbereichen*, pages 24-66 (1921),
DOI `10.1007/BF01464225`. An open Zenodo scan (record `1428306`, PDF SHA-256
`285a94136dd344a49b1347ea98ae11fa12f2b1ce1739ef4f9fca6c9b9332d52b`) was inspected. In
Section 1, printed page 29 defines a commutative ring and explicitly says it need not have a unit;
page 30 defines an ideal with a finite ideal basis and imposes that finiteness condition. Satz I,
printed pages 30-31, derives eventual identity of a countable ideal chain and then says conversely
that the theorem gives existence of finite ideal bases. Its older ideal-divisibility language must
be translated carefully because its order wording is opposite modern inclusion notation.

The footnote to Satz I credits Dedekind with the number-module theorem and Lasker with the
polynomial-ideal case, so the catalog attribution is not a settled priority claim. The primary
passage is strong evidence for the selected theorem family, but a complete translation,
assumption/proof/errata map and independent review remain open; it therefore supports `H1`, not
`H0`.

The Stacks Project, *Commutative Algebra*, Section 10.31 "Noetherian rings" (tag `00FM`, 2026
citation version), states: a ring is Noetherian when every ideal is finitely generated, and this is
equivalent to the ascending chain condition for ideals. The inspected 2026-05-30 algebra PDF had
SHA-256 `fba39d5b24a98d3317d20bb58dca4335b9d4bc5edd08b086c5258055127a7b91` and places the
passage at PDF text lines corresponding to Section 31, immediately before Lemma 31.1. This is an
authoritative modern secondary definition/equivalence cross-check, not a replacement for the
missing historical source packet or independent source review.

The resulting human status is `H1`: the theorem family and modern statement are stable, but exact
historical fidelity, premise/definition/proof mapping, errata, and review remain open.

## Component mapping

| Catalog component | Intake-selected meaning | Pinned Lean candidate | Status |
|---|---|---|---|
| "ring" | historical commutative ring, not necessarily unital; Lean root is the explicitly bounded unital specialization | `[CommRing R]` | exact modern domain frozen; wider historical-domain fidelity open |
| "ideal ascending chain" | every `f : Nat →o Ideal R` is constant from some index onward | exact `OrderHom` carrier in `IdealAscendingChainTarget` | elaborated and fingerprinted; proof uncredited |
| "Noetherian ring" | every ideal of `R` is finitely generated | exact explicit `Ideal.FG` premise; adjacent `IsNoetherianRing R` candidate | explicit premise frozen; predicate transport uncredited |
| theorem relation | finite ideal bases imply ACC stabilization | exact one-way implication in `IdealAscendingChainTarget` | target frozen; no inhabitant or proof credit |
| Emmy Noether / 1921 | historical catalog attribution | no formal component | pinpoint primary-source audit and independent review open |
| `已验证` | catalog status label | no formal component | explicitly no H/M credit |

## Pinned formal candidates

At immutable mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, source file
`Mathlib/RingTheory/Noetherian/Defs.lean:159-162` declares:

```text
monotone_stabilizes_iff_noetherian :
  (forall f : Nat ->o Submodule R M, exists n, forall m, n <= m -> f n = f m) <->
    IsNoetherian R M
```

Specializing `M := R` makes this adjacent to the ideal-chain claim because `IsNoetherianRing R`
abbreviates `IsNoetherian R R`. The selected one-way root still must expose or transport the
finite-generation premise rather than assume the desired class instance without explanation. The
same file at lines 195-204 declares
`isNoetherianRing_iff_ideal_fg`, which identifies the ring predicate with finite generation of all
ideals. It also exposes well-founded-order and maximal-element characterizations.

`IntakeProbe.lean` checks these APIs and reports that
`monotone_stabilizes_iff_noetherian` depends on `propext`, `Classical.choice`, and `Quot.sound` in
the pinned environment. This is discovery evidence only. Intake does not freeze target identity,
inspect terminal bodies or transitive dependencies, accept the proof axiom profile, or establish
`M0`. `Statement.lean` now elaborates the exact ideal-chain target from the strictly smaller
`Mathlib.RingTheory.Finiteness.Defs` import, checks the regular-submodule and explicit-monotone
function transports, and freezes four mutations without importing the candidate chain theorem.

## Exactness risks held open

The statement phase freezes the one-way implication, commutativity, the explicitly bounded modern
unital specialization, natural-sequence stabilization, inclusion order, equality after the
stabilization index, finite generation of all ideals, and inclusion of the zero ring. It does not
claim fidelity to Noether's wider nonunital domain or credit the converse/full equivalence. Those
source and related-form questions remain downstream and cannot be inferred from a close name.

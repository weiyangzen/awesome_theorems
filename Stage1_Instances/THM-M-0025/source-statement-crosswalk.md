# THM-M-0025 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:200-205` names the Hilbert basis theorem, attributes it to David
Hilbert in 1890, and states `诺特环上的多项式环仍是诺特环`: a polynomial ring over a
Noetherian ring is still Noetherian. `Docs/Stage0_Blueprint.md:803-828` repeats that claim while
leaving exact definitions, premises, proof route, logical foundation, and machine artifact open.
All six catalog fields originated at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The manifest preserves `已验证` only as
untrusted source metadata.

## Human sources

Crossref metadata identifies David Hilbert, *Ueber die Theorie der algebraischen Formen*,
*Mathematische Annalen* 36(4), 473-534 (1890), DOI `10.1007/BF01208503`. This is a plausible
historical primary lead. Intake did not admit or inspect an immutable primary text, locate the
relevant theorem or page, map its definitions and hypotheses, check translations or errata, map
the proof to obligations, or obtain independent review. The historical lead therefore supports
`H1`, not `H0`.

Stacks Project, Section 10.31 and Lemma 10.31.1 (tag `00FN`), defines a commutative Noetherian ring
by finite generation of every ideal, records the ascending-chain equivalence, and states that any
finite type ring over a Noetherian ring is Noetherian. Its proof explicitly reduces to the
one-variable assertion that `R[X]` is Noetherian. This is a modern secondary statement/proof
cross-check. It does not replace the missing historical source packet or independent source
review.

## Component mapping

| Catalog component | Intake-selected meaning | Pinned Lean candidate | Status |
|---|---|---|---|
| "Noetherian ring" | commutative `R` in which every ideal is finitely generated | `[CommRing R] [IsNoetherianRing R]`; `isNoetherianRing_iff_ideal_fg` | checked iff frozen; source ratification open |
| "polynomial ring over" | univariate polynomials with coefficients in the same `R` | `Polynomial R`, notation `R[X]` | exact carrier and universe frozen |
| "is still Noetherian" | every ideal of the polynomial ring is finitely generated | `IsNoetherianRing (Polynomial R)` | canonical target elaborated and fingerprinted |
| David Hilbert / 1890 | historical catalog attribution | no formal component | pinpoint primary source and review open |
| `已验证` | catalog status label | no formal component | explicitly no H/M credit |

## Pinned formal candidate

The pinned source
`Mathlib/RingTheory/Polynomial/Basic.lean:732-806` labels and declares:

```text
Polynomial.isNoetherianRing {R : Type u} [CommRing R] [IsNoetherianRing R] :
  IsNoetherianRing (Polynomial R)
```

The immutable mathlib revision is `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The candidate is
an unusually close formal match. The statement phase freezes a canonical proposition with the
same implicit ring and instance binders without importing this proof-bearing module, and checks an
iff to the every-ideal-is-finitely-generated encoding. It does not credit the candidate body,
source fidelity, transitive dependencies, trust profile, or proof closure. Those remain
anchor-audit/proof/validation responsibilities.

## Exactness risks held open

The statement phase freezes the conventional commutative, one-variable reading, the
finite-generation encoding, inclusion of the zero ring, and absence of an extra nontriviality
premise. Pinpoint historical-source ratification and the ACC transport remain open. The
finite-variable `MvPolynomial` instance, the finite-type algebra theorem, and any noncommutative
one-sided theorem are related candidates, not silent replacements.

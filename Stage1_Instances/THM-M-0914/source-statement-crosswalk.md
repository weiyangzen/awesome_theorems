# THM-M-0914 source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `鸽巢原理`, Peter Dirichlet, the year 1834,
and the sole claim `n+1个物体放入n个盒子必有一个盒子至少有两个`. All six catalog lines originate
in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the record supplies no bibliography,
definition, theorem number, page, proof, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md` repeats the claim but explicitly leaves its exact definitions and
premises, proof route, dependencies, equivalent statements, axioms, machine status, and artifact
links open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`. None of
these projections is H or M evidence.

## Inspected modern source lead

Eric Lehman, F. Thomson Leighton, and Albert R. Meyer's *Mathematics for Computer Science*, 2018
revision, Section 15.8, printed pages 676-677, was inspected as an authoritative modern source
lead. Page 676 says that if there are more pigeons than occupied holes, at least two pigeons share
a hole. Rule 15.8.1 on page 676 states the rigorous form: if finite sets `A` and `B` satisfy
`|A| > |B|`, every total function `f : A -> B` maps two different elements of `A` to the same
element of `B`. Page 677 identifies `A`, `B`, and `f` with pigeons, holes, and placement.

The observed 1,048-page PDF had SHA-256
`ea4ced500d4a4bae7beb7a72ae9784abb96ed656ad905976f54c828cf6337dc1`. The text is licensed
CC BY-SA 3.0 according to its copyright page. It is not the historical Dirichlet source cited by
the catalog, is not preserved as an accepted immutable source artifact here, and has no
independent statement/proof/errata review. It supports a provisional `H1` family identification,
not `H0`.

The catalog's Dirichlet/1834 attribution remains an unverified historical lead. Public metadata
for Benoit Rittaud and Albrecht Heeffer, "The Pigeonhole Principle, Two Centuries Before
Dirichlet," *The Mathematical Intelligencer* 36(2), 27-29 (2014), DOI
`10.1007/s00283-013-9389-1`, was inspected as a provenance warning. Its title challenges exclusive
Dirichlet attribution, and its public references point to a Dirichlet 1842 paper, pages 93-95, and
the 1863 *Vorlesungen uber Zahlentheorie*, pages 405-406, rather than 1834. The article body and
those primary passages were not accessible or inspected, so this metadata earns no H credit. A
source audit must inspect the exact editions and passages, reconcile the chronology, or formally
select a reviewed modern source of record before H0 can be considered.

## Clause crosswalk

| Catalog phrase | Mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| `n+1个物体` | finite object collection of cardinality `n + 1` | `Fin (n + 1)` | exact concrete binder frozen |
| `n个盒子` | finite box collection of cardinality `n` | `Fin n` | exact concrete binder frozen |
| `放入` | each object occupies exactly one box | total function `f : Fin (n + 1) -> Fin n` | exact total-placement binder frozen; H0 source review open |
| `一个盒子` | a common image of two objects | `BoxWitnessTarget` names `b : Fin n` | checked iff to the collision root; `n = 0` remains vacuous |
| `至少有两个` | two distinct objects have the same box | `exists x y, x != y and f x = f y` | exact collision conclusion frozen; fiber-cardinality form uncredited |
| Peter Dirichlet / 1834 | historical provenance | no Lean proposition | uncited and unverified |
| `已验证` | untrusted inventory status | no proposition or proof credit | explicitly rejected as evidence |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Data.Fintype.Pigeonhole` exposes
`Fintype.exists_ne_map_eq_of_card_lt`, with exactly the finite-type cardinality premise and
distinct equal-image conclusion described above. `Fintype.card_fin` can support the prospective
`Fin (n + 1)`/`Fin n` specialization. `Fintype.not_injective_of_card_lt` and
`Function.Embedding.isEmpty_of_card_lt` are alternate interfaces.

These declarations are proof-bearing exact-family candidates, so the provisional machine status
is `M3`, not an absence claim. The statement phase now freezes the concrete catalog encoding and
its checked shared-box transport without importing a proof candidate. The later anchor audit must
resolve specialization, terminal bodies, dependencies, trust, placeholders, provenance, and source
identity before any `M0-W` proposal.

## Exit gate

The statement worker has elaborated, serialized, hashed, transported, boundary-checked, and
mutation-tested the literal concrete target with an empty direct-import set. Master acceptance of
that provisional packet remains open. Independent source-of-record review, historical disposition,
complete proof and errata mapping, and H0 remain later source gates rather than statement-proof
credit.

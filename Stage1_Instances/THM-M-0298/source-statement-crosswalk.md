# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:2139-2144` records only:

- title: `卡尔德龙-齐格蒙德分解`;
- attribution: Alberto Calderon / Antoni Zygmund;
- year: 1952;
- gloss: `函数的分解技术`;
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:8224-8250`
repeats this metadata while leaving exact definitions, premises, proof route, equivalent forms,
axioms, machine status, and artifact links open. These records establish catalogue identity only.

## Primary-source lead

Crossref and publisher metadata identify A. P. Calderon and A. Zygmund, *On the existence of
certain singular integrals*, **Acta Mathematica** 88 (1952), pages 85-139, DOI
`10.1007/BF02392130`. The Crossref record reports the title, authors, year, journal, volume, and
page range. The publisher article metadata agrees and advertises a PDF, but access during this
bounded intake returned the publisher article shell rather than immutable full text.

This is a matching primary-publication lead, not an accepted statement source. Intake did not
obtain and hash a stable primary full-text edition, pinpoint a decomposition theorem or lemma,
transcribe its incorporated definitions, determine which modern formulation the catalogue means,
audit corrections or errata, or obtain independent review. The provisional human debt is `H1`:
a published complete proof is believed and a named source is identified, while exact source-to-root
mapping remains open.

## Clause crosswalk

| Catalogue phrase or familiar clause | Human-source status | Prospective Lean surface | Intake decision |
|---|---|---|---|
| "function" | domain, codomain, measurability, and integrability absent | measurable functions or `L1` representatives | open |
| "decomposition" | outputs and equality sense absent | `f = g + sum' b` pointwise or almost everywhere | candidate only |
| selected regions | cubes/balls, grid, maximality, and disjointness absent | sets, boxes, balls, countable families | open |
| good-part bound | norm, constant, and exceptional set absent | almost-everywhere norm inequality | candidate only |
| bad-part cancellation | scalar integral, average, and convergence conventions absent | `integral` or `setAverage` identities | candidate only |
| bad-region control | exact constant and measure/norm form absent | `Measure`/`ENNReal` inequality | candidate only |
| `已验证` | untrusted inventory metadata | no proposition or proof object | no H or M credit |

## Pinned Lean candidate crosswalk

The intake probe elaborates adjacent APIs at the pinned revision:

| Declaration | Feasibility role | Unclosed gate |
|---|---|---|
| `MeasureTheory.setAverage_eq` | average over a measurable set | source convention, zero/infinite measure behavior, exact target |
| `MeasureTheory.setIntegral_setAverage_sub` | cancellation after subtracting a set average | only one expected leaf; no cube selection or root composition |
| `Real.volume_Icc_pi` | volume of a finite-dimensional closed box | source cube convention and boundary equivalence |
| `Vitali.exists_disjoint_subfamily_covering_enlargement_closedBall` | disjoint covering extraction for balls | source may use maximal dyadic cubes; constants and transport open |
| `Besicovitch.exists_disjoint_closedBall_covering_ae` | almost-everywhere disjoint ball covering | materially different hypotheses and conclusion from a cube decomposition |

A bounded case-insensitive search for `Calderon`, `Calderón`, `Zygmund`, and the exact decomposition
phrase over pinned mathlib Lean sources returned no match. External source inspection found a
credible immutable Lean proof lead:

- repository/revision: `fpvandoorn/carleson@fdcce451b494680b1fd5534236a71d9b258860b2`;
- file: `Carleson/TwoSidedCarleson/WeakCalderonZygmund.lean`;
- raw file SHA-256: `2c4fe4ac1248a43d4f7e5903633dd921780d824e6fab66f2e53e96e5a4f49495`;
- project blueprint SHA-256: `2ab2757dc1d710d83d7e846bc669bd19928bb38c6897851d066fe158a673ec67`;
- environment: Lean `v4.30.0-rc2`, mathlib
  `1a4917a18b30ea1333c195e597067fe044ac9176`, outside the local pinned closure.

Its theorem bundle covers a generalized ball decomposition, including approximation/remainder sum
identities, good-part bounds, bad-part support and cancellation, overlap, ball-volume, and `L1`
estimates. The exact canonical root is not a single declaration, and its bounded finite-support
complex-function hypotheses are not silently identified with the unfrozen catalogue claim. It was
source-inspected only; the worker did not clone, fetch, mutate `.lake`, or claim local elaboration.
This supports provisional `M1`, pending the later exhaustive immutable anchor/provenance audit and
source-to-formal transport.

Before leaving `H1`, an accountable source reviewer must preserve an immutable primary edition,
identify the exact theorem/section/page, crosswalk every incorporated definition, ordered binder,
hypothesis, constant, conclusion, and boundary case, audit corrections and errata, and approve the
mapping independently. Before statement acceptance, Lean work must freeze minimal imports and an
elaborated expression and pass removed-hypothesis, changed-domain, binder-scope, and boundary-case
mutations.

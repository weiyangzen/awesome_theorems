# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7001-7006` supplies exactly the title `Croot-Lev-Pach方法`, the
attribution Croot/Lev/Pach, year 2017, the gloss `多项式方法在cap集问题中的应用`, importance
"high," and status `已验证`. All six uncited lines entered at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:26146-26171` repeats the gloss while explicitly leaving the formal
system, exact definitions and premises, proof route and date, dependencies, evidence type,
alternate forms, axioms, machine status, and artifact links open. Rev-5.6 retains `已验证` only as
untrusted metadata and resets this target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Primary-source meaning | Required formal component | Intake result |
|---|---|---|---|
| `Croot-Lev-Pach方法` | the polynomial-method route introduced in the CLP paper, not by itself a proposition | one selected root plus an explicit proof-provenance policy | open |
| "cap-set problem" | a related progression-free-set problem; CLP proves a `Z_4^n` result, while the classical cap-set problem uses `F_3^n` | exact ambient group and checked terminology boundary | CLP family matched; classical cap-set substitution excluded |
| "application of the polynomial method" | Lemma 1 feeds Proposition 1 and Theorem 1 | typed proof graph and checked child-to-parent composition if provenance is in scope | no method/provenance credit |
| Croot/Lev/Pach, 2017 | exact authors and publication year | immutable edition, result locator, correction audit, and independent review | matching primary paper inspected |
| `已验证` | untrusted inventory metadata | accepted source and kernel receipts | no H or M credit |

## Primary source

Ernie Croot, Vsevolod F. Lev, and Peter Pal Pach, "Progression-free sets in Z_4^n are
exponentially small," *Annals of Mathematics* 185(1) (2017), pp. 331-337, DOI
`10.4007/annals.2017.185.1.7`. The inspected publisher PDF has 7 pages, 314538 bytes, and SHA-256
`9829dbcdb774826379ba2c98f62cc4267ca8d0e24ad7a89f596bcc2c5c224b3e`. The publisher page
records the same authors, title, year, volume, issue, pages, DOI, and abstract. The corresponding
immutable preprint lead is arXiv `1605.01506v2`, dated 2016-05-21; its version comment reports a
minor improvement, simplification, and correction.

The external PDF was inspected in temporary storage and is not vendored or admitted as repository
proof evidence. Correction history matters: arXiv v1 states only
`|A| < 2*(sqrt(n)+1)*4^(gamma*n)`, whereas v2 adds the tensor-power step and the published theorem's
`|A| <= 4^(gamma*n)`. The v2 TeX also has `2^(gamma*n)` in its intermediate equation `(int4)`,
while the governing published p. 335 correctly prints `4^(gamma*n)`. A later audit must use the
publisher version as statement/proof authority and treat v2 only as an immutable correction lead;
v1 cannot govern the target. No independent source reviewer, accepted full correction audit, or
complete source-to-node mapping exists, so no numbered result is H0.

## Numbered-result crosswalk

| Source locator | Source clause | Formal obligations if selected | Status |
|---|---|---|---|
| Definition, printed pp. 331-332 | `A` in an additive abelian group is progression-free when no pairwise-distinct `a,b,c` in `A` satisfy `a+b=2c` | exact set/group predicate and checked relation to `ThreeAPFree` | incorporated definition candidate only |
| Theorem 1, printed p. 332 | for base-two `H`, `gamma = max { (H(1/2-epsilon)+H(2*epsilon))/2 | 0<epsilon<1/4 }`, approximately `0.926`; for `n>=1`, progression-free `A` in `Z_4^n` has `|A| <= 4^(gamma*n)` | product group, cardinality, entropy normalization, outer factor `1/2`, maximum/supremum, real power, casts | likely result candidate; not selected |
| Corollary 1, printed p. 332 | finite-abelian-group bound using the number of invariant factors divisible by four | decomposition, `rk_4`, coset transport, cardinal arithmetic | distinct candidate; not selected |
| Lemma 1, printed p. 333 | off-diagonal vanishing of a low-degree multilinear polynomial on a sufficiently large set forces vanishing at zero | polynomial representation, degree and binomial threshold, linear-independence argument | reusable method core; not selected as root |
| Proposition 1, printed pp. 334-335 | exponentially few involution-subgroup cosets contain many elements of `A` | cosets, doubling map, entropy/binomial estimates, application of Lemma 1 | intermediate candidate only |
| Proof of Theorem 1, printed pp. 335-336 | layer-cake integral estimates followed by the tensor-power trick | real integration, bounds, product preservation of progression-freeness, limiting argument | downstream proof architecture only |

## Neighbor boundary

`THM-M-0960` is separately cataloged as the Ellenberg-Gijswijt theorem with the gloss "cap-set
upper bound." Its primary paper explicitly says the CLP method is used for subsets of `F_q^n` and
specializes `q = 3` to the cap-set problem. That extension is not the same theorem as CLP's
`Z_4^n` result and receives no state or proof transfer. `THM-M-0957` and `THM-M-0958` own lower-bound
constructions; `THM-M-0961` owns Meshulam's upper bound.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.Additive.AP.Three.Defs` supplies `ThreeAPFree` and product preservation;
`Mathlib.Data.Fintype.BigOperators` supplies `Fintype.card_pi_const`; `Mathlib.Data.ZMod.Basic`
supplies `ZMod`; and `Mathlib.Analysis.SpecialFunctions.BinaryEntropy` supplies natural-log
`Real.binEntropy`. The source's base-two entropy therefore needs an explicit normalization.
Moreover, `ThreeAPFree` is strictly stronger than the source predicate on `ZMod 4`: the set
`{0, 2}` witnesses the mismatch via `0 + 0 = 2 + 2`. It is adjacent substrate, not the source
definition.

The nearby Behrend module proves a lower bound for three-term-progression-free subsets of natural
intervals. A bounded source-name and exact-topic search located no Croot-Lev-Pach, `Z_4^n`
exponential upper-bound, or source-identical declaration. `IntakeProbe.lean` authenticates only
these adjacent APIs; it declares no target theorem and supplies no proof body or anchor credit.

## Source gate

Before `S56-M-0959-STATEMENT`, accountable reviewers must select one exact numbered result or
provenance-sensitive package, preserve and hash the governing edition, map every incorporated
definition and premise, reconcile the preprint correction and neighbor ownership, and independently
approve the mapping. Only then may statement work freeze minimal imports, ordered binders,
canonical expression and environment fingerprints, checked transports, and the four required
mutation classes.

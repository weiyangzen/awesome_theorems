# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7015-7020` supplies exactly the title `Meshulam定理`, attribution
to Roy Meshulam, the year 1995, the gloss `cap集的上界` ("upper bound for cap sets"), importance
"high," and status `已验证`. All six uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:26200-26225` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Primary-source lead

Crossref and the DOI landing record identify Roy Meshulam, "On subsets of finite abelian groups
with no 3-term arithmetic progressions," *Journal of Combinatorial Theory, Series A* 71(1)
(1995), 168-172, DOI `10.1016/0097-3165(95)90024-1`. The metadata matches the catalog's author and
year and identifies the relevant progression-free finite-group subject. The inspected Crossref
response has SHA-256 `37f961a10e8516951a9145e5eeb31c619e81b9dcb3c418aae63d09aa750bb63c`.

This is a primary-paper identification, not an `H0` packet. The five-page article text was not
available in the repository or admitted during this intake. No theorem number/page passage,
verbatim formula, incorporated definitions, complete assumptions, proof boundary, correction or
errata audit, or independent reviewer crosswalk has been accepted.

CORE record `201940438` reproduces an abstract stating that `G` is a finite abelian group of odd
order, defining `D(G)` as the maximum size of a subset without a three-term arithmetic progression,
and reporting a cyclic-direct-sum inequality plus a logarithmic corollary. The observed response has
SHA-256 `78e4229cd6728069b1d3f5b97cdd7a6c852b941571e27b33adbb1279fd740d6a`.
Its formula is text-conversion damaged (`2((k1 ... kn/n)`), however, and it does not expose the
paper's progression definition or any separate hypotheses on the cyclic factors. It narrows the
scope but cannot freeze the exact formula. Focused DOI/Crossref searches found no correction or
erratum; that bounded negative finding is not evidence that none exists.

## Exact secondary cross-reference

Yu-Ru Liu, Craig V. Spencer, and Xiaomei Zhao, "A generalization of Meshulam's theorem on subsets
of finite abelian groups with no 3-term arithmetic progression (II)," *European Journal of
Combinatorics* 32 (2011), 258-264, DOI `10.1016/j.ejc.2010.09.008`, gives an exact retrospective
cross-reference. Printed page 258 states that for a finite abelian group `G` of odd order, Meshulam
proved `D3(G) <= 2 |G| / c(G)`. Printed page 259 defines an invariant-factor decomposition
`G ~= Z/k1 Z + ... + Z/kM Z` with each cyclic factor nontrivial and `k_i` dividing `k_(i-1)` for
`2 <= i <= M`, and defines `c(G) = M`; it explicitly attributes the bound to `[8, Theorem 1.2]`.
The observed seven-page publisher-version PDF has SHA-256
`cae43200716c7f2fdf10b5d3936d50b732e661c51aac8a47dec30ad9d02fded4`.

This repairs the damaged abstract formula and identifies the leading primary theorem candidate. It
remains retrospective secondary evidence: the primary theorem, its own definition of a 3AP, and its
proof were not directly inspected, and no accountable independent reviewer has approved the
source-to-catalog choice. Accordingly it supports H1 and a precise statement-phase handoff, not H0
or a non-null canonical statement at intake.

Liu and Spencer, *Designs, Codes and Cryptography* 52 (2009), 83-91, DOI
`10.1007/s10623-009-9268-0`, independently gives the same retrospective Theorem 1.2 bound and treats
the trivial solutions of `x1 - 2*x2 + x3 = 0` as `x1 = x2 = x3`. The observed repository copy has
SHA-256 `15f990fec8e2afaec60ecb73fd55748eaab6f545dcbe278a33e0bb63506a919a`.
This strengthens the source lead but remains secondary and unreviewed under the H0 gate.

## Secondary disambiguation lead

Michael Bateman and Nets Hawk Katz, *New Bounds on cap sets*, arXiv `1101.5851v2`, explicitly says
that Meshulam proved a constant-`C` density bound of order `C / N` for cap sets in `F_3^N`, and
Section 3 reviews the Fourier/density-increment argument. The observed 38-page PDF has SHA-256
`e78cf5ccc0707ad92ea548c232c33c60c32eac32cdfedae60a165e22eb818a6b`.

This later paper is useful for distinguishing Meshulam's bound from the later
`C / N^(1 + epsilon)` improvement and from the Ellenberg-Gijswijt exponential bound. It is not the
1995 primary statement, does not resolve the general finite-abelian formulation in Meshulam's title,
and is not credited as a source-faithful root or proof.

## Component crosswalk

| Catalog component | Source/lead component | Prospective Lean surface | Intake status |
|---|---|---|---|
| Meshulam / 1995 | matching JCTA paper and DOI | immutable source provenance | paper identified; exact theorem and review open |
| cap set | later lead: subset of `F_3^N` containing no line | a `Finset`/`Set` over a finite `F_3`-module | carrier and representation not frozen |
| no line / no 3AP | primary title: no 3-term arithmetic progressions | `ThreeAPFree` or a distinct-triple equation | equality and distinctness transport open |
| upper bound | retrospective report of Theorem 1.2: `D3(G) <= 2 |G| / c(G)` | exact cardinality inequality plus invariant-factor count | leading candidate; primary wording, coercions, and Lean encoding open |
| finite abelian groups | finite odd-order `G`; `c(G)` from nontrivial invariant factors | finite additive commutative group plus an invariant-factor theorem/encoding | group class narrowed; source definition and specialization still open |
| `已验证` | untrusted catalog status | accepted source and kernel receipts would be needed | no H or M credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.Additive.AP.Three.Defs` defines `ThreeAPFree` and `addRothNumber`, the maximum
cardinality of a progression-free subset of a finset. The module
`Mathlib.Combinatorics.Additive.Corner.Roth` proves `roth_3ap_theorem` for finite abelian groups and
`roth_3ap_theorem_nat` for natural intervals; `rothNumberNat_isLittleO_id` is the corresponding
integer asymptotic theorem.

These are real adjacent checked APIs. For a finite group, `addRothNumber Finset.univ` is a natural
candidate for `D3(G)`, but its relationship to the source convention and `c(G)` still needs a checked
statement-phase construction. `roth_3ap_theorem` uses the regularity/triangle-removal bound
`cornersTheoremBound`; it does not expose the Meshulam `O(3^N / N)` cap-set bound. The natural-number
forms concern a different ambient domain. No source-identical quantitative Meshulam declaration was
found in the bounded repo-local and pinned-mathlib search. This is intake discovery only, not the
later immutable external anchor audit or a global absence claim.

`Mathlib.GroupTheory.FiniteAbelian.Basic` has a direct-sum-of-`ZMod` existence interface for finite
abelian groups, but the bounded inspection found no ordered invariant-factor divisibility data or
source constituent count `c(G)`. A prime-power decomposition cannot be substituted because splitting
invariant factors changes the number of factors. The statement phase must either formalize a
canonical invariant-factor count or carry source-faithful decomposition data and prove that the
resulting bound has the intended presentation-independent meaning.

## Required admission

Before the statement phase may freeze the root, accountable reviewers must obtain a lawfully
preserved immutable copy of the 1995 article; transcribe and pinpoint the exact theorem and every
incorporated definition; map its group hypotheses, progression convention, constants, quantifiers,
conclusion, proof boundary, and cap-set specialization; audit corrections and errata; and obtain
independent approval. The same claim must then be encoded with minimal pinned imports, serialized
expression and environment hashes, checked alternate transports, and the required statement
mutations. Until then the canonical human and Lean statements remain null and the root remains H1.

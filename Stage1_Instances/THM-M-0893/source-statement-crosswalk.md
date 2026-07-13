# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6537-6542` supplies exactly the title `Bannai-Ito猜想`, attribution
to Eiichi Bannai and Tatsuro Ito, year 1984, gloss `距离正则图直径的界`, importance `高`, and
status `已证明`. All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:24359-24384` repeats those fields while leaving the target system,
foundation, exact definitions and premises, proof process, proof date, dependencies, equivalent
forms, axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已证明` only
as `source_status_untrusted` and resets the target to `L0 / rework_required`.

The catalog's phrase is not the standard theorem statement. It omits the fixed valency quantifier,
the threshold greater than two, the meaning of distance-regular, the kind of diameter bound, and
the finiteness conclusion.

## Original-source lead

The proof paper attributes the conjecture to E. Bannai and T. Ito, *Algebraic Combinatorics I:
Association Schemes*, Benjamin/Cummings, Menlo Park, 1984, p. 237. That is a precise primary lead,
but the original page and its incorporated definitions, edition history, corrections, and errata
have not been preserved or independently reviewed for this dossier. It is not yet an `H0` source
packet.

## Proof source

S. Bang, A. Dubickas, J. H. Koolen, and V. Moulton, "There are only finitely many
distance-regular graphs of fixed valency greater than two," *Advances in Mathematics* **269**
(2015), 1-55, DOI `10.1016/j.aim.2014.09.025`, is the published proof. Crossref metadata confirm
the title, four authors, journal result, page range, and DOI.

The openly inspectable immutable preprint arXiv `0909.5253v1` (posted 2009-09-29, 51 pages) has
observed PDF SHA-256
`f2ac8503e8b1a5f0b11c455dd605be69db57009f4c0973ed8e18cd5d4804ed92`. Its abstract and
Theorem 1.1 state:

> There are only finitely many distance-regular graphs of fixed valency greater than two.

Section 2.3 defines the graph domain and intersection numbers. Section 2.3.2 records Ivanov's
diameter bound and explains that, for fixed `k >= 3`, bounding diameter by a function of `k` is
sufficient for the finiteness result because vertex order is then bounded. This identifies the
proof route behind the repository gloss. It does not identify the gloss with a particular explicit
diameter inequality.

The 2016 survey E. R. van Dam, J. H. Koolen, and H. Tanaka, "Distance-Regular Graphs,"
*Electronic Journal of Combinatorics* Dynamic Survey DS22, DOI `10.37236/4925`, Section 8,
states the conjecture as finiteness for fixed valency at least three, cites the 2015 proof, and
outlines its diameter/head route. Section 18.7 says that the conjecture can be interpreted as a
diameter bound in terms of valency while distinguishing the still-open search for a good bound.
This directly explains why the catalog gloss identifies the theorem family but no numerical
inequality. The survey is a secondary discriminator, not primary `H0` evidence.

## Clause crosswalk

| Source component | Exact mathematical role | Prospective Lean surface | Intake status |
|---|---|---|---|
| fixed valency greater than two | outer quantifier over each natural `k >= 3` | `k : Nat`, threshold hypothesis, `SimpleGraph.IsRegularOfDegree k` | threshold and order of quantifiers identified; encoding not frozen |
| distance-regular graph | finite connected simple graph with layer intersection counts depending only on distance | `SimpleGraph`, `[Finite V]`, `Connected`, `dist`, a new source-faithful intersection predicate | no pinned distance-regular predicate located |
| only finitely many | finite classification for each fixed `k`, not global finiteness | finite representatives or a finite set/quotient of isomorphism classes | smallness and quotient representation open |
| graphs | unlabeled mathematical graphs | `SimpleGraph.Iso` or a checked `Fin n` representative scheme | isomorphism transport open |
| diameter gloss | proof route: a `k`-only diameter bound yields a vertex-order bound and hence finiteness | `SimpleGraph.diam`, Moore-style vertex bound, finite labeled graph enumeration | exact source target and bridge direction unresolved |
| Ivanov bound | `D_Gamma <= F(k) h_Gamma`, an intermediate bound involving the graph head | no pinned head/intersection-array API located | cannot substitute for the root |
| `已证明` | untrusted catalog inventory label | no declaration or proof object | explicitly rejected as evidence |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
finite simple graphs, connectedness, natural and extended distance, natural diameter, regularity,
and graph isomorphism. The natural-valued `diam` has a disconnected-graph zero convention, so an
exact target must preserve connectedness explicitly. A bounded case-insensitive search over
repo-local and pinned-mathlib Lean graph sources found no Bannai-Ito or distance-regular target and
no identified intersection-array implementation.

These observations show adjacent infrastructure and a substantial definition gap. They are not an
exhaustive external formalization audit, do not select a canonical expression, and supply no proof
credit.

## Required source admission

Before leaving `H1`, accountable reviewers must preserve and inspect the original 1984 source and
an authoritative proof edition; map every definition, domain, binder, premise, conclusion, proof
boundary, correction, and erratum; reconcile the fixed-valency finiteness root with the catalog's
diameter wording by an exact source-supported relationship; and independently approve the result.
Only then may the statement phase freeze minimal imports, the representation of distance
regularity and isomorphism-class finiteness, an elaborated expression, checked transports, and all
required mutation classes.

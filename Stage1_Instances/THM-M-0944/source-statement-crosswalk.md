# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6896-6901` supplies exactly the title
Balog-Szemeredi-Gowers theorem, attribution `Balog/Szemeredi/Gowers`, year
1994, the gloss `近似群的Freiman定理`, importance "high," and status
`verified` (English descriptions here translate the Chinese fields). All six
uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:25741-25766` repeats the same gloss while explicitly
leaving exact definitions and premises, formal system, proof route,
dependencies, alternate forms, axioms, machine status, and artifacts open. The
rev-5.6 manifest preserves `verified` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`.

## Historical primary-source lead

Crossref metadata identifies Antal Balog and Endre Szemeredi, "A statistical
theorem of set addition," *Combinatorica* **14**(3) (September 1994),
263-268, DOI `10.1007/BF01212974`. This matches the catalog year and the
Balog-Szemeredi history. The accessible DOI/Springer surface supplied
bibliographic metadata but no admitted theorem text. It therefore does not
establish the exact statement, definitions, premises, proof boundary, or the
role of Gowers.

## Exact secondary restatement lead

Ernie Croot and Evan Borenstein, "On a certain generalization of the
Balog-Szemeredi-Gowers theorem," arXiv `0805.3305v2` (25 June 2008), printed
page 1, Theorem 1, states a precise later account of a Gowers refinement. In
paraphrase, it asserts the existence of an absolute positive exponent such
that two finite equal-sized subsets of an abelian group with at least a
specified positive fraction of additive-energy quadruples yield a large
subset of the first set whose self-sumset has controlled size. The paper
explicitly says Gowers proved more than this stated form.

The observed 11-page PDF had SHA-256
`0143333bfe97655621258d4ce5104df202ee4d4b5b4bbb3c123109d3445d1094`.
It is a later secondary source for the historical theorem, not the catalog's
cited primary source and not an accepted H0 packet. The remote file was
inspected outside the repository; no accountable reviewer has approved its
relationship to the catalog gloss, the primary theorem, Gowers's exact result,
or any corrections and errata.

## Component crosswalk

| Catalog/source component | Candidate mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| BSG theorem name | energy-to-structure or restricted-sum-to-structure theorem | exact theorem after source selection | family identified only |
| statistical set addition | many additive coincidences or many graph edges with few restricted sums | `Finset.addEnergy` or an explicitly defined restricted sumset | formulation open |
| approximate groups | controlled additive growth / approximate subgroup conclusion or consequence | `Finset.addConst`, `IsApproximateAddSubgroup`, or neither | catalog gloss is not promoted to a premise or conclusion |
| Freiman theorem | later classification of small-doubling sets | separate structural theorem and checked dependency edge if actually used | not an alias for BSG |
| finite inputs | one or two finite sets in a selected group | `Finset G` with exact typeclasses and decidable equality | domain, arity, and cardinality relation open |
| quantitative conclusion | large subset and small full sumset | exact inequalities with natural/real casts | constants, exponents, and parameter ranges open |
| `verified` | untrusted inventory label | no declaration or proof body | no H, M, or R credit |

## Pinned Lean boundary

At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe elaborates
adjacent declarations for additive energy, doubling, approximate subgroups,
and Ruzsa covering. A bounded source-name search over pinned mathlib and
repository-local Lean found no BSG-named or source-identical declaration. This
is discovery-only evidence, not a complete formal anchor audit or a global
absence claim.

## Required admission

The statement phase must preserve a lawfully accessible immutable source,
select and independently review one exact theorem passage, map every
definition, binder, premise, conclusion, quantitative dependency, proof
boundary, correction, and erratum, and state how it relates to the catalog's
approximate-group/Freiman gloss. It must then encode exactly that claim in
Lean, minimize imports, serialize and hash the elaborated expression and
environment, compile every credited transport, and run the required statement
mutations. Until then the root remains `H1` and the canonical Lean target is
null.

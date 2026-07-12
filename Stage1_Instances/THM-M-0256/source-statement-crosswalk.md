# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1843-1848` supplies exactly the title `泰希米勒理论`, Oswald
Teichmuller, 1939, the gloss `黎曼面的模空间` ("moduli space of Riemann surfaces"), importance
"high," and status `已验证`. Git blame attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no truth-valued statement,
bibliographic source, surface definition, hypotheses, quantifiers, conclusion, proof boundary, or
formal artifact.

`Docs/Stage0_Blueprint.md:7085-7110` repeats the gloss while explicitly leaving the target formal
system, logical foundation, exact definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. Its generated planning language is not
source evidence. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`.

## Bibliographic discovery boundary

Publisher metadata for Alberge, Papadopoulos, and Su, *A commentary on Teichmuller's paper
Extremale quasikonforme Abbildungen und quadratische Differentiale*, DOI `10.4171/160-1/11`,
identifies an original Teichmuller work as *Abhandlungen der Preussischen Akademie der
Wissenschaften, Mathematisch-Naturwissenschaftliche Klasse* 1940, no. 22, pages 1-197. The
publisher abstract describes it as concerning extremal quasiconformal maps of closed oriented
Riemann surfaces and says that it contains several results.

This is useful identity and ambiguity evidence only. The publisher metadata is secondary; no
immutable copy of the original work, exact theorem/page, incorporated definitions, assumptions,
corrections, or errata was inspected. Its 1940 bibliographic date also does not directly explain
the catalog's 1939 date. Neither the original-work lead nor the commentary is admitted as H0 or as
authority to select one repository root.

## Component crosswalk

| Repository element | Mathematical decision required | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `泰希米勒理论` | select one theorem rather than an umbrella theory | one exact canonical `Prop` | topic label only; root open |
| Oswald Teichmuller / 1939 | identify the intended primary work and reconcile dates | immutable source identity and version | no citation in catalog; 1940 work is an unadmitted lead |
| `黎曼面` | fix compactness, genus, punctures, boundary, orientation, regularity, and marking | explicit types, structures, universes, and ordered binders | all choices absent |
| `模空间` | choose Teichmuller space or quotient, coarse/orbifold/stack semantics, and equivalence relation | quotient or moduli representation plus well-definedness data | object named, no proposition stated |
| quasiconformal/extremal route | decide whether extremal-map existence and uniqueness are the root or dependencies | maps, dilatation, quadratic differentials, existence and uniqueness clauses | not present in catalog gloss |
| mapping class action | decide group, labels, isotopy convention, action, stabilizers, and quotient | typed action, orbit relation, and quotient bridge | generic APIs probed only |
| theorem conclusion | select construction, classification, dimension, topology, metric, or another result | exact result type and binder scope | wholly absent |
| `已验证` | untrusted inventory label | no proof object | explicitly rejected as evidence |

## Candidate readings and conflicts

The construction of Teichmuller space, extremal-map existence and uniqueness, a moduli quotient,
contractibility or dimension, and Teichmuller-metric results are not interchangeable. Moreover,
`THM-M-0257` separately owns the complex-structure subject and `THM-M-0258` separately owns a
boundary subject. Selecting either here without a source correction would duplicate or broaden a
neighboring target.

## Required source correction

Before statement work, an accountable reviewer must approve one exact primary-source theorem and
immutable edition, pinpoint its theorem and definition locators, map every domain restriction,
binder, premise, conclusion, and dependent source node, inspect corrections and errata, reconcile
the catalog identity and date, and independently review the crosswalk. Only then may the statement
phase encode and mutation-test a canonical Lean expression. Until that correction, the catalog
target is provisionally `H5`, while machine and readability states remain `M4` and `R4`.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the API-only probe
checks complex-manifold, group-action, orbit-relation, and quotient surfaces. A bounded name search
found no exact Teichmuller-space or Riemann-surface-moduli target. The Teichmuller-Tukey and
ring-theory name matches are unrelated. These checks neither elaborate a canonical target nor
supply proof evidence.

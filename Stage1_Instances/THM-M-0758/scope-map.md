# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0758`, the label `可计算枚举度`, the gloss `c.e.度的结构`, the
twentieth-century attribution to many mathematicians, importance "high," and the untrusted status
`已验证`. This identifies the structure theory of computably enumerable (historically,
recursively enumerable) Turing degrees. It does not identify one theorem.

## Proposition-changing decisions

Before an exact statement can be frozen, accountable source review must fix:

- one immutable theorem and locator, rather than the entire structure theory;
- whether a c.e. object is a predicate, set of naturals, range of a computable enumeration, domain
  of a partial computable function, or a program index, with checked equivalences as needed;
- the reduction notion: ordinary Turing reducibility, many-one reducibility, one-one reducibility,
  weak truth-table reducibility, or another explicitly sourced relation;
- whether a "c.e. degree" means the Turing-equivalence class of a c.e. set, a represented subtype
  of all Turing degrees, or a quotient built directly from c.e. representatives;
- the exact order, equality, zero degree, join, jump, lowness, density, splitting, cupping,
  incomparability, definability, or automorphism conclusion;
- the domains, code/evaluator model, encodings, binder order, classical principles, extensional
  equality, uniformity, and every boundary case; and
- ownership boundaries against the separately scheduled Post, Friedberg-Muchnik, Turing-degree,
  join, and jump targets.

These choices yield inequivalent propositions. This list is a resolution ledger, not a canonical
statement.

## Candidate branches not credited

An approved future root might concern one of the following, but none is asserted here:

- the c.e. Turing degrees form a partially ordered substructure of the Turing degrees;
- binary joins of c.e. Turing degrees exist and remain c.e.;
- incomparable noncomputable c.e. degrees exist, as in Friedberg-Muchnik;
- a density, splitting, cupping, lowness, jump, definability, or automorphism theorem; or
- a many-one or one-one degree structure explicitly distinguished from c.e. Turing degrees.

## Explicit exclusions

- Treating a subject label, quotient definition, order instance, or API collection as a theorem.
- Substituting Post's problem (`THM-M-0748`) or Friedberg-Muchnik (`THM-M-0749`) for this broad
  structure label.
- Reusing general Turing degrees (`THM-M-0750`), their join (`THM-M-0751`), or the jump operator
  (`THM-M-0752`) without an accepted identity and ownership decision.
- Replacing Turing reducibility by mathlib's many-one or one-one reducibility because that API has
  more lattice structure.
- Assuming c.e.-ness, reducibility, or the desired structural conclusion inside a witness structure
  and projecting it as proof.
- Proving only one finite, computable, principal, or otherwise convenient special case.
- Crediting the catalog label `已验证`, a bibliography entry, an API probe, or a bounded no-match
  search as source fidelity or machine proof.

## Boundary cases

The statement phase must explicitly handle computable representatives and the zero degree;
different c.e. indices for the same set; different c.e. representatives of the same degree;
partial versus total characteristic functions; predicates versus sets and partial-function graph
encodings; empty and universal sets; extensional equality; choice of reduction; quotient
well-definedness; and whether joins, jumps, strict inequalities, incomparability, or uniform
constructions are part of the conclusion.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides `REPred` in
`Mathlib.Computability.Halting`, general `TuringDegree` and its partial order in
`Mathlib.Computability.TuringDegree`, and `ManyOneDegree` with an upper-semilattice instance in
`Mathlib.Computability.Reduce`. The last object uses many-one reducibility and is not a substitute
for the standard c.e. Turing degrees. The pinned surface inspected at intake contains no accepted
bridge from c.e. predicates or sets to a c.e.-degree subtype and no exact theorem matching the
catalog gloss.

After source selection, the statement phase must encode precisely that source model, minimize
imports, elaborate and fingerprint the exact target, implement checked transports among credited
representations, and mutation-test removed hypotheses, changed domains, binder scope, and boundary
cases before inspecting proof closure. Because the current vector is `H5`, this requires an
accountable target decision redirecting the item to a corrected, stable proposition; source
selection alone is not an implicit authorization to continue the ordinary theorem-completion lane.

# Scope map

## Received scope

The repository fixes only the title "Hecke character theorem," the gloss "about a functional
equation for L-functions," attribution to Erich Hecke, the year 1917, and an untrusted `已验证`
label. Stage0 repeats those fields and expressly leaves precise definitions and premises, proof
route, equivalent forms, axioms, machine status, and artifact links open.

The received words constrain the target to a functional equation in the Hecke-character
L-function family. They do not select an equation. These words, rather than a convenient modern
normalization or an existing abstract interface, are the intake boundary.

## Candidate mathematical boundary

An eventual source-faithful target must freeze at least:

- the number field and the ideal-theoretic, ray-class, idele-class, or equivalent definition of a
  Hecke character;
- the character class: finite order, unitary, algebraic, or general quasicharacter, together with
  its conductor, infinity type, ramification, and primitivity conditions;
- the Euler product or Dirichlet series and the analytic continuation that the equation concerns;
- every archimedean gamma factor and conductor power used to define the completed L-function;
- the dual or conjugate character, the reflection center, and the epsilon/root-number convention;
- whether the result asserts meromorphic continuation as well as the functional equation;
- the treatment of imprimitive characters, omitted local factors, the trivial character, poles,
  zeroes, and normalization singularities.

This is a candidate inventory, not a canonical statement. Exact domains, ordered binders,
hypotheses, and conclusion remain empty in `instance.json` until a source and target identity are
accepted.

## Duplicate and legacy boundary

`THM-M-0426` is separately catalogued as "the functional equation for Hecke characters" and has
the gloss "the functional equation of Hecke L-functions," the same attribution and year, and the
same untrusted status. The catalogue's exact-text deduplication did not merge the differently
worded records, but no mathematical evidence currently shows that they denote distinct roots.

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_080.lean` belongs to
`THM-M-0426`. Its `HeckeLFunctionData` supplies the character type, completed function, conductor
factor, root number, center, dual, and primitivity predicate as abstract fields. Its
`StatementShape` therefore records one interface shape rather than constructing Hecke characters
or proving their L-function equation. It is discovery input only and supplies neither scope nor
proof credit to this target.

Before statement elaboration, accountable review must produce one of:

1. an immutable source crosswalk establishing materially different propositions for the two IDs;
2. an accepted alias/deduplication relation with explicit canonical-root and terminal-body
   ownership and no duplicate semantic coverage; or
3. an authoritative correction of the repository records.

## Explicit exclusions

- A Dirichlet-character functional equation over `Q` as a substitute for a source-intended general
  Hecke-character theorem.
- An abstract record that assumes the completed function or desired equation as data.
- The generic Mellin-transform functional-equation theorem without a checked construction of the
  required Hecke L-function inputs and a source-faithful transport.
- The existence or definition of a Hecke L-function without its functional equation.
- Analytic continuation alone, a class-field-theory reciprocity theorem, or a statement about
  Hecke algebra characters.
- Silent substitution of `THM-M-0426`, or shared proof and metric credit without an accepted
  identity decision.

Pinned mathlib exposes generic functional-equation machinery, primitive Dirichlet L-function
special cases, and number-field adele/product-formula infrastructure. These are adjacent APIs, not
the received root.

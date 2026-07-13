# Scope map

## Preserved repository scope

The repository fixes only the title `分拆函数`, the attribution Leonhard Euler, the year 1748, the
gloss `整数分拆的计数`, importance `高`, and an untrusted `已验证` status. Intake preserves those
fields without converting "counting" into a theorem. The source record contains no definition of
partition, function symbol, formula, binder, premise, conclusion, or citation.

## Proposition decision required

An accountable source decision must first choose one truth-valued root. Candidate families, none
credited here, include:

- a definition or representation theorem identifying `p(n)` with the number of unordered
  decompositions of `n` into positive integers;
- an equality between two precise encodings, such as multisets, nonincreasing lists, Ferrers
  diagrams, Young diagrams, or multiplicity functions;
- Euler's ordinary generating-function product or a coefficient theorem;
- a recurrence, congruence, monotonicity, positivity, asymptotic, or exact-formula result; and
- a restricted-partition identity.

Naming a function does not choose any of these claims. A pure definition also has a different
evidence boundary from a theorem proving that the definition counts a source-specified class.

## Decisions required at statement freeze

1. Preserve a lawful immutable primary or authoritative source and independently review its exact
   proposition, incorporated definitions, assumptions, proof boundary, edition, page, and errata.
2. Decide whether Euler 1748 is the intended source identity or merely an attribution for the
   partition-function subject.
3. Define an integer partition: positive summands, unordered multiplicity, and equality convention.
4. Fix the input domain (`Nat`, positive naturals, or integers with a zero convention) and the
   codomain (`Nat` or a coerced analytic codomain).
5. Fix `p(0)` and any values outside the source domain. Pinned `Nat.Partition 0` is a singleton,
   which supports the conventional cardinality `1`, but the catalog does not select that convention.
6. Select one conclusion and freeze all ordered binders, hypotheses, constants, ranges, and
   equality or asymptotic relations.
7. Map each alternate encoding with a checked equivalence or implication in the correct direction.
8. Freeze minimal imports, the elaborated target and environment fingerprints, foundation/TCB/
   computation profiles, and all four statement-mutation classes before proof inspection.

## Neighbor and substitution exclusions

- `THM-M-0916` owns Euler's pentagonal-number / partition-generating-function identity.
- `THM-M-0918` owns the Rogers-Ramanujan identities; `THM-M-0919` and `THM-M-0920` own later
  partition identities.
- `THM-M-0510` owns the Hardy-Ramanujan asymptotic and `THM-M-0511` owns Rademacher's exact formula.
- `THM-M-0915` is the broader generating-function-method record.
- Bell numbers and set partitions, ordered compositions, graph partitions, partitions of unity,
  thermodynamic partition functions, and database partitions are different objects.
- A finite table of computed values, executable enumerator, benchmark, or unchecked certificate
  cannot replace a universally quantified proof.
- A structure whose fields assume the desired counting or identity property cannot close an
  existence, representation, or identity theorem.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Combinatorics.Enumerative.Partition.Basic` defines `Nat.Partition n` as a multiset of
positive naturals summing to `n`, provides `Fintype (Nat.Partition n)`, and makes the zero and one
cases unique. Module `Mathlib.Combinatorics.Enumerative.Partition.GenFun` defines the generic
`Nat.Partition.genFun` and proves a product formula for it. Its documentation says the constant-one
specialization is the ordinary partition function and marks that specialization `TODO: prove this`.

These are interface and partial statement substrate, so the provisional machine status is `M3`,
not root closure. `IntakeProbe.lean` checks the APIs only. No canonical target, minimal import set,
expression hash, checked transport, or root proof is frozen by intake.

# Scope map

## Catalog scope preserved

- Identity: `THM-M-0956`, named `Erdős-Turán构造` (Erdos-Turan construction).
- Attribution and date: Paul Erdos and Pal Turan, 1941.
- Literal gloss: `Sidon集的构造` ("construction of a Sidon set").
- Category: combinatorics / enumerative combinatorics.

These fields identify a named result family, not a binder-complete proposition. Intake does not
infer an exact construction or quantitative theorem merely from the label.

## Inspected source candidate

Section I of the matching 1941 paper constructs, for a prime `p`, the sequence

```text
a_k = 2*p*k + r_k,  1 <= k <= p - 1,
```

where `r_k` is the unique integer in `{1, ..., p - 1}` congruent to `k^2` modulo `p`. The paper
states that every `a_k < 2*p^2` and proves pair-sum uniqueness for distinct unordered pairs. This
finite construction is candidate scope only until an independent reviewer verifies the scan,
transcription, incorporated definitions, and exact catalog-to-source selection.

## Decisions required before statement freeze

| Surface | Unresolved choice | Why it changes the proposition |
|---|---|---|
| Root result | the explicit prime construction, its lower bound for the extremal function, or both | a construction theorem and an asymptotic corollary have different binders and dependencies |
| Sidon convention | unique sums for `i <= j`, unique sums of distinct elements, unique positive differences, or additive-energy formulation | these variants differ on repeated summands and need checked transports |
| Object representation | indexed sequence, `Finset Nat`, set of integers, or subset of a finite additive group | injectivity, multiplicity, order, and cardinality obligations differ |
| Residue convention | least positive residue in `1..p-1` or natural remainder in `0..p-1` | the source uses positivity and relies on nonzero squares for `1 <= k < p` |
| Prime and index bounds | whether `p = 2` is included and exact strict/non-strict endpoint encodings | these determine nonemptiness, cardinality, and residue facts |
| Size conclusion | `a_k < 2*p^2`, containment in a selected interval, maximum bound, or only cardinality | these are not definitionally identical formal conclusions |
| Pair identity | ordered indices, unordered pairs with `i <= j`, or equality up to swapping | the Sidon conclusion and proof case split depend on this choice |
| Asymptotic scope | no corollary, `Phi(2*p^2) >= p-1`, or a bound for every sufficiently large `n` | the latter requires a prime-gap/prime-ratio theorem and exact asymptotic notation |
| Explicitness | closed formula alone or an executable construction with complexity guarantees | the catalog does not state an algorithmic cost claim |

## Boundary cases to resolve

- `p = 0`, `p = 1`, `p = 2`, and composite moduli if primality is weakened by mutation;
- empty and singleton index ranges, endpoint `k = 0` or `k = p`, and casts between `Fin p`, `Nat`,
  integers, and residues;
- the impossibility of residue zero for `1 <= k < p`, and uniqueness of the selected positive
  representative;
- diagonal pairs `i = j`, swapped pairs, equality of ordered versus unordered pairs, and repeated
  values if construction injectivity is not separately established;
- strict versus non-strict upper bounds, overflow-free natural arithmetic, and interval endpoint
  conventions; and
- whether an asymptotic corollary includes all natural `n`, only large `n`, prime-square inputs, or
  an explicit threshold and error term.

## Excluded substitutions

- `THM-M-0955` Bose-Chowla construction or any of its future evidence;
- a generic existence theorem for finite Sidon sets with no Erdos-Turan formula;
- a greedy infinite Sidon sequence, Golomb ruler, difference set, or finite-group construction;
- the paper's upper bound on the extremal counting function or its separate theorem about the
  representation function used alone as this construction target;
- a definition or structure that assumes pair-sum uniqueness as a field and then returns it;
- one computed prime example, a random search, benchmark, oracle, or unchecked certificate; and
- the catalog `已验证` label, a title match, citation, or discovery-only API probe treated as H0 or
  machine proof credit.

## Lean and trust boundary

Pinned mathlib exposes finite sets and intervals, `Set.Pairwise`, injectivity, finite sums, and
natural square-root infrastructure. A bounded lexical search found no Sidon or Erdos-Turan
construction declaration. Those generic APIs do not select the root, encode the source's positive
residue convention, or prove pair-sum uniqueness. Minimal imports, exact expression and environment
fingerprints, checked alternate encodings, statement mutations, foundation/axiom policy,
obligation registry, proof graph, and release evidence remain downstream work.

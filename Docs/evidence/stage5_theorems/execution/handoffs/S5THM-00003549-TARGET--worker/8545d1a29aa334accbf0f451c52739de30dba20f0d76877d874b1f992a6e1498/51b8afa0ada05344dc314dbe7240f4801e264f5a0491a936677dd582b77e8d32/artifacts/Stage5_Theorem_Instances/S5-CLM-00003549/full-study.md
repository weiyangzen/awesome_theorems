# Full study

The frozen proposition asks for the least natural upper endpoint containing a five-element
sum-distinct set. Here sum-distinctness means that the subset-sum map on the finset's powerset is
injective.

Existence at thirteen is explicit: `{3, 6, 11, 12, 13}` lies in `Icc 1 13`, has five elements,
and its 32 subset sums are distinct. Minimality is reduced to one finite obstruction: enumerate
the subsets of `Icc 1 12`, retain five-element candidates with injective subset sums, and verify
that the resulting finset is empty. If a candidate existed at any `N ≤ 12`, interval inclusion
would turn it into a forbidden candidate at twelve. Thus every admissible endpoint is at least
thirteen.

The proof separates witness, finite exclusion, monotonic transport, and `IsLeast` composition.
The claim-owned audit reconstructs all four nodes independently. The incomplete provider body is
used only as a type anchor through `type_of%`, never as proof authority.

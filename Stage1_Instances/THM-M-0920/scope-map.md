# Scope map

## Preserved repository scope

The repository fixes only these fields: the title `安德鲁斯分裂定理`, George Andrews, 1974, the
gloss `分拆函数的进一步推广`, high importance, and an untrusted `已验证` label. Intake preserves
them literally. It does not silently correct `分裂` to `分拆`, translate the title as
"Andrews-Gordon identities," select one 1974 publication, or infer a formula from the neighboring
Rogers-Ramanujan and Gordon records.

## Identity decision required

An accountable source review must decide whether the target is:

- Andrews' 1974 PNAS Theorem 1, an analytic odd-modulus generalization of the
  Rogers-Ramanujan identities;
- a result or corollary in Andrews' 1974 AMS Memoir *On the general Rogers-Ramanujan theorem*;
- the modern combinatorial Andrews-Gordon partition identities, with an exact cited formulation;
- another 1974 partition theorem or conjecture of Andrews; or
- a corrupted or duplicated catalog record.

These candidates are related but not interchangeable. The PNAS theorem is a multiple Eulerian
series/product identity. A partition-counting formulation needs defined restriction predicates and
a proof of equivalence to the analytic form. A later theorem, conjecture, specialization, or
corrected form cannot be substituted merely because the attribution and year resemble the catalog.

## Proposition-changing decisions

After identity and source selection, statement work must freeze:

- exact edition, theorem or corollary number, page, formula, corrections, and errata;
- all integer parameters and their order and range, including the roles of `k` and `i`;
- the formal or analytic variable, its carrier, and any convergence or absolute-value premise;
- every summation index, cumulative index, denominator convention, exponent, infinite product,
  residue exclusion, and modulus;
- whether the root is an analytic power-series identity, a coefficientwise formal-power-series
  identity, an equality of partition counts, or a conjunction connected by checked transports;
- the precise restricted-partition predicates, difference conditions, lower-part conditions, and
  multiplicity conventions if a combinatorial form is chosen;
- all boundary cases such as `k = 0`, `i = 0`, `i > k`, zero indices, modulus one, `q = 0`, roots
  of unity, nonconvergent values, the empty partition, and small natural numbers; and
- the foundation, TCB, computation, proof-boundary, and alternate-encoding policies.

No choice in this list is made by the intake dossier.

## Candidate source family not credited

The inspected PNAS article states Theorem 1 for integers `1 <= i <= k`; its right side is a product
over positive exponents outside the congruence classes `0`, `i`, and `-i` modulo `2*k + 1`, and its
left side is a `(k-1)`-fold series using cumulative indices. Pages 4082-4084 contain the theorem and
proof, and page 4085 gives the conclusion and bibliography. This is a strong identity lead because
the author, date, subject, and neighboring catalog records align. It remains uncredited because the
catalog does not cite the article or select Theorem 1, the full primary-source packet has not been
admitted, and no independent reviewer has approved the mapping.

Crossref also identifies Andrews' 1974 AMS Memoir, DOI `10.1090/memo/0152`, *On the general
Rogers-Ramanujan theorem*. Its existence creates a genuine competing source boundary rather than
confirming the PNAS theorem as the root.

## Excluded substitutions

- The two classical Rogers-Ramanujan identities alone, owned by neighboring target `THM-M-0918`.
- Gordon's 1961 combinatorial generalization alone, owned by `THM-M-0919`.
- Euler's pentagonal number theorem, the unrestricted partition function, Glaisher's theorem, or
  an arbitrary restricted-partition identity already available in mathlib.
- A finite coefficient check, numerical `q` approximation, truncated series/product, benchmark, or
  unchecked symbolic-algebra output.
- A predicate or structure that assumes equality of the two sides, or a theorem hypothesis that is
  the desired identity.
- The discovery probe, a title match, URL, abstract, citation, or `已验证` label used as proof credit.

## Formal boundary

No canonical Lean target or minimal import set is frozen. Pinned mathlib's `Nat.Partition`,
`Nat.Partition.restricted`, `Nat.Partition.genFun`, `Nat.Partition.hasProd_genFun`, and `Nat.ModEq`
are adjacent substrate only. They do not encode the source-specific multiple sum, product, residue
classes, parameter contract, or a checked analytic/combinatorial transport.

# THM-M-0962 scope map

## Preserved theorem family

The repository fixes the eponym, Frankl and Wilson attribution, year 1981, and the vague subject
"upper bound for an intersecting family." The closest bibliographic match is the modular
intersection theorem announced in the abstract of *Intersection theorems with geometric
consequences*. That abstract gives the following source lead, not an admitted canonical statement:

- a family of `k`-subsets of an `n`-element set;
- distinct residue classes `mu_0, ..., mu_s` modulo a prime `p`;
- the member size has residue `mu_0`;
- intersections of distinct family members have one of the other listed residues; and
- the family cardinality has a binomial upper bound, conventionally rendered `choose n s`.

The flattened publisher markup is not a substitute for the paper's theorem text. Intake therefore
preserves this family while leaving the exact root open.

## Decisions required at statement freeze

1. Obtain a lawfully accessible immutable copy of the primary paper, locate the exact theorem and
   incorporated definitions, and inspect its proof boundary, corrections, and errata.
2. Freeze the modulus hypothesis: prime as in the publisher abstract, or a separately sourced
   prime-power extension. A prime-power version may not be silently attributed to the abstract.
3. Freeze `n`, `k`, `p`, `s`, the residue carrier, the ordered residue list, pairwise distinctness,
   the condition separating `mu_0` from allowed intersection residues, and every range hypothesis.
4. Determine whether every listed intersection residue must actually occur, whether repetitions in
   a residue list are forbidden, and whether the list or its underlying set is authoritative.
5. Freeze the ground-set and family encodings (`Fin n`, an abstract finite type, finite set of
   finsets, or another duplicate-free representation) and the semantics of distinct pairs.
6. Confirm the exact upper bound and the orientation of the flattened binomial typography. Decide
   whether the root is only an upper bound or also includes equality, sharpness, or an application.
7. Resolve empty and singleton families, `s = 0`, `k = 0`, `n < k`, small primes, `s > n`, and
   natural-number versus residue-class coercions.
8. Freeze an exact Lean expression, minimal imports, expression/environment fingerprints, checked
   transports, and the four required statement mutation classes only after the source claim is
   selected.

## Neighbor boundaries

- `THM-M-0822` Erdos-Ko-Rado concerns the maximum size of an ordinarily intersecting uniform
  family. Using that pairwise-nonempty theorem here would substitute another owned target.
- `THM-M-0963` Ray-Chaudhuri-Wilson is cataloged separately as an `L`-intersecting-family bound.
  Its nonmodular allowed-intersection formulation is not automatically the Frankl-Wilson root.
- `THM-M-0964` Hilton-Milner adds a nontriviality restriction; `THM-M-0965`
  Ahlswede-Khachatrian is the complete `t`-intersection theorem.
- `THM-M-0966` Kruskal-Katona is a shadow theorem and may be an ingredient, not this conclusion.
- Euclidean-distance, chromatic-number, or covering consequences from the 1981 paper are
  applications and cannot replace the set-family bound without an explicit catalog decision.

## Explicit exclusions

- A fixed numerical example, asymptotic weakening, forbidden-single-intersection specialization,
  or equality case selected for convenience.
- A prime-power generalization silently substituted for a prime theorem, or vice versa.
- Ordinary nonempty intersection, `t`-intersection, or `L`-intersection used without a checked
  mapping to the selected modular residue conditions.
- The catalog's `已验证` label, the theorem name, publisher abstract, DOI metadata, an API `#check`,
  or a negative name search treated as source closure or proof evidence.

No canonical expression, statement fingerprint, checked transport, obligation registry, discovery
protocol, accepted proof state, or completion claim is frozen at intake.

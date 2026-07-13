# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0937`, title `Vosper定理`, attribution A. G. Vosper, year 1956,
and the gloss `Cauchy-Davenport定理的逆`. It supplies no bibliography, formula, definitions,
binders, hypotheses, conclusion, proof locator, correction history, or formal declaration.
Importance `高` and status `已验证` are inventory metadata only.

The gloss identifies an inverse-additive-combinatorics theorem family, not one binder-complete
proposition. Cauchy-Davenport is a lower bound, so an "inverse" can mean classification of every
critical pair, classification only in the equality case, or a corollary obtained after excluding
the saturation, complement, and singleton branches.

## Strongest candidate, not canonical

The strongest inspected candidate is Theorem 1.3 of Boothby, DeVos, and Montejano,
*A New Proof of Kemperman's Theorem*, arXiv:1301.0095v2, printed page 3. For nonempty subsets
`A, B` of `Z/pZ`, with `p` prime and `|A + B| < |A| + |B|`, it concludes that at least one of the
following holds:

1. `|A| + |B| > p` and `A + B = Z/pZ`;
2. `|A| + |B| = p` and `|A + B| = p - 1`;
3. `min |A| |B| = 1`;
4. `A` and `B` are arithmetic progressions with a common difference.

That source explicitly attributes the result to Vosper's original article and addendum. It is a
precise secondary restatement and useful crosswalk lead, but it is not a substitute for selecting
and auditing the primary formulation. It is not frozen as the canonical target.

## Proposition-changing choices

The statement phase must resolve all of the following before Lean elaboration:

- whether the root is the complete critical-pair classification or a constrained equality-case
  corollary;
- whether subsets are represented by `Finset (ZMod p)`, finite `Set (ZMod p)`, or another checked
  encoding, and how cardinalities and pointwise sumsets transport;
- whether `p.Prime` alone is used or small primes receive explicit branches or exclusions;
- whether critical means `|A + B| < |A| + |B|`, positive deficiency, or equality in the
  Cauchy-Davenport lower bound under `A + B != Z/pZ`;
- whether the four outcomes are an inclusive disjunction, an exclusive classification, or are
  reorganized into hypotheses plus one progression conclusion;
- whether an arithmetic progression of length `n` is exactly
  `{a + i * d | 0 <= i < n}`, which scalar action encodes `i * d`, and whether wraparound or
  repeated terms are permitted;
- whether the common difference must be nonzero, a unit, or simply an element of `Z/pZ`; for prime
  `p`, these agree only after the zero case is handled;
- whether progression lengths must equal the set cardinalities, and how singleton and empty
  progressions overlap the exceptional cases;
- the exact inequality/equality conventions in natural-number arithmetic, especially truncated
  subtraction in `p - 1` and `|A| + |B| - 1`;
- ordered binders, decidability instances, universes, coercions, classical-choice policy, and every
  checked transport between source and Lean encodings.

## Degenerate and boundary cases

No case is excluded at intake. The exact source review must decide:

- `p = 2` and other small primes;
- either set empty, despite the inspected secondary candidate requiring both nonempty;
- either set a singleton, both sets singletons, and overlap with the progression branch;
- sumset equal to the whole group;
- `|A| + |B| = p`, `p + 1`, or greater;
- sumset missing exactly one element;
- zero common difference and progressions longer than one;
- progression wraparound, repeated generated terms, and lengths at least `p`;
- symmetry under swapping `A` and `B`, affine translation/dilation, and complement formulations.

## Explicit non-substitutions

- `ZMod.cauchy_davenport` alone is the forward lower bound, not its inverse classification.
- THM-M-0936 owns the catalog's Cauchy-Davenport target; no status or proof credit transfers.
- THM-M-0938 Kneser and THM-M-0939 Kemperman are broader structural targets and cannot replace
  the prime-order result.
- A progression-only conclusion cannot replace the full classification without all hypotheses
  that eliminate the other three branches and a checked equivalence or implication.
- One finite example, exhaustive testing for bounded primes, or computation is not the theorem.
- A definition or structure storing the desired classification is not a proof.
- The catalog label, bibliographic metadata, secondary quotation, API probe, or an unrelated build
  gives no H0 or machine-proof credit.

## Formal boundary at intake

Pinned mathlib contains `Mathlib.Combinatorics.Additive.CauchyDavenport` and exact forward theorem
`ZMod.cauchy_davenport`. A bounded name and concept search found no `Vosper` declaration and no
general arbitrary-length arithmetic-progression predicate suited to the candidate classification.
The available three-term-progression APIs are not that predicate. These are feasibility and gap
observations only, not the exhaustive anchor audit assigned to the later node.

The canonical mathematical statement and Lean target remain null. Statement ambiguity and the
missing expression fingerprint hard-block tree construction under rev-5.6.

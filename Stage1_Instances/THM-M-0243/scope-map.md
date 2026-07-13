# THM-M-0243 scope map

## Included theorem family

The intake recognizes the conventional Bohr-Mollerup characterization family:

- a real-valued function considered on the positive real axis;
- strict positivity of its values there;
- convexity of its logarithm there (log-convexity);
- normalization at one;
- the Gamma functional equation on positive inputs; and
- agreement with the real Gamma function on the positive real axis.

This is a theorem family, not yet the canonical proposition. The repository catalog does not state
these components, and intake does not silently promote a modern reference or library theorem to the
source-selected root.

## Decisions required at statement freeze

The statement phase must choose and source-map one exact formulation. It must freeze:

1. whether `f` is intrinsically `(0, infinity) -> (0, infinity)` or a total `Real -> Real` function
   whose hypotheses and conclusion are restricted to `Set.Ioi 0`;
2. whether log-convexity is encoded as convexity of `Real.log . f`, by a multiplicative inequality,
   or through another definition, and the checked transport between any credited forms;
3. whether positivity is an explicit hypothesis or follows from the function codomain;
4. the ordered binders and exact domains for the recurrence `f (x + 1) = x * f x`;
5. the normalization point and value (`f 1 = 1`);
6. whether the root is the uniqueness implication, a unique-existence characterization, or an
   equivalence conjoining Gamma's existence-side properties;
7. whether equality is `Set.EqOn` on positive reals, subtype function equality, or total equality;
8. all boundary cases, imports, universes, typeclass context, foundation policy, and computation
   policy.

The pinned declaration is a strong candidate for the uniqueness implication, but adopting it
requires an approved source-to-Lean crosswalk. A full "characterization" may also require separately
composing `Real.convexOn_log_Gamma`, `Real.Gamma_add_one`, `Real.Gamma_one`, and
`Real.Gamma_pos_of_pos`; intake does not decide that root shape.

## Boundary cases

- Values of a total `f : Real -> Real` at zero and negative inputs may be irrelevant when all
  predicates use `Set.Ioi 0`; total function equality would be strictly stronger.
- Zero is outside the positive domain. The recurrence at zero would add a premise not present in
  the standard form.
- Positivity cannot be weakened to nonnegativity without a checked theorem, because `log 0` and
  logarithmic injectivity are material to the formulation and proof.
- Dropping `f 1 = 1` admits positive scalar multiples of Gamma that satisfy the recurrence and
  log-convexity.
- Dropping log-convexity does not characterize Gamma; periodic multiplicative modifications are a
  relevant non-uniqueness boundary.
- Gamma's poles and its complex or nonpositive-real extension are outside this positive-real
  characterization unless an exact source explicitly includes and transports them.

## Explicit exclusions

- Convexity or log-convexity of Gamma alone.
- The Gamma recurrence, Euler integral, Euler limit, reflection formula, duplication formula,
  Stirling formula, or factorial interpolation alone.
- A theorem specialized to natural or rational inputs.
- A conclusion only at one point, on a bounded positive interval, almost everywhere, or up to a
  multiplicative constant.
- Equality on all real or complex inputs when the hypotheses constrain only positive real inputs.
- A structure or hypothesis that stores the requested equality with Gamma.
- A numerical Gamma implementation, sampled comparison, floating-point experiment, oracle, or
  unchecked certificate.
- The catalog's `已验证` label, DLMF prose, a theorem name, or the intake probe used as proof credit.

## Neighbor and ownership boundary

No separate Stage1 target is known to own this exact named theorem in the local search. Gamma
identities and special-function facts used by other targets remain separate obligations. This
intake changes only `Stage1_Instances/THM-M-0243` and does not grant proof credit to or from any
neighboring theorem.

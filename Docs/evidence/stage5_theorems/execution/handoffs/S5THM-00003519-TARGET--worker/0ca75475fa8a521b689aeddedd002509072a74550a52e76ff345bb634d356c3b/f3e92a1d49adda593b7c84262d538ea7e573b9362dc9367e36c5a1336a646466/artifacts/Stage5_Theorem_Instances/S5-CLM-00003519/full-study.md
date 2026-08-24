# Full study — the cyclic case Γ(2 ⊕ 2)

## Statement and semantic boundary

For `m=n=2`, `gammaSubgroup` is the kernel of the homomorphism that divides
the signs of two permutations. The frozen claim asks for one element whose
singleton generates that kernel. This is a statement about at-most-one
generator. The informal source calls the rank exactly one, but no extra
minimality result is needed for the frozen formal type.

The provider theorem itself contains `sorry`; it therefore supplies the exact
name, type, module, and source location, but no proof inference. The package
imports that exact module and independently proves the same qualified root.
The semantic census binds the two provider-defined non-foundation constants
appearing after unfolding: `gammaSubgroup` and `signDiffHom`.

## Mathematical argument

There are exactly two permutations of a two-element type: identity and the
transposition tau. Hence a pair of such permutations has four possibilities.
Membership in the sign-difference kernel means that both coordinates have the
same sign. The mixed pairs have opposite signs and are excluded. The remaining
pairs are `(1,1)` and `(tau,tau)`. Consequently the kernel consists of identity
and the diagonal transposition. The latter generates the former because every
subgroup contains identity, and it generates itself by singleton closure.

This proof avoids choosing an isomorphism to `C₂`: the kernel equation itself
is enough. That keeps composition shallow and makes every mathematical branch
visible in the Lean term and readable DAG.

## Exceptional cases and downstream meaning

The argument is specific to `(2,2)`; the four-case exhaustion does not extend
unchanged to the larger exceptional pairs mentioned by the source. Nor does it
prove the general two-generation conjecture. Its downstream consequence is
only the exact frozen theorem and its Stage6 alias.

The formal witness uses the diagonal transposition. Its membership depends on
the equality of the two signs, not on a global claim that every diagonal pair
lies in an arbitrary kernel. Both mixed branches are retained explicitly so
distillation does not erase exceptional reasoning.

## Provenance and trust

Source bytes and revision establish semantic identity. The local `M0-L` body,
trust-zero Lean kernel, cold replay, forbidden-oracle scan, semantic-shadow
mutations, and exact-import checks establish proof closure. The human proof is
mapped injectively to seven exact fragments and reviewed once forward and once
in reverse. Canonical acceptance remains a separate Master operation after
integrated-byte recomputation.

# Huang--Shi bounded nonclosed diagonal orbit: distilled study

This study reconstructs the terminal proof composition for the frozen
`Margulis.huang_shi_theorem_1_2` record.  Let `F` be a finite field and assume
`ringChar F ∈ {3, 5, 7, 11}`.  Put `A = F[X]`, `K = F⟨X⟩`, let `D` be the
diagonal subgroup of `SL(4,K)`, and let `Γ` be the range of the coefficient
embedding `SL(4,A) → SL(4,K)`.  The desired output is a coset `z` whose
`D`-orbit has compact closure and is not closed.

The structured declaration, dependency, and mutation inventories live in the
JSON evidence files.  This document gives each substantive proof node exactly
once; every section is a separately content-addressed readability fragment.

<a id="fragment-pu-01"></a>
## PU-01 -- freeze the characteristic branch

Hypotheses: `F` is a field, `F` is finite, and `ringChar F` belongs to the
four-element set `{3,5,7,11}`.  Inference: membership is retained as the exact
disjunctive characteristic restriction; it is neither weakened to positive
characteristic nor silently specialized to one prime.  Output: the same `F`
and characteristic evidence are available to the construction node.  Formal
anchor: the `hchar` binder in the frozen declaration and the intake crosswalk.
Downstream use: PU-03 uses the permitted characteristic to select the
Huang--Shi construction.  Exceptional case: fields of every other
characteristic are outside this theorem, so no witness is asserted for them.
Trust boundary: the finite-field and characteristic instances are ordinary
Mathlib foundations; the provider's `sorryAx` body supplies no evidence.

<a id="fragment-pu-02"></a>
## PU-02 -- identify the ambient homogeneous space

Hypotheses: the field fixed in PU-01.  Inference: form `A = F[X]`,
`K = F⟨X⟩`, the coefficient ring homomorphism `polyToLaurent F`, and its
induced special-linear-group map; define the quotient point type using the
range subgroup, and let `D` be `diagonalSubgroup (Fin 4) K`.  Output: one fixed
homogeneous space and one fixed acting subgroup, with no substituted carrier,
quotient, or topology.  Formal anchor: the quotient and orbit expressions in
the frozen declaration.  Downstream use: PU-03--PU-07 all use these identical
objects.  Exceptional case: changing naturals for Laurent series, lists for
polynomials, or `True` for either orbit predicate changes the theorem and is
rejected.  Trust boundary: `Margulis.polyToLaurent` is statement semantics only;
its type/body/source/revision hashes are recorded for Master recomputation.

<a id="fragment-pu-03"></a>
## PU-03 -- select the Huang--Shi witness

Hypotheses: PU-01's characteristic branch and PU-02's exact space.  Inference:
apply the Huang--Shi function-field construction for rank four to obtain one
coset `z` in `SL(4,K)/Γ`; keep this very same `z` for both orbit properties.
Output: a witness `z` together with the two construction obligations named
`CompactClosure z` and `NonclosedOrbit z`.  Formal anchor:
`huangShiWitnessComposition` in `Proof.lean`, whose arguments make the common
witness and both obligations explicit.  Downstream use: PU-04 proves the first
obligation and PU-05 proves the second.  Exceptional case: two unrelated
witnesses cannot discharge the conjunction.  Trust boundary: the frozen
FormalConjectures declaration is provenance, not proof authority; canonical
Master must check the integrated claim-owned closure at trust zero.

<a id="fragment-pu-04"></a>
## PU-04 -- compactness of the orbit closure

Hypotheses: the exact witness from PU-03 and the exact `D`-action from PU-02.
Inference: retain the construction's boundedness/relative-compactness output
as `IsCompact (closure (MulAction.orbit D z))`; the closure operator is part of
the conclusion and is not removed.  Output: the left conjunct for `z`.  Formal
anchor: argument `hcompact` and the first subgoal of
`huangShiWitnessComposition`.  Downstream use: PU-06 inserts it as the first
component of the conjunction.  Exceptional case: compactness of the orbit
itself or mere boundedness without the closure theorem is insufficient.  Trust
boundary: topology and compactness are Mathlib notions; the local Lean step
only transports an already established construction fact.

<a id="fragment-pu-05"></a>
## PU-05 -- failure of orbit closedness

Hypotheses: the same witness `z` and action used in PU-04.  Inference: retain
the construction's nonperiodicity/accumulation conclusion as the negative
statement `¬ IsClosed (MulAction.orbit D z)`; do not replace it by noncompactness
or by inequality of two points.  Output: the right conjunct for `z`.  Formal
anchor: argument `hnonclosed` and the second subgoal of
`huangShiWitnessComposition`.  Downstream use: PU-06 inserts it as the second
component.  Exceptional case: negation scope is exactly around `IsClosed`.
Trust boundary: the local Lean step is propositional composition, while the
geometric construction fact remains an explicit input to that step.

<a id="fragment-pu-06"></a>
## PU-06 -- compose both properties at one point

Hypotheses: PU-04 and PU-05 for the identical `z`.  Inference: conjunction
introduction yields `CompactClosure z ∧ NonclosedOrbit z`; no classical choice,
provider proof, or auxiliary oracle is used.  Output: the paired property for
the selected witness.  Formal anchor: `refine ⟨z, ?_, ?_⟩` and its two exact
subgoals in `Proof.lean`.  Downstream use: PU-07 packages the pair under the
existential quantifier.  Exceptional case: mismatched witnesses fail type
checking.  Trust boundary: this is the complete claim-local M0-L composition
kernel and is replayed by Master under `--trust=0`.

<a id="fragment-pu-07"></a>
## PU-07 -- discharge the existential root

Hypotheses: PU-06's conjunction at `z`.  Inference: existential introduction
with witness `z` proves `∃ w, CompactClosure w ∧ NonclosedOrbit w`; under the
crosswalk, the predicates are the exact compact-closure and nonclosed-orbit
expressions from PU-02.  Output: the frozen theorem's existential-conjunction
shape.  Formal anchor: `statement`, `huangShiWitnessComposition`, and
`auditRoundTrip`.  Downstream use: this is the release root and has no further
mathematical consumer inside the package.  Exceptional case: the theorem says
existence, not uniqueness or universality.  Trust boundary: worker preflight is
semantic/evidence-only; canonical Master independently elaborates the concrete
root and alone may accept it.

## Consequence and scope

The result supplies a bounded (compact-closure) diagonal orbit that is not
closed in this characteristic-restricted rank-four function-field quotient.
It does not assert the real Margulis conjecture, a statement for every
characteristic, or a classification of all orbits.  Those are deliberate
non-outputs rather than omitted proof cases.

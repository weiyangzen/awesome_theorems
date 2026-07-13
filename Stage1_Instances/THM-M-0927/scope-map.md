# Scope map

## Preserved catalog scope

The received claim is exactly "an explicit formula for the Fibonacci sequence," under the title
"Binet's formula." Intake preserves that closed-form identity family. It does not infer an exact
formula or binder-complete proposition from the title alone.

A leading conventional candidate is the zero-based natural-index real identity

```text
F_n = (((1 + sqrt 5) / 2)^n - ((1 - sqrt 5) / 2)^n) / sqrt 5.
```

This display is a candidate scope map, not the canonical statement. The statement phase must adopt
it only through an accepted source crosswalk and must freeze every convention below.

## Proposition-changing decisions

1. Whether the index domain is `Nat`, all integers with a negafibonacci extension, or another
   source-defined range.
2. Whether the Fibonacci sequence is zero-based with `F_0 = 0`, `F_1 = 1`, one-based, or shifted
   from a historical rabbit-counting convention.
3. Whether values are compared in `Real`, `Complex`, an algebraic extension, or another carrier,
   including the exact coercion from integral Fibonacci values.
4. Whether the characteristic roots are named `phi` and `psi` or expanded as radical expressions,
   and which square-root branch and division conventions apply.
5. Whether the root is pointwise universal equality, equality of functions, or an explicitly
   approved pair of equivalent formulations with a checked transport.
6. Whether integer exponentiation and negative-index signs belong to the root or only to a distinct
   extension.
7. The ordered binders, definitions, incorporated initial conditions or recurrence facts,
   hypotheses, conclusion, foundation profile, TCB profile, and every credited alternate.

These choices are not cosmetic. In particular, `Nat.fib`, `Int.fib`, natural powers, and integer
powers are distinct formal surfaces, and a one-based formula requires a checked index shift.

## Boundary cases

No case is excluded at intake. Statement review must explicitly cover index zero, index one, the
first recurrence step, the positivity and nonzeroness needed for division by `sqrt 5`, coercion of
natural values to the selected codomain, and negative indices if the integer extension is selected.
It must also mutation-test a changed domain, changed binder scope, a changed root or sign, and a
boundary index before proof evidence is inspected.

## Explicit non-substitutions

- `THM-M-0925` owns the Fibonacci sequence/recurrence family; its definition or recurrence alone
  is not the closed-form formula.
- `THM-M-0924` owns Lucas numbers and `THM-M-0926` owns Cassini's identity.
- `THM-M-0048` is the unrelated Cauchy-Binet determinant formula.
- The ratio limit of consecutive Fibonacci numbers, the asymptotic `F_n ~ phi^n / sqrt 5`, and a
  nearest-integer or rounding formula are consequences or approximations, not this exact identity.
- An isolated numerical computation, fast Fibonacci evaluator, recurrence solver interface, or
  golden-ratio identity is not a substitute for the universally quantified closed form.
- The integer-index theorem, a generalized recurrence, or a complex-valued spelling cannot replace
  the natural-index formula without accepted source selection and checked relationships.
- The untrusted catalog label, module documentation, theorem name, API probe, or axiom diagnostic
  supplies no H0 or M0 credit.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.NumberTheory.Real.GoldenRatio` defines `Real.goldenRatio = (1 + sqrt 5) / 2` and
`Real.goldenConj = (1 - sqrt 5) / 2`. It exposes the direct natural-index pointwise candidate
`Real.coe_fib_eq`, the function-equality candidate `Real.coe_fib_eq'`, and the broader
integer-index candidate `Real.coe_intFib_eq`.

These interfaces make statement feasibility unusually strong. Intake does not freeze any of them
as the source-identical root, certify the import as minimal for an absent target, inspect terminal
proof provenance, accept an axiom profile, or grant proof credit.

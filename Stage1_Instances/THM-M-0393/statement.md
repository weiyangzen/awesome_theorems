# THM-M-0393 Statement Freeze

## Canonical Target

`Statement.lean` freezes Thue's theorem as finiteness of the set of ordered integer pairs
`(x,y)` satisfying `F(x,y)=m`, where:

- `F : MvPolynomial (Fin 2) Int` is a binary form;
- `F.IsHomogeneous n` fixes its homogeneous degree and `3 <= n` excludes degrees below three;
- `Irreducible (F.map (Int.castRingHom Rat))` means irreducibility after coefficient extension to
  the rationals;
- `m : Int` is nonzero, matching the classical Thue-equation statement;
- the conclusion is `(solutionSet F m).Finite`.

The variable convention is `0 -> x` and `1 -> y`. The ordered binders are `n`, `F`, and `m`,
followed by the degree bound, homogeneity, rational irreducibility, and nonzero-right-side
hypotheses. There are no implicit theorem parameters or universes. The empty solution set is
allowed. The zero polynomial is automatically excluded by rational irreducibility. No primitive
coefficient hypothesis is imposed: rational irreducibility is the relevant classical hypothesis,
and adding primitivity would unnecessarily narrow the theorem.

The exact-type fixture `thueStatement_exact_type` checks this binder order and full proposition by
definitional equality. `mem_solutionSet_iff` checks the set encoding. Neither declaration proves
Thue's theorem.

## Import And Environment Freeze

The sole direct import is `Mathlib.RingTheory.MvPolynomial.Homogeneous`. It supplies the
`MvPolynomial` evaluation and coefficient-map APIs, `IsHomogeneous`, `Irreducible`, and the finite
set proposition through its pinned transitive closure. No umbrella `Mathlib` import is used.

- Lean toolchain: `leanprover/lean4:v4.29.0`
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Lake manifest version: `1.1.0`
- repository base revision: `7303634b5bee63e4735691cc42a5633b2bbbecbe`

## Scope And Mutation Boundary

Removing homogeneity or its connection to `n` admits lower-degree polynomials despite the numeric
degree binder. Removing `3 <= n` admits homogeneous linear and quadratic equations. Removing
rational irreducibility admits forms with a free-variable factor and potentially infinite fibers.
Changing `Int x Int` to naturals or rationals changes the theorem's domain. Allowing `m = 0` is a
deliberate mutation away from the standard nonzero Thue equation, even though irreducibility also
severely constrains its zero fiber. These mutations receive no target equivalence or proof credit.

The earlier intake's predicate-parametric legacy shape is superseded for statement purposes: the
canonical target uses concrete mathlib predicates and an actual bivariate polynomial object.

## Validation Evidence

Run from repository root unless a `cwd` is shown:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots,
  1546 uniform-L0 Lean 4 targets, execution skill present)
python3 scripts/stage1_target.py check
  exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
python3 scripts/stage1_target.py show THM-M-0393
  exit 0: rank 6; baseline L0; rework_required true; lifecycle planned; theorem_complete false
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0393/Statement.lean
  exit 0: no Lean diagnostics
git diff --check -- Stage1_Instances/THM-M-0393
  exit 0: no output
```

This evidence establishes exact target elaboration only. It does not establish source fidelity,
the theorem proof, anchor closure, trust closure, or theorem completion. Node-specific acceptance
remains the integration master's decision.

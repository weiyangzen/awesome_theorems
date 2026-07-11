# THM-M-0393 Intake: Thue's Theorem

## Instance Boundary

- Item: `S56-M-0393-INTAKE`
- Lifecycle: `planned`
- Baseline: `L0 / rework_required`
- Lane: `hard_mathlib_anchor_and_wrapper`
- Canonical topic: finiteness of integral solutions of an irreducible binary-form equation.
- Completion boundary: this dossier freezes a research scope only. It neither freezes an exact Lean proposition nor credits the legacy artifact or any proof of Thue's theorem.

## Human Claim And Scope Map

The intended classical claim is: if `F(X,Y)` is a homogeneous irreducible binary form over the integers of degree at least three and `m` is a nonzero integer, then the set of pairs `(x,y)` of integers satisfying `F(x,y) = m` is finite. Here irreducibility is intended over the rationals (equivalently, after the appropriate primitive normalization, over the integers). The exact coefficient representation and normalization are deliberately left to the statement phase.

| Scope component | Included interpretation | Still to freeze in statement phase |
|---|---|---|
| Form | homogeneous binary polynomial with integer coefficients | `MvPolynomial`, coefficient vector, or univariate homogenization |
| Degree | total degree at least three | exact degree API and treatment of the zero form |
| Irreducibility | irreducible over `Rat` | coercion/content normalization and checked equivalences |
| Right side | fixed `m : Int` with `m != 0` | whether primitive-form hypotheses alter the formulation |
| Solutions | `(x,y) : Int x Int` with `F(x,y)=m` | evaluation map and set/subtype representation |
| Conclusion | finitely many integral pairs | exact `Set.Finite` expression |

The boundary cases remain explicit. The zero right-hand side is excluded because homogeneous forms can have scaling families of zeros. Degrees zero, one, and two are outside this normalized Thue claim. An empty solution set is allowed and is finite. Reducible forms are excluded; no stronger assertion for them is implied.

## Source-Statement Crosswalk

| Source ID | Source and locator | Role | Mapping and caveat |
|---|---|---|---|
| `SRC-THUE-1909` | Axel Thue, *Uber Annaherungswerte algebraischer Zahlen*, Journal fur die reine und angewandte Mathematik 135 (1909), 284-305 | primary historical source | Supplies the approximation theorem underlying finiteness of Thue equations. The exact theorem/page-to-modern-binary-form derivation and errata have not been independently checked, so this is discovery evidence and remains `H3`. |
| `SRC-MAH-CUBIC` | K. Mahler, *Zur Approximation algebraischer Zahlen. I: Uber den grossten Primteiler binarer Formen*, Mathematische Annalen 107 (1933), 691-730 | historical binary-form cross-check | Helps locate the binary-form formulation and later terminology; it is not accepted as a substitute for a pinpoint audit of Thue's source. |
| `LEGACY-S1-M-006` | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_006.lean` at repository base `5997161aebf527e8a1e05724d4fbd4ce07dfd815` | discovery-only Lean artifact | Contains a predicate-parametric/object-model statement candidate and extensive ledgers. Rev-5.6 marks legacy artifacts unaccepted; it supplies no statement or proof credit at intake. |

The form, irreducibility, degree, nonzero right side, integral solution variables, and finiteness conclusion are all represented in the crosswalk. No component yet has both an exact primary-source pinpoint and independent review. Accordingly the root vector is `H3 / M4 / R3`.

## Open Intake DAG

1. `STMT-FORM`: choose the Lean representation of an integral homogeneous binary form and evaluation.
2. `STMT-IRREDUCIBLE`: freeze the coefficient coercion, content convention, and rational irreducibility predicate.
3. `STMT-DEGREE`: express homogeneity and degree at least three, including malformed/zero-form exclusions.
4. `STMT-RHS`: freeze `m != 0` and mutation-test the zero-right-side boundary.
5. `STMT-ROOT`: elaborate the exact finite-solution proposition and any checked transports.
6. `SRC-PINPOINT`: inspect a stable scan/edition for exact theorem/page, assumptions, derivation, and errata.
7. `ANCHOR-AUDIT`: audit pinned mathlib and external Lean 4 candidates after statement acceptance.

Tasks 1--4 and 6 feed `STMT-ROOT`; `ANCHOR-AUDIT` follows the accepted statement. Every task is open and no proof obligation receives closure credit.

## Intake Validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

Pre-write repository checks:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
python3 scripts/stage1_target.py check
  exit 0: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
python3 scripts/stage1_target.py show THM-M-0393
  exit 0: rank 6, L0/rework_required, planned, theorem_complete false
```

Known open gates: source pinpointing, exact Lean elaboration, transports and mutation tests, anchor audit, kernel closure, independent human/readability review, node-specific receipt, and master acceptance.

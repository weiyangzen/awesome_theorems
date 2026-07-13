# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6777-6782` supplies exactly the title `比内公式`, attribution to
Jacques Binet, year 1843, gloss `斐波那契数列的显式公式`, importance `中`, and status `已验证`.
Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, bibliography,
edition, page, definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, or reviewer.

`Docs/Stage0_Blueprint.md:25282-25307` repeats the gloss and identifies a formula/identity family,
while explicitly leaving the formal system, foundation, exact definitions and premises, proof
route, dependencies, alternate forms, axioms, machine status, and artifact links unresolved. The
rev-5.6 manifest assigns rank 1546, baseline `L0 / rework_required`, no legacy slot,
`lifecycle_mode: planned`, and `theorem_complete: false`. Its `已验证` field is untrusted.

## Modern authoritative statement lead

NIST Digital Library of Mathematical Functions, version 1.2.7 (released 2026-06-15), section
26.11, was inspected on 2026-07-13.
Equation group 26.11.5 defines the Fibonacci numbers by `F_0 = 0`, `F_1 = 1`, and
`F_n = F_(n-1) + F_(n-2)` for `n >= 2`. Equation 26.11.7 gives, for a nonnegative integer `n`,

```text
F_n = ((1 + sqrt 5)^n - (1 - sqrt 5)^n) / (2^n * sqrt 5).
```

The stable TeX response for equation 26.11.7 was 68 bytes with SHA-256
`a217ded8cf322e549eba3b2889a18abfea7e01f3d4bdd34e2aed017b25aa2adb`. The TeX responses for
the three recurrence clauses 26.11.5a-c had SHA-256 values
`4861208d1f848b5b939ed87aa134b855702fef94d4281246612132c0a7e64d2b`,
`b50a026822fc6cd8502fe718db2845c5340e964076efc19efc9faa685124bcfc`, and
`194c9de92b23fc4d5d12245d46567f10cf25ca3eb05650732442bc8d76a16d15`.
These are replayable pinpoint modern statement leads that sharpen the formula and indexing. They
are not a primary historical proof source, do not establish the repository's Binet/1843
attribution, and were not independently admitted as a complete
definition/proof/correction/errata crosswalk. They support H1, not H0.

OEIS A000045 was also inspected as a mutable secondary Fibonacci reference. Its live HTML embeds
request-varying material, so the one-time whole-response hash is deliberately not treated as a
replayable source input. It supplies many formulas and references but is not used to select the
root or clear source debt. A MathWorld page titled
"Binet's Fibonacci Number Formula" was observed (46,509 bytes, SHA-256
`32e42bc77fa5ede627865dc047c168f8b92040e94e3f5d53a8c6b18db798275c`), but its accessible body
did not supply the needed pinpoint formula/proof crosswalk and earns no stronger credit.

No primary 1843 Binet edition, theorem/page, transcription, translation, proof, correction history,
or errata review was located and admitted during this bounded intake. The historical attribution
therefore remains catalog metadata to be audited, not a source fact promoted by repetition.

## Clause crosswalk to the leading pinned candidate

| Mathematical clause | Pinned Lean surface | Intake assessment |
|---|---|---|
| Fibonacci sequence | `Nat.fib` | zero-based natural-valued candidate; source adoption open |
| nonnegative index | implicit `n : Nat` in `Real.coe_fib_eq` | close to DLMF 26.11.7; canonical binder not frozen |
| real-valued equality | coercion `(Nat.fib n : Real)` | exact codomain/coercion candidate; source identity open |
| positive root | `Real.goldenRatio = (1 + sqrt 5) / 2` | candidate abbreviation for the first radical factor |
| conjugate root | `Real.goldenConj = (1 - sqrt 5) / 2` | candidate abbreviation for the second radical factor |
| exponentiation | natural powers of both real roots | direct candidate for nonnegative `n` |
| denominator | `/ sqrt 5` after roots already divide by 2 | algebraically matches DLMF's `2^n * sqrt 5`; checked source transport still open |
| universal formula | `Real.coe_fib_eq : forall n, ...` | direct pointwise candidate, not an accepted root |
| function form | `Real.coe_fib_eq'` | alternate candidate; pointwise/function transport not credited yet |
| negative indices | `Real.coe_intFib_eq` using `Int.fib` and integer powers | broader candidate, not silently included |

## Pinned Lean candidate ledger

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, source
`Mathlib/NumberTheory/Real/GoldenRatio.lean` documents that it proves Binet's formula and exposes:

```text
Real.coe_fib_eq' :
  (fun n => Nat.fib n : Nat -> Real) =
    fun n => (Real.goldenRatio ^ n - Real.goldenConj ^ n) / sqrt 5

Real.coe_fib_eq (n : Nat) :
  (Nat.fib n : Real) =
    (Real.goldenRatio ^ n - Real.goldenConj ^ n) / sqrt 5

Real.coe_intFib_eq (n : Int) :
  (Int.fib n : Real) =
    (Real.goldenRatio ^ n - Real.goldenConj ^ n) / sqrt 5
```

The source file SHA-256 is
`e3a6e5160e654dfb4c5594c66a624fa7a5edffa4c1b839d992be7d1ba2dd7ac3`. The discovery-only
probe checks these types and reports `propext`, `Classical.choice`, and `Quot.sound` for each
candidate. It declares no target or proof body. These observations support M3 interface evidence,
not a canonical-expression fingerprint, terminal-body audit, accepted trust closure, or M0.

## First downstream gate

Before statement acceptance, accountable reviewers must preserve and independently review an
approved source; resolve historical attribution and corrections; select natural or integer indices,
indexing convention, codomain, roots, powers, denominator, formula spelling, and boundary cases;
and map every definition, binder, hypothesis, and conclusion. The statement phase must then encode
only that approved claim, minimize pinned imports, serialize the elaborated expression and
environment, compile checked transports, and run all four required mutation classes before any
proof evidence is credited.

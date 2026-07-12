# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `西格尔-瓦尔菲施定理`, attributes it
to Carl Siegel and Arnold Walfisz, dates it to 1936, and gives only `L函数零点的估计` ("estimates
for zeros of L-functions"). Stage0 repeats this metadata while leaving exact definitions,
assumptions, proof route, equivalent statements, axioms, and formal artifacts open. The rev-5.6
manifest preserves `已验证` only as `source_status_untrusted`.

The gloss describes proof technology or a neighboring result, not the usual conclusion of the
named theorem. It supplies no formula, quantifier order, normalization, theorem/page locator, or
formal declaration. It therefore cannot support an `H0` crosswalk.

## Mathematical family and unresolved variants

The standard name refers to a prime number theorem in arithmetic progressions that is uniform for
moduli bounded by a fixed power of `log x`. Sources commonly state variants for an unweighted prime
count, a logarithmically weighted prime count, or the von Mangoldt sum. They also present different
but related error estimates. Intake records this family only to prevent substitution; it does not
select one variant as the repository theorem.

A subsequent source audit must locate an immutable primary or authoritative edition and record its
exact theorem or formula and page, every premise and constant dependence, proof boundary, errata,
and an independent reviewer. Historical attribution and the 1936 date must also be verified rather
than inherited from metadata.

## Crosswalk

| Repository or conventional phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "primes in a residue class" | prime-counting function with congruence restriction | `Nat.Prime`, `Nat.ModEq` or equality in `ZMod q`, finite sums/counts | encoding ingredients available; normalization open |
| "reduced residue class" | coprimality or unit condition on `a mod q` | `Nat.Coprime`, `IsCoprime`, or `IsUnit (a : ZMod q)` | pinned API probed; exact encoding open |
| `phi(q)` main term | Euler totient normalization | `Nat.totient` and a source-selected real coercion | candidate only |
| uniform for logarithmic-size moduli | quantified bound on `q` in terms of `x` | real logarithm, powers, inequalities, and uniform quantifiers | exact order/range absent |
| error estimate | big-O or explicit bound with parameter-dependent constants | asymptotic relation or explicit existential constant | exact form absent |
| "L-function zero estimate" | possible proof input concerning Dirichlet L-functions | Dirichlet-character L-function APIs and analytic estimates | not the named conclusion; no proof credit |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe
imports `Mathlib.NumberTheory.LSeries.PrimesInAP`. It checks Dirichlet characters, the von Mangoldt
arithmetic function, Euler's totient, modular congruence, and mathlib's qualitative theorem
`Nat.infinite_setOf_prime_and_eq_mod`. The latter is a nearby theorem and proves only infinitude,
not a Siegel-Walfisz asymptotic. A bounded name/text search found no declaration named for
Siegel-Walfisz in pinned mathlib; that observation is not the later immutable anchor audit.

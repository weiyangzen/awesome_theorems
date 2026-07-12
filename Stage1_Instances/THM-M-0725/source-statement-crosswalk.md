# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `指数时间层次`, attributes it to
"many mathematicians", dates it only to the 1970s, and states `指数时间复杂性类`
("exponential-time complexity classes"). Stage0 repeats this metadata and leaves the precise
definitions, assumptions, proof route, axioms, and formal artifact open. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted`. No proposition, proof source, edition, theorem
number, page, or formal declaration is supplied.

The neighboring entries for the polynomial hierarchy, PSPACE-completeness, and randomized
complexity classes locate a broad subject area but do not disambiguate this target. Adjacency is not
source evidence.

## Candidate source work

Primary literature on deterministic and nondeterministic time hierarchy is a candidate locator if
the intended claim is strict containment at exponential bounds. Literature defining the
alternation/oracle exponential hierarchy is a separate candidate locator if that is the intended
term. The anchor audit must not blend these families: it must identify an immutable publication,
edition or version, exact definition/theorem and page, assumptions, proof boundary, and errata,
then obtain independent review. No candidate is `H0` evidence at intake.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "time" | number of steps as a function of encoded input length | machine step semantics and `EvalsToInTime`-style predicate | pinned API probed; exact cost model open |
| "exponential" | bounds such as `2^(p n)` or a union over exponents | exact natural-valued bound, rounding, growth, constructibility | absent from source record |
| "complexity class" | languages decidable/recognizable within a bound | encoded languages, acceptance, machine quantification | generic function-computation API only |
| "hierarchy" | strict time-class inclusion | two bound families and diagonalization theorem | candidate only |
| "hierarchy" | alternation/oracle levels and their union | alternating/oracle machines and level definitions | candidate only |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Computability.TuringMachine.Computable`. It checks the bundled finite
Turing-machine type, step-bounded output predicate, arbitrary-time computation package, and
polynomial-time specialization. These are encoding ingredients only. A bounded repository/mathlib
search found no declarations named for `EXPTIME`, an exponential-time class, or a time-hierarchy
theorem; this negative name search is not a substitute for the later immutable anchor audit.

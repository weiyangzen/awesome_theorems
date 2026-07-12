# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `狄利克雷L函数`, attributes the entry
to Peter Dirichlet, dates it to 1837, and gives the sole statement gloss `等差数列素数定理`.
Stage0 repeats that gloss and leaves exact definitions, assumptions, proof process, dependencies,
axioms, and formal artifacts open. The rev-5.6 manifest preserves `已验证` only in the explicitly
untrusted metadata field `source_status_untrusted`.

The gloss is sufficient to exclude a generic theorem about L-functions and to freeze the familiar
human scope of Dirichlet's theorem: every reduced residue class contains infinitely many primes.
It is not sufficient for `H0`. No primary-source edition, section/page, original notation,
assumption crosswalk, proof boundary, translation, or errata record has yet been inspected.

## Source work still required

The source audit must pin and independently inspect either Dirichlet's 1837 memoir or a specified
critical/authoritative edition and translation. It must locate the exact result, map its modulus and
coprimality assumptions and conclusion to the modern canonical claim, distinguish the original
proof's L-series machinery from the theorem statement, record any editorial modernization and
errata, and identify a reviewer. Until then the human axis remains `H1`.

## Crosswalk

| Repository phrase | Mathematical component | Expected Lean component | Intake status |
|---|---|---|---|
| `狄利克雷L函数` | Dirichlet characters and associated complex L-functions used in the analytic proof | `DirichletCharacter`, `DirichletCharacter.LFunction` | pinned API probed; proof-role only |
| `等差数列` | a residue class `a mod q` with `gcd(a,q)=1` | `a : ZMod q` plus `IsUnit a`, or an equivalent coprimality encoding | representation open |
| `素数定理` in this entry | infinitely many primes in each reduced residue class | an infinite set of prime naturals satisfying reduction modulo `q` | human scope frozen; exact expression open |
| equivalent unbounded form | above every bound lies such a prime | universally quantified bound and existential prime | candidate alternate; transport open |
| `1837`, Peter Dirichlet | historical attribution and date | provenance only | secondary metadata; not H0 |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.NumberTheory.LSeries.PrimesInAP` and checks the types of the L-function,
its agreement with its Dirichlet series, its nonvanishing on the relevant half-plane, and mathlib's
two named Dirichlet-theorem declarations. This establishes a concrete later audit surface only.
Statement identity, terminal proof-body provenance, transitive dependency/trust closure, axiom
profile, and acceptance are deliberately not decided in intake.

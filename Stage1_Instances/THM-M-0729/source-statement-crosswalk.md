# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md` records `PCP定理`, attributes it to Sanjeev Arora and Shmuel
Safra, dates it to 1992, and gives only `概率可检验证明` ("probabilistically checkable proofs").
`Docs/Stage0_Blueprint.md` repeats that topic gloss. Neither supplies a proposition.

`Docs/researches/cs_theorems.md` independently records the more informative shorthand
`NP = PCP[O(log n), O(1)]`, attributes the 1992--1998 theorem family to Arora, Safra, Arora, Lund,
and others, and labels it verified. This locates the intended classical PCP theorem, but the table
does not define its notation or cite an edition, theorem number, page, assumptions, proof boundary,
or errata. The rev-5.6 manifest therefore correctly preserves `已验证` only as
`source_status_untrusted`.

## Primary-source boundary

The Arora--Safra paper and the Arora--Lund--Motwani--Sudan--Szegedy paper are candidate primary
source families, not accepted citations at intake. The statement phase must inspect an immutable
edition, identify one exact main statement plus every referenced definition, record pages and
assumptions, check errata, and obtain independent source review. It must not combine constants or
definitions from different formulations merely to produce familiar notation. No `H0` credit is
assigned here.

## Crosswalk

| Repository phrase | Mathematical component needing a source definition | Lean discovery candidate | Intake status |
|---|---|---|---|
| `NP` | languages accepted by polynomial-time nondeterministic computation or witnesses | `Language`, deterministic polynomial-time computation as an ingredient | exact NP encoding absent |
| `PCP` | randomized polynomial-time oracle verifier with completeness and soundness | `PMF` may express finite randomized outcomes | no PCP/verifier declaration selected or located |
| `O(log n)` | asymptotic randomness budget relative to encoded input length | `Asymptotics.IsBigO` and logarithm infrastructure | resource function and filter open |
| `O(1)` | constant query budget under a precise access/counting convention | asymptotic bounds plus finite query traces | oracle and counting semantics open |
| `=` | extensional equality of two classes of encoded languages | set or predicate extensionality | both inclusions and transports open |
| `已验证` | untrusted inventory status | none | explicitly rejected as proof evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded
`IntakeProbe.lean` checks `Language`, deterministic time/polytime computation, `PMF`, and
`Asymptotics.IsBigO`. These are possible low-level ingredients only. They do not define NP or PCP,
provide random-access proof oracles, select completeness/soundness conventions, or prove either
class inclusion. Formal-candidate discovery and a repository-wide immutable anchor audit remain
later dependent phases.

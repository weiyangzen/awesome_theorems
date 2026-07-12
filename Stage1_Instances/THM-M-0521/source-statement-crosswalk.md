# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `科利瓦金定理`, attributes it to Victor
Kolyvagin, dates it to 1988, and gives only `椭圆曲线秩为0或1时的BSD` ("BSD for elliptic curves
of rank 0 or 1"). Stage0 repeats that gloss. The rev-5.6 manifest deliberately preserves `已验证`
only as `source_status_untrusted`. None supplies a definition of rank, a quantified conclusion,
hypotheses, an edition/page, an erratum record, or a formal artifact.

## Candidate source locators, not accepted source evidence

The later source audit should examine Kolyvagin's papers commonly translated as "Finiteness of
E(Q) and Sha(E,Q) for a subclass of Weil curves" (1988/1989 publication metadata varies by
translation) and "Euler systems", in *The Grothendieck Festschrift*, volume II (1990). It must also
separate what is proved there from the Gross-Zagier input and from modern corollary formulations.
These bibliographic leads were not pinned to an inspected theorem/page during this intake, receive
no H0 credit, and must not be silently converted into a canonical statement.

## Crosswalk

| Repository phrase | Mathematical decision required | Lean component required | Intake status |
|---|---|---|---|
| "elliptic curve" | base field and exact curve category | an elliptic curve over that field and its rational-point group | `WeierstrassCurve.IsElliptic` probed; arithmetic object open |
| "rank" | analytic rank, Mordell-Weil rank, or asserted equality | elliptic L-function vanishing order and/or rank of rational points | absent as an elliptic-curve API in the bounded probe |
| "0 or 1" | two branches or one `<= 1` hypothesis; analytic or algebraic | exact disjunction/inequality and branch conclusions | source ambiguous |
| "BSD" | rank equality, Sha finiteness, prime-primary order, or full formula | Tate-Shafarevich group, regulators, periods, Tamagawa factors as applicable | exact conclusion absent |
| "Kolyvagin" | Euler-system theorem versus a Gross-Zagier consequence | concrete Heegner/Euler-system and Selmer-control chain | absent from source record |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports elliptic-curve projective points, generic L-series derivatives, and the
Dedekind-domain Selmer group. It checks six concrete declarations. The generic L-series is not by
itself the Hasse-Weil L-function of an elliptic curve, and `IsDedekindDomain.selmerGroup` is not by
itself the Galois-cohomological Selmer group used in Kolyvagin's argument. No terminal theorem,
formal candidate, or proof closure is credited at intake.

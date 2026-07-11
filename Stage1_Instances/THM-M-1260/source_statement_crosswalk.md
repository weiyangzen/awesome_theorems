# Source-statement crosswalk

| Claim component | Available source anchor | Lean target | Intake assessment |
|---|---|---|---|
| "Pseudodifferential operators" | Stage0 title `伪微分算子` | None | A subject/class name, not a proposition |
| "Generalization of differential operators" | Stage0 content `微分算子的推广` | None | Motivational relationship lacks definitions and a conclusion |
| Date and attribution | Stage0 says 1965; Kohn, Nirenberg, and Hormander | None | Bibliographic discovery metadata only; no work, edition, theorem, or page is specified |
| Source status | Stage0 says `已验证` (verified) | None | Untrusted metadata label; it provides no human-source or machine-proof evidence |

## Non-equivalent candidate interpretations

| Candidate | Decisions needed before it can become a claim | Why intake does not select it |
|---|---|---|
| Every differential operator has a symbol in a specified pseudodifferential class | coordinate setting, coefficient regularity, symbol convention, order and type | This most closely matches "generalization", but the source does not state it |
| Composition theorem for pseudodifferential operators | symbol classes, proper support, quantization, asymptotic meaning | A central calculus theorem but substantially stronger and different |
| Sobolev or Schwartz-space mapping theorem | spaces, symbol estimates, order, topology, continuity notion | A regularity result, not the definition/generalization claim itself |

No canonical human claim can truthfully be reconstructed from the repository entry alone. In
particular, the name does not determine whether the intended object is the Kohn-Nirenberg
quantization on Euclidean space, another quantization, or a theorem in a manifold calculus.

Primary-source audit must locate an immutable edition and map an exact theorem/page, assumptions,
notation, and corrections to the selected statement. Likely bibliographic search terms include
Kohn-Nirenberg's work on non-coercive boundary value problems and Hormander's symbol/operator
calculus, but these are discovery leads only, not accepted citations. Independent review is needed
before `H0`; exact Lean elaboration and checked transports are needed before machine credit.

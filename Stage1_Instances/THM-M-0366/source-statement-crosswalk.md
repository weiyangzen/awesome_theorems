# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` gives the authors Ronald Coifman, Alan McIntosh, and Yves Meyer,
the year 1982, and only `Lipschitz曲线上的Cauchy积分` ("Cauchy integrals on Lipschitz curves").
`Docs/Stage0_Blueprint.md` repeats this metadata and leaves precise definitions, assumptions,
proof route, axioms, and formal artifacts open. The manifest retains `已验证` only as untrusted
source metadata; it supplies neither a proposition nor kernel evidence.

## Primary source candidate

R. R. Coifman, A. McIntosh, and Y. Meyer, "L'integrale de Cauchy definit un operateur borne sur
L2 pour les courbes lipschitziennes," *Annals of Mathematics*, second series, **116** (1982),
361-387. The title, authors, journal, volume, year, and page range identify the intended headline
result. This intake has not inspected an immutable scan's exact theorem text, definitions imported
by reference, page-level assumptions, proof boundaries, or errata, so the citation is not `H0`.

## Crosswalk

| Source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| Lipschitz curve | planar curve with controlled Lipschitz parametrization | `LipschitzWith` plus a source-faithful curve representation | generic API probed; exact model open |
| Cauchy integral | singular kernel along the curve with a deleted diagonal | complex Bochner/interval integral, truncations, measurability | ordinary integral APIs exist; singular operator absent |
| defines an operator | initial dense-domain operator and a well-defined extension | linear/continuous linear map between source-specified spaces | conclusion encoding open |
| bounded on `L2` | an `L^2` norm inequality with specified measure and constant | `MemLp`/`Lp`, `eLpNorm`, or a continuous linear map on `Lp` | generic APIs probed; exact inequality open |
| `已验证` | repository inventory label | no Lean declaration or receipt | explicitly rejected as evidence |

## Fidelity and formal boundary

The statement phase must inspect and cite the exact primary theorem/page, freeze all hypotheses and
normalizations, record any errata or later qualifications, and obtain independent review. It must
distinguish uniform bounds for truncations, principal-value existence, and bounded extension rather
than treating them as interchangeable.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
general Lipschitz, interval/path integral, circle Cauchy-integral, and `L^p` vocabulary. A bounded
text search found circle-integral Cauchy formulas but no Coifman-McIntosh-Meyer declaration or
general Lipschitz-curve Cauchy singular-integral operator. This is intake feasibility evidence only,
not the immutable exhaustive audit required by `S56-M-0366-ANCHOR_AUDIT`.


# Source-statement crosswalk

## Source boundary

The generated repository entry says only `Korteweg-de Vries方程` and "非线性波动方程". Its
`已验证` label is explicitly untrusted under rev-5.6 and supplies neither theorem wording nor a
citation. It therefore cannot support H0 or determine a Lean proposition.

A historical primary-source candidate is D. J. Korteweg and G. de Vries, "On the Change of Form of
Long Waves advancing in a Rectangular Canal, and on a New Type of Long Stationary Waves",
*Philosophical Magazine*, fifth series 39 (1895), 422-443. This bibliographic anchor has not yet
been inspected against a stable scan, exact equation/page, notation, assumptions, or errata, so it
is discovery evidence only. A later theorem source will probably be necessary if the intended root
is modern well-posedness rather than derivation or travelling waves.

## Crosswalk

| Repository or legacy phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| Korteweg-de Vries equation | normalized nonlinear dispersive PDE | scalar field and partial derivatives | subject included; exact encoding open |
| `u_t + 6*u*u_x + u_xxx = 0` | one common normalization | pointwise, weak, or distributional equality | provisional; source transport open |
| nonlinear wave equation | descriptive classification | no proposition by itself | insufficient as theorem claim |
| global solution package | existence, trace, conservation, uniqueness | concrete function spaces and proofs | legacy alternative, not accepted |
| one-soliton verification | explicit travelling-wave substitution | derivative identities for `sech^2` | legacy alternative, not accepted |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_207.lean` defines a pointwise residual, an
abstract global-solution package, and an explicit soliton profile. It also selects one-soliton
verification while defining `StatementShape` as global existence for Schwartz-like data. Those are
not equivalent roots, and the file expressly records that the hard PDE proof remains open. The
statement phase must select exactly one source-backed claim, elaborate it with minimal pinned
imports, and give checked transports for alternative normalizations.

Before H0, an independent reviewer must verify the primary edition, exact theorem/equation and
page, all assumptions and conventions, errata, and every source-to-Lean row. Before M credit, the
chosen expression must elaborate and its terminal body and trust closure must be inspected.

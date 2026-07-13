# THM-M-0240 rev-5.6 intake

`THM-M-0240` is the complex-analysis catalog item `阿贝尔-雅可比定理`
(`Abel-Jacobi theorem`). The repository supplies only the noun phrase `代数曲线的雅可比簇`
(`the Jacobian variety of an algebraic curve`), the attribution Niels Abel/Carl Jacobi, the year
1834, and an untrusted `verified` label. Those fields identify a classical subject family, not one
binder-complete theorem.

## Intake result

This dossier creates a fail-closed `planned` instance and preserves that ambiguity. The catalog
does not say whether the target is existence/representability of a Jacobian, an identification
`Pic^0(C) ≃ J(C)`, Abel's divisor criterion, Jacobi inversion, a property of the Abel-Jacobi map,
or an Albanese/Picard universal property. These readings have different base fields, curve and
point hypotheses, constructions, quantifiers, conclusions, and boundary cases.

The neighboring catalog targets are material boundaries: `THM-M-0238` separately names Abel's
theorem, and `THM-M-0239` separately names Jacobi inversion. Neither is imported, conjoined, or
substituted here.

## Source and formal boundary

J. S. Milne's corrected 2021 edition of *Jacobian Varieties* was inspected as a source-family
lead. Its Theorem 1.1 gives an algebraic representability/existence result, while Theorem 2.5 gives
a complex analytic/algebraic identification derived from Abel's theorem and Jacobi inversion.
That divergence confirms that the catalog wording does not select one proposition. The catalog
does not cite Milne, and no theorem has been admitted as the target or independently reviewed;
the source therefore supplies discovery context only, not `H0` evidence.

`IntakeProbe.lean` elaborates only adjacent pinned scheme smoothness/properness and elliptic
Jacobian-coordinate APIs. Pinned mathlib's `WeierstrassCurve.Jacobian` is an abbreviation for a
Weierstrass curve expressed in Jacobian coordinates, not the Jacobian variety of a general
algebraic curve. A bounded exact-topic search found no general Abel-Jacobi or curve-Jacobian
declaration in pinned mathlib. This is intake discovery, not the exhaustive anchor audit and not
proof of absence from external projects.

The canonical mathematical statement and Lean expression remain null. The provisional root vector
is `[H5, M4, R4]`: `H5` classifies the received noun phrase as not yet a stable proposition; it does
not say that standard Abel-Jacobi mathematics is false or open. No exact usable formal artifact or
source-faithful reconstruction is identified. All six downstream tasks remain open. No `H0`,
`M0`, `R0`, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.

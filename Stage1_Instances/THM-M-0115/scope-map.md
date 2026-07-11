# THM-M-0115 Scope Map

## Canonical Claim

The intake freezes the classical nonsingular quasi-projective variety formulation: for a proper
morphism `f : X -> Y` over a field and `alpha in K_0(X)`,

`ch(f_* alpha) cap td(T_Y) = f_*(ch(alpha) cap td(T_X))`

in `A_*(Y) tensor Q`. Here the left pushforward is the K-theory pushforward, the right pushforward
is proper pushforward on Chow groups, `ch` is the Chern character, and `td(T_)` is the Todd class of
the tangent bundle.

## Binder And Boundary Map

| Surface | Included | Not silently substituted |
|---|---|---|
| Base | an arbitrary field | only `C`, a fixed characteristic, or a general base scheme |
| Objects | nonsingular quasi-projective varieties | singular schemes, stacks, analytic spaces |
| Morphism | proper morphism over the base field | only closed immersions or projective morphisms |
| Input | every class in `K_0(X)` | only vector bundles or the structure sheaf |
| Output | equality in rational Chow homology of `Y` | equality of Euler characteristics or a numerical corollary |

Empty objects and the zero K-class are not excluded. A special-case proof cannot close the root.

## Formal Surface Needed Next

The statement phase must identify exact Lean representations for varieties/schemes, smoothness,
quasi-projectivity, properness, `K_0`, Chow groups, both pushforwards, Chern character, tangent
bundle, Todd class, cap/product, and rational coefficients. Until all are elaborated together, the
canonical formal expression and its hash remain deliberately null and machine debt remains `M5`.

No theorem, proof body, source completeness, or repo-local machine closure is claimed by intake.

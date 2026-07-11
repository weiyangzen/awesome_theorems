# Scope map

## Frozen source boundary

- Repository label: `Cauchy估计` / Cauchy estimates.
- Literal content: derivative estimates for holomorphic functions.
- Attribution/date metadata: Augustin Cauchy, 1831.
- Evidence quality: repository secondary metadata; no edition, page, theorem number, or primary text.

## Unresolved mathematical scope

The intake does not decide whether the function is complex-valued on a disk, analytic on a
neighborhood of a closed disk, or holomorphic on a general domain. It also does not decide whether
the bound uses a boundary maximum or a supremum on the disk, whether the center is arbitrary,
whether all derivative orders are quantified, or whether the result is the usual
`‖f^(n)(z₀)‖ ≤ n! M / R^n` inequality. These choices materially change the Lean statement.

The standard disk inequality is a discovery hypothesis only. It must not be promoted until a
primary source or an explicit project-level scope decision fixes the claim and its degenerate cases
(`R = 0`, `n = 0`, open versus closed disk, and finiteness of the supremum).

## Profiles and exclusions

- Foundation, classical logic, choice, imports, computation, and terminal proof provenance: open.
- Excluded substitutions: Cauchy integral formula alone, a coefficient estimate alone, real-analytic
  derivative bounds, or a PDE interior estimate merely sharing the name "Cauchy estimate".
- Next gate: freeze an exact human statement and elaborate its minimally imported Lean expression.

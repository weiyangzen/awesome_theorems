# Scope map

## Received scope

The repository fixes only `解对参数的可微性`, the attribution "many mathematicians," the period
"20th century," and `解对参数的导数` ("derivative of solutions with respect to parameters"). It
supplies no citation, definitions, hypotheses, theorem locator, or formal artifact. Stage0 repeats
those fields and explicitly leaves the exact premises and definitions open.

The words constrain the target to differentiable dependence of ODE solutions on an external
parameter. They do not select one theorem. In particular, "parameter" must not silently mean time
or initial data, because the catalogue separately schedules continuous initial-data dependence as
`THM-M-1339` and a variational equation as `THM-M-1341`.

## Candidate mathematical boundary

An eventual exact target must obtain a reviewed source and freeze:

- the state and parameter spaces, including finite dimension versus Banach-space generality;
- the time-state-parameter domain and whether it is open or requires within-derivatives;
- an autonomous field or a time-dependent field `f(t, x, lambda)`;
- the regularity order and whether regularity is joint or only partial in state and parameter;
- fixed or parameter-dependent initial time and initial value;
- the local existence and uniqueness hypotheses and a common neighborhood for varying parameters;
- the solution map's domain, especially local versus maximal solutions and boundary/blow-up cases;
- Frechet, coordinatewise, strict, within-set, or `C^k` differentiability; and
- whether the conclusion only asserts differentiability or also identifies its derivative by an
  inhomogeneous sensitivity equation.

Teschl's Theorem 2.11 is a concrete finite-dimensional candidate: `f` is `C^k` on an open
time-state-parameter domain and the local solution map is jointly `C^k` in time, initial time,
initial state, and parameter. It is source evidence for the theorem family, not the canonical root,
because the repository does not cite it and no independent source review has selected it.

## Proposition-changing cases

The statement phase must decide and mutation-test at least:

1. removal or weakening of differentiability in the parameter or state variable;
2. replacement of finite-dimensional Euclidean spaces by arbitrary normed or Banach spaces;
3. external parameter versus initial state, initial time, or time itself;
4. fixed initial data versus parameter-dependent initial data;
5. joint `C^k` dependence versus differentiability only in the external parameter;
6. a uniform local solution domain versus parameter-dependent maximal intervals;
7. open parameter neighborhoods versus boundary points and within-derivatives; and
8. the parameter-free, zero-dimensional, zero-derivative, domain-boundary, and finite-time blow-up
   cases.

## Explicit exclusions

- `THM-M-1339` continuous dependence on initial data as a differentiability theorem.
- `THM-M-1341` the variational or sensitivity equation without a theorem connecting it to the
  derivative of the solution map.
- Differentiability of a solution in time, or ordinary smoothness of the vector field alone.
- A scalar, autonomous, linear, global, analytic, or parameter-independent special case substituted
  for a source-selected general claim.
- A local flow or implicit-function theorem with no checked bridge to the exact ODE solution map.
- A bundled structure that accepts the desired differentiability or sensitivity result as data.
- Numerical sensitivity, finite differences, an API probe, or the catalogue label `已验证` as proof
  evidence.

No canonical Lean target is frozen at intake. The pinned environment exposes ODE solution
predicates, local-existence interfaces, and Frechet derivatives, but the bounded search located no
theorem-specific parameter-differentiability result. The statement and anchor-audit phases must not
infer one from these adjacent APIs.

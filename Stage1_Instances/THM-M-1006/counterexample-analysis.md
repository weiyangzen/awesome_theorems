# THM-M-1006 counterexample analysis for the frozen all-positive-exponent target

The finite discrete-time statement in `Statement.lean` is already false for martingales with jumps
at `p = 1 / 2`; analogous families obstruct the subunit range. This note gives a self-contained
upper-direction counterexample at that concrete exponent.
It explains the obstruction certified in part by `Counterexample.lean`; it is not a replacement
positive theorem and it does not by itself claim a kernel proof of `Not (StatementShape (1 / 2))`.

## Finite martingales

For every integer `N >= 2`, put

```text
m = N^2,   q = 1/m,   s = 1-q,   a = (1-q)/q = m-1.
```

Let `Omega_N = (Fin m)^(Fin N)` with the uniform product probability measure and its coordinate
filtration. Let `T` be the first coordinate whose value is zero, taking `T = N` if there is none.
Define a process starting at zero by the increments

```text
Delta f_(i+1) =  1    when T > i,
                 -a   when T = i,
                  0   when T < i,
```

for `0 <= i < N`, and keep the process constant afterward. On `{T >= i}`, the next increment is
`1` with probability `s` and `-a` with probability `q`, and

```text
s - q*a = (1-q) - q*((1-q)/q) = 0.
```

On `{T < i}` the next increment is zero. Thus every conditional increment has mean zero and this
is a real-valued martingale for the coordinate filtration. The algebraic centering identity is
kernel-checked as `Counterexample.upper_transition_centered`.

## Exact moments

The cases are disjoint and have probabilities

```text
P(T = N) = s^N,       P(T = j) = s^j*q  for 0 <= j < N.
```

On `T = N`, the path is `0, 1, ..., N`, so the frozen maximal process `M_N` and quadratic
variation `Q_N` are both `N`. On `T = j`, the path is `0, 1, ..., j, j-a, j-a, ...`, hence

```text
M_N = max(j, |j-a|),       Q_N = j + a^2.
```

At `p = 1/2`, write the two finite moments in the upper frozen inequality as

```text
U_N = E[M_N^(1/2)]
    = s^N*N^(1/2) + sum_(j<N) s^j*q*max(j, |j-a|)^(1/2),

V_N = E[Q_N^(1/4)]
    = s^N*N^(1/4) + sum_(j<N) s^j*q*(j+a^2)^(1/4).
```

In particular, `U_N >= s^N*N^(1/2)`. Bernoulli's inequality gives
`s^N >= 1-N*q = 1-1/N >= 1/2`. Moreover, `a <= q^(-1) = N^2` and `j < N <= N^4`, so

```text
(j+a^2)^(1/4) <= 2^(1/4)*N.
```

The total probability of the rare-jump cases is `1-s^N <= N*q`. Therefore

```text
V_N <= N^(1/4) + 2^(1/4),

U_N / V_N >=
  (1/2)*N^(1/2) / (N^(1/4) + 2^(1/4)).
```

Here `V_N > 0` because its no-jump term is positive. The last expression tends to infinity like
`(1/2)*N^(1/4)`. The generic transition algebra is kernel-checked in `Counterexample.lean`. That
module also checks asymptotic ingredients for an alternative exponentially rare parameter choice;
the polynomial choice used here makes the final estimates simpler and avoids needing an
exponential-limit argument.

## Contradiction and scope

If `StatementShape (1 / 2)` held, its one finite constant `C : ENNReal`, quantified before the
probability space and martingale, would give `U_N <= C*V_N` for every `N`. All terms here are finite,
so taking `ENNReal.toReal` would bound `U_N / V_N` by the fixed real number `C.toReal`, contradicting
the divergence above. Hence the frozen all-`p > 0` upper comparison cannot be proved.

This does not refute the classical continuous-martingale BDG theorem. A source-faithful repair must
either restrict the discrete-jump statement to an exponent range for which this square-function
comparison is valid, add the jump control needed below one, or select the intended continuous
martingale formulation. Any repair changes the canonical statement fingerprint and invalidates the
current downstream registry, so it belongs to a reopened statement phase rather than this proof
worker.

Consequently `S56-M-1006-PROOF` is blocked. This note is counterexample evidence for master review,
not a proof receipt, provisional completion, or theorem-completion claim.

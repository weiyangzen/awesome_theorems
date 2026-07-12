# Exact-statement gate: blocked

Item: `S56-M-1287-STATEMENT`
Base revision: `b18a08591e70d8b29ed5ebb3f76a33bb76ca1f83`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated from the frozen intake and repository
source. The complete repository wording is "the isoperimetric inequality for the first
eigenvalue", together with the names Faber and Krahn and the year 1923. That wording identifies a
theorem family, but it does not identify one proposition. In particular, it does not fix:

- the dimension and its lower bound;
- the admissible domain class (open, bounded open, Lipschitz, measurable, or quasi-open) and its
  connectedness or regularity conditions;
- the definition and sign normalization of the first Dirichlet eigenvalue, including the Sobolev
  or Rayleigh-quotient convention;
- whether the claim includes only the sharp inequality, attainment by balls, or also the rigidity
  direction;
- the equality relation (literal equality, translation/congruence, equality almost everywhere,
  or equality up to capacity zero) and the hypotheses under which rigidity is valid;
- the treatment of zero/infinite volume, empty domains, and unavailable eigenfunctions.

These choices give genuinely different statements. The intake deliberately leaves every one of
them to this phase and records the same first blocker in `task-dag.json`. It also requires a stable
primary edition with theorem/page and exact hypotheses before those choices are frozen. No such
source is present in the repository. Choosing the common bounded-open-domain formulation, dropping
the equality case, or replacing the Dirichlet Laplacian by an arbitrary real-valued `lambda1`
would therefore broaden or substitute the theorem rather than elaborate the exact intake claim.
The historical `已验证` label is untrusted metadata and supplies neither source nor kernel evidence.

## Lean infrastructure boundary

The pinned mathlib tree contains the finite-dimensional continuous-linear-map Rayleigh quotient in
`Mathlib.Analysis.InnerProductSpace.Rayleigh`, but the scoped repository search found no Faber-Krahn
declaration or concrete first Dirichlet eigenvalue API for Euclidean domains. The Rayleigh module is
not an exact replacement: it concerns bounded operators on an abstract inner-product space and
does not encode domain volume, zero boundary values, a Dirichlet Laplacian, or ball rigidity.

Consequently there is no canonical expression on which to determine minimal imports, serialize an
expression fingerprint, compile a source-shape transport, or meaningfully mutation-test a removed
hypothesis, changed domain, changed binder scope, and boundary case. An abstract structure carrying
an unconstrained eigenvalue function, or a hypothesis that assumes the desired comparison, is
explicitly excluded by the intake scope map and receives no statement credit.

## Required unblock

An accountable source reviewer must first identify a stable primary or source-authoritative modern
edition by exact theorem/page and freeze all domain, dimension, normalization, equality, and
degenerate-case conventions. The statement can then select a concrete Lean encoding of the first
Dirichlet eigenvalue and domain equivalence, elaborate it using the minimal pinned imports, print
and hash the expression, compile any credited transports, and execute the four required mutation
classes. If the pinned library lacks the necessary analytic definitions, that fact must remain an
explicit formalization blocker rather than be hidden behind an abstract assumed interface.

## Narrow validation evidence

Commands were run inside this worker clone on 2026-07-12. The existing pinned `.lake` artifacts
were read only; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1287` | exit 0; rank 458, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded after the table below |
| `rg -n -i 'Faber|Krahn|Dirichlet.*eigen|first.*eigenvalue' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; no matching Faber-Krahn or Dirichlet-first-eigenvalue declaration |

Environment hashes:

- `Formalizations/Lean/lean-toolchain`:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json`:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

First failed gate: exact source-statement identity. Known failures are the canonical formal target,
minimal-import determination, expression fingerprint, checked transports, and mutation tests. The
assigned phase is therefore not self-tested or complete, and no `.stage1-worker-selftest.json` is
emitted. No statement acceptance, theorem completion, or downstream-node credit is claimed.

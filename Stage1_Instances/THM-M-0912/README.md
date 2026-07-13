# THM-M-0912 rev-5.6 dossier

## Statement-phase handoff

`Statement.lean` now freezes the conservative source-shaped target selected from the only preserved
formula-level published lead, NIST DLMF 26.3.5:

```text
forall m n : Nat, n <= m -> 1 <= n ->
  Nat.choose m n = Nat.choose (m - 1) n + Nat.choose (m - 1) (n - 1)
```

The exact target elaborates with the sole direct import `Mathlib.Data.Nat.Choose.Basic`. Checked
transports cover a conjunction spelling of the source constraint, reversed summand order, and a
domain-preserving successor reindexing. Four expression-distinct mutations and explicit boundary
witnesses protect the positive-column premise, natural-number domain, universal column scope, and
included diagonal. The unrestricted all-natural successor recurrence remains explicitly outside
the root because it includes index pairs excluded by `m >= n >= 1`.

`statement.json`, `statement-validation.md`, `statement-receipt.json`, and `check_statement.py`
record the expression and environment fingerprints and the provisional self-test. This establishes
statement elaboration only. It adds no root proof body and claims no H0, M0, audit completion,
theorem completion, release, or master acceptance. The vector remains `[H1, M3, R4]`; source,
anchor, proof, obligation, readability, validation, and release work stays downstream.

## Intake record

This directory is the fail-closed `planned` intake dossier for the repository label `帕斯卡恒等式`
(`Pascal's identity`). The catalog supplies only the gloss `组合数的递推关系` ("the recurrence
relation for binomial coefficients"), an attribution to Blaise Pascal, the year 1654, and an
untrusted `已验证` label. It gives no formula, indexing convention, domain, boundary convention,
proof source, or formal declaration.

A strong modern statement lead was inspected: NIST DLMF 1.2.7, Chapter 26, Section 26.3(iii),
equation 26.3.5, states

```text
C(m,n) = C(m-1,n) + C(m-1,n-1),  m >= n >= 1.
```

The pinned mathlib source independently contains the zero-extended all-natural successor form
`Nat.choose_succ_succ`. These surfaces align after an index change when the DLMF side conditions
hold, but they do not have identical stated domains: mathlib's theorem also covers columns beyond
the row through its zero convention. Choosing the all-natural extension, the source-restricted
formula, or a conditional predecessor formulation was therefore deferred to the dependent
statement phase. That phase now provisionally selects the DLMF-constrained predecessor form above;
the intake rationale itself grants no statement credit.

The provisional root vector is `[H1, M3, R4]`. `H1` records a published modern statement lead whose
historical source, complete proof, incorporated definitions, correction/errata history, and
independent review remain open. `M3` records an exact self-tested target and pinned statement
interfaces, but no accepted proof. `IntakeProbe.lean` authenticates only candidate APIs; current
target identity belongs to the statement artifacts.

`scope-map.md` records the proposition-changing choices and reconciled boundary cases,
`source-statement-crosswalk.md` records the catalog/source/Lean relationship, and `task-dag.json`
leaves every downstream phase open. The statement sidecars now freeze a provisional exact Lean
target, but no accepted execution state, proof credit, audit completion, theorem completion, or
master acceptance is claimed.

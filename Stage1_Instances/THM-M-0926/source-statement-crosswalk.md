# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6770-6775` supplies only the title `卡西尼恒等式`, attribution to
Jean-Dominique Cassini, year 1680, the gloss `斐波那契数列的恒等式`, importance, and the untrusted
formalization label `已验证`. All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:25255-25280` repeats the gloss and explicitly leaves exact definitions,
premises, equivalent formulations, axioms, logic dependencies, machine status, and artifact links
open. Neither record supplies a truth-valued formula, source page, proof, translation, correction,
erratum, or independent review. Rev-5.6 therefore retains the target's identity but grants the
catalog no H or M credit.

## Modern statement lead

Eric W. Weisstein's MathWorld entry, "Cassini's Identity," was observed on 2026-07-13 at
`https://mathworld.wolfram.com/CassinisIdentity.html`. Its rendered formula is

```text
F_(n-1) * F_(n+1) - F_n^2 = (-1)^n.
```

It says this identity was also discovered by Simson, identifies it as Catalan's identity with
`r = 1`, and cites Coxeter and Greitzer (1967, page 41), Coxeter (1969, pages 165-168), Wells
(1986, page 62), and Petkovsek, Wilf, and Zeilberger (1996, page 12). The observed 52,085-byte HTML
response has SHA-256 `cc85db96bde2915bc1bb676527629bcabe97324713cc7458af570a17cdc77fbe`.

This supports recognition of the conventional formula family, not H0. It is a mutable secondary
encyclopedia page; it does not give the catalog's asserted 1680 edition or page, fix the index
domain or Fibonacci convention, supply a complete proof, audit attribution conflicts, corrections
or errata, or have an independent source-review receipt. The listed books are bibliography leads
only and were not admitted during this intake.

## Component crosswalk

| Component | Conventional lead | Pinned Lean candidate | Intake assessment |
|---|---|---|---|
| Fibonacci numbers | `F_n`, definition unstated on the identity page | `Int.fib` extending `Nat.fib` | definition and index convention remain source choices |
| index | an untyped `n` in the rendered formula | `n : Int` | candidate is materially broader than a usual positive-natural statement |
| predecessor/successor | `F_(n-1)` and `F_(n+1)` | `fib (n - 1)` and `fib (n + 1)` | exact on the integer candidate; natural zero boundary remains open |
| determinant difference | predecessor times successor minus square | same left side | strong formula-level alignment only |
| alternating sign | `(-1)^n` | `(-1) ^ n.natAbs` | agrees on nonnegative indices; negative-index interpretation needs review |
| equation orientation | difference equals sign | same orientation | rearranged or shifted forms require checked transports |
| `已验证` | untrusted catalog metadata | no receipt | no H or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, module
`Mathlib.Data.Int.Fib.Lemmas` exposes:

```text
Int.fib_succ_mul_fib_pred_sub_fib_sq (n : Int) :
  Int.fib (n + 1) * Int.fib (n - 1) - Int.fib n ^ 2 = (-1) ^ n.natAbs
```

The pinned source explicitly calls this Cassini's identity. It also contains a file-local
natural-cast auxiliary and the broader public Catalan identity. The auxiliary cannot be referenced
as a public API declaration outside its module. The file has SHA-256
`5622457f63665e6bcbbef34e67c2a27cd8faf98911678550a6b93ba34d685536` and originated in upstream
mathlib commit `4eb9bc7aa8fa0750e90c05d945d0d78b6d7e7d1f` (Monica Omar, 2025-11-28,
`feat(Data/Int/Fib): the Cassini and Catalan identities (#30882)`).

`IntakeProbe.lean` establishes candidate availability and reports its current axiom surface only.
It does not select the integer theorem as the repository root, normalize a source-identical
expression, audit terminal provenance or transitive trust, or assign M0 proof credit. The statement
phase must first record an approved target correction/source selection, then freeze minimal imports,
the exact expression and environment fingerprints, checked transports, and required mutations.

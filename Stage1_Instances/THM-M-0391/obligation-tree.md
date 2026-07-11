# Frozen obligation architecture

## Freeze boundary

This is the version-1 registry for `S56-M-0391-OBLIGATION_TREE`. It freezes 15
root-relevant semantic obligations before any proof implementation. All 15 are
eligible on the machine, human-source, and readable axes; there are no
exclusions. The canonical sorted projection digest is recorded in
`obligation-registry.json`. Planned fingerprints identify exact intended
claims, not elaborated Lean declarations or proof evidence.

The architecture is deliberately a proof plan. Only `M0391-S-BOUNDARY` has a
local checked body, and that body proves statement transport rather than
Mihailescu's theorem. Every other node remains `[H1, M4, R4]`; the root remains
open. The paper's exact lemma-to-node mapping is not invented here: the
cyclotomic core is marked as an unmapped source boundary pending primary-source
audit.

## Proof and refinement tree

```text
M0391-ROOT  exact Nat theorem
|-- M0391-S-BOUNDARY  statement/domain/transport boundary [checked transport]
|-- M0391-N-EXPONENT  choose even or odd-prime exponent divisors
|-- M0391-N-POWER-LIFT  rewrite bases after divisor selection
|-- M0391-B-EXHAUSTIVE  exhaustive normalized branch split
|   |-- M0391-B-EE  square/square impossibility
|   |-- M0391-B-EO  square/odd-prime classification
|   |   |-- M0391-L-EO-FACTOR  factorization and coprimality
|   |   `-- M0391-L-EO-CLASSIFY  unit/coefficient classification
|   |-- M0391-B-OE  odd-prime/square impossibility
|   |   `-- M0391-L-OE-FACTOR  factorization and coprimality
|   `-- M0391-B-OO  odd-prime/odd-prime impossibility
|       |-- M0391-L-OO-CYCLOTOMIC  cyclotomic construction and invariants
|       `-- M0391-L-OO-DESCENT  terminal contradiction
`-- M0391-T-LIFTBACK  recover the original bases and exponents
```

`typed-graphs.json` separates proof requirements from refinement,
provenance, evidence, trust, documentation, and workflow ordering. In
particular, source and documentation links are not proof premises. The four
branch nodes jointly refine `M0391-B-EXHAUSTIVE`; later proof work must supply a
checked composition harness consuming every branch and the lift-back result.

## Leaf ledgers and expansion triggers

No open core node is certified as a final `<=100`-step leaf merely because its
title is short. The following ledgers state the minimum proof work and where
further splitting is mandatory.

| Obligation | Substantive ledger | Budget state |
|---|---|---|
| `S-BOUNDARY` | Bind the exact curried target; transport to the conjunction form in both directions; preserve all four strict bounds and the oriented equation. | 8 steps, checked locally; no root closure |
| `N-EXPONENT` | For each exponent greater than one, decide divisibility by two or select an odd prime divisor; retain divisor positivity/primality. | planned `<=100`; exact Lean signature required |
| `N-POWER-LIFT` | Write each original perfect power as a square or odd-prime power of a lifted base; prove associativity of exponentiation and that lifted bases stay greater than one. | planned `<=100`; exact Lean signature required |
| `B-EXHAUSTIVE` | Form four exponent-type branches; prove exhaustiveness and disjoint handling; consume all four branch conclusions. | planned `<=100`; composition certificate required |
| `B-EE` | Factor `X^2-Y^2=1`; use positivity and adjacent-factor constraints to contradict `X,Y>1`. | planned `<=100` |
| `B-EO` | Establish the factorization/coprimality package; apply the classification package; return only `(X,Y,q)=(3,2,3)`. | nonleaf; two required children |
| `L-EO-FACTOR` | Choose the required quadratic/cyclotomic setting; factor; establish integrality, units, gcd/ideal conditions, and the exact power relation. | split-required before proof: construction and invariant work is hidden |
| `L-EO-CLASSIFY` | Analyze units and coefficients; exclude all parameters except `3,2,3`; verify the surviving tuple. | split-required before proof: central classification theorem |
| `B-OE` | Apply the odd-prime-minus-one factorization; show its coprime factors cannot multiply to a nontrivial square under the branch hypotheses. | nonleaf; factorization child required, likely further split |
| `L-OE-FACTOR` | Factor, compute the gcd, control parity, and derive the incompatible square-factor allocation. | planned `<=100`; exact Lean signature required |
| `B-OO` | Build the cyclotomic objects and consume the descent/contradiction theorem. | nonleaf; two required children |
| `L-OO-CYCLOTOMIC` | Define the number field/ring/units/ideals used by the proof; prove well-definedness, ramification and compatibility invariants; derive relations from a solution. | split-required: construction and multiple high-risk invariants |
| `L-OO-DESCENT` | Use the cyclotomic relations to run the terminal descent or contradiction and discharge all exceptional cases. | split-required: central published proof package |
| `T-LIFTBACK` | From the sole normalized solution, prove the selected divisors and lifted bases force `x=3,a=2,y=2,b=3`; reject exponent multiples and alternative perfect-power representations. | split-required: uniqueness/lift-back is root-critical |
| `ROOT` | Introduce the canonical hypotheses; invoke normalization; run all branches; transport the sole surviving result back; construct the fourfold conjunction. | nonleaf; exact child-to-parent certificate required |

## Typed provenance and trust boundary

The only known terminal local body is
`Stage1Instances.THMM0391.mihailescuTarget_iff_legacyStatementShape`. The
Formal Conjectures declaration audited earlier contains `sorry` and therefore
does not appear as a proof-body provenance node. The pinned mathlib polynomial
theorem is statement-mismatched and is likewise absent from the proof graph.

The checked transport trusts Lean 4.29.0 and `Init`. Root trust remains pending:
future proof work must record the complete import and declaration closure,
axioms, computation boundaries, and proof-body origins. No source link,
workflow acceptance, or documentation edge can change machine debt.

## Phase verdict

The registry and graphs are frozen and structurally self-tested. This phase
does not close a proof obligation, complete the audit, or complete the theorem.
The next proof cut set is `N-EXPONENT`, `N-POWER-LIFT`, the four branch
packages (especially the cyclotomic construction/descent), and `T-LIFTBACK`.

# THM-M-0387 rev-5.6 Process And Tree Audit

> Audit date: `2026-07-10` (`Asia/Shanghai`)
> Authority: `Docs/Stage1_Blueprint_rev-5.6.md`

This stable audit records proof-tree structure, readable routing, and the
boundary between checked proof bodies and machine-open plans. It contains no
worker, scheduler, process, private-path, or runtime evidence.

## Stable Surfaces

| role | stable path | authority boundary |
|---|---|---|
| execution requirements and cursor | `Docs/Stage1_Blueprint_rev-5.6.md` | only progress authority |
| proof DAG and debt ledger | `THM-M-0387/proof_units.json` | derived evidence manifest, not a second checklist |
| short route | `THM-M-0387/proof_outline.md` | root-to-terminal reader map |
| checked-node reconstruction | `THM-M-0387/readable/machine_closed_nodes.md` | ten-part entries for `M0-*` nodes |
| general odd-prime route | `THM-M-0387/readable/wiles_taylor_wiles_process.md` | human proof plan and machine blockers |
| external discovery | `THM-M-0387/readable/external_candidate_ledger.md` | dated immutable candidate audit |
| special branches | `THM-M-0387/eligibles/` | detailed `n=3`, `n=4`, and regular-prime reconstruction |
| machine evidence | `THM-M-0387/machine_checked_audit.md` | types, pins, axioms, proof-body locations |
| reproducibility | `THM-M-0387/build_validation.md` | dated commands and results |

## Tree Identity

The manifest has one exact root, `M0387-ROOT`, whose formal target is
`FermatLastTheorem`. Its mandatory children cover:

1. `M0387-S`: definitions, domains, equivalences, boundary cases, and the
   accepted axiom policy.
2. `M0387-R`: exponent reduction and the exact conditional composition theorem
   `FermatLastTheorem.of_odd_primes`.
3. `M0387-B3`: mathlib's exponent-three descent branch.
4. `M0387-B4`: mathlib's exponent-four infinite-descent branch and derived
   transports.
5. `M0387-RP`: the pinned `flt-regular` regular-prime branch plus checked small
   exponents `3 <= n <= 16`.
6. `M0387-WTW`: the historical Frey, modularity, level-lowering, and low-level
   contradiction route for all remaining odd prime exponents.
7. Explicit trust nodes for the Lean kernel, mathlib, pinned `flt-regular`,
   primary papers, and the blocked Imperial candidate.

All final leaves carry an independently reviewable logical-step ledger bounded
by `100`. High-risk imported theorems are bridge or trust nodes rather than
being hidden as one-line proof steps. Graph validity, reachability, reciprocal
edges, acyclicity, leaf budgets, classifications, and metrics are recomputed by
`python3 scripts/lint_theorem_dossier.py THM-M-0387`.

The final recomputed metrics are classification `132/132`, machine closure
`29/93 (31.18%)`, readable closure `132/132`, and human-source `H0` closure
`0/113`. All nodes remain `H1` because the exact primary-source
section/theorem/page and assumption crosswalk is unfinished. This is
source-reconstruction debt, not a claim that the historical proof is unknown.

## Composition Boundary

The checked local composition edge is:

```lean
fermatLastTheoremRootOfOddPrimesPath :
  OddPrimeExponentClosure -> fermatLastTheoremRootStatement
```

It wraps mathlib's:

```lean
FermatLastTheorem.of_odd_primes :
  (forall p, Nat.Prime p -> Odd p -> FermatLastTheoremFor p) ->
  FermatLastTheorem
```

This theorem checks only the implication. The premise
`OddPrimeExponentClosure` is not locally proved. Therefore the exact root is
`M2`, not `M0-*`; no composition wording in the human route closes that gap.

## Checked Branches

| branch | exact checked endpoint | proof-body boundary |
|---|---|---|
| statement and reduction | `StatementAndReductionPath` wrappers | local wrapper bodies over pinned mathlib |
| exponent `3` | `flt3Path : FermatLastTheoremFor 3` | `Mathlib/NumberTheory/FLT/Three.lean:750` |
| exponent `4` | `flt4Path : FermatLastTheoremFor 4` | `Mathlib/NumberTheory/FLT/Four.lean:266` |
| selected exponent-four internals | `flt4PositiveOddMinimalPath`, `flt4CoprimeSquareSumSymmPath`, `flt4NoMinimalPath`, `flt4BridgeTerminalPath` | exact local wrappers over pinned mathlib bodies |
| integer `4` | `flt4IntPath : FermatLastTheoremWith Int 4` | derived local wrapper over mathlib transport |
| exponent `8` | `flt8ViaFlt4Path : FermatLastTheoremFor 8` | derived local wrapper using exponent monotonicity |
| small exponents | `fltSmallExponentsPath`, including wrappers for `5,7,11,13` | pinned `flt-regular` dependency |
| regular odd primes | `regularPrimesPath` | pinned `FltRegular/FltRegular.lean:14`, not vendored |
| selected regular-prime internals | `regularPrimePrimitivePath`, `regularPrimeCaseIPath`, `regularPrimeCaseIIPath` | exact local wrappers over pinned `flt-regular` bodies, not vendored |

Each audited endpoint reports only the accepted baseline
`[propext, Classical.choice, Quot.sound]`; the generic monotonicity theorem
reports `[propext]`. The detailed source reconstruction and leaf budgets live
in the checked-node and eligible surfaces named above.

## Human Route

The exact FLT statement is historically proved by the joint published package
of Wiles and Taylor-Wiles. The readable tree separates this human fact from
machine status:

1. `W01` normalizes a primitive counterexample for an odd prime exponent.
2. `W02` builds the Frey curve and establishes its local invariants.
3. `W03` constructs the mod-`p` representation and establishes irreducibility
   and local conditions.
4. `W04` obtains semistable modularity through deformation rings, Hecke
   algebras, Taylor-Wiles primes, patching, `R=T`, and lifting.
5. `W05` applies Ribet level lowering to reach weight two and level two.
6. `W06` computes that the required level-two cusp-form space is zero.
7. `W07` combines modularity and lowering into a contradiction.
8. `W08` quantifies over the remaining odd primes and merges exponent `3`.
9. `W09` uses the checked conditional assembly edge with exponent `4`.

`THM-M-0387/readable/wiles_taylor_wiles_process.md` recursively expands
`W02` through `W06`. A node remains `H1` where exact primary section/theorem/page
mapping has not been completed even though the historical proof is accepted.
Readable prose for an `M3` or `M4` node is explicitly a proof plan, never a
claim that Lean has checked it.

## External Candidate Boundary

At immutable revision
`44df7744a2a65cdc111875dc1b6f0db85477348f`, the Imperial College London project
contains an exact `flt : FermatLastTheorem`, but its terminal chain includes
`B4_proof : B4 := sorry`. Its terminal positive-natural theorem reports
`[knownin1980s, propext, sorryAx, Classical.choice, Quot.sound]`, and
`knownin1980s` proves an arbitrary proposition. The source scan found `86`
`sorry` occurrences in `25` Lean files. It is therefore an `M5/E3` blocker,
not a machine proof. Its modern compatible-family route also must not be
presented as the historical Ribet `W05/W06` route.

## Audit Decision

Audit completion and theorem completion are separate decisions. A fully
classified DAG, a complete source-boundary ledger, and readable plans can
finish the rev-5.6 audit while the exact root remains machine-open. Theorem
completion is blocked until an exact local `FermatLastTheorem` declaration
passes the kernel, type, axiom, placeholder, pin, and composition gates without
disallowed axioms.

The remaining checklist blockers are dependency-specific:

- `H02` remains open because exponent reduction and `n=3/n=4` still lack an
  exact primary human-source statement/assumption crosswalk.
- `H03` remains open because the Kummer regular-prime Case I/II formal tree has
  not been mapped to pinpoint primary proof locations.
- `H04` is blocked by `H02` and `H03`, even though every node has the
  conservative classification `H1`.
- `C06` remains open because W01-W06 have no compatible placeholder-free exact
  Lean proof packets; `C07` is consequently open, so dependency-gated `C08`,
  `R04-R06`, and `V01-V07` remain open as well.
- Exact theorem completion remains blocked at `[H1, M2, R0]`; the Imperial
  candidate is only `M5/E3` and cannot satisfy the root gate.

The worker cursor therefore advances only the dependency-valid prefix through
`C05` and `R03`. Although the final validation command itself passed, `V01`
depends on still-open `C08`; the successful command is durable evidence, not
permission to bypass the authoritative dependency DAG.

# THM-M-0387 rev-5.6 Build Validation

> Validation date: `2026-07-10` (`Asia/Shanghai`)
> Scope: exact local source, pinned dependency closure, proof DAG, and stable dossier surfaces

This record is durable evidence for the declarations and audits named below.
It is not evidence that the exact `FermatLastTheorem` root is proved.

## Pinned Environment

| component | version or immutable revision |
|---|---|
| Lean | `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| Lake | `5.0.0-src+98dc76e` |
| mathlib | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `leanprover-community/flt-regular` | `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` |
| `checkdecls` in dependency manifest | `3d425859e73fcfbef85b9638c2a91708ef4a22d4` |

Pins are recorded in `Formalizations/Lean/lakefile.lean` and
`Formalizations/Lean/lake-manifest.json`. The validation lint also compares
them with the local dependency checkouts and `proof_units.json`.

## Node-Scoped Lean Checks

The following direct source checks passed with exit code `0`:

```bash
cd Formalizations/Lean
lake env lean AwesomeTheorems/NumberTheory/THM_M_0387/StatementAndReductionPath.lean
lake env lean AwesomeTheorems/NumberTheory/THM_M_0387/SmallExponentsPath.lean
lake env lean AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean
lake env lean AwesomeTheorems/Stage1/S1_M_001.lean
lake env lean AwesomeTheorems.lean
lake env lean ../../THM-M-0387/FermatLastTheorem_Sample.lean
```

The direct target build also passed:

```bash
cd Formalizations/Lean
LAKE_NUM_JOBS=1 lake build \
  +AwesomeTheorems.NumberTheory.THM_M_0387.StatementAndReductionPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path \
  +AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path \
  +AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.SmallExponentsPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.Sample \
  +AwesomeTheorems.Stage1.S1_M_001 \
  +AwesomeTheorems
```

The final canonical run completed successfully: node-scoped build `3742`
jobs, Stage1 wrapper `3741`, shared aggregator `3743`, and full Lake build
`3744`. The job counts are incidental build output, not coverage metrics.

## Aggregate Gate

From the repository root, the canonical command is:

```bash
bash THM-M-0387/run_local_validation.sh
```

It performs the following gates in one reproducible path:

1. checks Lean and Lake versions;
2. builds the statement/reduction, `n=3`, `n=4`, regular-prime,
   small-exponent, sample, Stage1, and aggregate modules;
3. checks the dossier-local Lean entrypoint;
4. validates the rev-5.6 proof DAG and metrics;
5. checks exact declaration types and parses terminal axiom reports;
6. audits dependency pins and proof-body locations;
7. scans relevant local, mathlib, and pinned `flt-regular` proof sources for
   placeholders and disallowed custom axioms;
8. checks stable public paths and cross-surface root status.

Final result: exit code `0`. The theorem-folder sample passed, Python lint
compilation passed, and the strict dossier lint reported:

```text
lint_theorem_dossier: ok (THM-M-0387, schema 5.6, 132 nodes, 29 exact-type/axiom probes)
```

A pass covers the exact nodes listed in the generated audit; it does not
synthesize the missing odd-prime family.

## Coverage And Debt Ledger

| metric | final value |
|---|---:|
| tree classification | `132 / 132` (`100%`) |
| machine closure | `29 / 93` (`31.18%`) |
| readable closure | `132 / 132` (`100%`) |
| human-source `H0` closure | `0 / 113` (`0%`) |
| exact root machine closed | `false` |

Machine debts are `M0-L: 7`, `M0-W: 10`, `M0-P: 12`, `M2: 10`,
`M3: 33`, `M4: 56`, and `M5: 4`. All `132` nodes remain `H1`: primary
sources are identified for the historical route, but the exact
section/theorem/page-to-node statement and assumption crosswalk required for
`H0` is not complete. All `132` public nodes are `R0`; open machine nodes are
written as plans or blockers rather than completed proofs.
The exact root vector remains `[H1, M2, R0]`.

## Axiom And Placeholder Evidence

Direct `#print axioms` probes for the local statement/reduction wrappers,
`flt3Path`, `flt4Path`, `flt4IntPath`, `flt8ViaFlt4Path`, `flt5Path`, `flt7Path`,
`flt11Path`, `flt13Path`, `fltSmallExponentsPath`, `regularPrimesPath`, the
upstream terminals `fermatLastTheoremThree`, `fermatLastTheoremFour`,
`FLT_small`, and `flt_regular` report only:

```text
[propext, Classical.choice, Quot.sound]
```

`FermatLastTheoremWith.mono` reports `[propext]`. These are the accepted
baseline axioms for this dossier. Relevant local and pinned dependency source
scans found no `sorry`, `admit`, `sorryAx`, or custom `axiom` in the checked
proof bodies.

The Imperial full-FLT candidate is outside this accepted closure: at revision
`44df7744a2a65cdc111875dc1b6f0db85477348f`, it has
`B4_proof : B4 := sorry` and terminal axioms including `sorryAx` and the
arbitrary-proposition axiom `knownin1980s`. It is recorded as `M5/E3` only.

## Exact Type And Body Locations

| conclusion | declaration or wrapper | proof-body location |
|---|---|---|
| exact root alias | `fermatLastTheoremRootStatement_iff` | repo-local definitional wrapper |
| primitive equivalence | `fermatLastTheoremFor_iff_coprime` | repo-local composition over mathlib primitive reduction |
| integer/rational transport | `fermatLastTheoremFor_iff_integer`, `fermatLastTheoremFor_iff_rational` | repo-local wrappers over `Mathlib/NumberTheory/FLT/Basic.lean` |
| conditional root assembly | `fermatLastTheoremRootOfOddPrimesPath` | repo-local wrapper over `Mathlib/NumberTheory/FLT/Four.lean:275` |
| exponent `3` | `flt3Path : FermatLastTheoremFor 3` | `Mathlib/NumberTheory/FLT/Three.lean:750` |
| exponent `4` | `flt4Path : FermatLastTheoremFor 4` | `Mathlib/NumberTheory/FLT/Four.lean:266` |
| exponent-four internal endpoints | `flt4PositiveOddMinimalPath`, `flt4CoprimeSquareSumSymmPath`, `flt4NoMinimalPath`, `flt4BridgeTerminalPath` | `Mathlib/NumberTheory/FLT/Four.lean`, exposed through `InternalCoveragePath.lean` |
| regular primes | `regularPrimesPath` | `FltRegular/FltRegular.lean:14` in pinned dependency |
| regular-prime internal endpoints | `regularPrimePrimitivePath`, `regularPrimeCaseIPath`, `regularPrimeCaseIIPath` | pinned `FltRegular/MayAssume`, `CaseI`, and `CaseII` sources, exposed through `InternalCoveragePath.lean` |
| `3 <= n <= 16` | `fltSmallExponentsPath` | `FltRegular/SmallNumbers/SmallNumbers.lean:15` in pinned dependency |

The regular-prime proof body is checked through a pinned dependency and is not
vendored into this repository.

## Root Decision

No declaration of exact type `FermatLastTheorem` is locally proved without an
open premise. The only exact-root route is conditional on
`OddPrimeExponentClosure`, whose nonregular odd-prime Wiles/Taylor-Wiles leaves
remain machine-open. Consequently:

```text
exact root kernel closure: no
root machine debt: M2
theorem completion: blocked
audit completion: accepted by master validation
```

## Master Acceptance

The supervising master independently reran the canonical seven-stage command,
inspected the exact-root search, recomputed the DAG/leaf/coverage counts, and
rechecked the public-status lint after the worker handoff. The result remained
`132` classified nodes, `101` final leaves with no budget above `100`, `29/93`
machine closure, and no placeholder-free local declaration of exact type
`FermatLastTheorem`.

The authoritative rev-5.6 checklist therefore has `35` master-accepted items
and `6` intentionally open items. The open set is exact and not an audit
failure:

- `H02`, `H03`, and `H04`: exact page/theorem/assumption crosswalks for the
  historical special-case and Kummer sources remain incomplete, so all nodes
  conservatively remain `H1`.
- `C06` and `C07`: the general Wiles/Ribet/Taylor-Wiles leaves and their root
  composition are not kernel-closed in this repository.
- `V07`: theorem completion is not accepted because the exact root is still
  `M2`.

This closes the attainable rev-5.6 audit while preserving the remaining human
source debt and exact-root machine blocker as explicit work rather than
manufacturing completion.

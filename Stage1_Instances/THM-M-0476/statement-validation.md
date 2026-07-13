# Statement validation

Item: `S56-M-0476-STATEMENT`

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b` (tree
`78b0a751473bf6d71f453a6aad18b130268a3428`).

Validation date: 2026-07-13 (Asia/Shanghai).

## Frozen target

`Stage1Instances.THM_M_0476.WilsonTheoremTarget` is the conventional forward reading selected at
intake:

```text
forall (p : Nat), p.Prime -> ((p - 1)! : ZMod p) = -1
```

The ordered binders are `p : Nat` and `hp : p.Prime`; the conclusion casts
`Nat.factorial (p - 1)` into `ZMod p` and compares it with the additive inverse of one. The target
includes `p = 2`. Zero, one, and composite moduli are outside it only because they fail the prime
premise. The stronger primality characterization is not substituted.

The direct imports are exactly `Mathlib.Data.Nat.Factorial.Basic`,
`Mathlib.Data.Nat.Prime.Defs`, and `Mathlib.Data.ZMod.Defs`. Independent deletion tests reject every
proper two-module subset; single-module probes also fail. The proof-bearing
`Mathlib.NumberTheory.Wilson` module is deliberately absent.

`wilsonTheoremTarget_iff_factTarget` checks the exact binder transport to the
`[Fact p.Prime]` form. It reports `propext` and `Quot.sound`; that observation is not a formal
candidate trust audit or proof credit.

All four mutations elaborate to propositions distinct from the frozen target and cannot be used
directly where its exact type is expected. These identity tests do not generally assert logical
independence or non-implication. The boundary mutation receives a stronger semantic check: it
wrongly includes composite modulus `p = 4`, and `mutationIncludedCompositeFour_false` kernel-refutes
it with the decidable `p = 4` counterexample.

## Commands and results

All commands ran in this worker clone. Lean used the pre-existing automation-provided canonical
`.lake` symlink read-only; no update, build, clone, fetch, or dependency mutation was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0476` | exit 0; rank 1357, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0476/Statement.lean)` | exit 0; canonical target, checked Fact transport, four expected mutation type rejections, transport axioms, and explicit target expression emitted |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0476/check_statement.py)` | exit 0; expression SHA-256 `ee76edb160426d3e8d95b11bfedca7febcfe915f50007e042875c922ebc8a4ac`; all four mutations distinguished; each proper import subset rejected; pins and worker handoff agreed |
| `python3 -B Stage1_Instances/THM-M-0476/check_intake.py` | exit 0; historical planned intake invariants agree with the expanded statement dossier and unchanged open task DAG |
| `python3 -m json.tool` on each owned JSON and `.stage1-worker-selftest.json` | exit 0 for every file |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0476-statement-pycache python3 -m py_compile Stage1_Instances/THM-M-0476/check_intake.py Stage1_Instances/THM-M-0476/check_statement.py` | exit 0; both checkers compiled outside the repository tree |
| scoped prohibited-construct scan over owned Lean files | exit 1 as expected; no prohibited declaration or proof escape matched |
| `git diff --check -- Stage1_Instances/THM-M-0476 .stage1-worker-selftest.json` plus no-index checks for untracked files | exit 0; no whitespace diagnostics |

## Status boundary

The repository record still supplies no primary edition or authoritative pinpoint, explicit domain
or prime premise, definitions, correction or errata review, or independent source approval. The
selected natural-prime target is therefore an explicit conventional formalization choice, not an
`H0` source claim. Anchor and terminal proof-body provenance/trust audit, obligation freeze, proof,
composition, readable reconstruction, hermetic replay, deterministic evidence bundle, independent
verification, release, and master acceptance remain open.

This worker statement proposal remains `[H1, M3, R4]` and supplies no proof, accepted receipt,
audit completion, or theorem completion.

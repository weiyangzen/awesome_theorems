# Statement validation

Item: `S56-M-0484-STATEMENT`

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b` (tree
`78b0a751473bf6d71f453a6aad18b130268a3428`).

Validation date: 2026-07-13 (Asia/Shanghai).

## Frozen target

`Stage1Instances.THM_M_0484.LucasLehmerTestTarget` freezes the exact intake-selected criterion:
for every natural `p` with `3 <= p`, `LucasLehmerTest p` holds if and only if `mersenne p` is
prime. The test is the zero-based residue after `p - 2` recurrence updates from seed four.

The sole direct import is `Mathlib.NumberTheory.LucasLehmer`, the public exact-topic module that
owns all required vocabulary. Deleting it makes the statement module fail. The module also checks
the definitional `ZMod` residue form and the library's integer-remainder form. It does not invoke
either Lucas-Lehmer correctness theorem to prove the canonical target and claims no proof credit.

The conventional odd-prime, one-based `S_(p-1)` source form remains uncredited. The catalog gives
no proposition or citation, the primary 1930 article has not been audited, and the modern source
lead omits a necessity proof. Thus exact formal scope is frozen while human-source fidelity remains
`H1`, not `H0`. The adjective "fast" remains outside the proposition because no cost model exists.

## Commands and results

All commands ran inside this worker clone. The scheduler-provided canonical `.lake` symlink was
used read-only; no update, build, clone, fetch, or dependency mutation was performed. The symlink
makes this dirty worker run nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0484` | 0 | rank 1365, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0484/Statement.lean)` | 0 | exact target and both transports elaborated; four expected type mismatches, four mutation refutations, and the `p = 2` counterexample checked; explicit target printed |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0484/check_statement.py)` | 0 | expression SHA-256 `6bd6024bd44d0bd9c50f6425b9ce5fdaecaf783ac84d32688717d3bde3151aea`; file SHA-256 `1baec8791288b46d6df61e060be07aa190ac1d0424229595523a095e8259c8dc`; all mutations distinct; sole import necessary |
| `python3 -B Stage1_Instances/THM-M-0484/check_intake.py` | 0 | expanded planned dossier preserves intake identity, six open tasks, `[H1,M3,R4]`, and empty accepted state |
| `python3 -B Stage1_Instances/THM-M-0484/check_statement_artifacts.py --worker-packet .stage1-worker-selftest.json` | 0 | structured records, authoritative/local task identity, exact changed paths, fingerprints, provisional boundaries, and worker packet agree |

The final statement record, provisional receipt, intake reconciliation, worker packet, prohibited-
construct scan, Python compilation, JSON parsing, and whitespace checks are captured in
`statement-receipt.json` after artifact finalization.

## Boundary and status

`p = 2` is a genuine counterexample to either an unconditional iff or a prime-exponent iff:
`mersenne 2 = 3` is prime, while the residue at `2 - 2 = 0` is `4 mod 3 = 1`. The checked
mutations also distinguish removal of `3 <= p`, relocating its binder scope, and weakening it to
`2 <= p`. Composite exponents at least three stay in the selected sharper formal domain.

This is statement-only evidence pending master acceptance. Primary-source review, source-domain and
one-based-index transport, anchor/provenance audit, obligation registry, proof and composition,
readable reconstruction, hermetic replay, deterministic evidence, independent verification,
release, audit completion, and theorem completion all remain open.

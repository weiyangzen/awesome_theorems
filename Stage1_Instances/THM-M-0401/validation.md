# Statement validation

Base revision: `ca5213c506afa21d64fb8f2481ac658887786c6e`.

The validation uses the existing pinned `.lake` dependency artifacts. It does not update, fetch, or otherwise mutate dependencies.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets; ranks 1..1546; all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0401
  exit 0: execution rank 14; planned; theorem_complete=false
(cd Formalizations/Lean && lake env lean --version)
  exit 0: Lean 4.29.0; commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0401/Statement.lean)
  exit 0: exact target and iff elaborated; all four guarded mutation failures observed; fully explicit target printed
python3 -m json.tool Stage1_Instances/THM-M-0401/instance.json
  exit 0
git diff --check -- Stage1_Instances/THM-M-0401 .stage1-worker-selftest.json
  exit 0
```

The Lean output is preserved canonically in `normalized-expression.txt`. The check covers statement elaboration only. It does not inspect a proof body, establish source fidelity, close an obligation tree, or support theorem completion.

After that successful check, a replay found that the shared canonical mathlib `.olean` tree had disappeared from the symlinked `.lake` directory and failed with `unknown module prefix 'Mathlib'`. No dependency command was run and no replacement artifact was fetched. The successful scoped elaboration above is the worker self-test evidence; fresh master replay requires restoration of the canonical pinned artifacts.

## Validation-phase execution

Item: `S56-M-0401-VALIDATION`. Base revision:
`76065c6d4727c5f002398b7e5310e0e68c872b56`. Validation timestamp:
`2026-07-11T19:46:00Z`.

The canonical pinned artifacts were available for this run. `Validation.lean`
independently reconstructs the only proof-phase body, the
`M0401-N-INTEGER-POINT` normalization leaf, without importing or invoking
`Proof.lean`. `check_validation.py` binds the frozen input and dependency
hashes, verifies all 14 registry/graph identities and the authoritative open
`M4` boundary, runs the obligation-tree validator, scans the Lean sources, and
replays the statement, proof leaf, and independent probe.

| command | exit | exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0401` | 0 | rank 14, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0401/validate_obligation_tree.py` | 0 | 14 obligations and 23 typed edges passed; root open M4 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0401/Statement.lean)` | 0 | exact target, checked `iff`, and mutation guards elaborated |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0401/Proof.lean)` | 0 | proof leaf elaborated; axioms: `propext`, `Classical.choice`, `Quot.sound` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0401/Validation.lean)` | 0 | independently reconstructed leaf elaborated with the same permitted axiom profile |
| `python3 Stage1_Instances/THM-M-0401/check_validation.py` | 0 | frozen inputs, pins, graph boundary, hygiene, and Lean recipes passed; root remains open M4 |
| `python3 -m json.tool Stage1_Instances/THM-M-0401/validation-receipt.json` | 0 | structured provisional receipt is valid JSON |
| prohibited-token scan of `Statement.lean`, `Proof.lean`, and `Validation.lean` | 1, expected empty | no local `sorry`, `admit`, `axiom`, or `unsafe` construct |
| `git diff --check -- Stage1_Instances/THM-M-0401 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, `lake build`, clone, fetch, or `.lake` mutation was performed.
The exact recipes and hashes are in `validation-receipt.json`.

This validates one partial leaf, not Schmidt's theorem. The proof dependency
is not root-closed, the frozen authority records zero accepted obligations and
no composition certificate, and the Subspace-Theorem and independence-limit
cut remains open. Root provenance/trust cannot close without a root body.
Empty-cache offline replay, a distinct signed runner, an independently
implemented release verifier, H0/R0 review, SBOM/licenses, CI, and a
deterministic release bundle are also absent. Therefore `audit_complete=false`,
`theorem_complete=false`, and the root vector remains `[H1, M4, R3]`.

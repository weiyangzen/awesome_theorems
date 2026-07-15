# Intake validation

Base revision: `2ff2721a0184cf5f856054cb7d46b10dbc703f5a`.

This record covers target membership, planned-dossier structure, JSON integrity, and a narrow
pinned Lean API probe. The shared canonical `.lake` link/artifacts were used read-only. No update,
build, fetch, or clone was run. Because exact source and encoding choices remain open, no canonical
expression hash, mutation result, proof, or accepted receipt is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0711` | exit 0; rank 751, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0711/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0711/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; planned lifecycle, empty accepted state, open formal expression, false terminal flags, and six open downstream tasks confirmed |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0711/IntakeProbe.lean)` | exit 0; seven group-presentation/computability API checks elaborated |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0711 -g '*.lean'` | exit 1, expected no-match; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0711` | exit 0; no output |

Known downstream work remains open: primary-source acceptance and independent review,
obligation/discovery freezes, formal-anchor audit,
proof, hermetic replay, and release acceptance. These prevent theorem completion but do not
invalidate a truthful self-tested `planned` intake.

## Statement phase (S56-M-0711-STATEMENT)

| Command | Result |
|---|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0711/Statement.lean)` | exit 0; canonical target and three expected structural mutation failures elaborated; explicit expression printed (7297 bytes, SHA-256 `1186dd31dd2f2126cb5998ef79ec6d9b64396acccdbdfc16dc6baa09c66edd3c`) |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0711` | exit 0; rank 751, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0711/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0711/statement-receipt.json` | exit 0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0711 -g '*.lean'` | exit 1, expected no-match |
| `git diff --check -- Stage1_Instances/THM-M-0711` | exit 0; no output |

The statement phase freezes and elaborates the exact repository target but supplies no proof.
Primary-source fidelity and every downstream proof/release gate remain open, so the root vector is
unchanged and `theorem_complete` remains false.

## Anchor-audit phase (S56-M-0711-ANCHOR_AUDIT)

Audit base revision: `136ebf643dcdcbc42cef34e415177189578060ef`.

| Command | Result |
|---|---|
| `rg -l -i 'Novikov|Boone' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` and corresponding `word[ _-]?problem|wordProblem` search | exit 1 expected no-match for each; zero terminal-name files at pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| same terminal-name search over each package named in `Formalizations/Lean/lake-manifest.json` | zero matching Lean files in all eleven pinned packages |
| immutable archive inspection for the three revisions in `anchor-audit-receipt.json` | exit 0; 17, 152, and 18 Lean files inspected respectively; no target-term match; third project contains at least 20 executable placeholder lines |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0711/AnchorAudit.lean)` | exit 0; all five adjacent declarations and explicit halting type checked; both audited theorems report `[propext, Classical.choice, Quot.sound]` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0711/Statement.lean)` | exit 0; frozen target and all three statement mutations re-elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0711/anchor-audit-receipt.json` and `instance.json` | exit 0 for both |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0711 -g '*.lean'` | exit 1 expected no-match |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0711` | exit 0; rank 751, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-0711` | exit 0; no output |

No dependency update, build, fetch, or clone was run in `.lake`. External archives were inspected
under `/tmp` only. The anchor audit is self-tested as a bounded negative inventory. It neither
asserts global nonexistence nor closes the target: the finite-presentation construction, checked
reduction, human-source gates, and all downstream phases remain open.

## Obligation-tree phase (S56-M-0711-OBLIGATION_TREE)

Validation base revision: `3a479c703900e8096e6b239e7bf5b0da25472b8a`.

| Command | Result |
|---|---|
| `python3 Stage1_Instances/THM-M-0711/build_obligation_artifacts.py` | exit 0; generated registry denominator `9fbdae321a68e51a301e942864c9a785fab407f21f25247ab04cb74277bd8d24` |
| `python3 Stage1_Instances/THM-M-0711/check_obligation_tree.py` | exit 0; PASS, 17 obligations and 38 typed edges; root explicitly open M4 |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-0711 -o /tmp/thm-m-0711-lean/Statement.olean ../../Stage1_Instances/THM-M-0711/Statement.lean` | exit 0; canonical statement elaborated to an ephemeral output outside `.lake` |
| `cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-0711-lean lake env lean -R ../../Stage1_Instances/THM-M-0711 ../../Stage1_Instances/THM-M-0711/ObligationTree.lean` | exit 0; conditional composition checked; axioms `[propext, Classical.choice, Quot.sound]` |
| `python3 -m json.tool` on the registry, typed graphs, validation specs, receipt, instance, and task DAG | exit 0 for all |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0711 -g '*.lean'` | exit 1 expected no-match; no prohibited placeholder or primitive declaration |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0711` | exit 0; rank 751, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-0711` | exit 0; no output |

No `.lake` dependency was mutated. The ephemeral `Statement.olean` exists only because the
obligation module imports the owned statement module without adding either file to the project
build. The frozen architecture and final conditional composition are self-tested. The finite
presentation, compiler, reduction correctness, source acceptance, trust closure, proof, and all
release gates remain open, so no theorem completion is claimed.

## Proof phase (S56-M-0711-PROOF)

Validation base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`.

| Command | Result |
|---|---|
| `bash Stage1_Instances/THM-M-0711/check_proof.sh` | exit 0; isolated `Statement.olean`, `ObligationTree.olean`, and `Proof.lean` elaborated at `--trust=0`; eight local/pinned declarations were sorry-free and reported exactly `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0711/check_proof.py` | exit 0; exact declarations, frozen fingerprints and denominator, pinned sources, receipt/blocker boundary, worker packet, and changed-path set passed |
| `python3 Stage1_Instances/THM-M-0711/check_obligation_tree.py` | exit 0; 17 obligations and 38 typed edges passed; root remains open M4 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0711` | exit 0; rank 751, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-0711 .stage1-worker-selftest.json` | exit 0; no whitespace errors |

The proof phase provisionally checks quotient normalization, the pinned halting leaf, and generic
many-one transfer. Its terminal declarations keep the missing halting-to-finite-presentation
reduction as an explicit premise and therefore do not close the unconditional witness or root.
Top-level Lake loading was unavailable because the unrelated shared `flt-regular` checkout could
not resolve `HEAD`; the narrow recipe selected the matching Lean binary and already pinned build
closure through the clean mathlib package, adjusted only process-local search paths, and wrote
target oleans outside `.lake`. No dependency source or artifact was changed. Exact details and
hashes are recorded in `proof-validation.md` and `proof-receipt.json`.

The first failed gate is `M0711-B-REDUCTION`; `M0711-S-FOUNDATION` is the other member of the frozen
root cut. The root remains `[H1, M4, R4]`, accepted state is unchanged, and validation, release,
audit completion, and theorem completion remain open.

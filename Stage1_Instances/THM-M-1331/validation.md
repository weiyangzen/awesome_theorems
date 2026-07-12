# Intake validation

Base revision: `bbb685ee4adcd9f19b5a727d1523cc7d6ad3b07f` (tree
`aadea0300fd76d31a98264ab39039d2247f8e049`).

This validation covers target membership, the fail-closed planned dossier and open DAG, repository
source provenance, JSON and scoped invariants, and one narrow pinned Lean API probe. The probe only
authenticates adjacent Picard-Lindelof existence and Gronwall uniqueness interfaces; it neither
selects nor proves a combined canonical statement. The automation-provided canonical `.lake`
symlink was used read-only. No update, build, clone, fetch, or dependency mutation was performed.
Because that symlink is a pre-existing untracked input and the dossier is new, this is nonrelease
worker evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1331` | exit 0; rank 943, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | exit 0; initial status contained only the pre-existing `Formalizations/Lean/.lake` symlink; final status adds only this dossier and the authorized root self-test packet |
| `git blame -L 9710,9718 -- Docs/researches/math_theorems.md` | exit 0; all catalogue lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | exit 0; revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes `651c8acc...b1d2` and `321626c8...2d81` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1331/IntakeProbe.lean)` | exit 0; nine adjacent pinned existence, uniqueness, fixed-point, flow, and autonomous-special-case interfaces elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1331/instance.json`, repeated for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each; all four files are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1331-pycache python3 -m py_compile Stage1_Instances/THM-M-1331/check_intake.py` | exit 0; the scoped validator compiles without writing generated files into the repository |
| `python3 Stage1_Instances/THM-M-1331/check_intake.py` | exit 0; target identity, planned H1/M3/R4 boundary, null canonical target, exact artifact inventory, provisional packet, and six open downstream tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)[[:space:]]\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1331` | exit 1 as expected with no matches; no prohibited Lean escape or bodyless declaration |
| `git diff --check -- Stage1_Instances/THM-M-1331 .stage1-worker-selftest.json` | exit 0; no tracked whitespace error; `check_intake.py` independently checks final new-file bytes, line endings, and trailing whitespace |

Known downstream failures remain deliberately open: immutable primary-source selection and pinpoint
transcription; exact assumptions, definitions, historical attribution, translation, errata, and
independent review; an authoritative distinction or deduplication relation with `THM-M-1332`;
canonical Lean elaboration, expression and environment fingerprints, transports, and statement
mutations; formal anchor and terminal-body provenance/trust audit; discovery and obligation
freezes; proof, composition, and readable reconstruction; hermetic replay, deterministic bundle,
independent verification, and master acceptance. They prevent audit or theorem completion but do
not invalidate this truthful `planned` intake.

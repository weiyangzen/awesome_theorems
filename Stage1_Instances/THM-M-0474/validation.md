# Intake validation

Base revision: `dd8846dbc83818f6ba7124151d5d4b7b29bb5b0d`.

This validation covers target membership, the planned dossier and open DAG, JSON integrity, source
provenance, and one narrow pinned Lean discovery probe. The probe checks the candidate API, two
candidate premise encodings, and the counterexample to the literal unconditional catalog reading.
It does not freeze the canonical statement, run the later statement mutation gate, audit a formal
anchor or terminal proof body, or claim proof credit. The automation-provided canonical `.lake`
symlink was used read-only; no dependency update, build, clone, fetch, or mutation was performed.
The symlink is a pre-existing untracked automation input, so this is nonrelease worker evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0474` | exit 0; rank 938, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes `651c8acc...b1d2` and `321626c8...2d81` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0474/IntakeProbe.lean)` | exit 0; eight pinned declarations printed; both premise forms and the unconditional counterexample kernel-checked |

The final JSON checks, `check_intake.py`, prohibited-construct scan, and scoped whitespace checks
all exited as recorded in `intake-receipt.json`. `#print axioms` on the candidate reported
`propext`, `Classical.choice`, and `Quot.sound`; this is a candidate observation only, not accepted
foundation or transitive trust closure.

Known downstream failures remain intentionally open: pinpoint primary-source selection, exact
assumption/domain/translation/errata mapping, and independent source review; canonical statement
elaboration, expression/environment fingerprints, checked alternate transports, and all required
mutations; discovery and obligation freezes; formal-candidate, proof-body, provenance, axiom, and
TCB audits; proof/composition/readability work; hermetic replay; deterministic evidence bundle;
independent verification; and master acceptance. They prevent audit or theorem completion but do
not invalidate a truthful `planned` intake.

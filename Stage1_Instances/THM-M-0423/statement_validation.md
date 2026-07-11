# Statement validation

Item: `S56-M-0423-STATEMENT`. Base revision:
`91cf43768c2b03b5c98d8ca436c450ba5a70babb`.

The exact coordinate-free target elaborates with the four imports listed in
`statement.json`. It uses mathlib's actual finite and infinite completion types
and `QuadraticForm.baseChange`, rather than the abstract local-data shape in the
legacy discovery module. No theorem proof is asserted.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets agree |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0423` | 0 | rank 67, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0423/Statement.lean` | 0 | exact target elaborated; `#print` emitted the frozen expression |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-0423 -o ../../Stage1_Instances/THM-M-0423/Statement.olean ../../Stage1_Instances/THM-M-0423/Statement.lean && LEAN_PATH="$(pwd)/../../Stage1_Instances/THM-M-0423:${LEAN_PATH:-}" lake env lean -R ../../Stage1_Instances/THM-M-0423 ../../Stage1_Instances/THM-M-0423/StatementMutations.lean` | 1 (expected) | four type mismatches: removed hypothesis, changed domain, changed binder scope, and zero-vector boundary are not definitionally equal to the frozen expressions |
| `python3 -m json.tool Stage1_Instances/THM-M-0423/statement.json >/dev/null` | 0 | statement record is valid JSON |
| `rg -n '\\b(sorry|axiom|admit)\\b' Stage1_Instances/THM-M-0423/Statement.lean Stage1_Instances/THM-M-0423/StatementMutations.lean` | 1 (expected) | no prohibited proof placeholders or axioms |
| `git diff --check -- Stage1_Instances/THM-M-0423` | 0 | no whitespace errors |

The temporary `Statement.olean` used to import the target into the negative test
is deleted after the run and is not evidence. The coordinate-polynomial alternate
encoding has no checked transport and is explicitly uncredited. Proof, source
audit, obligation-tree, hermetic validation, and release gates remain open.

# Intake validation record

Base revision: `e3d0fd205c9c81486cb86f68cdc66d4d4e5bb264`.

Commands were run from the repository root on 2026-07-12. Intake does not
claim an exact Lean elaboration or build; that work belongs to the dependent
statement node.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups, execution skill present, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0522` | 0 | rank 894, planned, L0, rework required, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | pinned executable available: Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-0522/intake.json` | 0 | valid JSON |
| `python3 -c "from pathlib import Path; r=Path('Stage1_Instances/THM-M-0522'); q={'README.md','intake.json','scope.md','source_statement_crosswalk.md','validation.md'}; assert q <= {p.name for p in r.iterdir() if p.is_file()}; t='\\n'.join((r/n).read_text() for n in sorted(q)); assert 'S56-M-0522-INTAKE' in t and 'THM-M-0522' in t and 'theorem_complete\\\": false' in t and 'Audit complete: no. Theorem complete: no.' in t"` | 0 | required five dossier files exist; item/theorem IDs and non-completion boundary are present |
| `git diff --check -- Stage1_Instances/THM-M-0522` | 0 | no whitespace errors |

These are the smallest real checks for this intake: repository-standard and
manifest consistency, availability of the pinned Lean executable, structured
record syntax, dossier completeness, and patch hygiene. They supply no
statement elaboration, axiom result, source acceptance, or theorem proof.

Known failures and follow-up boundaries: no exact Lean module or declaration,
expression hash, environment fingerprint, checked alternate encoding,
immutable source receipt, obligation registry, discovery protocol, proof body,
or independent review exists yet. Accordingly the root remains
`H1 / M3 / R4`, and both audit and theorem completion are false.

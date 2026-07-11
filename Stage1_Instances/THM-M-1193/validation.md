# Intake validation record

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

Commands below validate only manifest membership and dossier structure. No Lean declaration is
introduced, so no kernel-proof result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranked targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1193` | 0 | rank 387, planned, hard anchor/wrapper lane, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1193/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '^\\s*(axiom|theorem|lemma).*(:=\\s*)?(sorry|by\\s+sorry)\\b' Stage1_Instances/THM-M-1193` | 1 | no Lean placeholder declaration (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1193 .stage1-worker-selftest.json` | 0 | no whitespace errors before self-test manifest creation |

Master acceptance and all dependent statement, anchor, obligation, proof, validation, and release
nodes remain outstanding.

# Intake validation record

Base revision: `63ac99affece901f4fef1712ff25edca64d438f5`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0657` | 0 | rank 702, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0657/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -c "import json, pathlib; d=pathlib.Path('Stage1_Instances/THM-M-0657'); p=json.loads((d/'intake.json').read_text()); assert p['item_id']=='S56-M-0657-INTAKE'; assert p['theorem_id']=='THM-M-0657'; assert p['execution_rank']==702; assert p['lifecycle_mode']=='planned'; assert p['canonical_formal_target']['gate_state'].startswith('open_'); assert p['audit_complete'] is False and p['theorem_complete'] is False; assert p['accepted_proof_state']==[]; assert all((d/f).is_file() for f in ('README.md','source-statement-crosswalk.md','validation.md'))"` | 0 | item identity, lifecycle boundary, open formal gate, empty accepted state, and dossier references agree |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1090/S0002-9947-1965-0175782-0' \| python3 -c "import json,sys; m=json.load(sys.stdin)['message']; assert m['title']==['Categoricity in power']; assert m['author'][0]['given']=='Michael' and m['author'][0]['family']=='Morley'; assert m['published-print']['date-parts'][0][0]==1965; assert m['volume']=='114' and m['issue']=='2' and m['page']=='514-538'; print(m['DOI'], m['title'][0], m['page'])"` | 0 | Crossref returned the expected DOI, author, title, year, volume/issue, and pages; discovery metadata only |
| `! rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)' Stage1_Instances/THM-M-0657` | 0 | no prohibited Lean proof declarations found |
| `git diff --check -- Stage1_Instances/THM-M-0657` | 0 | no whitespace errors |

These checks establish target membership, standard consistency, JSON syntax,
cross-file identity, and absence of prohibited proof declarations only. This
intake introduces no Lean declaration, so there is no kernel proposition or
proof to compile. The Lean statement gate and master acceptance remain open.

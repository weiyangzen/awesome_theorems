# Intake validation

Base revision: `dc2eb1390c8f2a88e7afcbdbd35f92ab43f64fb8`; base tree:
`25138aaafcff80ee47bf04805bccd804978e6754`.

This validation covers target membership, the planned dossier and open task DAG, repository and
primary-source provenance, JSON and scoped invariants, a narrow pinned Lean substrate probe,
prohibited-construct hygiene, and whitespace. It does not validate a canonical theorem statement
or proof. The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink; it was used read-only and not modified.

## Source boundary

The MathNet primary scan of Suslin's 1976 four-page paper was retrieved to `/tmp`, inspected at
journal pages 1063-1066, and hashed. It locates the opening field formulation, the paper's
finitely-generated-projective convention, Theorem 3* over Dedekind domains and PIDs, and the
independent-Quillen footnote. It has not undergone independent translation, full proof-node
mapping, errata review, or source acceptance. Quillen's Crossref metadata was checked, while the
Springer full-text endpoint returned HTML rather than a PDF. Thus the source state remains `H1`.

## Commands and results

Commands ran from the repository root on 2026-07-13 (Asia/Shanghai), unless a `cwd` is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0034` | 0 | rank 1078; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 263,268 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0 stage1-intake' -sS 'https://api.crossref.org/works/10.1007/BF01390008' -o /tmp/quillen-crossref.json`; `jq`; `sha256sum`; `wc -c` | 0 each | Quillen, *Projective modules over polynomial rings*, Inventiones 36(1), 167-171, December 1976; 4,370-byte payload SHA-256 `c7e501fdb9473fadc536a6a99c7b5696e3740115a5f1d60cf1392ae9e004efc4` |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0 stage1-intake' -sS 'https://link.springer.com/content/pdf/10.1007/BF01390008.pdf' -o /tmp/quillen1976.pdf`; `file`; `sha256sum` | 0 | endpoint returned a 226,392-byte HTML access page, not a PDF; no Quillen full text was credited |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0 stage1-intake' -sS 'https://www.mathnet.ru/eng/dan40545' -o /tmp/suslin-mathnet.html`; `rg`; `sha256sum` | 0 | MathNet metadata confirms title, Doklady 229(5), 1063-1066, received 26 February 1976, MR0469905; 22,732-byte page SHA-256 `e565cd779f1c4b5f5a006bb568f743b9fc4bf4c24b3ef88ea56ef5d18278d199` |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0 stage1-intake' -sS 'https://www.mathnet.ru/php/getFT.phtml?jrnid=dan&paperid=40545&what=fullt&option_lang=eng' -o /tmp/suslin1976.pdf`; `file`; `wc -c`; `sha256sum`; `pdfinfo`; `pdftotext -layout`; `sed` | 0 each | four-page, 529,533-byte primary Russian PDF; SHA-256 `b01635ee5a28e8b78bc20c18301e4b2f5978dfa85933e8564cd6c3e64cc91353`; relevant statements inspected on journal pages 1063 and 1066 |
| bounded `rg` for Quillen-Suslin, Serre's conjecture, and projective modules over polynomial rings in repo-local Lean and pinned mathlib | 0/1 | no target-level declaration found; only unrelated noise and adjacent projective/free/polynomial APIs; bounded discovery only |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and `rev-parse HEAD^{tree}` | 0 each | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned package clean |
| `sha256sum` over authority files, toolchain locks, and the pinned substrate files | 0 | hashes recorded in `instance.json`; no input was modified |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0-src+98dc76e |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0034/IntakeProbe.lean` | 0 | ten adjacent API types and the standard-axiom report for `Module.Projective.of_free` elaborated; no target theorem stated |
| `python3 -m json.tool` for all JSON artifacts and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0034-pycache python3 -m py_compile Stage1_Instances/THM-M-0034/check_intake.py` | 0 | scoped checker compiles without writing inside the owned path |
| `python3 -B Stage1_Instances/THM-M-0034/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned lifecycle, `H1/M3/R4`, null formal target, exact inventory, hashes, receipt packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0034/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0034` | 1 (expected no match) | no prohibited Lean escape or declaration |
| `for f in Stage1_Instances/THM-M-0034/* .stage1-worker-selftest.json; do ... git diff --no-index --check /dev/null "$f" ...; done` | 0 | no whitespace diagnostics for any new file; the expected no-index difference exit was handled |
| `git diff --check -- Stage1_Instances/THM-M-0034 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0034-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source/root selection and independent review,
canonical Lean elaboration and mutation tests, anchor audit, discovery and obligation freezes,
typed graphs, proof, composition, trust closure, hermetic replay, deterministic release bundle, and
independent verification remain open. They prevent theorem completion but do not invalidate the
planned intake.

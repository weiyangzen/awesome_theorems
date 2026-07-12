# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the `planned` dossier and open task DAG, catalog and
source-discovery provenance, structured invariants, a narrow pinned Lean substrate probe,
prohibited-construct hygiene, and whitespace. It does not validate a canonical Artin reciprocity
statement or proof. The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It was used read-only and not modified.

## Source discovery boundary

Milne's author-hosted *Class Field Theory* v4.03 PDF was retrieved to a temporary path, inspected at
Chapter V, Section 5, printed pages 177-179, and hashed. It distinguishes the reciprocity law in
Theorem 5.3 from the existence theorem in Theorem 5.5. Crossref and publisher metadata for Artin's
1927 paper were also checked, but the article body was inaccessible. These checks support the
theorem-family crosswalk and `H1`, not an accepted exact statement or H0 review.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0015` | 0 | rank 1065; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 128,133 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 30 -sS -A 'Mozilla/5.0' 'https://www.jmilne.org/math/CourseNotes/CFT.pdf' -o /tmp/milne-cft-a.pdf` | 0 | retrieved the author-hosted v4.03 discovery copy outside the repository |
| `file /tmp/milne-cft-a.pdf`; `wc -c /tmp/milne-cft-a.pdf`; `sha256sum /tmp/milne-cft-a.pdf`; `pdfinfo /tmp/milne-cft-a.pdf`; `pdftotext -layout /tmp/milne-cft-a.pdf /tmp/milne-cft.txt` | 0 each | 296-page, 2,072,714-byte PDF; SHA-256 `50d79af78250a9f1117ad9d337e0b231704a533fc707966ed1bfa52e13d498f5`; title, author, version, and date confirmed; text extracted |
| `rg -n -C 40 '^5\.3\|T HEOREM 5\.3\|Theorem 5\.3' /tmp/milne-cft.txt` | 0 | located Chapter V Theorem 5.3, principal-idele kernel and finite-level norm quotient clauses |
| `sed -n '9685,9772p' /tmp/milne-cft.txt > /tmp/thm-m-0015-milne-v5.txt`; `sha256sum /tmp/thm-m-0015-milne-v5.txt` | 0 | extracted Proposition 5.2 through Theorem 5.5; SHA-256 `70a5370b18f732f834ae040acb47b8ce77d2bfd287b9a4d32b50c4f4e384c686` |
| `curl -L --fail --max-time 30 -sS -A 'Mozilla/5.0' 'https://api.crossref.org/works/10.1007/bf02952531' -o /tmp/artin-crossref.json` | 0 | Artin, 1927, title, journal 5(1), pages 353-363, DOI confirmed; response SHA-256 `723ef6d072aae8adc20b803479c5ccdd16a4c339e5e7802bec8b061e16b86c5c` |
| `curl -L --fail --max-time 30 -sS -A 'Mozilla/5.0' 'https://doi.org/10.1007/bf02952531' -o /tmp/artin-doi.html` | 0 | publisher metadata confirmed; page offered paid access, so article text was not inspected |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision `8a178386...eea95`; tree `bdc39a31...c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...85b1d2` and `321626c8...d81`, as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake 5.0.0; no update, build, clone, or fetch was run |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0015/IntakeProbe.lean)` | 0 | eight pinned number-field, adele, class-group, abelian-Galois, and quotient APIs elaborated; complete stdout SHA-256 `5fa6b62838bcc702800275a704a5fa482a127400fb2209fb0577831a7df19007`; no target theorem stated |
| `rg -n -i --glob '*.lean' 'Artin[ _-]*reciprocity\|global[ _-]*reciprocity\|class[ _-]*field[ _-]*theory' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | only a comment link to an external local-CFT project matched; no terminal Artin reciprocity declaration found in this bounded search |
| `python3 -m json.tool Stage1_Instances/THM-M-0015/instance.json`; same command for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0015-pycache python3 -m py_compile Stage1_Instances/THM-M-0015/check_intake.py` | 0 | scoped validator compiles without generated files under the owned path |
| `python3 Stage1_Instances/THM-M-0015/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R3 boundary, null formal target, exact artifact inventory, packet, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-0015/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0015` | 1 (expected no match) | no prohibited Lean proof escape or declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and `.stage1-worker-selftest.json` | 0 after interpreting new-file exit 1 | no whitespace diagnostics; each exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0015 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0015-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source and encoding selection, independent
review, canonical Lean elaboration and mutation tests, formal-anchor and discovery audits,
obligation and typed-graph freezes, proof, composition, trust closure, hermetic replay,
deterministic release evidence, and independent verification remain open. They prevent theorem
completion but do not invalidate the self-tested intake.

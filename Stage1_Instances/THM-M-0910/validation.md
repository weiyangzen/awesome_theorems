# THM-M-0910 intake validation

Validation covers only the `planned` intake for `S56-M-0910-INTAKE`. The automation-provided
`Formalizations/Lean/.lake` symlink and canonical pinned artifacts were used read-only. No
`lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was run.

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44`

Base tree: `050ab5c6392560337051d2eadd1b82277dbe1c4f`

Pinned Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`

Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`

## Source boundary

The catalog contains only `Caucal定理`, Didier Caucal, 1996, and `图的可判定性`. Temporary source
inspection located the matching ICALP 1996 publication and a separate IRISA-hosted expanded
manuscript of unresolved exact version/date. Multiple
candidate nodes were observed, including Proposition 2.5 and Corollaries 2.8 and 3.7; they are not
interchangeable. No source node or edition was selected or admitted, and no corrections/errata or
independent-review gate passed. The root therefore remains the unstable catalog gloss at `H5`, not
a source-selected theorem at `H1` or `H0`.

## Commands and results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0910` | 0 | rank 1452; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided `?? Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6656,6661 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `tmp=$(mktemp --suffix=.ps.gz); curl -L --fail --silent --show-error -o "$tmp" ftp://ftp.irisa.fr/local/caucal/monadic.ps.gz; gzip -cd "$tmp" > "${tmp%.gz}"; ps2pdf "${tmp%.gz}" "${tmp%.ps.gz}.pdf"; pdfinfo "${tmp%.ps.gz}.pdf"; pdftotext -layout "${tmp%.ps.gz}.pdf" -; sha256sum "$tmp" "${tmp%.gz}"; wc -c "$tmp"; rm -f "$tmp" "${tmp%.gz}" "${tmp%.ps.gz}.pdf"` | 0 | 188,268-byte gzip SHA-256 `601c0129...d8f`; decompressed PostScript SHA-256 `fce643da...d5e`; 50-page temporary projection and candidate nodes inspected; no source retained or dependency installed |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.1007%2F3-540-61440-0_128` | 0 | 1996 ICALP author, title, venue, year, pages, and DOI metadata confirmed |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1016%2FS0304-3975(01)00089-5'` | 0 | 2003 same-title TCS metadata confirmed; publication relationship remains unverified |
| `curl -L --fail --silent --show-error https://api.core.ac.uk/v3/outputs/24312769` | 0 | indexed abstract and IRISA FTP URL inspected as discovery evidence; no H0 credit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree shown above; mathlib source worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0910/IntakeProbe.lean)` | 0 | eleven adjacent first-order graph/model-theory, DFA/regular-language, and computability interfaces elaborated; 889 bytes; combined output SHA-256 `843c8da1...927`; no target or proof declared |
| `rg -n -i 'Caucal|REC_Rat|prefix-recognizable|decidable monadic|monadic theory' Formalizations/Lean Stage1_Instances --glob '*.lean' --glob '!.lake/build/**'` | 1 (expected no match) | no exact-topic theorem under the recorded patterns; not a complete anchor audit or external absence claim |
| `python3 -m json.tool` on structured owned artifacts and worker packet | 0 | all JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0910-pycache python3 -m py_compile Stage1_Instances/THM-M-0910/check_intake.py` | 0 | scoped validator compiled without writing under the owned path |
| `python3 -B Stage1_Instances/THM-M-0910/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, authority hashes, planned H5/M4/R4 boundary, null formal target, artifact hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0910/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null FILE` and scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 was accepted only when it represented a clean new-file diff |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0910-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
graph/MSO/effectivity design, canonical Lean elaboration and mutations, formal anchor audit,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay, deterministic
release bundle, and independent verification remain open. These failures prevent statement,
audit-completion, and theorem-completion claims but do not invalidate the planned intake.

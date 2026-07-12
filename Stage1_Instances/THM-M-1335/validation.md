# Intake validation

Base revision: `85da7777da7cc5104d4bc4eaa1d947b8137ca5f5`; base tree:
`ae4ad4de219b61476e1ed10c008e8139247b9d77`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, an authoritative source-family inspection, JSON and scoped invariants, a narrow pinned
Lean substrate probe, bounded name search, prohibited-construct hygiene, and whitespace. It does
not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The author-hosted preliminary edition of Gerald Teschl's *Ordinary Differential Equations and
Dynamical Systems* was retrieved to `/tmp`, hashed, and inspected at printed pages 36 and 50-54.
Theorem 2.13, Lemma 2.14, Corollaries 2.15-2.16, and Theorem 2.17 demonstrate that the catalog gloss
can denote several inequivalent results. Crossref metadata for the AMS monograph was also checked.
No downloaded file was added to the repository. The catalog does not cite this source, and no
historical genealogy, complete errata audit, or independent H0 source review is claimed.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1335` | 0 | rank 946; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 9740,9745 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '9740,9745p' Docs/researches/math_theorems.md \| sha256sum` | 0 | excerpt SHA-256 `1fdf5733aa1bbeddd6674c6568b249a28dab483626ff5886464339013f1fcb27` |
| `curl -L --fail --max-time 45 -A 'Mozilla/5.0' -sS 'https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf' -o /tmp/teschl-ode.pdf` | 0 | retrieved the author-hosted AMS-permitted preliminary edition outside the repository |
| `file /tmp/teschl-ode.pdf` | 0 | PDF document, version 1.4 |
| `wc -c /tmp/teschl-ode.pdf` | 0 | 4,133,331 bytes |
| `pdfinfo /tmp/teschl-ode.pdf` | 0 | 364 pages; title Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems* |
| `pdftotext -layout /tmp/teschl-ode.pdf /tmp/teschl-ode.txt` | 0 | text extraction completed |
| `sed -n '2261,2365p' /tmp/teschl-ode.txt > /tmp/thm-m-1335-source-setup.txt` | 0 | extracted 105 lines containing the IVP and Picard-Lindelof setup |
| `sed -n '3039,3188p' /tmp/teschl-ode.txt > /tmp/thm-m-1335-source-continuation.txt` | 0 | extracted 150 lines containing the separate Section 2.6 candidate results |
| `sha256sum /tmp/thm-m-1335-source-setup.txt /tmp/thm-m-1335-source-continuation.txt` | 0 | extract hashes `c9578760...635f` and `d2ce15c7...3677`; the mutable remote PDF itself is not admitted as an immutable source |
| `rg -n 'Theorem 2\.13\|Lemma 2\.14\|Corollary 2\.15\|Corollary 2\.16\|Theorem 2\.17' /tmp/thm-m-1335-source-continuation.txt` | 0 | located all five distinct maximal-solution, extension, compact-continuation, compact-escape, and global-existence statements |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://api.crossref.org/works/10.1090/gsm/140' -o /tmp/teschl-crossref.json`; `jq` metadata inspection; `sha256sum` | 0 | Teschl, AMS Graduate Studies in Mathematics, published 2012, DOI `10.1090/gsm/140`; response SHA-256 `1d7b3155e42a00fefdebecd49635d2b13f6b962eeccafb6ad6838b3e82f6a8f2` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1335/IntakeProbe.lean)` | 0 | eight pinned integral-curve, local-existence, and open-interval/local-uniqueness API checks elaborated; no target theorem stated |
| `rg -n -i --glob '*.lean' 'maximal[ _-]*(ode[ _-]*)?(solution\|interval\|existence)\|ode[ _-]*(solution[ _-]*)?(continuation\|extension)\|compact[ _-]*escape\|blow.?up[ _-]*alternative' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/ODE Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no target-specific maximal-solution, maximal-existence-interval, ODE continuation, compact-escape, or blow-up-alternative declaration found; intake discovery only, not a complete anchor audit or global absence claim |
| `python3 -m json.tool Stage1_Instances/THM-M-1335/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1335/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1335/intake-receipt.json` | 0 | valid JSON after finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1335-pycache python3 -m py_compile Stage1_Instances/THM-M-1335/check_intake.py` | 0 | scoped checker compiles without writing generated files into the owned path |
| `python3 Stage1_Instances/THM-M-1335/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and DAG identity, planned H5/M4/R4 boundary, null target, exact inventory, packet agreement, and six open downstream tasks agree |
| `python3 Stage1_Instances/THM-M-1335/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet and permits authoritative intake state `[ ]` or `[_]` while still requiring no accepted theorem state |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1335` | 1 (expected no match) | no prohibited proof escape or declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and `.stage1-worker-selftest.json` | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1335 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-1335-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay, deterministic
release bundle, and independent verification remain open. These failures prevent statement,
audit-completion, and theorem-completion claims, but they do not invalidate the planned intake.

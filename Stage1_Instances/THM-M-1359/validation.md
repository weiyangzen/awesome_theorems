# Intake validation

Base revision: `9898aa12e1dd435f018a54a6266ec411ed09a26a`; base tree:
`c0abfcd8c20a1be4b894a7664746d02086072b9d`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, bounded repository/mathlib discovery, prohibited-construct hygiene, and whitespace. It does
not validate a canonical saddle-node statement or proof because the catalog does not identify one.
The structured recipes record a denied-network policy for master replay; this inherited worker run
did not independently enforce network isolation and is explicitly nonhermetic evidence.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The author-hosted preliminary edition of Gerald Teschl's *Ordinary Differential Equations and
Dynamical Systems* was inspected as a temporary worker input. Section 6.5, printed page 200 (PDF
page 211), presents equation (6.33), `x' = mu + x^2`, as a prototypical saddle-node example and
states the necessary implicit-function degeneracy condition. It does not give the general theorem
or select the catalog target.

The reacquisition locators are the author page
`https://www.mat.univie.ac.at/~gerald/ftp/book-ode/index.html`, the linked preliminary text
`https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf`, and the linked errata
`https://www.mat.univie.ac.at/~gerald/ftp/book-ode/errata.pdf`. These mutable URLs are discovery
locators only; future source admission must reacquire and rehash them rather than assume identity.

The PDF had 4,133,331 bytes and SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`.
`pdftotext -f 211 -l 211 -layout <temporary-source-pdf> - | sed -n '1,21p'` produced a 1,553-byte
passage with SHA-256 `8c2019a0410b2edefb2a2242736e4c77480916b3941865f7c45261713578fd8d`.
The author-linked errata PDF had SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`; a bounded search found no
entry naming page 200, equation (6.33), saddle-node, or bifurcation. These mutable remote inputs were
not added to the repository and are not an immutable H0 packet. Complete source, proof-boundary,
errata, historical, and independent reviews remain open.

## Environment

- Linux `7.0.0-27-generic`, `x86_64`; timezone `Asia/Shanghai`.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1359` | 0 | rank 969; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 9908,9913 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `pdftotext -f 211 -l 211 -layout <temporary-source-pdf> - \| sed -n '1,21p'` | 0 | external discovery input; 1,553 bytes; passage SHA-256 `8c2019a...78fd8d` |
| bounded exact-topic search of the extracted current errata | 1 (expected no match) | no page-200, equation-(6.33), saddle-node, or bifurcation entry; not a complete errata audit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no dependency-mutating operation run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | pinned hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1359/IntakeProbe.lean)` | 0 | nine adjacent generic APIs elaborated; complete output SHA-256 `5abe81de...a00474c`; no target theorem declared |
| `rg -n -i --glob '*.lean' 'bifurcat\|saddle.?node\|fold bifurcation' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no exact-topic declaration; bounded intake discovery only, not an exhaustive external audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=<temporary-cache> python3 -m py_compile Stage1_Instances/THM-M-1359/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1359/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source pins, null target, H5/M4/R4 boundary, exact artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1359/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| `rg -n -i 'sorry\|admit\|sorryax\|axiom\|constant\|opaque\|unsafe\|placeholder\|fake result' Stage1_Instances/THM-M-1359 --glob '*.lean'` | 1 (expected no match) | no prohibited declaration or proof escape in the discovery-only Lean probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 per new file means only that content differs from `/dev/null` |
| `git diff --check -- Stage1_Instances/THM-M-1359 .stage1-worker-selftest.json` | 0 | no tracked-diff diagnostics; the preceding no-index checks cover untracked files |

## Status boundary

This is provisional worker self-test evidence for `S56-M-1359-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
canonical Lean elaboration and statement mutations, exhaustive anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay, deterministic
release bundle, and independent verification remain open. These failures prevent statement,
audit-completion, and theorem-completion claims, but they do not invalidate the planned intake.

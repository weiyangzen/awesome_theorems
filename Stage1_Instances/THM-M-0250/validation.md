# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`).

Validation date: 2026-07-13 (Asia/Shanghai). This validation covers target membership, repository
source provenance, the planned dossier and open downstream DAG, JSON and scoped invariants, and a
narrow pinned Lean API probe. Because the source wording is not a proposition, no canonical target,
expression fingerprint, statement mutation, formal anchor, terminal proof body, or proof is
claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It was reused read-only. No `lake update`, `lake build`,
dependency clone or fetch, or `.lake` mutation was performed.

Environment fingerprint:

- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0250` | 0 | rank 1260, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | initial status contained only the pre-existing `.lake` symlink; final status adds only the assigned dossier and authorized root packet |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree recorded above |
| `git blame -L 1801,1806 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 https://api.crossref.org/works/10.1112/plms/s2_14.1.269` | 0 | metadata identifies Hardy's 1915 article, volume, issue, pages, and DOI; response SHA-256 `1c2640497632e9021dae24424f2989ed4a959822a9a459c99c47bd7b2a92e739`; no article text or exact theorem obtained |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `rg -n -i --glob '*.lean' 'Hardy[ _-]?[Ss]pace\|HardySpace\|Hardy space\|Hardy spaces\|Hardy.*H\^p\|H\^p.*Hardy' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match result; no exact Hardy-space-named declaration found in the bounded pinned source search |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0250/IntakeProbe.lean` | 0 | all six adjacent pinned interfaces elaborated; no Hardy-space target or proof credit asserted |
| `python3 -m json.tool` on all structured dossier artifacts and the root packet | 0 | every artifact parsed as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0250-pycache python3 -m py_compile Stage1_Instances/THM-M-0250/check_intake.py` | 0 | scoped checker compiled outside the repository |
| `python3 -B Stage1_Instances/THM-M-0250/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, H5/M4/R4 boundary, null target, source and dependency hashes, artifact inventory, packet, and six open tasks agreed |
| `python3 -B Stage1_Instances/THM-M-0250/check_intake.py` | 0 | public replay passed without depending on the worker handoff |
| `rg -n --pcre2 --glob '*.lean' '\b(?:sorry\|admit\|sorryAx)\b\|^\s*(?:axiom\|constant\|opaque)\s+\|^\s*unsafe\b' Stage1_Instances/THM-M-0250` | 1 | expected no-match result; the API-only probe contains no prohibited proof escape or bodyless declaration |
| scoped per-file `git diff --no-index --check` and `git diff --check -- Stage1_Instances/THM-M-0250 .stage1-worker-selftest.json` | 0 | no whitespace errors; the checker also validates final newlines and bytes |

Known downstream failures remain deliberately open: immutable primary or authoritative source text,
an exact proposition and incorporated definitions, assumption/proof/errata mapping and independent
review; exact Lean elaboration, transports and mutations; immutable formal-candidate and terminal
body audit; discovery and obligation freezes; typed graphs; proof and composition; readable
reconstruction; hermetic replay; deterministic evidence bundle; independent verification; and
master acceptance. They prevent statement execution, audit completion, and theorem completion but
do not invalidate this truthful `planned` intake.

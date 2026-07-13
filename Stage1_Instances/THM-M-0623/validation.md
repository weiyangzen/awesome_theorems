# Intake validation

Base revision: `5bc32428da3d17f138ceca67f30fbc2d149da1ba` (tree
`7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f`). Validation ran on 2026-07-13 in the
isolated worker clone.

Validation is limited to target-set consistency, planned-dossier structure, scope and
non-substitution invariants, repository and bibliographic provenance, pinned environment identity,
a narrow Lean exact-topic candidate and axiom probe, bounded source inspection, proof-escape
hygiene, JSON integrity, and whitespace. Because the historical regularity convention and exact
source-to-Lean transport are not accepted, no canonical target, expression fingerprint, statement
mutation, source closure, or root proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux `x86_64`, kernel `7.0.0-27-generic`, timezone `Asia/Shanghai`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Python: `3.14.4`; Git: `2.53.0`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned Urysohn source SHA-256:
  `f3ff7368d39fdff7848c7a9c696be962a0347dc9043ae4b658e66430e300feb0`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0623` | 0 | rank 1317, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 4622,4627 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa...b74f` |
| `curl -LfsS --max-time 30 https://api.crossref.org/works/10.1007/BF01208661 -o /tmp/urysohn-crossref-doi.json` | 0 | metadata identifies Paul Urysohn, *Mathematische Annalen* 94(1), 1925, pages 309-315, DOI `10.1007/BF01208661`; retrieved payload SHA-256 `fa259d8f...e47` |
| `curl -LfsS --max-time 30 https://link.springer.com/article/10.1007/BF01208661 -o /tmp/urysohn-publisher.html` | 0 | article-page response was 215669 bytes with SHA-256 `e6042576...bd0d`; metadata confirmed citation and received/issue dates |
| `curl -LfsS --max-time 30 https://link.springer.com/content/pdf/10.1007/BF01208661.pdf -o /tmp/urysohn-pdf-response.html` | 0 | response was an HTML access page, 215635 bytes with SHA-256 `f2d302d3...c179`; no primary theorem text was added or credited |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision/tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; package worktree clean |
| exact bounded `rg` over the pinned Urysohn, Regular, and Metrizable sources | 0 | bare regularity excludes T0 and yields pseudometrizability; T3 is regular plus T0 and yields full metrizability |
| exact pinned `git log --all --reverse -S...` history query recorded in the receipt | 0 | current split-file origin `442eef6f...e1`; original Lean 4 port of the full metric candidate `94a92f15...b55` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0623/IntakeProbe.lean)` | 0 | eleven interfaces and four two-point-indiscrete boundary examples elaborated; both exact-topic candidates report axioms `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `0af3b056...aa4e` |
| the four exact `python3 -m json.tool <path>` commands listed in `.stage1-worker-selftest.json` | 0 | all JSON documents parse after finalization |
| Python `ast.parse` and isolated `py_compile` on `check_intake.py` | 0 | validator parses and compiles without creating files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0623/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H1/M3/R4 boundary, null target, source and pin hashes, exact inventory, receipt/packet agreement, and six open tasks agree |
| exact prohibited-declaration scan shown below | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0623 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace diagnostics in changed files |

## Known downstream failures

- No lawful immutable primary theorem passage is accepted and independently reviewed with the
  source definition of regularity, assumptions, conclusion, proof boundary, translation,
  corrections, and errata.
- The separation convention, metric-versus-pseudometric meaning, canonical binder form, exact
  compatible-structure encoding, attribution/version boundary, and degenerate cases remain open.
- The pinned pseudometric and metric candidates are strong exact-topic artifacts, but no source
  transport, canonical expression/environment fingerprint, checked alternate encoding, or four
  statement mutation classes exist.
- Exhaustive anchor and terminal-body provenance audits, discovery protocol, obligation registry,
  typed graphs, proof/composition credit, readable reconstruction, hermetic replay, deterministic
  bundle, independent release verification, and master acceptance remain open.

These failures prevent statement, source-fidelity, proof, audit-completion, and theorem-completion
claims. They do not invalidate a truthful, self-tested `planned` intake whose purpose is to freeze
the convention boundary and open the downstream DAG. Only the integration lane may accept the
provisional worker receipt.

The exact proof-escape scan was:

```bash
rg -n --glob '*.lean' '(^|[^[:alnum:]_])(sorry|admit|sorryAx)([^[:alnum:]_]|$)|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' Stage1_Instances/THM-M-0623
```

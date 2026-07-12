# Intake validation

Base revision: `95073b656f2c285c788e4814325a47fdb4dc1879`.

Validation date: `2026-07-12` (`Asia/Shanghai`). This evidence covers manifest membership, the
planned dossier and open-DAG invariants, JSON integrity, a narrow elaboration probe against pinned
recurrence APIs, the bounded formal-name search, prohibited-construct hygiene, and whitespace. It
does not freeze or prove a canonical Kakutani statement.

The preflight worktree contained the existing untracked shared link `Formalizations/Lean/.lake`,
which points to the canonical checkout's pinned artifacts. It was used read-only and is not a
changed path. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was
run. This is worker-local, dirty/nonrelease evidence.

Environment fingerprint:

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Inspected J-STAGE primary PDF SHA-256:
  `054e0d2296324bec6f0b319bcb9aea5044a72b941f3dd83b75b788968320b16b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1409` | 0 | rank 908; planned; L0/rework_required; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` | 0 | before editing, only the pre-existing untracked `Formalizations/Lean/.lake` link was present |
| `cd Formalizations/Lean && lake env lean --version && lake --version && sha256sum lean-toolchain lake-manifest.json && git -C .lake/packages/mathlib rev-parse HEAD && git -C .lake/packages/mathlib status --short` | 0 | versions, file hashes, and pinned mathlib revision agree with the fingerprint; package worktree status was empty |
| `curl -L --fail --silent --show-error --max-time 30 <J-STAGE-article-URL> \| rg -n -i 'Induced Measure\|Kakutani\|635\|641\|1943\|10\\.3792\|citation_' \| head -n 160` | 0 | J-STAGE metadata reported Kakutani, title, 1943, volume 19 issue 10, pages 635-641, DOI, and the PDF locator |
| `tmp=$(mktemp); curl -L --fail --silent --show-error --max-time 30 <J-STAGE-PDF-URL> -o "$tmp"; sha256sum "$tmp"; wc -c "$tmp"; pdfinfo "$tmp"; rm -f "$tmp"` | 0 | retrieved 717145-byte, seven-page PDF with the recorded SHA-256; temporary copy removed |
| `tmp=$(mktemp); curl -L --fail --silent --show-error --max-time 30 <J-STAGE-PDF-URL> -o "$tmp"; pdftotext -f 1 -l 3 -layout "$tmp" -; rm -f "$tmp"` | 0 | inspected Sections 1-3, historical measure/strong/weak definitions, Lemmas 1-2, construction, and finite-measure footnote |
| `python3 -m json.tool Stage1_Instances/THM-M-1409/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1409/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1409/intake-receipt.json` | 0 | valid JSON after receipt finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after self-test finalization |
| `python3 Stage1_Instances/THM-M-1409/check_intake.py` | 0 | persistent dossier/manifest/DAG/source invariants pass without depending on ephemeral worker metadata |
| `python3 Stage1_Instances/THM-M-1409/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | worker packet identity, base, complete owned artifact inventory, and `[_]` state also agree |
| `python3 -m py_compile Stage1_Instances/THM-M-1409/check_intake.py` | 0 | intake invariant checker is syntactically valid; the generated `__pycache__` was removed and is not an artifact |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1409/IntakeProbe.lean` | 0 | six pinned measure-preserving/conservative recurrence interfaces elaborated and printed with exact types |
| `rg -n -i 'Kakutani tower\|Kakutani skyscraper\|induced measure preserving\|induced transformation\|return time\|first return map\|first-return' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/PFun.lean --glob '*.lean'` | 0 | no ergodic Kakutani/induced-transformation anchor; only generic partial-function `PFun.fix` matched "first return map" |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-1409 --glob '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom declaration in the target Lean source |
| `git diff --check -- Stage1_Instances/THM-M-1409 .stage1-worker-selftest.json` | 0 | no whitespace errors |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-1409/*; do git diff --no-index --check -- /dev/null "$f" >/dev/null; code=$?; test "$code" -le 1 \|\| exit "$code"; done` | 0 | all nine owned files and the worker self-test had only expected added-content differences and no whitespace-error exit greater than 1 |

The first failed downstream gate is the exact-statement gate. The primary paper's Section 3
locates a likely node family, but the catalog does not decide whether its root is return existence,
the least-return construction, strong-sense preservation/ergodicity, the weak-sense induced map, or
a combined theorem. Strong/weak definitions, null-set representatives, measure hypotheses, source
proof boundary, errata, and independent review remain open. Consequently the canonical Lean
expression and fingerprint, transports, mutation tests, discovery/obligation hashes, formal-anchor
audit, proof tree, proof, hermetic replay, and independent release validation also remain open.
Those failures prevent statement, audit, and theorem completion but do not invalidate this
truthful, self-tested `planned` intake.

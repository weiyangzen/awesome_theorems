# Intake validation

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44`; base tree:
`050ab5c6392560337051d2eadd1b82277dbe1c4f`.

This validation covers target membership, the planned dossier and open task DAG, exact repository
source provenance, neighbor-target and non-substitution boundaries, structured intake invariants,
a narrow pinned Lean substrate probe, bounded local search, prohibited-construct hygiene, and
whitespace. It does not validate a canonical theorem statement or proof because the catalog does
not supply one.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; the package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0906` | 0 | rank 1448; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6628,6633 -- Docs/researches/math_theorems.md` | 0 | all six uncited target catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 -A 'Mozilla/5.0 (Stage1 intake research)' 'https://encyclopediaofmath.org/wiki/Graph_colouring' -o /tmp/thm-m-0906-eom-graph-colouring.html` | 0 | mutable secondary overview fetched to `/tmp`; observed SHA-256 `36b2447b88a5b1c84513a73bee2fc885e1886db3ee541bf3837f2545c0298115`; nonselective E5 discovery only, with no source credit |
| `curl -L --fail --silent --show-error --max-time 30 -A 'Mozilla/5.0 (Stage1 intake research)' 'https://en.wikipedia.org/api/rest_v1/page/html/List_coloring' -o /tmp/thm-m-0906-list-coloring.html` | 28 | request timed out; no output admitted or credited and no effect on the intake conclusion |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at the commit above on x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree shown above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0906/IntakeProbe.lean)` | 0 | eight ordinary-coloring, chromatic-number, and finite-set APIs elaborated; output SHA-256 `e8fa74d4770eedf1237f569d6d2530da03b8269b14813e641c3c5391c38f1882`; no target declared |
| bounded `rg` search for list coloring, choosability, choice number, or list chromatic declarations in pinned mathlib and `Formalizations/Lean` | 1, expected no match | no target declaration located in that stated scope; ordinary coloring substrate was separately inspected; not an exhaustive repository or external anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0906-pycache python3 -m py_compile Stage1_Instances/THM-M-0906/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 Stage1_Instances/THM-M-0906/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authoritative target and DAG identity, planned H5/M4/R4 boundary, null target, exact artifact inventory, packet, input pins, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-0906/check_intake.py` | 0 | repository replay mode passes without the scheduler-only packet; it verifies the recorded base object rather than requiring current HEAD to remain at the worker base |
| `if rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0906; then exit 2; else printf 'no prohibited Lean declarations\n'; fi` | 0 | inner `rg` returned expected no-match exit 1; no prohibited declaration in the API-only probe |
| exact ten-path shell loop recorded in `intake-receipt.json`: capture `git diff --no-index --check /dev/null "$path"` diagnostics for every owned file and the packet, require them empty, then run `git diff --check -- Stage1_Instances/THM-M-0906 .stage1-worker-selftest.json` | 0 aggregate | no whitespace diagnostics; each ignored no-index status 1 was only the expected new-file difference |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0906-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. An immutable exact source and independent review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof and composition, trust closure, readable reconstruction,
hermetic replay, deterministic release bundle, and independent verification remain open. These
failures prevent statement, audit-completion, and theorem-completion claims, but they do not
invalidate the self-tested planned intake.

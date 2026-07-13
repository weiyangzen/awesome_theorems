# Intake validation

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54`; base tree:
`fb2cfc62077d5b53e9938632cd6361dd60872067`. Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and all-open downstream DAG,
catalog/source provenance, variant and neighbor boundaries, JSON and scoped invariants, and a
narrow pinned Lean substrate probe. It does not validate a canonical theorem statement or claim
proof credit, because the catalog has not selected an exact jump-inversion proposition. The initial
worktree contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink. It
was used read-only; no update, build, clone, fetch, or other dependency mutation was performed.
This dirty worker evidence is nonrelease evidence.

## Source discovery boundary

An immutable Encyclopedia of Mathematics revision was retrieved through its canonical MediaWiki
API revision query, inspected, and hashed. It states the conventional range result: every degree
`a >= 0'` equals `b'` for some degree `b`, and cites general books by Rogers, Shoenfield, and Sacks.
It does not pinpoint the primary theorem or proof. No referenced book was inspected, no primary
source was accepted, and no H0 or variant-identity claim is made. The API response is external
source input, not a public dossier artifact; its exact URL, revision, byte count, digest, and replay
command below make that boundary reproducible.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `TuringDegree.lean` SHA-256:
  `d5fd0caf5c321343ec378e2601913aec152efac58f113ce3b602dca7345b1e5c`.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0753` | 0 | rank 1339; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 5549,5554 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '5514,5568p' Docs/researches/math_theorems.md`; `sed -n '20530,20625p' Docs/Stage0_Blueprint.md`; `jq '.targets[] \| select(.theorem_id == "THM-M-0753")' Docs/Stage1_Targets_rev-5.6.json` | 0 each | confirmed the sparse image-of-jump gloss, separate degree/jump/hierarchy neighbors, and uniform L0 boundary |
| `curl -L --fail --max-time 30 -sS 'https://encyclopediaofmath.org/api.php?action=query&prop=revisions&revids=46619&rvprop=ids%7Ctimestamp%7Ccontent&rvslots=main&format=json&formatversion=2' -o /tmp/thm-m-0753-eom-rev46619.json`; `wc -c /tmp/thm-m-0753-eom-rev46619.json`; `sha256sum /tmp/thm-m-0753-eom-rev46619.json`; `jq -r '.query.pages[0].revisions[0].slots.main.content' /tmp/thm-m-0753-eom-rev46619.json \| rg -n -C 3 'For every degree|References|Rogers|Shoenfield|Sacks'` | 0 each | immutable revision replayed as 6,850 bytes with SHA-256 `547f7674...1224`; conventional `a >= 0'` inversion direction observed; no primary proof or H0 credit |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/Computability/TuringDegree.lean'` | 0 | pinned revision, tree, and source blob `e321ed033ccef4c29c9611e4d27e58116c021544` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | empty output; dependency worktree remained clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/TuringDegree.lean` | 0 | hashes recorded above |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0753/IntakeProbe.lean)` | 0 | recursive-in, Turing reducibility/equivalence/degree/order, reflexivity, and transitivity declarations elaborated; no jump or target declared |
| `rg -n -i --glob '*.lean' 'Turing[ _-]*jump\|jump[ _-]*inversion\|Friedberg.*jump\|turingJump\|turing_jump' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no named target definition/declaration found; intake discovery only, not exhaustive anchor audit |
| `for f in Stage1_Instances/THM-M-0753/*.json .stage1-worker-selftest.json; do python3 -m json.tool "$f" >/dev/null \|\| exit; done` | 0 | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0753-pycache python3 -m py_compile Stage1_Instances/THM-M-0753/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0753/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, planned lifecycle, null target, H1/M4/R4 boundary, source/formal inventories, receipt packet, exact artifact inventory, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0753/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0753` | 1 (expected no match) | no prohibited proof escape or declaration |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0753/*; do out=$(git diff --no-index --check /dev/null "$f" 2>&1) && code=0 \|\| code=$?; test "$code" -eq 1 && test -z "$out" \|\| exit 1; done`; `git diff --check -- Stage1_Instances/THM-M-0753 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; no-index exit 1 was accepted only as the expected new-file difference with empty diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0753-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact primary-source selection and independent
review, theorem-variant and neighbor reconciliation, canonical Lean elaboration and mutation tests,
anchor audit, discovery and obligation freezes, typed graphs, proof and composition provenance,
trust closure, readable reconstruction, hermetic replay, deterministic release bundle, independent
verification, and master acceptance remain open. These gates prevent theorem completion but do not
invalidate the planned intake.

# Intake validation

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800`; base tree:
`400e6edf1f69b971b60a367e3ea29be359b07907`. Validation date: 2026-07-13
(Asia/Shanghai). The complete final replay ran from `16:41:58+08:00` through `16:42:18+08:00`.

This validation covers target membership, the planned dossier and all-open downstream DAG,
catalog/source provenance, formulation and neighbor boundaries, JSON and scoped invariants, and a
narrow pinned Lean candidate probe. It does not validate a canonical theorem statement or claim
proof credit because the catalog and admitted sources do not select one exact formulation or decide
ownership relative to the neighboring fixed-point record.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref metadata for Kleene's 1938 paper was retrieved to `/tmp` and hashed. No accepted immutable
copy of the primary article text was obtained, so no primary theorem passage, incorporated
definition, assumption, proof, correction, or erratum was admitted. The immutable Spring 2024
Stanford Encyclopedia of Philosophy article was retrieved to `/tmp`, hashed, and inspected at
Section 3.4. Theorem 3.5 confirms the total-computable natural-index formulation and semantic
program equality; Corollary 3.2 confirms the parameterized partial-computable formulation. This is
strong secondary discovery evidence only. It neither clears H0 nor decides ownership among
`THM-M-0742`, `THM-M-0743`, and `THM-C-0006`.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `PartrecCode.lean` SHA-256:
  `543fdfc34bbc62e0d2bdff524be58e58abdd4ebded0ca25fac7edf791aadb2df`.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0742` | 0 | rank 1330; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 5472,5477 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of the catalog, Stage0 projection, adjacent targets, and outside-scope `THM-C-0006` | 0 | confirmed sparse self-reference wording, distinct fixed-point/s-m-n rows, outside-scope duplicate name, and unresolved ownership |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://api.crossref.org/works/10.2307/2267778' -o /tmp/thm-m-0742-kleene-crossref.json` | 0 | Crossref identifies Kleene, *On notation for ordinal numbers*, JSL 3(4), 1938, pages 150-155; response SHA-256 `55a07514...83cc`; metadata only |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://plato.stanford.edu/archives/spr2024/entries/recursive-functions/' -o /tmp/thm-m-0742-sep-spr2024.html` | 0 | immutable secondary archive retrieved; 299,572 bytes; SHA-256 `7d856ecd...af1` |
| `rg` inspection of SEP Theorem 3.5, its fixed-point warning, and Corollary 3.2 | 0 | confirmed total-transformer and parameterized forms, semantic equality, and explicit rejection of literal `f(n)=n` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/Computability/PartrecCode.lean'` | 0 | pinned revision, tree, and source blob `6a5a8cd7a1819f65ca068a13e8216714fa9c9401` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | empty output; dependency worktree remained clean |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no update or build run |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0742/IntakeProbe.lean)` | 0 | code/evaluator, computability, s-m-n, `fixed_point`, and `fixed_point₂` types elaborated; both candidates reported `propext`, `Classical.choice`, and `Quot.sound`; stdout 900 bytes/10 lines, SHA-256 `166ccdfc...adb4`; no target or wrapper declared |
| bounded recursion/fixed-point exact-topic `rg` search in repo-local Lean | 1 (expected no match) | no repo-local exact target artifact found; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `python3 -B Stage1_Instances/THM-M-0742/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, planned lifecycle, null target, H1/M4/R4 boundary, candidates, neighbors, source hashes, packet, exact inventory, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0742/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null FILE`, then scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 was accepted only for clean new-file differences |

## Known open gates

An accepted immutable primary or approved authoritative source, exact result and incorporated
definitions, complete premise/conclusion/proof-boundary and correction crosswalk, neighboring target
ownership decision, and independent source review remain open. So do the canonical Lean target and
minimal imports, expression/environment fingerprints, checked transports, four statement mutation
classes, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion.

These failures block the downstream statement phase but do not invalidate a truthful, self-tested
`planned` intake. The provisional root vector `[H1, M4, R4]` gives no proof credit.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0742-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.

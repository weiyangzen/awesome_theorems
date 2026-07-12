# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`. Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and all-open downstream DAG,
catalog/source provenance, variant and neighbor boundaries, JSON and scoped invariants, and a
narrow pinned Lean candidate probe. It does not validate a canonical theorem statement or claim
proof credit, because the catalog has not resolved which fixed-point formulation belongs to this
target. The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It was used read-only; no update, build, clone, fetch, or other
dependency mutation was performed. This dirty worker evidence is nonrelease evidence.

## Source discovery boundary

Crossref metadata for Kleene's 1938 paper was retrieved to `/tmp` and hashed. The article text was
not available, so no primary theorem passage or proof was inspected. The immutable Spring 2024
Stanford Encyclopedia of Philosophy article was also retrieved to `/tmp`, hashed, and inspected at
Section 3.4, Theorem 3.5. It confirms the total-computable natural-index formulation and explains
that the "fixed point" is equality of computed partial functions rather than `f n = n`. This is a
strong secondary source lead only; it neither clears H0 nor decides whether that formulation belongs
to `THM-M-0743` rather than `THM-M-0742`.

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
- Pinned `PartrecCode.lean` SHA-256:
  `543fdfc34bbc62e0d2bdff524be58e58abdd4ebded0ca25fac7edf791aadb2df`.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0743` | 0 | rank 1061; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 5479,5484 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of `Docs/researches/math_theorems.md:5472-5491`, `Docs/Stage0_Blueprint.md:20272-20324`, `Docs/researches/cs_theorems.md:28`, and the target manifest | 0 | confirmed the sparse target wording, separate recursion/s-m-n neighbors, outside-scope duplicate gloss, and uniform L0 boundary |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://api.crossref.org/works/10.2307/2267778' -o /tmp/thm-m-0743-kleene-crossref.json` | 0 | Crossref response identifies Kleene, *On notation for ordinal numbers*, JSL 3(4), 1938, pages 150-155; response SHA-256 `55a07514...83cc`; metadata only |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://plato.stanford.edu/archives/spr2024/entries/recursive-functions/' -o /tmp/thm-m-0743-sep-spr2024.html` | 0 | immutable secondary-source archive retrieved; 299,572 bytes; SHA-256 `7d856ecd...af1` |
| `rg -n -i -C 5 'Theorem 3\.5\|Fixed Point Theorem\|does not guarantee\|On notation for ordinal numbers' /tmp/thm-m-0743-sep-spr2024.html` | 0 | inspected the total-computable index-transformer statement, semantic-equality warning, and bibliography |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/Computability/PartrecCode.lean'` | 0 | pinned revision, tree, and source blob `6a5a8cd7a1819f65ca068a13e8216714fa9c9401` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | empty output; dependency worktree remained clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/PartrecCode.lean` | 0 | hashes recorded above |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0743/IntakeProbe.lean)` | 0 | code/evaluator, computability, s-m-n, `fixed_point`, and `fixed_point₂` types elaborated; both candidates reported axioms `propext`, `Classical.choice`, `Quot.sound`; no target or wrapper declared |
| `rg -n --glob '*.lean' 'Partrec\.Code\.fixed_point\|Rogers.? fixed-point\|Kleene.?s second recursion' Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no repo-local exact candidate artifact found; bounded intake discovery, not exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0743-pycache python3 -m py_compile Stage1_Instances/THM-M-0743/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0743/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, planned lifecycle, null target, H1/M4/R4 boundary, candidate and neighbor inventories, receipt packet, exact artifact inventory, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0743/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet and permits authoritative intake state `[ ]` or `[_]` |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0743` | 1 (expected no match) | no prohibited Lean proof escape or declaration |
| per-new-file `git diff --no-index --check /dev/null FILE`, then `git diff --check -- Stage1_Instances/THM-M-0743 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; no-index exit 1 for a new file was treated as normal only when output was empty |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0743-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact primary-source selection and independent
review, target identity and neighbor reconciliation, canonical Lean elaboration and mutation tests,
anchor audit, discovery and obligation freezes, typed graphs, proof and composition provenance,
trust closure, readable reconstruction, hermetic replay, deterministic release bundle, independent
verification, and master acceptance remain open. These gates prevent theorem completion but do not
invalidate the planned intake.

# Intake validation

## Result boundary

The planned intake is structurally self-tested. The narrow Lean probe elaborates nine pinned graph
interfaces and does not declare or prove the target. No canonical statement, obligation, proof
body, source-fidelity closure, audit completion, theorem completion, or accepted state is claimed.

The worktree began with only the automation-provided untracked `Formalizations/Lean/.lake` symlink.
It targets the canonical pinned build artifacts and was used read-only. No `lake update`, build,
fetch, clone, package mutation, or other `.lake` write was performed. New owned artifacts and the
root worker packet make the final tree dirty and nonrelease.

## Environment

- Base revision: `444860f481e8bbf64a3357008fd4d01a52006f08`.
- Base tree: `dee24a14497f877ebd81712a99d2da08de62d7ad`.
- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source boundary

The Renyi Institute scan of Erdos and Stone, "On the structure of linear graphs", *Bulletin of
the American Mathematical Society* 52 (1946), 1087-1091, was inspected at PDF SHA-256
`83ae35a7185e2e6462ccc314c3a20c2b6d85fc142a2cc857603fbf9661f550e1`.
Pages 1087-1090 cover the finite theorem, complement restatement, proof, and sharpness example.
OCR damage, exact transcription, epsilon-slack transport, modern fixed-forbidden-graph
equivalence, correction status, complete node mapping, and independent review prevent H0.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless `cwd` says
otherwise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0841` | 0 | rank 1398; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6173,6178 -- Docs/researches/math_theorems.md` | 0 | all six source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 240 --retry 3 --retry-delay 2 -sS https://www.renyi.hu/~p_erdos/1946-08.pdf -o /tmp/erdos-stone-1946.pdf` | 0 | 5-page, 432122-byte PDF; source hash recorded above |
| `pdftotext -layout /tmp/erdos-stone-1946.pdf /tmp/erdos-stone-1946.txt` plus visual page inspection | 0 | extracted-text SHA-256 `525253ccb9e0b855a7c2a58884d86f47af1026946a0a8ba849eb333ddb083de8`; theorem and proof pages crosswalked |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `git -C Formalizations/Lean/.lake/packages/mathlib merge-base --is-ancestor b9df47b72b287802f6d40cf7588dada976bc657d HEAD` | 1 (expected) | later Erdos-Stone commit is not in the pinned history |
| `git -C Formalizations/Lean/.lake/packages/mathlib cat-file -e HEAD:Mathlib/Combinatorics/SimpleGraph/Extremal/ErdosStoneSimonovits.lean` | 128 (expected) | candidate module is absent from the pinned tree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0841/IntakeProbe.lean)` | 0 | nine pinned interfaces elaborated; complete output SHA-256 `73b3bf9cb390ef552f54fe6f89d41bbaf639f602427dcd489b88ee64b7d56d2e`; no target proof credit |
| `python3 -m json.tool` on structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `check_intake.py` | 0 | validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0841/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | planned H1/M3/R4 identity, null target, pins, receipt, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0841/check_intake.py` | 0 | public replay mode passes without scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0841 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; preceding no-index checks cover untracked files |

## Known downstream failures

- The catalog does not choose the original sparse/complement containment statement, the modern
  fixed-`H` chromatic-density formula, or an equivalence package.
- Exact iterated-log syntax, complement tolerance transport, normalization, chromatic-number
  indexing, strictness, coercions, quantifier order, and degenerate cases remain open.
- Exact source transcription, corrections/errata, complete assumption/proof mapping, the modern
  equivalence proof, and independent review remain open.
- No canonical Lean expression, exact minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- The only named Erdos-Stone Lean lead discovered is later than and absent from the pinned tree; it
  is also a minimum-degree fixed-part theorem, not automatically identical to either candidate root.
- Formal candidate/provenance audit, discovery and obligation freezes, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures block statement, audit-completion, and theorem-completion claims. They do not
invalidate this truthful, self-tested `planned` intake. Only the integration lane may accept its
provisional worker receipt.

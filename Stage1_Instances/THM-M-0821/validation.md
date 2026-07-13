# Intake validation

Base revision: `902d9ce008e88a35a2307c85355560a230cc33c2`; base tree:
`dfc20d8141f18f6b09a03e818acfff408e836714`.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, the inspected primary-source statement/proof boundary, JSON and scoped invariants, a
narrow pinned Lean candidate probe, prohibited-construct hygiene, and whitespace. It does not
validate a canonical theorem statement or proof because the catalog does not decide whether
"maximum size" includes only the upper bound, an attaining middle layer, or the complete equality
classification in the primary paper.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

The Goettingen Digitization Centre copy of Emanuel Sperner, *Ein Satz uber Untermengen einer
endlichen Menge*, *Mathematische Zeitschrift* 27 (1928), 544-548, was inspected at PDF SHA-256
`236629931717954288c77d99e487a1ff98c40af2fb29908eb06738ee253bbbde`. Printed page 544 defines the
finite antichain family, states the middle-binomial upper bound, records its middle-layer witnesses,
and classifies equality for even and odd ground-set sizes. Printed pages 545-548 contain the proof.
An accountable translation, complete premise/proof mapping, corrections or errata audit, and
independent review remain open, so this is H1 rather than H0.

The Crossref record for DOI `10.1007/BF01171114` was also inspected at JSON SHA-256
`bbc733df69e609e38875f64569f7f77586f48bff317b772ae39989f0c543bb7a`. It confirms the bibliographic
fields but contains a replacement character in the title and is not used as the exact title source.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0821` | 0 | rank 1379; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6033,6038 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail -sS https://gdz.sub.uni-goettingen.de/download/pdf/PPN266833020_0027/LOG_0034.pdf -o /tmp/thm-m-0821-primary.pdf` | 0 | 6-page, 447376-byte archive PDF; SHA-256 recorded above |
| visual inspection of the five 400-DPI IIIF article-page images | 0 | printed pages 544-548 inspected; page 544 supplies the exact theorem-family and equality split |
| `curl -L --fail -sS https://api.crossref.org/works/10.1007/bf01171114 -o /tmp/thm-m-0821-crossref.json` | 0 | 2314-byte metadata payload; SHA-256 recorded above; title encoding defect noted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0821/IntakeProbe.lean)` | 0 | eight upper-bound-candidate and middle-layer APIs elaborated; complete output SHA-256 recorded in `intake-receipt.json`; no target or proof credit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0821/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0821/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M3/R4 boundary, null target, inventory, source hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0821/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0821 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- An independent source reviewer must verify the primary German statement, translation, inclusion
  convention, binomial/floor notation, equality wording, boundary cases, proof mapping, and errata.
- The root must be selected explicitly among the upper bound, exact maximum with attainability, and
  the primary paper's full equality classification.
- No canonical Lean expression, exact minimal imports, expression/environment fingerprint, checked
  alternate transport, or statement mutation is frozen.
- The pinned upper-bound candidate is not yet source-transported or audited for terminal body,
  provenance, axioms, TCB, placeholders, or exact root closure; equality cases remain absent.
- Discovery and obligation freezes, typed graphs, proof, composition, readable reconstruction,
  hermetic replay, deterministic bundle, independent release verification, and master acceptance
  remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.

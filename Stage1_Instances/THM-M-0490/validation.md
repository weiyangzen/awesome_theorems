# Intake validation

Base revision: `997541734bb32f987fb15f163335a82512992120`; base tree:
`2c866b9d840d48c48ac839740c62d3b9440be0e5`. Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and all-open downstream DAG,
catalog provenance, the primary published consequence and stronger source-theorem boundary, JSON
and scoped invariants, and one narrow pinned Lean statement-substrate probe. It does not validate a
canonical target or any bounded-gap proof. Indexing, liminf/infinitely-often equivalence, gap
domain, casts, subtraction, mutations, and independent source review remain statement-phase work.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It was used read-only. No `lake update`, `lake build`, clone,
fetch, or other dependency mutation was performed. The owned dossier and root worker packet make
the final worktree dirty as expected, so all evidence here is nonrelease worker evidence.

## Source inspection boundary

The publisher's landing page, complete 54-page PDF, and Crossref metadata were retrieved to
`/tmp`, not added to the repository. The abstract and Theorem 1 on journal pages 1121-1122 were
inspected. They identify the exact consecutive-prime strict liminf consequence and the stronger
admissible-tuple proof source. The journal page also records receipt, revision, acceptance, and
publication dates. This supports H1 source reconstruction only: no independent reviewer, complete
proof-node and incorporated-source mapping, correction/errata audit, Chinese-gloss review, or
checked equivalence to a Lean infinitude predicate exists.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree remained clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `PrimeCounting.lean` SHA-256:
  `ab721488feeb7d0e5668758e29e0ca20543e16e738f80b632c5cabe9e949ff25`.
- The successful Lean probe combined-output SHA-256 is
  `e3f281515b7acbbf05e6653544c9f65160841085a55293cfc6225d2ff8506078`.

## Commands and results

All commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0490` | 0 | rank 1367; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 3595,3600 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of the catalog, Stage0 projection, target manifest, authoritative blueprint, skill, and execution DAG | 0 | confirmed the sparse catalog, planned L0 target, and exact intake ownership |
| `curl -L --fail --silent --show-error https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n3-p07-p.pdf -o /tmp/zhang.pdf` | 0 | publisher PDF retrieved; 621,946 bytes; SHA-256 `231a33cf...a1` |
| `pdftotext -f 1 -l 5 -layout /tmp/zhang.pdf /tmp/zhang.txt` and inspection | 0 | abstract and Theorem 1 identify consecutive gaps, strict bound, admissible-tuple source, and consequence; no H0 credited |
| publisher landing-page and Crossref retrieval for DOI `10.4007/annals.2014.179.3.7` | 0 | title, author, volume, issue, pages, DOI, dates, and PDF link cross-checked; response hashes recorded |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/NumberTheory/PrimeCounting.lean'` | 0 | pinned revision, tree, and source blob recorded |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | empty output; pinned dependency remained clean |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no update or build run |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0490/IntakeProbe.lean)` | 0 | six pinned APIs, two adjacent facts, and the prospective proposition type elaborated; no target theorem or proof declared |
| bounded case-insensitive `rg` for Zhang, bounded/prime gaps, the DOI, and `70000000` over repo-local Lean and pinned mathlib | 1 (expected no match) | no target-specific Lean declaration located; bounded intake fact, not an exhaustive external audit |
| `python3 -m json.tool` on all structured intake records and `.stage1-worker-selftest.json` | 0 each | all JSON valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0490-pycache python3 -m py_compile Stage1_Instances/THM-M-0490/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0490/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, pins, source hashes, null target, H1/M4/R4 boundary, inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0490/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-0490` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null FILE`, then scoped `git diff --check` | 0 | no whitespace diagnostics; no-index status 1 for each new file was accepted only with empty diagnostic output |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0490-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Independent source and correction review, exact
Lean statement and transports, environment/expression fingerprints, four statement mutations,
exhaustive formal discovery, obligation freeze and typed graphs, proof/composition provenance,
trust closure, readable reconstruction, hermetic replay, deterministic evidence, independent
verification, and master acceptance remain open. These gates prevent audit or theorem completion
but do not invalidate the planned intake.

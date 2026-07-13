# Intake validation

Base revision: `f294137feee7840fd105a4d3f6073d5cf45508ea`; base tree:
`234b8f273d252c2c42ce6860315ed973049c871a`.

Validation ran on 2026-07-13 (Asia/Shanghai) in the isolated worker clone. It covers target
membership, the planned dossier and open task DAG, repository provenance, inspected source
boundaries, JSON and scoped invariants, a narrow pinned Lean substrate probe, bounded local formal
discovery, prohibited-construct hygiene, and whitespace. It does not validate a canonical theorem
statement or proof.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

The catalog record was traced to its uncited introduction commit. The complete GDZ scan of Fejer's
1903 *Untersuchungen uber Fouriersche Reihen* was inspected at pages 51-52 and 59-60. It gives a
real `2*pi`-periodic continuous function, symmetric Fourier partial sums, the `n`-term arithmetic
means through `s_(n-1)`, and explicit uniform convergence. The scan's observed SHA-256 is
`c68ca6a...83963`. The two-page collected-works preview of the 1900 *Comptes rendus* note was also
inspected; its PDF/text hashes are `6be38bd0...11689` and `8cac4a06...757b10b`.
Springer and Crossref date the expanded article to March 1903, while the GDZ volume wrapper labels
1904; the source crosswalk preserves that discrepancy.

These temporary discovery copies were not added to the repository and are not H0 evidence.
Catalog-to-source identity, incorporated definitions, full proof boundary, translation,
corrections and errata, 1900/1903 source roles, and independent review remain open. Master
acceptance must lawfully preserve, independently rehash, and review the selected source.

## Environment fingerprint

- Platform: Linux `7.0.0-27-generic`, x86_64, Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0291` | 0 | rank 1297; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 2090,2095 -- Docs/researches/math_theorems.md` | 0 | all six uncited record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| retrieve and inspect the GDZ article PDF at `PPN235181684_0058/LOG_0008.pdf` | 0 | 20-page, 1147538-byte container with a 19-page article scan; pages 51-52 and 59-60 inspected; SHA-256 `c68ca6a...83963` |
| retrieve and inspect the Springer preview for DOI `10.1007/978-3-0348-5902-8_6` | 0 | two pages expose the 1900 locator and bounded-integrable pointwise theorem; PDF/text SHA-256 `6be38bd0...11689` / `8cac4a06...757b10b` |
| inspect Springer/Crossref metadata for DOI `10.1007/BF01447779` | 0 | Fejer, article title, *Mathematische Annalen* 58, pages 51-69, March 1903; no H0 or statement credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0291/IntakeProbe.lean)` | 0 | eight adjacent pinned interfaces elaborated; 13 lines/1091 bytes; complete output SHA-256 `5403d9ac...3b16`; no target theorem declared |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 only for unrelated Cesaro uses | no Fejer-named pinned terminal declaration outside the distinct `THM-M-0347` dossier; discovery snapshot only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts parse after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0291/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0291/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | exact authority rows/hashes, planned H1/M4/R4 boundary, null target, exact inventory, receipt/packet agreement, probe replay, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0291/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate after treating new-file difference as expected | no whitespace diagnostics for any new file |
| `git diff --check -- Stage1_Instances/THM-M-0291 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- No independently accepted catalog-to-source identity, complete definition/proof crosswalk,
  translation, correction and errata audit, 1900/1903 role decision, or H0 review exists.
- Source-literal versus transported circle domain, period, scalar field, Fourier normalization,
  symmetric-sum indexing, Cesaro indexing, uniform-convergence encoding, binders, and boundary cases
  remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to preserve source scope and
open work. Only the integration lane may accept the provisional receipt.

# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target membership, the planned dossier and six-task open DAG, catalog and source
lead provenance, JSON syntax and scoped invariants, exact owned-file inventory, a narrow pinned
Lean candidate probe, prohibited-construct hygiene, and whitespace. It does not validate a
canonical theorem statement or proof because the catalog supplies no truth-valued proposition.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Boncompagni's 1857 transcription of *Liber Abbaci* was inspected through the authenticated BSB
IIIF object `bsb10525679`. Printed pages 283-284/canvases 289-290 state the rabbit assumptions,
calculate monthly totals through 377, and explicitly describe successive addition. The manifest
SHA-256 is `2b265efa274c23a265cfa60910bc0b69629131cf914dc82ad836cb971c53b81e`; canvas OCR digests are
`eb0e47ee147fad613d9cac3cdc6d8622d3fa935c90f51934892242ab874caee2` and
`b0acbf4f82645030752a6414be4fa837e7e33fd17f6ac1d46d3f2b3225597f0d`; the first page image digest
is `e71de1f16c08586f9ad6af916cafdf236ac90be68e3194aa6f8a096e26fba162`. This is a transcription
witness, not the original 1202 manuscript or an accepted H0 crosswalk. It exposes an essential
index shift between the historical monthly totals and `Nat.fib`.

MacTutor biography/Scott-Marketos/Vogel sources were also inspected. Their observed digests are
`0b6fdc363c504ae034cea426cd2cf811ae7ed9a41cfa2ecc3bb2e4b640f1a62c`,
`78585a06b28b31dad1400111328e6bff5297454fe2e4f83f1fe500a2ece469ed`, and
`36bb6bbc340a57cf04da8a5ef204885e5af7f81bd8617143fb6a64d01f9608ad`. They confirm the rabbit
model, indexing ambiguity, and distinction between Fibonacci's sequence and the modern formula,
but remain secondary accounts.

OEIS A000045 was inspected as a modern statement and bibliography lead. It gives the recurrence
`F(n) = F(n-1) + F(n-2)` with initial values `F(0) = 0`, `F(1) = 1`, discusses pre-Fibonacci
Indian history, cites *Liber Abaci* (1202), and points to the rabbit problem on pages 404-405 of
Laurence Sigler's translation. The observed HTML response was 218,934 bytes, SHA-256
`75edfbb494709bada5251fa3fb63d427c4c9456a8d2fed8cc356918f0d8f0c3e`.

OEIS is mutable secondary evidence. Its current comment and bibliography disagree on the number
and page of a related Sigler remark (`[27]`, page 637 versus `[26]`, page 627). Crossref metadata
confirms Sigler's 2002 Springer translation and DOI `10.1007/978-1-4613-0079-3`; that response was
1,977 bytes, SHA-256
`12262f404a459d4b5ad527641eae87ae590b256b9de6ad5371f15c926d4a1287`. The relevant translation
pages and original 1202 manuscript were not accessed or preserved, and no complete model, statement, proof,
translation, correction, errata, or independent-review crosswalk was established. These sources do
not repair the catalog into an accepted proposition or support H0.

Pinned mathlib contains precise natural Fibonacci definition and recurrence interfaces. The Lean
probe validates their availability only, supporting provisional `M3`. It confers no `M0` proof
credit because no canonical catalog root exists to match.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `Mathlib/Data/Nat/Fib/Basic.lean` SHA-256:
  `cc677908e449079923644aed447699e331e0100c88597d8a3c6e491db98267a0`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0925` | 0 | rank 1466; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | produced the base revision and tree above |
| `git blame -L 6763,6768 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| BSB manifest/OCR/image, MacTutor historical HTML/PDFs, OEIS, Crossref, and Springer `curl` requests plus `pdfinfo`, `pdftotext`, scoped extraction, `wc -c`, and `sha256sum` | 0 | historical rabbit model, recurrence/index shift, edition and book identity, locator discrepancy, response sizes, and digests recorded; no H0 or target-correction claim |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0925/IntakeProbe.lean)` | 0 | six Fibonacci interfaces elaborated; `Nat.fib` definition and candidate axiom reports printed; output SHA-256 `10f449b124ae0d7866e7c819768d0685597064a31c1080fa8abafe4697c47ace` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0925-pycache python3 -m py_compile Stage1_Instances/THM-M-0925/check_intake.py` | 0 | scoped validator compiled without writing into the owned path |
| `python3 -B Stage1_Instances/THM-M-0925/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H5/M3/R4 boundary, null canonical target, hashes, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0925/check_intake.py` | 0 | public replay mode passed without the scheduler-only root packet |
| prohibited Lean proof-escape/declaration scan over `IntakeProbe.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, theorem, lemma, or example declaration |
| `git diff --check -- Stage1_Instances/THM-M-0925 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog object/example wording is H5 because it does not select one stable proposition. An
  approved target correction or redirection, immutable source, exact formula and model, proof and
  translation boundary, corrections, errata, and independent review remain open.
- Zero- versus one-based indexing, natural versus other index/value domains, definition versus
  recurrence-property versus uniqueness/counting strength, ordered binders, initial values,
  recurrence orientation, and every boundary case remain statement decisions.
- No canonical Lean expression, minimal-import certificate, expression or environment fingerprint,
  checked alternate encoding, or required statement mutation exists.
- Formal anchor audit, obligation registry, typed graphs, proof integration, composition,
  provenance and trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the received scope
and correction route. Only the integration lane may accept the provisional worker receipt.

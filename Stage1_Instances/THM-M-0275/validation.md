# Intake validation

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, primary-source and scope crosswalk, duplicate-target
boundary, open task DAG, structured invariants, and pinned Lean candidate probe. It does not
validate a canonical Uniform Boundedness proposition or proof because the historical sequence
versus arbitrary-family choice, scalar/operator scope, exact binders, and checked transport remain
open. The automation-provided canonical `.lake` symlink was pre-existing and used read-only. No
update, build, clone, fetch, or dependency mutation was performed. Dirty worker evidence is
nonrelease.

Source downloads and rendered pages used for intake inspection were written only under `/tmp` and
are not part of the repository. The observed hashes record those transient bytes; they are not a
vendored archive, independent review, content-addressed accepted evidence, or release input.

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

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0275` | exit 0; rank 1281, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame` on both catalog records | exit 0; base revision/tree recorded above; both identical source records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --max-time 30 -sS 'https://api.crossref.org/works/10.4064/fm-9-1-50-61' -o /tmp/thm-m-0275-crossref.json` | exit 0; 1624-byte Crossref record; SHA-256 `a7eb1d2a8adf8456f77f76748c38a2a940924b70a5e036255efffa952748871f`; title, authors, year, volume, pages, publisher, and DOI agree |
| `curl -L --max-time 30 -sS -D /tmp/thm-m-0275-doi-headers.txt -o /tmp/thm-m-0275-doi.html 'https://doi.org/10.4064/fm-9-1-50-61'` | exit 0; resolved publisher page is 42178 bytes; SHA-256 `720f6d7989dd940499f4d4d9b7f2c0f216fca7da7bd585b10ad940d4701b4b9b`; metadata and CC-BY download label inspected |
| `curl -L --max-time 60 -sS 'https://www.impan.pl/shop/en/publication/transaction/download/product/92672?download.pdf' -o /tmp/thm-m-0275-banach-steinhaus-1927.pdf` | exit 0; publisher scan is 567964 bytes; SHA-256 `1ae76c338ac45f26c4da9093435fde2b1db942cc65332569f216139a114e0548` |
| `pdfinfo /tmp/thm-m-0275-banach-steinhaus-1927.pdf`; `pdftoppm -jpeg -r 220 -f 1 -l 6 /tmp/thm-m-0275-banach-steinhaus-1927.pdf /tmp/thm-m-0275-pages/page` | exit 0; six image sheets rendered and visually inspected; Section 2, Lemma 3 and its proof on journal page 53 are the sequential result recorded as an H1 lead, not admitted as H0 |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0275/IntakeProbe.lean)` | exit 0; five direct/supporting Banach-Steinhaus, equicontinuity, and barrelled interfaces elaborated; all three candidate theorem reports were `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `f34086bcee8003db3bc966e0bdce8c9606cf612ea06e97196808595cba50bed5` |
| bounded `rg` and pinned-source inspection | exit 0; the direct arbitrary-family declaration, iSup encoding, barrelled dependency, equicontinuity bridge, and same-family THM-M-0312 target were located; no root identity or proof credit inferred |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization; all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0275-pycache python3 -m py_compile Stage1_Instances/THM-M-0275/check_intake.py` | exit 0; checker compiled without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0275/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authorities, source/dependency hashes, duplicate boundary, H1/M3/R4 planned state, null target, artifact hashes, receipt/packet, Lean probe, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` remains permitted |
| per-file `git diff --no-index --check /dev/null <file>` for every owned artifact and the root worker packet | exit 1 for each expected new-file difference; no whitespace diagnostics; the scoped checker independently enforces final newline and rejects CR, NUL, and trailing spaces/tabs |
| `git diff --check -- Stage1_Instances/THM-M-0275 .stage1-worker-selftest.json` | exit 0; no tracked diagnostics; this is not treated as coverage for the wholly untracked files |

## Known open gates

Independent source review, exact historical convention translation, sequence-to-family mapping,
correction or errata audit, common-field versus semilinear scope, ordered proposition, bounds, and
boundary decisions remain open. So do the canonical Lean expression and environment fingerprint,
checked real-bound/iSup and historical/modern transports, statement mutations, exhaustive anchor
and provenance audit, discovery and obligation freezes, typed graphs, proof and composition, trust
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion. These open gates do not invalidate a
truthful self-tested `planned` intake.

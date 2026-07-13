# Intake validation

Base revision: `adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55` (tree
`3c83596059f716cde0d50a5f6b390ada6ca7c8e1`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers only the planned dossier, literal source boundary, overlap boundary, open
task DAG, structured intake invariants, and a narrow pinned Lean infrastructure probe. It does not
validate a canonical Menger proposition or proof because the catalog has not fixed one. The
automation-provided `.lake` symlink was pre-existing and used read-only. No dependency update,
build, clone, fetch, or other `.lake` mutation was performed. Dirty worker evidence is nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0813` | exit 0; rank 1372, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 5977,5982 -- Docs/researches/math_theorems.md` and `git blame -L 6320,6325 -- Docs/researches/math_theorems.md` | exit 0; both Menger-family catalog records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -sS 'https://www.impan.pl/shop/publication/transaction/download/product/92646?download.pdf' -o /tmp/menger-impan.pdf` | exit 0; publisher supplied a 10-page, 1,531,980-byte image-only scan; SHA-256 `45f0dce723f85dae5d360892b6e9596aeaef70ea222b3ea9a0ea2e7c54ae3602` |
| `curl -L --max-time 60 -sS -H 'Accept: application/vnd.citationstyles.csl+json' 'https://doi.org/10.4064/fm-10-1-96-115' -o /tmp/menger-doi.json` | exit 0; 1,309-byte DOI metadata response identifies Menger, title, journal, volume 10, pages 96-115, and 1927; SHA-256 `5d801900763f0e3e77c229ecd27792c7170866b8035d6451ce8176a90b8b85cf` |
| `pdftotext -layout /tmp/menger-impan.pdf /tmp/menger-impan.txt` | exit 0; output contained only ten form-feed bytes, confirming the scan has no usable text layer; SHA-256 `cb7c7f5a50363e843bf55318c122a7f82614928eb2580384dc6aca3a963ef1cd` |
| `curl -L --fail --max-time 60 -sS 'https://www.math.uni-hamburg.de/home/diestel/books/graph.theory/preview/Ch3.pdf' -o /tmp/diestel-ch3.pdf` | exit 0; author-hosted sixth-edition Chapter 3 retrieved; SHA-256 `1d54f8cf0a846e8acedc5a5eb87839173a3145148a6c23eba49e4d4d6d0c8775` |
| `pdftotext -layout /tmp/diestel-ch3.pdf /tmp/diestel-ch3.txt` | exit 0; Theorem 3.3.1, Corollary 3.3.5, and Theorem 3.3.6 inspected; text SHA-256 `32d3e2e70d912de714c2ec2529835627437be4a7b44382a2c529992a6baa0268` |
| `curl -L --fail --max-time 60 -sS 'https://www.math.uni-hamburg.de/home/diestel/books/graph.theory/preview/Ch1.pdf' -o /tmp/thm-m-0813-diestel-ch1.pdf` | exit 0; author-hosted definitions chapter retrieved; SHA-256 `ebd9084653a1a534b964cbe327eeb8ab6b46a5e98deeee94280b05ebb6f37b56` |
| `pdftotext -layout /tmp/thm-m-0813-diestel-ch1.pdf /tmp/thm-m-0813-diestel-ch1.txt` | exit 0; finite-graph, path, separation, and connectivity conventions inspected; text SHA-256 `94ff5b77d20b0499aed7aa377d9aa223f0fa610f68c67d7d21e1850790f6b6f7` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package-status output |
| `rg -n -i --glob '*.lean' 'Menger|vertex[ _-]?connect|internally[ _-]?(vertex[ _-]?)?disjoint|vertex[ _-]?separator|disjoint.*path|path.*disjoint' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph Formalizations/Lean/AwesomeTheorems` | exit 0; only the local `IsPath.disjoint_support_of_append` support lemma matched; no Menger declaration or vertex-separator/path-packing theorem was found in this bounded search |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0813/IntakeProbe.lean)` | exit 0; eight adjacent path/reachability/induced-graph/edge-connectivity APIs elaborated; stdout SHA-256 `acddbc7c967786d595d8bce3393b249946d3bd2b5e495df6f246698d6b8c21d7`; no target statement or proof body was declared |
| `python3 -m json.tool` for `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization; all structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0813-pycache python3 -m py_compile Stage1_Instances/THM-M-0813/check_intake.py` | exit 0; checker compiled without generating files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0813/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, source and dependency pins, H1/M4/R4 boundary, null target, exact inventory, receipt/packet agreement, and six open tasks agreed |
| `rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' Stage1_Instances/THM-M-0813` | exit 1 as expected; no prohibited declaration or proof escape in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0813 .stage1-worker-selftest.json` | exit 0; no tracked-diff whitespace diagnostics |
| `bash -lc 'for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0813/*; do git diff --no-index --check /dev/null "$f" >/tmp/stage1-thm-m-0813-diff-check.out 2>&1; rc=$?; if test "$rc" -ne 1; then exit 1; fi; if test -s /tmp/stage1-thm-m-0813-diff-check.out; then exit 1; fi; done'` | exit 0; every new file produced the expected difference exit 1 and no whitespace diagnostics |

## Known open gates

An accepted identity and root-ownership decision for `THM-M-0813` versus `THM-M-0862` remains
open. So do an independently reviewed exact source proposition, original-source passage and
translation mapping, corrections or errata, graph model, terminal data, vertex/edge disjointness,
separator and cardinal conventions, local/global choice, every boundary case, canonical Lean
expression and environment fingerprint, checked transports, statement mutations, exhaustive anchor
and provenance audit, discovery and obligation freezes, typed graphs, proof and composition, trust
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion. These open gates do not invalidate a
truthful self-tested `planned` intake.

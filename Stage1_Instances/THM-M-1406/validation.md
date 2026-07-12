# Intake validation

Base revision: `3d1d6d3eb018f17657cae1cfd7d25fc30492a12b` (tree
`3aa3dd324b35549da6cf2c5a54183a63ed1bfff9`).

Validation date: `2026-07-12` (`Asia/Shanghai`). This validation is limited to target membership,
repository-standard consistency, dossier structure, source discovery, JSON integrity, pinned API
availability, prohibited-construct hygiene, and formatting. Because the catalog does not identify
a proposition, no canonical expression, statement mutation, `H0` source packet, proof body, or
kernel theorem result is claimed.

The automation-provided `Formalizations/Lean/.lake` symlink is an untracked input pointing to the
canonical pinned artifacts. It was used read-only. No dependency update, build, clone, fetch, or
`.lake` mutation was performed. This is nonrelease worker evidence.

## Exact commands and results

Commands were run from the repository root unless a subshell is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1406` | 0 | rank 905, planned, no legacy slot, unaccepted legacy artifacts, theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree are those recorded above |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned mathlib source tree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1406/IntakeProbe.lean)` | 0 | eight nearby measure, dynamics, measurable-partition, generated-space, and information-function API checks elaborated |
| `rg -n -i --glob '*.lean' 'measure.?theoretic entropy\|kolmogorov.?sinai\|kolmogorov entropy\|partition entropy\|metric entropy\|measure entropy' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability` | 1 | expected no-match exit; this is not a saturated anchor audit |
| `curl -A 'Mozilla/5.0' --fail --location --silent --show-error --output /tmp/thm-m-1406-kolmogorov-1958.pdf 'https://www.mathnet.ru/php/getFT.phtml?jrnid=dan&paperid=22922&what=fullt&option_lang=eng'` | 0 | retrieved the four-page Math-Net primary scan |
| `file /tmp/thm-m-1406-kolmogorov-1958.pdf` | 0 | PDF document, version 1.6, four pages |
| `pdfinfo /tmp/thm-m-1406-kolmogorov-1958.pdf` | 0 | PDF 1.6, four pages, 595,299 bytes, not encrypted |
| `pdftotext -layout /tmp/thm-m-1406-kolmogorov-1958.pdf /tmp/thm-m-1406-kolmogorov-1958.txt` | 0 | text extraction completed for bounded structural inspection |
| `sha256sum /tmp/thm-m-1406-kolmogorov-1958.pdf` | 0 | `abf376fa2e2aefaf1492308a8808d79be3431dae4c821ca546719f35a1d4bf85` |
| `curl --fail --location --silent --show-error --get 'http://www.scholarpedia.org/w/api.php' --data-urlencode 'action=query' --data-urlencode 'prop=revisions' --data-urlencode 'revids=91407' --data-urlencode 'rvprop=ids\|timestamp\|content' --data-urlencode 'format=json' --output /tmp/thm-m-1406-scholarpedia-91407-api-a.json` | 0 | retrieved fixed revision-content response A |
| `curl --fail --location --silent --show-error --get 'http://www.scholarpedia.org/w/api.php' --data-urlencode 'action=query' --data-urlencode 'prop=revisions' --data-urlencode 'revids=91407' --data-urlencode 'rvprop=ids\|timestamp\|content' --data-urlencode 'format=json' --output /tmp/thm-m-1406-scholarpedia-91407-api-b.json` | 0 | retrieved fixed revision-content response B |
| `file /tmp/thm-m-1406-scholarpedia-91407-api-a.json` | 0 | JSON text data |
| `wc -c /tmp/thm-m-1406-scholarpedia-91407-api-a.json` | 0 | 10,659 bytes |
| `sha256sum /tmp/thm-m-1406-scholarpedia-91407-api-a.json /tmp/thm-m-1406-scholarpedia-91407-api-b.json` | 0 | both responses `f29e718b4bc265ca6e04b78eb1c1bf13e253549b3f9d0abb0dba926a2710a706` |
| `cmp -s /tmp/thm-m-1406-scholarpedia-91407-api-a.json /tmp/thm-m-1406-scholarpedia-91407-api-b.json` | 0 | responses are byte-identical |
| `python3 -m json.tool /tmp/thm-m-1406-scholarpedia-91407-api-a.json >/dev/null` | 0 | valid JSON |
| `rg -o -n 'revid.{0,30}\|timestamp.{0,40}\|Definition 1\|Theorem 1\|quasi-regular' /tmp/thm-m-1406-scholarpedia-91407-api-a.json` | 0 | revision 91407, timestamp `2011-10-21T04:11:14Z`, Definition 1, Theorem 1, and historical markers located |
| `python3 -m json.tool Stage1_Instances/THM-M-1406/instance.json >/dev/null` and the same command for `task-dag.json` | 0 | both preliminary structured artifacts parsed |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|opaque)[[:space:]]\|\bunsafe\b' Stage1_Instances/THM-M-1406 -g '*.lean'` | 1 | expected no-match exit; no prohibited proof construct or unsafe declaration found |
| `for f in Stage1_Instances/THM-M-1406/*; do git diff --no-index --check /dev/null "$f" >/dev/null; rc=$?; if [ "$rc" -gt 1 ]; then exit "$rc"; fi; done` | 0 | all preliminary untracked dossier files passed whitespace checks; exit 1 from ordinary content difference is accepted, while exit greater than 1 fails |
| `python3 Stage1_Instances/THM-M-1406/check_intake.py` after receipt finalization | 0 | target/DAG identity, lifecycle, null canonical target, provisional debt vector, artifact hashes, and six open tasks agree |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json`, each redirected to `/dev/null` | 0 | all structured handoff artifacts parse |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|opaque)[[:space:]]\|\bunsafe\b' Stage1_Instances/THM-M-1406 -g '*.lean'` | 1 | expected no-match exit; no prohibited proof construct or unsafe declaration found |
| `for f in Stage1_Instances/THM-M-1406/* .stage1-worker-selftest.json; do git diff --no-index --check /dev/null "$f" >/dev/null; rc=$?; if [ "$rc" -gt 1 ]; then exit "$rc"; fi; done` | 0 | every owned handoff file and root self-test passed the whitespace check |
| `git status --short --untracked-files=all` | 0 | only the pre-existing `.lake` link, the nine owned dossier files, and the authorized root self-test are untracked |

The primary scan was inspected only to identify its visible structure; no unreviewed
Russian-to-English theorem translation is credited. The Scholarpedia article is a secondary
definition and history anchor, not `H0`. The API probe and bounded name search are feasibility
evidence only, not a canonical target, a complete anchor audit, or proof evidence.

Known downstream failures are target correction and exact claim selection; accepted primary-source
statement, definitions, translation and independent review; reconciliation with `THM-M-1404` and
`THM-M-1405`; canonical Lean elaboration and all four statement mutation classes; frozen discovery
and obligation registries; formal candidate audit; proof; hermetic replay; and independent release
verification. They prevent statement, audit, and theorem completion but do not invalidate this
truthful `planned` intake.

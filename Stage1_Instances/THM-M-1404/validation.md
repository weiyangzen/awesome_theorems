# Intake validation

Base revision: `028e2535b68678b8296e63e2cacb05ed9775a2d8` (tree
`2845b046547e71984e5d93f4f04045663bd3bcbb`).

This validation is limited to target membership, repository-standard consistency, dossier
structure, source discovery, JSON integrity, pinned API availability, prohibited-construct hygiene,
and formatting. Because the catalog does not identify a proposition, no canonical expression,
mutation result, source acceptance, proof body, or kernel theorem result is claimed. The
automation-provided `Formalizations/Lean/.lake` symlink is an untracked input pointing to the
canonical pinned artifacts. It was used read-only; no dependency update, build, clone, fetch, or
`.lake` mutation was performed. This is nonrelease worker evidence.

## Exact commands and results

Commands were run from the repository root unless a subshell is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1404` | 0 | rank 903, planned, no legacy slot, unaccepted legacy artifacts, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned mathlib source tree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1404/IntakeProbe.lean)` | 0 | six nearby measure, dynamics, measurable-partition, and information-function APIs elaborated |
| `rg -n -i --glob '*.lean' 'measure.?theoretic entropy\|kolmogorov.sinai\|kolmogorov entropy\|partition entropy' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory` | 1 | expected no-match exit; no matching source name in this bounded intake search |
| `curl -A 'Mozilla/5.0' --fail --location --silent --show-error --output /tmp/dan22922_repro.pdf 'https://www.mathnet.ru/php/getFT.phtml?jrnid=dan&paperid=22922&what=fullt&option_lang=eng'` | 0 | retrieved the Math-Net full-text scan |
| `file /tmp/dan22922_repro.pdf` | 0 | PDF 1.6, four pages |
| `sha256sum /tmp/dan22922_repro.pdf` | 0 | `abf376fa2e2aefaf1492308a8808d79be3431dae4c821ca546719f35a1d4bf85` |
| `cmp -s /tmp/dan22922.pdf /tmp/dan22922_repro.pdf` | 0 | independently retrieved file matches the initially inspected scan byte for byte |
| `python3 -m json.tool Stage1_Instances/THM-M-1404/instance.json >/dev/null` | 0 | structured intake parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1404/task-dag.json >/dev/null` | 0 | open task DAG parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1404/intake-receipt.json >/dev/null` | 0 | provisional worker report parsed after finalization |
| `python3 Stage1_Instances/THM-M-1404/check_intake.py` | 0 | identity, lifecycle, legal debt vector, null target, artifact hashes, and six open tasks agree |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|opaque)[[:space:]]\|\bunsafe\b' Stage1_Instances/THM-M-1404 -g '*.lean'` | 1 | expected no-match exit; no prohibited proof construct or unsafe declaration found |
| `for f in Stage1_Instances/THM-M-1404/* .stage1-worker-selftest.json; do git diff --no-index --check /dev/null "$f" >/dev/null; rc=$?; if [ "$rc" -gt 1 ]; then exit "$rc"; fi; done` | 0 | every untracked handoff artifact passed the whitespace check |
| `git status --short` | 0 | only the automation-provided `.lake` symlink, the owned dossier, and the root self-test packet are untracked |

The scan structure was checked visually; no unreviewed Russian-to-English theorem translation is
credited. The API probe and bounded search are feasibility evidence only, not an anchor audit.
Known downstream failures are exact claim selection and target correction, accepted primary-source
passage and independent review, canonical Lean elaboration and mutation tests, frozen discovery and
obligation registries, formal candidate audit, proof, hermetic replay, and independent release
verification. They prevent audit and theorem completion but do not invalidate this truthful
`planned` intake.

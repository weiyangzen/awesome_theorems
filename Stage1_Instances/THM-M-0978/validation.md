# Intake validation

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a`; base tree:
`cc5285432a02107fadffb68c698690d1b98ac5f2`.

Validation was performed on 2026-07-13 (Asia/Shanghai). It covers target membership, the planned
dossier and six-node open DAG, literal repository scope, the duplicate-target conflict, primary
source and non-substitution boundaries, JSON and file invariants, and a narrow pinned Lean
exact-topic API probe. It does not validate a canonical root or proof because the exact source
proposition and target-ID allocation have not been frozen. The automation-provided canonical
`.lake` symlink existed before editing and was used read-only. No dependency update, build, clone,
fetch, or other `.lake` mutation was performed. This dirty worker run is nonrelease evidence.

## Source inspection

The inspected North Carolina State University repository scan is a 25-page, 891,780-byte PDF with
SHA-256 `e4c1f30fef09d420bc4b791a53f95cb461f47b363d0d9debaf13e15fbaaef203`.
The title page identifies a May 1962 University of North Carolina Institute of Statistics
mimeo; the catalog and journal bibliography use 1963. The introduction, Theorem 2 on printed page
6 (equation (2.10)), and its Section 3 proof on printed pages 12-13 were inspected. The scan is
source-discovery evidence only; no immutable source admission or independent H0 review is claimed.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Mathlib/Probability/Moments/SubGaussian.lean` SHA-256:
  `1261993867efbddb6781a6ce9d0855335fab6891f819062ac83b8d9f6d94c440`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0978` | exit 0; rank 1512, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before editing | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 7141,7146 -- Docs/researches/math_theorems.md` and `git blame -L 7266,7271 -- Docs/researches/math_theorems.md` | exit 0; both Hoeffding records originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded repository search for `THM-M-0978`, `THM-M-0994`, Hoeffding, and exact mathlib candidates | exit 0; confirmed the duplicate records, located the other-target artifacts and pinned exact-topic declarations, and found no authority for inheriting another target's statement or state |
| `curl -L --fail --silent --show-error --max-time 60 -o /tmp/hoeffding1963.pdf <NCSU repository bitstream URL>` | exit 0; retrieved the 891,780-byte, 25-page scan with the source digest recorded above |
| `pdfinfo /tmp/hoeffding1963.pdf`, page rendering, and direct visual inspection | exit 0; title page, introduction, Theorem 2 equation (2.10), and Section 3 proof located; no OCR-derived exact transcription or H0 claim |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `git -C ... status --short` | exit 0; pinned revision/tree recorded above and package worktree clean |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0978/IntakeProbe.lean)` | exit 0; eight exact-topic interfaces elaborated; two candidate bodies reported only `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `ea68b349a7c4befcf877dbbe1a6628dd9029af0ac9d3af8dd02106b9b5096790`; stderr empty |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0978-pycache python3 -m py_compile Stage1_Instances/THM-M-0978/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0978/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and DAG identity, null root, H1/M3/R4 boundary, duplicate record, source and dependency pins, artifact inventory, receipt, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0978` | exit 1 as expected; no prohibited proof escape or declaration token matched |
| `rg -n '\r\|[ \t]+$' Stage1_Instances/THM-M-0978 .stage1-worker-selftest.json` | exit 1 as expected; no carriage return or trailing whitespace matched; the scoped checker also checks final newlines and NUL bytes |
| `git diff --check -- Stage1_Instances/THM-M-0978 .stage1-worker-selftest.json` plus direct checks for new files | exit 0; no whitespace diagnostics |

## Known open gates

The catalog contains two near-verbatim Hoeffding targets and supplies no approved allocation rule.
An independently approved exact source proposition, the 1962 mimeograph/1963 journal edition
relationship, corrections and errata, finite-index and nonempty conventions, pointwise versus
almost-sure bounds, average versus centered-sum normalization, positive versus nonnegative
threshold, one-sided versus two-sided scope, exponent algebra, denominator-zero and other boundary
semantics, complete source-node mapping, and source review remain open. So do the canonical Lean
expression and environment fingerprints, minimal imports, checked transports, statement
mutations, immutable anchor and terminal-body provenance audit, discovery and obligation freezes,
typed graphs, proof composition, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion.

The inspected proof source and pinned declarations make later work concrete, but they do not
invalidate the planned-intake boundary: no canonical root or proof state is accepted by this phase.

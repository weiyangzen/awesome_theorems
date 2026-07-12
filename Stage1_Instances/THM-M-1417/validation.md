# Intake validation

Base revision: `61ce73b9038706a45488f5644ad0e0f3d98937a1` (tree
`c8e94ac73b6875f43c55ae766b0c4af4abc7ba3e`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source-
discovery metadata, pinned environment identity, a narrow Lean API probe, a bounded local name
search, proof-escape hygiene, and whitespace. The source record is not a proposition, so
elaborating a purported canonical Lean target would invent missing mathematics.
`IntakeProbe.lean` therefore checks possible substrate only and supplies no statement or proof
credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

Environment fingerprint:

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Inspected secondary survey PDF SHA-256:
  `5de3a2ed19f2f03f0f46cdd1f681419a61589e1a9f8579442e4b842cbc725e42`.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1417` | 0 | rank 916, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short` | 0 | before editing, only the pre-existing untracked `Formalizations/Lean/.lake` link was present |
| `git blame -L 10355,10360 -- Docs/researches/math_theorems.md` | 0 | all six uncited source-record lines originate at commit `bcf3f9fa...b74f` |
| `curl -L --fail --silent --show-error --max-time 30 https://api.crossref.org/works/10.2307/2373810 \| jq -r <compact-metadata-projection>` | 0 | Ruelle, article title, journal 98(3), starting page 619, year 1976, and DOI confirmed; no exact theorem text |
| `curl -L --fail --silent --show-error --max-time 30 https://www.jstor.org/stable/2373810` | 22 | HTTP 403; primary article text not inspected, recorded as an access limitation |
| `tmp=$(mktemp); curl -L --fail --silent --show-error --max-time 30 https://cims.nyu.edu/~lsy/papers/SRBsurvey.pdf -o "$tmp"; sha256sum "$tmp"; wc -c "$tmp"; pdfinfo "$tmp"; pdftotext -f 1 -l 4 -layout "$tmp" -; rm -f "$tmp"` | 0 | 246558-byte, 21-page PDF; digest above; Theorem 1 and its explicit Axiom A/equivalence scope inspected as secondary ambiguity evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-1417/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1417/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1417/intake-receipt.json` | 0 | valid JSON after receipt finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after worker manifest finalization |
| `python3 Stage1_Instances/THM-M-1417/check_intake.py` | 0 | target identity, H5/M4/R4 planned boundary, null target, empty accepted state, exact artifact inventory, and six open tasks agree |
| `python3 -m py_compile Stage1_Instances/THM-M-1417/check_intake.py` | 0 | intake validator compiles; generated cache removed |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1417/IntakeProbe.lean)` | 0 | seven pinned Birkhoff-average, measure-preserving, ergodicity, measure, volume, and derivative API checks elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and package status | 0 | pinned mathlib revision above; package worktree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes agree with the fingerprint |
| `rg -n -i '(^\|[^A-Za-z])(SRB\|Sinai[- ]Ruelle[- ]Bowen\|physical measure(s)?\|dissipative (system\|dynamics)\|unstable conditional measures?)' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match exit; intake discovery only, not an exhaustive anchor audit |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant)\b' Stage1_Instances/THM-M-1417` | 1 | expected no-match exit; no prohibited proof escape or declaration |
| `git diff --check -- Stage1_Instances/THM-M-1417 .stage1-worker-selftest.json` plus per-file no-index whitespace checks | 0 | no whitespace diagnostics in all ten changed files |

The compact Crossref projection used was:

```bash
curl -L --fail --silent --show-error --max-time 30 \
  'https://api.crossref.org/works/10.2307/2373810' | \
  jq -r '.message | [(.title[0]), (.author | map(.given + " " + .family) | join(", ")), (."container-title"[0]), .volume, .issue, .page, (.published["date-parts"][0][0] | tostring), .DOI, .URL] | @tsv'
```

The first failed theorem gate is exact source/statement identity: the catalog names a measure
concept but no truth-valued proposition. An approved immutable primary-source theorem, its exact
definitions and assumptions, proof boundary, errata, and independent crosswalk remain open. So do
the canonical Lean target and fingerprints, checked transports and mutations, formal anchor,
discovery and obligation freezes, proof and composition, hermetic replay, deterministic bundle,
independent release verification, and master acceptance. These failures prevent ordinary theorem
execution and completion but do not invalidate a truthful, self-tested `planned` intake.

# Intake validation

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702`; base tree:
`02279a8caa5f31ed8e37e35c8584a336eed9b974`.

Validation was performed on 2026-07-13 (Asia/Shanghai). It covers target membership, the planned
dossier and six-node open DAG, literal repository scope, the duplicate-target conflict, source and
non-substitution boundaries, JSON and file invariants, and a narrow pinned Lean exact-topic API
probe. It does not validate a canonical root or proof because the exact source proposition and
target-ID allocation have not been frozen. The automation-provided canonical `.lake` symlink was
present before editing and was used read-only. No dependency update, build, clone, fetch, or other
`.lake` mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Mathlib/Probability/Moments/Variance.lean` SHA-256:
  `920c022075149257307335beccbc8a62c7360fb3d9d73571b8240093dc2d72f0`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Inspected NUMDAM/Gallica PDF SHA-256:
  `e651494a4b2710e4c81cc10be402c230507043aae9dca4575eb17bc93f141f02`;
  498,189 bytes and 9 PDF pages.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0282` | exit 0; rank 1288, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before editing | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 2027,2032 -- Docs/researches/math_theorems.md` and `git blame -L 7245,7250 -- Docs/researches/math_theorems.md` | exit 0; both probability Chebyshev records originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `rg -n --hidden --glob '!.git/**' 'THM-M-0282\|THM-M-0992\|切比雪夫不等式\|Chebyshev\|meas_ge_le_variance_div_sq\|meas_ge_le_evariance_div_sq' .` | exit 0; confirmed the duplicate probability records, located the pinned variance candidates, and found no source support for reallocating this ID to the deterministic sum inequality |
| `wget -O /tmp/chebyshev1867-full.pdf --timeout=60 --tries=3 --continue 'https://www.numdam.org/item/JMPA_1867_2_12__177_0.pdf'` | exit 0; retrieved 498,189-byte NUMDAM/Gallica scan, SHA-256 `e651494a4b2710e4c81cc10be402c230507043aae9dca4575eb17bc93f141f02` |
| `pdfinfo /tmp/chebyshev1867-full.pdf` and `pdftotext -layout /tmp/chebyshev1867-full.pdf /tmp/chebyshev1867-full.txt` | exit 0; 9 pages and 442 extracted lines; title, author, journal metadata, opening theorem, proof through printed page 182, average/weak-law form, and Bernoulli corollary inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `git -C ... status --short` | exit 0; pinned revision/tree recorded above and package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0282/IntakeProbe.lean)` | exit 0; eight candidate interfaces elaborated; both candidate theorem bodies reported only `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `e95be81d3c5910ef5d867e9217c870ccfb3541beb34370e09bccbe64910cf95c` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0282-pycache python3 -m py_compile Stage1_Instances/THM-M-0282/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0282/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null root, H1/M3/R4 boundary, duplicate record, pins, artifact inventory, receipt, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0282` | exit 1 as expected; no prohibited declaration token matched |
| `rg -n '\r\|[ \t]+$' Stage1_Instances/THM-M-0282 .stage1-worker-selftest.json` | exit 1 as expected; no carriage return or trailing whitespace matched; the scoped checker also checked final newlines and NUL bytes for every owned file |
| `git diff --check` | exit 0; no tracked-patch whitespace diagnostics; all new files are untracked and therefore covered by the explicit byte/regex checks above |

## Known open gates

The catalogue contains two probability Chebyshev targets and supplies no approved allocation rule.
An approved immutable human source, exact selection among the historical sum/average form and a
modern single-variable variance form, the historical proof's unstated mutual-independence premise,
the omitted positive/nonzero domain of `alpha`, probability-space encoding, strict inside-event to
closed-tail complement transport, variance codomain, Russian-original/French-translation and
Bienayme priority genealogy, complete premise/conclusion/proof-boundary/translation/errata
crosswalk, and independent source review remain open. Arbitrary finite measures belong only to the
generalized formal-candidate surface. So do the canonical Lean expression and environment
fingerprints, minimal imports, checked
transports, statement mutations, immutable anchor audit, terminal-body provenance, transitive trust
and placeholder closure, discovery and obligation freezes, typed graphs, proof composition,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion.

The inspected source and pinned declarations make the later formal route concrete, but they do not
invalidate the planned-intake boundary: no canonical root or proof state is accepted by this phase.

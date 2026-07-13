# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and six-node open task DAG,
repository and source-lead provenance, JSON and scoped intake invariants, a narrow pinned Lean API
probe, bounded topic search, prohibited-construct hygiene, and whitespace. It does not validate a
canonical Weierstrass factorization statement or proof because neither has been source-selected.
The automation-provided canonical `.lake` symlink existed before the intake and was used read-only;
no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty
worker evidence is nonrelease evidence.

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

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0230` | 0 | rank 1242; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 1661,1666 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository crosswalk inspection | 0 | catalog and Stage0 contain no pinpoint source, exact root, primary-factor definition, zero-divisor/multiplicity encoding, convergence semantics, assumption map, or formal artifact |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0 Stage1 intake research' -sS 'https://api.crossref.org/works/10.1007/978-3-662-43012-5_1' -o /tmp/thm-m-0230-weierstrass-crossref.json && wc -c /tmp/thm-m-0230-weierstrass-crossref.json && sha256sum /tmp/thm-m-0230-weierstrass-crossref.json && jq '.message \| {title:.title,author:.author,published:.published,container_title:."container-title",page:.page,DOI:.DOI,URL:.URL,relation:.relation}' /tmp/thm-m-0230-weierstrass-crossref.json` | 0 | 1865-byte mutable response, SHA-256 `5b2756586fcd0e910a41443825ef4fc7cbe147d1ee27cdf4f094b97f28282be7`; bibliographic discovery only |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0 Stage1 intake research' -sS 'https://api.crossref.org/works/10.1007/978-3-662-43012-5_8' -o /tmp/thm-m-0230-weierstrass-erratum-crossref.json && wc -c /tmp/thm-m-0230-weierstrass-erratum-crossref.json && sha256sum /tmp/thm-m-0230-weierstrass-erratum-crossref.json && jq '.message \| {title:.title,author:.author,published:.published,container_title:."container-title",page:.page,DOI:.DOI,URL:.URL,relation:.relation}' /tmp/thm-m-0230-weierstrass-erratum-crossref.json` | 0 | 1880-byte mutable response, SHA-256 `8c18da9122ca0f7e6dbea0de83290f635a492f85f8c0b930d4f213784a01f6f2`; page-261 erratum metadata only |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0 Stage1 intake research' -sS 'https://dlmf.nist.gov/1.10.ix?format=html' -o /tmp/thm-m-0230-dlmf.html && wc -c /tmp/thm-m-0230-dlmf.html && sha256sum /tmp/thm-m-0230-dlmf.html && rg -n -i -C 4 'Weierstrass Product\|1\.10\.22\|Titchmarsh\|infinite product' /tmp/thm-m-0230-dlmf.html \| head -100` | 0 | 361104-byte mutable response, SHA-256 `02a8b046c01e0f8c8b013bf9c5a46f30019079c731cb1e65b6bfabd292c791cb`; section 1.10(ix) and equation 1.10.22 are special-case E5 discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0230/IntakeProbe.lean)` | 0 | nine adjacent pinned APIs elaborated; 31 output lines, 2721 bytes, SHA-256 `533d3252d8320e72d4f8ec1928df18e4d4ee517f84a3a55a26f7f8d6165b4468`; two printed library declarations use only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `rg -n -i 'weierstrass.{0,80}(entire\|holomorphic\|infinite[ _-]*product\|canonical[ _-]*product)\|(entire\|holomorphic\|infinite[ _-]*product\|canonical[ _-]*product).{0,80}weierstrass' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | 1 (expected no match) | on 2026-07-13, no exact complex-analytic universal root or primary-factor implementation was found in the pinned mathlib and repo-local Lean trees; local bounded search only, not an external or exhaustive audit |
| `rg -n -i 'weierstrass[ _-]*(factor\|product)\|canonical[ _-]*product\|primary[ _-]*factor\|elementary[ _-]*factor\|Weierstrass.*entire\|entire.*Weierstrass' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | 0 | found the unrelated power-series preparation namesake and unrelated uses of canonical product; none is credited |
| `python3 -m json.tool Stage1_Instances/THM-M-0230/instance.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-0230/task-dag.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-0230/intake-receipt.json >/dev/null && python3 -m json.tool .stage1-worker-selftest.json >/dev/null` | 0 | all four structured records parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0230-pycache python3 -m py_compile Stage1_Instances/THM-M-0230/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0230/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned lifecycle, H1/M4/R4 boundary, null target, source pins, exact inventory and hashes, receipt/packet agreement, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '^[[:space:]]*axiom\b' -e '^[[:space:]]*constant\b' -e '^[[:space:]]*opaque\b' -e '^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0230 --glob '*.lean'` | 1 (expected no match) | no proof escape or bodyless/unsafe declaration in the discovery-only probe |
| `for f in Stage1_Instances/THM-M-0230/* .stage1-worker-selftest.json; do output=$(git diff --no-index --check /dev/null "$f" 2>&1) \|\| code=$?; test "${code:-0}" -le 1 && test -z "$output" \|\| { printf '%s\n' "$output"; exit 1; }; unset code; done` | 0 | no whitespace diagnostics for any new file; no-index exit 1 for a new file is accepted only when diagnostic output is empty |
| `git diff --check -- Stage1_Instances/THM-M-0230 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics after finalization |

## Known open gates

An accepted immutable source edition and exact proposition, complete incorporated
definition/premise/conclusion/proof-boundary/errata crosswalk, construction-versus-factorization
root decision, and independent source review remain open. So do the canonical Lean expression and
environment fingerprint, checked transports, statement mutations, exhaustive formal anchor audit,
discovery protocol, obligation registry, typed graphs, proof and composition, trust and provenance
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion. These failures do not invalidate a
truthful self-tested `planned` intake.

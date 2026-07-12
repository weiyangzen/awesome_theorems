# Intake validation

Base revision: `d1bb69e506d568ec4852bd68cc5bda1d61702852` (tree
`d9681ef41935162296b57b0170641d66404a53a9`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
provenance, pinned environment identity, a narrow Lean API probe, a bounded local name search,
proof-escape hygiene, and whitespace. The catalog wording is not a proposition, so elaborating a
purported canonical target would invent missing mathematics. `IntakeProbe.lean` checks only
possible substrate; it introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1437` | 0 | rank 935, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git blame -L 10495,10500 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.1007/BF01020332 -o /tmp/feig_crossref_1978.json` followed by `wc -c` and `sha256sum` | 0 | nonbundled Crossref metadata observation: 3863 bytes, SHA-256 `6aca29691c6d7aaa9976ec006e8f0aca378657b7999a79acb5fe1e8924dad326`; citation discovery only |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.1007/BF01107909 -o /tmp/feig_crossref_1979.json` followed by `wc -c` and `sha256sum` | 0 | nonbundled Crossref metadata observation: 3724 bytes, SHA-256 `0ee4e0f0e472bd838a1802160e28bf9b70a2a11887b9b1dd3e7137f7511857bd`; citation discovery only |
| `curl -L --fail --silent --show-error https://doi.org/10.1007/BF01020332 -o /tmp/feig_1978_landing.html` followed by metadata inspection | 0 | temporary publisher HTML observation: 243606 bytes, SHA-256 `65268bc0c1a63c29075947a7c0a76e0a46210a31e72524dd17f5f56c45aa4357`; publisher `dc.description` exposes alpha/delta claims and says the treatment is heuristic; not bundled or H evidence |
| `curl -L --fail --silent --show-error https://link.springer.com/article/10.1007/BF01107909 -o /tmp/feig_1979_landing.html` followed by metadata inspection | 0 | temporary publisher HTML observation: 245779 bytes, SHA-256 `a591f08e4e2aebe6311f94a05ab9ffcb944e272ca3c39c074cee24a6e77d691f`; publisher `dc.description` makes the spectral conjecture and conditional boundary explicit; not bundled or H evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1437/IntakeProbe.lean)` | 0 | ten pinned iteration, periodic-point, fixed-point, semiconjugacy, and limit API checks elaborated; no target declaration |
| `rg -n -i --glob '*.lean' 'Feigenbaum\|Coullet.?Tresser\|Lanford\|period[- ]doubl\|dynamical renormali[sz]ation\|unimodal.*bifurcat' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match result; bounded intake discovery only, not a complete anchor audit or external-project search |
| `python3 -m json.tool Stage1_Instances/THM-M-1437/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1437/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1437/intake-receipt.json` | 0 | valid JSON |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1437-pycache python3 -m py_compile Stage1_Instances/THM-M-1437/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1437/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, planned H5/M4/R4 boundary, null target, exact artifact inventory, handoff, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1437` | 1 | expected no-match result; no prohibited proof escape or declaration |
| `git diff --check -- Stage1_Instances/THM-M-1437 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; this does not cover untracked contents |
| per-file `git diff --no-index --check /dev/null <changed-file>` loop over the root packet and all nine owned files, accepting expected diff exit 1 | 0 | no whitespace diagnostics; `check_intake.py` independently checked final newline, LF-only content, NUL absence, and trailing spaces |

## Known downstream failures

- The catalog wording is not a stable proposition. No approved correction selects delta, alpha,
  a fixed-point or hyperbolicity theorem, exact map/operator class, binders, normalization, limit
  orientation, conclusion, boundary cases, or separation from neighboring targets.
- No independently reviewed immutable primary theorem, complete definition/assumption/proof/errata
  crosswalk, reconciliation of the 1975 date, or theorem locator is accepted.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification are open.

These failures prevent exact-statement, proof, and theorem-completion claims, while every downstream
audit gate remains open. They do not invalidate a truthful, self-tested `planned` intake whose
purpose is to freeze the honest ambiguity boundary and open DAG. Only the integration lane may
accept the provisional worker receipt.

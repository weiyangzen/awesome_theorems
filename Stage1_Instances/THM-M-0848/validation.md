# Intake validation

Item: `S56-M-0848-INTAKE`

Base revision: `444860f481e8bbf64a3357008fd4d01a52006f08`

Base tree: `dee24a14497f877ebd81712a99d2da08de62d7ad`

Validation date: 2026-07-13 (Asia/Shanghai)

Validation covers target membership, source and scope boundaries, the planned dossier structure,
the exact open downstream DAG, current input hashes, JSON and Python syntax, a discovery-only
pinned Lean API probe, prohibited-construct hygiene, and whitespace. It does not validate an exact
theorem statement or proof because the catalog supplies neither.

The initial working tree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It points to the canonical pinned artifacts and was used
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

## Environment fingerprint

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision/tree:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Binomial-random-graph definitions SHA-256:
  `c8effb70a7e4605a077198e04a771ecc8cba255a2243de9cd76a162788766dc7`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0848` | 0 | rank 1403, planned, score 86, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | only pre-existing untracked `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6222,6227 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl` Renyi Institute's `1959-11.pdf`, then `sha256sum`, `pdfinfo`, `pdftotext`, and page inspection | 0 | inspected eight-page primary scan; fixed-edge definition and four distinct result families identified; observed PDF SHA-256 `b41fac...e8108a`; no exact target or H0 admission |
| Crossref query for DOI `10.1214/aoms/1177706098` | 0 | Gilbert 1959 bibliographic identity, journal, volume, issue, and pages confirmed; primary theorem text not admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the recorded fingerprint |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0848/IntakeProbe.lean)` | 0 | nine adjacent completed `G(V,p)` graph/measure APIs elaborated; output SHA-256 `0872fce82a29f2fb8ce53604c2de1c8104d707b29f5ca1ccf3235b271c489215`; no target declaration or proof credit |
| `rg -n -i --glob '*.lean' 'THM.?M.?0848\|Erd[oőö]s.?R[eé]nyi.*random graph\|random graph.*Erd[oőö]s.?R[eé]nyi\|binomialRandom' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | located only the binomial random-graph definitions/results (plus their unfinished desired edge-count result), and no source-frozen `THM-M-0848` proposition; intake discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0848/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0848/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H5/M4/R4 boundary, null target, hashes, exact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0848/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited declaration/proof-escape `rg` scan over `IntakeProbe.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0848 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; the preceding per-file checks cover untracked artifacts |

## Known downstream failures

- The catalog phrase is not a truth-valued proposition. It selects neither `G(n,m)` nor `G(n,p)`,
  neither a definition nor a theorem, and none of the distinct finite or asymptotic conclusions.
- No repository-owned immutable primary source, exact result selection, incorporated-definition and
  premise/conclusion/proof-boundary crosswalk, corrections audit, or independent source review is
  accepted.
- Graph and probability encodings, parameter ranges, ordered binders, hypotheses, exact conclusion,
  limiting regime, and boundary cases remain open. Neighbor and duplicate ownership must be
  resolved without substitution.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  transport, or removed-hypothesis/domain/binder/boundary mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition,
  provenance/trust closure, readable reconstruction, hermetic replay, deterministic evidence
  bundle, independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze ambiguity and open
the downstream DAG. Only the integration lane may accept the provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0848-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.

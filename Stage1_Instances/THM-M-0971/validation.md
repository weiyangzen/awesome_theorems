# THM-M-0971 intake validation

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`). Validation date: 2026-07-13
(`Asia/Shanghai`).

This validation covers the planned dossier, scope and non-substitution boundaries,
source-statement crosswalk, open task DAG, structured intake invariants, and a narrow pinned Lean API
probe. It does not validate a canonical Shearer proposition or proof because neither is frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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

## Source inspection

The six catalog lines originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Crossref and Springer metadata identified the
matching 1985 Combinatorica paper, DOI `10.1007/BF02579368`. Dated remote responses had observed
SHA-256 digests `1eff4f19...29cd6` (Crossref, 2,858 bytes) and
`9a6d4657...ce655` (publisher page, 235,298 bytes). They were temporary discovery inputs, not
replay-stable validation recipes or accepted H0 artifacts. No primary full text was added to the
repository.

## Commands and results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0971` | 0 | rank 1505; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 7092,7097 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa...` |
| Crossref and Springer landing-page inspection for DOI `10.1007/BF02579368` | 0 | matching author, year, venue, pages, symmetric threshold abstract, and announced general sharp bound; H1 source lead only |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded above; package worktree clean |
| bounded exact-topic `rg` search over pinned mathlib and repository-local Lean | 1 (expected no match) | no Shearer, Lovasz Local Lemma, or independence-polynomial declaration; discovery-only, not an external absence claim |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0971/IntakeProbe.lean` | 0 | eight event-independence, intersection, complement, graph independent-set, neighborhood, and degree APIs elaborated; stdout SHA-256 `193db404...8dac2`; no target theorem declared |
| `python3 -m json.tool` over all structured artifacts and root worker packet | 0 | JSON syntax valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0971-pycache python3 -m py_compile Stage1_Instances/THM-M-0971/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0971/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, pins, null target, H1/M4/R4 boundary, artifact hashes, receipt, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0971/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited Lean construct scan | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null FILE` plus final scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |

## Known open gates

An accepted immutable primary edition, exact proposition, dependency and polynomial definitions,
ordered binders, inequalities, original/general/symmetric/optimality boundary, corrections and
errata, and independent source review remain open. So do the canonical Lean expression and
environment fingerprints, checked transports, statement mutations, exhaustive anchor audit,
discovery and obligation freezes, typed graphs, proof and composition, trust and provenance
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion. These open gates do not invalidate a
truthful self-tested `planned` intake.

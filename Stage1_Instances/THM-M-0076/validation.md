# Intake validation

Base revision: `0d2c3bdcd192266bc255ac3d5186da604517145a` (tree
`eafbcb48efd51d9cda34f0fc1afe780434abad64`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and non-substitution
boundaries, the six-node open task DAG, scoped intake invariants, and a narrow pinned Lean boundary
probe. It does not validate a canonical Brauer-character proposition or proof because neither is
frozen. The automation-provided canonical `.lake` symlink was pre-existing and used read-only; no
dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker
run is nonrelease evidence.

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
- Ordinary character module SHA-256:
  `fba5f95dd3b9346579b3ac042b9d8cb84bc7de8e400e4dc6c17ecf9e3b6a3b77`.
- Unrelated Haar modular-character module SHA-256:
  `b397fa221cf5b605f3212baf045d24b21f44907b35b75875e7daf454ffb5e047`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0076` | exit 0; rank 1104, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 561,566 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/<DOI>` for `10.2307/1968918`, `10.2307/1968774`, and `10.2307/2007097` | exit 0 for each on 2026-07-13; response SHA-256 values `976b72...`, `b98b27...`, and `737e09...`; returned 1941 Brauer-Nesbitt and Brauer modular-character records and a 1955 Brauer-Tate character record, all non-credited metadata leads rather than exact primary sources |
| `git -C Formalizations/Lean/.lake/packages/mathlib grep -in -E 'Brauer[ -]?character\|character[ -]?Brauer\|p-regular\|prime-regular\|p regular\|prime regular\|modular representation' HEAD -- Mathlib` | exit 0 on 2026-07-13; only an incidental `Regular.lean` false positive matched, so no exact finite-group Brauer-character surface was located in the pinned mathlib tree by this query |
| `rg -n -i 'Brauer[ -]?character\|character[ -]?Brauer\|p-regular\|prime-regular\|p regular\|prime regular\|modular representation' Formalizations/Lean/AwesomeTheorems Stage1_Instances --glob '!Stage1_Instances/THM-M-0076/**'` | exit 0 on 2026-07-13; only unrelated regularity/modularity occurrences matched and no repo-local exact target artifact was located by this query |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0076/IntakeProbe.lean)` | exit 0; seven boundary APIs elaborated; three inspected declarations reported only `propext`, `Classical.choice`, and `Quot.sound`; no Brauer-character or target declaration was added |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for every finalized JSON artifact |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0076-pycache python3 -m py_compile Stage1_Instances/THM-M-0076/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0076/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target/DAG identity, source and pin hashes, null target, H5/M4/R4 boundary, artifact inventory, provisional packet, Lean replay, and six open tasks agree |
| `rg -n --glob '*.lean' '(^|[^A-Za-z])(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)([^A-Za-z]|$)' Stage1_Instances/THM-M-0076` | exit 1 as expected; no prohibited declaration or proof escape matched |
| scoped `git diff --no-index --check /dev/null <new-file>` loop, followed by `git diff --check -- Stage1_Instances/THM-M-0076 .stage1-worker-selftest.json` | exit 0; every new file passed explicit whitespace validation, with no tracked-diff diagnostics |

## Known open gates

An accepted source edition and exact theorem passage, reconciliation of the catalog's 1956 date
with the discovered 1941/1955 leads, theorem identity, complete definition/assumption/proof/errata
crosswalk, independent source review, finite group, prime, prime-regular domain, modular system,
coefficient fields, representation/character conventions, ordered binders, hypotheses, conclusion,
and boundary cases remain open. So do canonical target elaboration and mutations, exhaustive
anchor/provenance/trust audits, discovery and obligation freezes, typed graphs, proof and
composition, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion. These gates do not
invalidate a truthful self-tested `planned` intake.

The provisional `H5` classification is the standard's ill-posed/unstable-proposition branch, not a
claim that a corrected Brauer-character theorem is refuted or open. It blocks ordinary proof
execution until source identification produces a stable exact proposition, at which point the
human-proof debt must be re-audited rather than inherited.

Schema authority remains an integration boundary: the dossier uses the repository's prevalent
`stage1-instance-intake/1.0`, `stage1-open-task-dag/1.0`, and `stage1-node-receipt/1.0` identifiers,
and the scoped checker enforces its intake fields, but no repository-wide published strict-schema
validator was found. This worker does not claim the master schema-acceptance gate.

The structured recipes state the environment policy required of a replay runner; this worker did
not enforce network isolation at the operating-system level. The checker made no network request,
and its Lean replay used the automation-provided external `.lake` symlink read-only, so neither
recipe is hermetic or release evidence.

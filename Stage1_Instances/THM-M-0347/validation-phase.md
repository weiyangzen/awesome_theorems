# THM-M-0347 validation-phase evidence

Item: `S56-M-0347-VALIDATION`. Base revision:
`57d8d01796f84ffc9de9adf1f5d0723555e7babb`; base tree:
`cdea5b3fad713816ee6c9ed6aae7a10f9009a18e`.

## Validation scope

The node recipe re-elaborates the exact statement, exact vendored ATLAS source,
frozen conditional composition, proof root, and a new differential root in a
fresh temporary output directory. Every Lean subprocess runs at trust level
zero inside a Bubblewrap network namespace with the host root read-only.
`Validation.lean` imports neither `Proof` nor `ObligationTree`; it separately
reconstructs the frozen partial sum and mean transports and composes
`fejer_uniform_convergence` to the unchanged target.

The selected source, proof, and differential declarations report exactly
`propext`, `Classical.choice`, and `Quot.sound`. Lean's `assert_no_sorry` and
`#print sorries` check nine terminal and differential declarations, and a
comment-stripped source scan rejects placeholders, bodyless declarations,
unsafe/native/oracle shortcuts, and external implementations. These are narrow
trust observations, not an accepted complete transitive foundation/TCB audit.

## Commands and results

Commands ran from this worker clone on 2026-07-15 (Asia/Shanghai). The
automation-provided pinned `.lake` symlink was reused without mutation. No
`lake update`, `lake build`, clone, fetch, dependency checkout, or network
request ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0347
  exit 0: rank 840, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0347/check_validation.sh
  exit 0: network-isolated trust-zero replay elaborated Statement,
  AtlasFourierSeries, ObligationTree, Proof, and the Proof-free differential
  Validation module; every requested axiom and sorry report passed

python3 -B Stage1_Instances/THM-M-0347/check_validation.py
  exit 0: exact target, hashes, source hygiene, selected provenance, pin,
  receipt, recipe, fail-closed decisions, and worker packet passed

env PYTHONOPTIMIZE=1 python3 -B \
  Stage1_Instances/THM-M-0347/check_validation.py
  exit 1 as expected: fail-closed checker rejected disabled assertions

python3 Stage1_Instances/THM-M-0347/check_statement.py
  exit 0 on final retry: exact expression hash `ae3d7a...` and all four
  statement mutations passed; an earlier attempt was blocked before
  elaboration by the canonical `flt-regular` package's then-invalid Git HEAD

python3 Stage1_Instances/THM-M-0347/check_obligation_tree.py
  exit 0: 15 obligations and all typed graph invariants passed; root remains M3

python3 -m json.tool Stage1_Instances/THM-M-0347/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0347/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m0347-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0347/check_validation.py
  exit 0: checker compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-0347 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The required `lake env lean` adapter and legacy statement checker initially
could not elaborate because the canonical pinned `flt-regular` package had an
invalid Git `HEAD`. The worker did not repair or mutate that shared package.
Another concurrent automation worker restored its pinned HEAD at 14:05 local
time; the final retry then passed all mutations. The recorded validation recipe
still identifies the pinned Lean executable directly and supplies an explicit
already-compiled `LEAN_PATH`, excluding `flt-regular`, so its evidence does not
depend on that external repair.

The predecessor `check_proof.sh` was also run: its Lean replay passed the exact
root and eight support declarations, after which its snapshot-bound Python
checker correctly rejected the current integrated revision. Validation binds
the immutable proof artifacts by hash and directly replays their Lean sources;
it does not mistake predecessor snapshot drift for a proof failure.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Exact statement, conditional composition, exact proof root, and separately reconstructed root elaborate at trust zero. |
| Placeholder and unsafe boundary | pass | Lean sorry checks and a comment-stripped scan found no prohibited construct. |
| Trust observation | provisional pass | All selected declarations report exactly the three observed axioms; an accepted complete foundation and TCB profile is absent. |
| Selected provenance | provisional pass | The exact vendored source has upstream and local Git blob `5d399cda...`, SHA-256 `f205a16c...`, pinned origin metadata, retained license, and clean mathlib pin. |
| Proof dependency | fail closed | `S56-M-0347-PROOF` is only `[_]`, not master accepted. |
| Frozen internal composition | fail closed | The external proof route has no accepted mapping to independently checked per-node frozen composition certificates. |
| License and full provenance | fail closed | ATLAS CC BY-NC 4.0 and its no-training/no-evaluation rider are unreviewed; the source postdates the anchor audit; complete transitive provenance/SBOM is absent. |
| Hermetic replay | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold bootstrap, offline-restorable closure, or deterministic release bundle. |
| Independent verification | fail closed | The differential proof shares this worker, checkout, Lean executable, and cache; there is no distinct signed runner or independent minimal release verifier. |

The first failed node gate is
`dependency.S56-M-0347-PROOF.master_acceptance`; the first failed proof-
acceptance gate is `provenance.ATLAS-license-rider-compatibility`; the first
failed release gate is `S56-10.6-HERMETIC-COLD-BUILD`. Accepted debt remains
`H1/M3/R4` with no accepted closed obligation. `audit_complete=false` and
`theorem_complete=false`.

This is self-tested `blocked` worker evidence. It claims no accepted `M0-P`,
`E0/E1`, license approval, complete trust/provenance, independent validation,
release, theorem completion, or master acceptance.

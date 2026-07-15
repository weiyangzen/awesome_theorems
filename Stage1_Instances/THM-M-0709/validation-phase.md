# THM-M-0709 validation-phase result

Item `S56-M-0709-VALIDATION` ran against base revision
`443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b` (tree
`c5771c47c12b80aba613e6d844570f83b39ded6d`). The phase adds no PCP
reduction proof content. Its verdict is `blocked`; provisional `[_]` means
only that this negative, fail-closed validation packet was implemented and
self-tested. It is not acceptance of the proof dependency or any failed gate.

## Narrow replay

The validator copied `Statement.lean`, `ObligationTree.lean`, `Proof.lean`,
and `Validation.lean` to a fresh temporary directory. Each source was
elaborated with pinned Lean 4.29.0 at `--trust=0` under Bubblewrap, with
outbound networking disabled, a read-only host root, fixed locale and
timezone, and only the temporary directory writable. It used only the
already compiled package roots needed by this target. It ran no `lake update`,
`lake build`, dependency clone, dependency fetch, or cache repair.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It separately
reconstructs the generic many-one pullback, wraps the pinned fixed-input
halting theorem, and composes those into the exact frozen root only from an
explicit `ValidationHaltingPredicate input <=0 HasSolution` input. That input
is precisely the missing reduction. The differential route therefore checks
the terminal argument without supplying a premise-free PCP undecidability
proof.

During read-only audit, a Lake command invoked by a collaborating audit worker
attempted to bootstrap the unrelated pinned `flt-regular` dependency before it
was interrupted. The shared canonical cache now contains an incomplete
`flt-regular` Git repository with no `HEAD` and no compiled artifact. This
incident is recorded rather than hidden or repaired. The theorem-scoped replay
bypasses that unused package by constructing `LEAN_PATH` from the existing
pinned compiled roots, but the shared cache cannot support release evidence.

## Gate decisions

| Gate | Decision | Evidence or boundary |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, root interface, partial proof, pinned terminals, and differential probes elaborate at trust zero. |
| Placeholder/unsafe observation | pass in observed boundary | Five proof declarations and the validation bundle are sorry-free; local parser-aware scans pass; the validation closure reports no bodyless nonaxiom or unsafe declaration. |
| Axiom observation | provisional pass | Every checked proof-bearing declaration reports exactly `propext`, `Classical.choice`, and `Quot.sound`. No accepted target-specific foundation or full TCB profile exists. |
| Selected provenance | partial pass | Mathlib revision, tree, clean state, remote, the Halting and Reduce source/blob/olean identities, and license agree. The serialized full transitive closure is absent. |
| Proof dependency | fail closed | `S56-M-0709-PROOF` is provisional `[_]`, not master accepted. |
| Exact root | fail | The halting-to-binary-PCP reduction is still an explicit premise. The accepted instance surface stays `[H1,M4,R3]`; the frozen graph and provisional proof evidence classify the exact root interface as `[H1,M3,R3]`. No obligation is newly accepted. |
| Hermetic release | fail closed | Lean children are network-isolated and read-only-root, but orchestration is not recipe-wide isolated and the cache is contaminated and warm, not a clean empty-cache cold replay or offline restoration. |
| Independent verification | fail closed | Differential probes share this worker, checkout, kernel, and cache; no second signed runner or independently implemented minimal release verifier exists. |

The validation closure walk observed 4,743 declarations across 163 modules and
reported `bodyless_nonaxioms=[]` and `unsafe=[]`. This is useful trust
observation, not the required serialized, content-addressed declaration,
import, compiled-artifact, executable, compiler/bootstrap, plugin, and SBOM
closure.

## Commands and results

All commands ran on 2026-07-15 from this worker clone.

```text
$ timeout 300 bash Stage1_Instances/THM-M-0709/check_proof.sh
exit 2 after a collaborating audit worker immediately interrupted the live
process when it printed `info: flt-regular: cloning
https://github.com/leanprover-community/flt-regular.git`; no validation credit
was granted, and the command was not rerun

$ python3 -B Stage1_Instances/THM-M-0709/check_validation.py --probe
exit 0; network-isolated trust-zero replay passed; closure declarations=4743,
modules=163, bodyless_nonaxioms=[], unsafe=[]

$ python3 Docs/tools/check_stage1_standard.py
exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

$ python3 scripts/stage1_target.py check
exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-0709
exit 0; rank 750, planned lifecycle, theorem_complete=false

$ python3 -B Stage1_Instances/THM-M-0709/check_obligation_tree.py
exit 0; 18 obligations and 81 typed edges passed; root remains open M3

$ python3 -B Stage1_Instances/THM-M-0709/check_validation.py \
    --worker-packet .stage1-worker-selftest.json
exit 0; receipt, recipe, worker packet, hashes, replay, trust observation,
selected provenance, and fail-closed decisions passed

$ python3 -m json.tool Stage1_Instances/THM-M-0709/validation-spec.json >/dev/null
$ python3 -m json.tool Stage1_Instances/THM-M-0709/validation-receipt.json >/dev/null
$ python3 -m json.tool .stage1-worker-selftest.json >/dev/null
exit 0 for all three JSON documents

$ PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0709-validation-pycache \
    python3 -m py_compile Stage1_Instances/THM-M-0709/check_validation.py
exit 0; checker syntax compiled outside the repository

$ git diff --check -- Stage1_Instances/THM-M-0709 \
    .stage1-worker-selftest.json
exit 0; no whitespace errors; the checker separately verified changed-file
text hygiene
```

The first workflow failure is
`dependency.S56-M-0709-PROOF.master_acceptance`. The first mathematical root
failure is `M0709-C-MACHINE.root_kernel_closure`. Full retry requires
dependency acceptance, a complete placeholder-free computable reduction into
the frozen binary-PCP predicate, accepted full provenance/foundation/TCB/SBOM
evidence, a clean cold offline replay, and a distinct signed independently
provisioned verifier with a minimal independent checker.

`audit_complete=false` and `theorem_complete=false`. This packet grants no
`E0/E1`, accepted `M0-*`, release, or master acceptance.

The accepted-state first open cut remains `M0709-N-HALTING`,
`M0709-C-MACHINE`, `M0709-C-MPCP`, `M0709-X-SOURCE`, and
`M0709-X-FOUNDATION`. The proof-phase provisional mathematical cut is
`M0709-C-MACHINE`, `M0709-C-MPCP`, `M0709-T-MPCP-PCP`,
`M0709-N-BINARY`, and `M0709-T-REDUCTION`. These two views are intentionally
not conflated.

The unused `flt-regular` Git metadata continued changing concurrently under
other scheduler workers after the narrow replay. It is absent from the
constructed `LEAN_PATH` and therefore unbound from the positive theorem-scoped
kernel observation. The concurrency independently prevents stable-cache,
freshness, hermetic, and release evidence; it does not turn the excluded
package into a proof input.

# THM-M-0498 validation-phase result

Item `S56-M-0498-VALIDATION` ran against base revision
`823dfcd5e231e84436ac3d88948d8e669c168fdb` (tree
`a87f5f99350f49ddeb9d7df23dc6e0fe6fe3011f`). The phase adds no
explicit-formula proof content. Its verdict is `blocked`; provisional `[_]`
means only that this negative/fail-closed validation packet was implemented
and self-tested. It is not acceptance of the proof dependency or any failed
gate.

## Narrow replay

The validator copied `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Validation.lean` to a fresh temporary directory. Each source was elaborated
with pinned Lean 4.29.0 at trust level zero under Bubblewrap with outbound
networking disabled for each Lean invocation, a read-only host root, fixed
locale/timezone, and only the temporary directory writable. Python, Lake, and
Git orchestration performed local inspection on the host and did not run in a
recipe-wide network namespace. The final theorem-scoped replay uses only the
existing compiled package roots needed by THM-M-0498 and mounts them read-only.
During review, an accidental Lake discovery command reconciled the unrelated
`flt-regular` package, recloned its pinned source, and left its compiled
artifact missing. No repair fetch/build was attempted; the shared cache is
therefore contaminated nonrelease evidence.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It separately
wraps mathlib's proved von Mangoldt logarithmic-derivative theorem and repeats
the literal conditional composition into the frozen root. The latter still
requires the analytic explicit-formula package as an input. These probes are
same-worker differential corroboration, not a second terminal proof body or an
independent-runner attestation.

## Gate decisions

| Gate | Decision | Evidence or boundary |
|---|---|---|
| Narrow kernel replay | pass | The exact statement, frozen conditional composition, proof bridge, and two differential probes elaborate at `--trust=0`. |
| Placeholder/unsafe observation | pass in observed boundary | `Proof.lean` and `Validation.lean` use `assert_no_sorry` and print-sorries probes; supplemental scans cover all four local modules, and the validation closure walk reports no bodyless nonaxiom or unsafe declaration. |
| Axiom observation | provisional pass | Every checked terminal, wrapper, composition, and probe reports only `propext`, `Classical.choice`, and `Quot.sound`. No accepted theorem-specific foundation or complete TCB profile exists. |
| Selected provenance | partial pass | Mathlib revision/tree/remote, terminal body/source/olean, and license agree. The serialized transitive import/artifact/TCB closure is absent. |
| Proof dependency | fail closed | `S56-M-0498-PROOF` is only provisional `[_]`, not master accepted. Its integrated Lean source replays, but its old phase checker is tied to its former base/DAG/packet. |
| Exact root | fail | The analytic package and its Perron, contour, residue, trivial-zero, and zero-sum packages remain unproved. Root state stays `[H3,M4,R4]`; no frozen proof obligation is newly closed. |
| Zero-enumeration realizability | fail closed | The structure elaborates, but no checked inhabitant of `NontrivialZeroEnumeration` is present. |
| Hermetic release | fail closed | The Lean invocations are network-isolated and read-only-root, but orchestration is not recipe-wide isolated and the shared cache is contaminated/warm rather than a clean checkout, empty-cache cold build, or offline archive restoration. |
| Independent verification | fail closed | The differential probes use this worker, checkout, kernel, and cache; no second signed runner or independently implemented minimal release verifier exists. |

The validation closure walk observed 56,102 declarations across 1,826 modules
and reported empty bodyless-nonaxiom and unsafe sets. This is useful trust
observation, but it is not a serialized, content-addressed declaration/import,
compiled-artifact, executable, compiler/bootstrap, plugin, and SBOM closure.

## Commands and results

All commands ran on 2026-07-14 from the worker clone. The planned validation
commands ran no `lake update`, `lake build`, or dependency fetch. The accidental
review-time Lake discovery described above did mutate `.lake`; that incident is
preserved as a blocker rather than repaired or hidden.

```text
$ python3 -B Stage1_Instances/THM-M-0498/check_validation.py --probe
exit 0; network-isolated trust-zero replay passed; closure declarations=56102,
modules=1826, bodyless_nonaxioms=[], unsafe=[]

$ python3 Docs/tools/check_stage1_standard.py
exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

$ python3 scripts/stage1_target.py check
exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-0498
exit 0; rank 258, planned lifecycle, theorem_complete=false

$ python3 -B Stage1_Instances/THM-M-0498/check_obligation_tree.py
exit 0; 15 obligations and 33 typed edges passed; root remains open M4

$ python3 -B Stage1_Instances/THM-M-0498/check_validation.py \
    --worker-packet .stage1-worker-selftest.json
exit 0; receipt, recipe, packet, hashes, replay, trust observation, selected
provenance, and all fail-closed decisions passed

$ python3 -m json.tool Stage1_Instances/THM-M-0498/validation-spec.json >/dev/null
$ python3 -m json.tool Stage1_Instances/THM-M-0498/validation-receipt.json >/dev/null
$ python3 -m json.tool .stage1-worker-selftest.json >/dev/null
exit 0 for all three JSON documents

$ PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0498-validation-pycache \
    python3 -m py_compile Stage1_Instances/THM-M-0498/check_validation.py
exit 0; checker syntax compiled outside the repository

$ git diff --check -- Stage1_Instances/THM-M-0498 \
    .stage1-worker-selftest.json
exit 0; no whitespace errors; the checker separately verified all changed
files for final newline, CR/NUL, and trailing whitespace
```

The first failed gate is
`dependency.S56-M-0498-PROOF.master_acceptance`. The root-critical mathematical
cut remains `M0498-T-ANALYTIC`. Full retry requires proof acceptance and root
implementation, checked enumeration realizability, accepted complete
provenance/foundation/TCB/SBOM evidence, a clean cold offline replay, and a
distinct signed independent verifier with a minimal independent checker.

`audit_complete=false` and `theorem_complete=false`. This packet grants no
`E0/E1`, accepted `M0-*`, release, or master acceptance.

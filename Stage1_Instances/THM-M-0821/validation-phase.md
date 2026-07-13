# THM-M-0821 validation-phase evidence

Item: `S56-M-0821-VALIDATION`. Base revision:
`4a10a7a4ddff88e302d5a303b16dd687d9468f63`; base tree:
`730de242597680b39a7087d3204dfd1e6c41c60e`.

## Validation scope

The node recipe re-elaborates the exact frozen statement, all six frozen package-composition
declarations, the proof root and its pinned terminal, and a separately written exact-root probe in
temporary output space. Every Lean subprocess runs in a Bubblewrap network namespace with the host
filesystem read-only except for the temporary directory. `Validation.lean` imports neither
`Proof` nor `ObligationTree`; it independently builds the lower-middle witness and applies
`IsAntichain.sperner`. This is same-worker differential corroboration, not an independent-runner
attestation, and it receives no separate proof credit.

All proof and differential declarations are sorry-free and report exactly `propext`,
`Classical.choice`, and `Quot.sound`. The composition declarations report nonempty subsets of that
observed profile. The validator binds the exact target expression, registry denominator, frozen
graph and predecessor receipt hashes, mathlib revision/tree, clean dependency source, LYM
source/blob/Sperner-body/compiled-object hashes, remote, license, and tool identities. No prohibited
proof or implementation mechanism was found.

This is narrow, nonrelease validation. The proof prerequisite is only `[_]`; accepted authority
remains `[H1, M3, R4]` with no accepted receipt or closed obligation. The eight internal LYM
source-body decomposition plans still lack abstract-child composition certificates and receive no
individual closure credit.

## Commands and results

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, clone, fetch, checkout,
dependency mutation, or network operation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0821
  exit 0: rank 1379, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0821/check_validation.sh
  exit 0: network-isolated exact proof and Statement-only differential roots elaborated; all six
  compositions were covered; seven proof/differential assertions plus the obligation terminal
  sorry report passed; stdout was
  11830 bytes at SHA-256 2f60f518d7193b8826f907c7d251fbf7731ca30ad7bdad8439ef1958eb0e05a6

python3 -B Stage1_Instances/THM-M-0821/check_validation.py
  exit 0: exact target/composition replay, hygiene, selected trust/provenance, frozen hashes, pin,
  receipt, recipe, and worker packet passed; authority and release gates failed closed

python3 -m json.tool Stage1_Instances/THM-M-0821/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0821/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0821-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0821/check_validation.py
  exit 0: validator compiled outside the repository tree

rg -n --glob '*.lean' '<prohibited construct pattern>' \
  Stage1_Instances/THM-M-0821/{Statement,ObligationTree,Proof,Validation}.lean
  exit 1 with empty output: expected pass, no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-0821 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed no-index checks
```

Snapshot-bound predecessor Python checkers are not current validation gates: `check_proof.py`
expects its proof-phase base and worker packet, while `check_obligation_tree.py` preserves its
pre-integration workflow snapshot. This phase binds their immutable artifacts and directly replays
the Lean proof instead of misreporting those expected snapshot mismatches as proof failures.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel and composition replay | provisional pass | The exact statement, six package compositions, exact proof root, terminal declaration, and differential exact root elaborate under network isolation. |
| Placeholder and unsafe boundary | pass | Lean sorry reports and a comment-stripped scan found no placeholder, bodyless, unsafe/native/oracle, or external implementation construct. |
| Trust observation | provisional pass | Root routes report exactly the candidate `propext`, `Classical.choice`, and `Quot.sound` set; accepted foundation and complete transitive TCB closure remain open. |
| Selected provenance | provisional pass | Exact local hashes and the pinned LYM source/blob/body/olean, clean revision/tree, remote, manifest, license, and tool hashes agree; complete transitive provenance and SBOM do not exist. |
| Internal source decomposition | fail closed | Eight source-body plans lack abstract-child composition certificates, so their mapped nodes receive no individual closure credit. |
| Structured authority | fail closed | `S56-M-0821-PROOF` is only `[_]`; the instance and graph accept no receipt or closed obligation and remain H1/M3/R4. |
| Hermetic replay | fail closed | Shared warm `.lake`; no separate immutable clean checkout, empty-cache cold bootstrap, content-addressed offline restoration, complete TCB/SBOM, or deterministic release bundle. |
| Independent verification | fail closed | The different reconstruction shares this worker, checkout, kernel, and cache; no distinct identity, runner, signature, or independently implemented minimal release verifier exists. |

The first failed node gate is `dependency.S56-M-0821-PROOF.master_acceptance`; the first failed
release gate is `S56-10.6-HERMETIC-COLD-BUILD`. The accepted vector remains `[H1, M3, R4]`.
Primary-source H0, independently reviewed R0, full trust/provenance, `AUDIT-Z`, `THEOREM-Z`,
release, and theorem completion are false. This self-tested worker evidence claims no `E1`,
accepted `M0-W`, independent validation, release, or master acceptance.

# THM-M-1065 validation-phase evidence

Item: `S56-M-1065-VALIDATION`. Base revision:
`3c3068d5f6ad9d773ce52d46d68a43c2a9272683`; base tree:
`f9413d0895f280a855bb16104daf0403d51a24fb`.

## Validation scope

The structured recipe re-elaborates the exact statement, the separate obligation-tree composition
interface, both available partial proof declarations, the fail-closed anchor decisions, and two
separately written statement/boundary probes in disposable output space. Every Lean subprocess uses
`--trust=0`, one Lean thread, a fixed locale and timezone, and a Bubblewrap network namespace.
`Validation.lean` imports only `Statement`; it neither states nor proves a KMT coupling, a maximal
tail estimate, or the canonical root.

The available `exists_commonIIDSequences` body constructs independent product-coordinate sequences
with the prescribed iid marginal laws. It is not the dependent KMT coupling and supplies no
discrepancy estimate. `measurableSet_discrepancyEvent` is conditional on genuinely measurable
increments, while `HasLaw` supplies only almost-everywhere measurability. Accordingly, neither body
closes a frozen obligation. All 18 registry terminal proof-body identities are null, all validation
spec IDs in the frozen graph remain pending, and the root stays open at `M4`.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused without mutation. The validation runner constructs `LEAN_PATH` only from
the already-present target-relevant package artifacts and does not invoke project discovery against
the unrelated `flt-regular` dependency. The successful recipe issued no `lake update`, `lake build`,
dependency clone/fetch, or checkout, and every Lean subprocess had its network namespace denied.
The shared mathlib checkout's tracked files were clean and all selected source/blob/olean identities
matched; another concurrent worker temporarily created an untracked scratch directory under that
shared checkout. That scratch is outside this target's inputs, but its presence is another reason the
run is classified as nonrelease rather than a clean-checkout receipt.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1065
  exit 0: rank 507, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-1065/check_anchor_audit.py
  exit 0: pinned mathlib tracked state and substrate checked; no terminal exact KMT candidate credited

python3 Stage1_Instances/THM-M-1065/check_obligation_tree.py
  exit 0: 18 obligations and 75 typed edges checked; zero closed obligations; root open at M4

bash Stage1_Instances/THM-M-1065/check_validation.sh
  exit 0: network-isolated trust-zero replay checked the exact statement, conditional composition,
  two partial proof bodies, two anchor decisions, and two differential statement probes; all were
  sorry-free and no observed axiom exceeded propext, Classical.choice, and Quot.sound

python3 -I -B Stage1_Instances/THM-M-1065/check_validation.py
  exit 0: recipe, authority, frozen hashes, kernel/trust observations, selected provenance, hygiene,
  and truthful failed root/release gates agreed

python3 -m json.tool Stage1_Instances/THM-M-1065/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1065/validation-receipt.json
python3 -m json.tool Stage1_Instances/THM-M-1065/validation-blocker.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m1065-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1065/check_validation.py
  exit 0: validator bytecode compiled outside the repository tree

rg -n --glob '*.lean' '<prohibited construct pattern>' Stage1_Instances/THM-M-1065
  exit 1 with empty output: expected pass; no placeholder, bodyless declaration, unsafe/external
  mechanism, implementation escape, or native oracle occurred in owned Lean source

git diff --check -- Stage1_Instances/THM-M-1065 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed explicit text-hygiene checks
```

The historical `check_proof_evidence.py` is intentionally not replayed. It asserts the old proof
worker's base revision and exact dirty-file packet. This phase instead hash-binds the integrated
proof receipt and blocker, then independently replays the actual Lean declarations.

An additional read-only attempt to run `python3
Stage1_Instances/THM-M-1065/check_statement.py` failed because that historical checker invokes
root-project `lake env lean`; concurrent scheduler activity had left the unrelated shared
`flt-regular` checkout without a resolvable `HEAD`, and Lake's external command failed with exit
128. Root-project discovery can enter dependency resolution, so a shared-cache side effect from that
failed attempt cannot be ruled out and is not credited as evidence; no target or dependency artifact
was intentionally changed by this worker. The successful network-isolated `check_validation.sh`
replay supersedes that attempt's statement-elaboration scope:
it fresh-compiles the exact `Statement.lean` at `--trust=0` from an explicit target-relevant
`LEAN_PATH`. The failed historical checker is excluded from passing evidence and reinforces the
nonrelease shared-cache boundary.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact statement | pass | The canonical target and checked expansion elaborate at the frozen expression fingerprint. |
| Conditional composition | pass, not root closure | `ObligationTree` repackages a complete witness premise, but duplicates its statement namespace and constructs no witness. |
| Partial proof bodies | pass, no frozen closure | The independent-product carrier and conditional event-measurability body elaborate without placeholders. |
| Placeholder and unsafe boundary | pass | Lean sorry reports and a nested-comment-aware source scan found no prohibited mechanism. |
| Trust observation | provisional pass | Checked declarations use only the standard classical mathlib surface; no theorem-specific accepted foundation profile or complete TCB closure exists. |
| Selected provenance | provisional pass | Frozen local hashes plus tracked-clean pinned mathlib revision/tree/remote/license and four source/blob/olean boundaries agree; shared untracked scratch is excluded and disclosed. |
| Structured authority | fail closed | `S56-M-1065-PROOF` is only worker-provisional `[_]`, accepted=false, with zero accepted closed obligations. |
| Exact root kernel closure | fail closed | The dependent KMT coupling, finite-block construction, and uniform exponential maximal-tail estimate have no proof bodies. |
| Hermetic release | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold bootstrap, offline archive restoration, deterministic bundle, or complete SBOM. |
| Independent verification | fail closed | The differential probes share this worker, checkout, kernel, and cache; no distinct signed runner or independent minimal verifier exists. |

The first node gate is `dependency.S56-M-1065-PROOF.master_acceptance`; the first mathematical gate is
`M1065-C-SPACE`; the first release gate is `S56-10.6-HERMETIC-COLD-BUILD`. The remaining theorem cut
is `M1065-C-SPACE`, `M1065-L-BLOCK-COUPLING`, and `M1065-L-MAXIMAL-TAIL`. The root vector remains
`[H2, M4, R4]`. `audit_complete=false` and `theorem_complete=false`.

Status boundary: self-tested worker evidence for a truthful blocked validation process. It claims no
closed frozen obligation, accepted receipt, E0/E1, M0, H0/R0, complete validation, release, audit or
theorem completion, or master acceptance.

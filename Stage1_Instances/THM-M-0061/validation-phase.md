# THM-M-0061 validation-phase result

Item: `S56-M-0061-VALIDATION`

Base revision: `250f9e73cbbb3ebd2da9d0cefff78f0ab8c0d056`

The exact Lagrange proof, every frozen composition, both proof-phase exact roots, and a separately
written exact-root adapter elaborate against pinned Lean 4.29.0 and mathlib `8a178386`. The adapter
imports neither `Proof` nor `ObligationTree`, but it reuses the same pinned mathlib terminal theorem.
It is useful same-worker corroboration, not implementation-diverse or distinct-runner verification.

## Exact validation

The validator obtains pinned executables through `lake env`, copies four Lean modules into a fresh
temporary directory, writes only temporary `.olean` files there, uses trust level zero and a fixed
minimal environment, then removes the directory. The automation-provided `.lake` symlink is reused
read-only. No Lake update/build, dependency clone/fetch, checkout, network request, or `.lake`
mutation is performed.

```text
python3 -B Stage1_Instances/THM-M-0061/check_validation.py
  exit 0
  PASS THM-M-0061 narrow validation
  PASS kernel replay: exact statement, all proof declarations, frozen compositions, two proof roots, and alternate exact-root adapter elaborated
  PASS trust observation: checked declarations depend only on propext, Classical.choice, and Quot.sound
  PASS selected provenance: frozen hashes, four source/blob/olean boundaries, clean mathlib pin, remote, license, and tool identities agree
  PASS hygiene: Lean assert_no_sorry plus a supplemental prohibited-construct scan passed
  FAIL CLOSED authority: proof master acceptance and structured state reconciliation are pending; accepted root remains H1/M3/R4
  FAIL CLOSED trust: no accepted theorem-specific foundation policy or complete transitive declaration/TCB/SBOM closure exists
  FAIL CLOSED hermetic/independent: shared warm .lake and same-worker adapter are neither cold offline replay nor distinct signed verification
  audit_complete=false; theorem_complete=false

bash Stage1_Instances/THM-M-0061/check_proof.sh
  exit 0: all 14 proof declarations were sorry-free and reported only
  [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets in ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0061
  exit 0: rank 1093, planned, L0/rework_required, theorem_complete false
```

The frozen `validation-specs.json` is not reported as a current pass. It belongs to the earlier
obligation-tree phase, invokes `check_obligation_tree.py`, covers no obligation IDs, and expressly
grants no M0 or proof-closure credit. The new node-specific `validation-spec.json` records the
current narrow validation without changing the frozen architecture or pretending the older recipes
validate proof closure.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The exact statement, all 14 proof declarations, every frozen composition, two exact proof roots, and the separate adapter elaborate in a fresh temporary module directory. |
| Placeholder and unsafe boundary | pass | `assert_no_sorry` checks the pinned terminal and adapter transitively; all 14 proof declarations print sorry-free, and a comment-stripped scan finds no placeholder, bodyless declaration, unsafe/native/oracle, or external implementation construct. |
| Trust observation | provisional pass | Checked declarations depend only on `propext`, `Classical.choice`, and `Quot.sound`; no unexpected axiom is observed. A theorem-specific accepted foundation policy and complete transitive trust closure are absent. |
| Selected provenance | provisional pass | Frozen owned hashes, exact terminal/body identity, four source/blob/olean triples, immutable clean mathlib revision/tree, canonical remote, tool hashes, manifest, and license agree. This is not complete transitive declaration/TCB/SBOM provenance. |
| Structured authority | fail closed | The proof prerequisite is only `[_]`; the authoritative instance and graph remain H1/M3/R4 with `root_closed=false`, no accepted receipt, and no accepted closed obligation. |
| Frozen recipe freshness | fail closed | `validation-specs.json` is obligation-tree evidence with empty coverage and an explicit no-proof-credit boundary. Only the new validation-node recipe applies to this snapshot. |
| Hermetic replay | fail closed | Shared warm `.lake`; no immutable clean checkout, cold empty-cache offline restoration, enforced network namespace, complete bootstrap/TCB inventory, or deterministic restorable SBOM archive. |
| Independent verification | fail closed | The separate adapter shares the terminal proof body, worker identity, checkout, and cache; no distinct signed verifier, independent runner, or independently implemented minimal verifier exists. |

The first failed node gate is `dependency.S56-M-0061-PROOF.master_acceptance`; the first failed
release gate is `S56-10.6-HERMETIC-COLD-BUILD`. This is genuinely self-tested validation evidence,
but it grants no accepted `M0-L`, release-grade `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-
completion credit. `audit_complete=false` and `theorem_complete=false` remain explicit.

# THM-M-0526 release decision

Item `S56-M-0526-RELEASE` has the exact verdict **blocked**. The lifecycle remains `planned`, the
recorded dossier vector remains `[H2, M4, R4]`, and both `AUDIT-Z` and `THEOREM-Z` remain blocked.
`audit_complete=false`, `theorem_complete=false`, and no receipt is accepted. Provisional `[_]`
means only that this negative release decision was implemented and self-tested; it is not release,
theorem completion, or master acceptance.

## Evidence reconciliation

The exact statement elaborates at trust level zero. The frozen child-to-parent certificates also
elaborate, but `compose_root` consumes existence and uniqueness packages as explicit premises; it
does not supply their proof bodies. `Proof.lean` genuinely implements square commutativity and the
finite open-cover subdivision lemma. The validation probe separately reconstructs those same two
areas without importing the proof or obligation-tree modules. These checks observe only `propext`,
`Classical.choice`, and `Quot.sound` and find no prohibited proof device in the checked local
boundary.

That evidence is partial. The frozen graph grants no accepted proof-body credit. Its authoritative
nine-node cut is unchanged because no receipt is accepted. After provisionally replaying two of its
leaves, the implementation frontier still contains seven nodes: `SVK-CHANGE-BASEPATH`, `SVK-WORD-DEFINITION`,
`SVK-REFINEMENT-INVARIANCE`, `SVK-HOMOTOPY-INVARIANCE`, `SVK-LIFT-HOM`, `SVK-GENERATION`, and
`SVK-AGREEMENT-ON-WORDS`. Consequently `LiftExistence` and `LiftUniqueness` remain unimplemented,
the exact root is not kernel closed, and machine debt remains `M4`.

The first workflow failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`. Validation is projected `[_]`, and
its receipt is provisional, `accepted=false`, `release_grade=false`, and not master accepted. The
first substantive theorem failure is `SVK-CHANGE-BASEPATH`. Human source and readability remain
recorded as `H2/R4`; however, the dossier does not identify the concrete mathematical condition or
gap required for `H2`, while its structural outline may warrant a different open `R` level. Their
classifications, source boundaries, inventories, evidence, public projections, and independent
reviews need reconciliation. Those audit-record gaps, rather than the open proof root itself, keep
`AUDIT-Z` blocked.

The first intrinsic release failure is `S56-10.6-HERMETIC-COLD-EMPTY-CACHE`. The strongest replay
used the scheduler-provided shared warm `.lake` symlink and the current worker checkout, not an
immutable clean empty-cache cold build or offline archive restoration. Complete transitive
provenance and TCB closure, SBOM/licenses, two distinct signed clean-runner attestations, an
independently implemented minimal verifier, protected adversarial CI, and a deterministic release
bundle are also absent.

## Commands and results

Commands ran on 2026-07-15 from base revision
`bb2a1ec294938a22b88699da0d30ced721d8ee7b` (tree
`d8d58ab94c83274db18efd3af989171acb898759`).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0526
  exit 0: rank 583; lifecycle planned; legacy artifacts unaccepted;
  theorem_complete=false

git status --short --untracked-files=all
  exit 0: the scheduler-provided Formalizations/Lean/.lake symlink and the four
  declared release changed paths are present; no unrelated target changed

python3 -B Stage1_Instances/THM-M-0526/check_obligation_tree.py
  exit 0: 17 obligations, 9 leaves, 16 proof edges, the frozen denominator,
  and all seven typed graph families agree

bash Stage1_Instances/THM-M-0526/check_proof.sh
  exit 0: fresh temporary Statement and ObligationTree oleans plus Proof.lean
  elaborated with --trust=0; the three partial declarations used only the
  observed classical axiom subset

python3 -B Stage1_Instances/THM-M-0526/check_release.py \
  --worker-packet .stage1-worker-selftest.json
  exit 0: dependency nonacceptance, H2/M4/R4, the unchanged frozen nine-node
  cut, seven-node proof frontier, false AUDIT-Z/THEOREM-Z, and every release
  blocker agree

python3 -m json.tool Stage1_Instances/THM-M-0526/release-decision.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for both JSON documents

git diff --check -- Stage1_Instances/THM-M-0526 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No `lake update`, `lake build`, dependency clone, dependency fetch, or `.lake` mutation was
performed. The shared `.lake` symlink is excluded from changed paths and supplies only warm-cache,
nonrelease evidence.

Audit retry is independent of proof closure: complete and reconcile the frozen inventory, source
boundaries, discovery/classification records, `H/M/R` evidence, typed graphs, and public projections,
then obtain independent review and master acceptance of `AUDIT-Z`; proof debt may remain open.

Theorem retry additionally requires accepted `AUDIT-Z`, implementations for the seven-node proof
frontier, accepted exact composition and dependency receipts, all required root-critical source and
`R0` records, complete provenance/foundation/TCB evidence, and separately provisioned cold offline
release validation. Supply-chain closure, distinct attestations, independent minimal verification,
deterministic bundling, and master reconciliation are required before `THEOREM-Z` can change.

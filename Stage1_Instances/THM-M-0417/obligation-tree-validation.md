# Obligation-tree validation record

Item: `S56-M-0417-OBLIGATION_TREE`  
Base revision: `27b6ad42a24208a552148406359bf415f32cf8fb`

## Result

Registry version 1 freezes nine required root-relevant obligations and zero exclusions before
proof-node acceptance. Separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs record typed relations. Four duplicate statement/wrapper surfaces map back to the
canonical root or unique terminal body and receive no denominator or proof-body credit.

`ObligationTree.root_compose` is a conditional composition certificate. It consumes the half-body
volume normalization, Blichfeldt collision bridge, and difference-extraction obligations and yields
the exact strict root; `root_exact_type` checks the root expression. The inputs remain assumptions,
so the certificate is architecture evidence rather than a theorem proof. The terminal body already
identified by the anchor audit remains merely an `M0-W` candidate until later proof, provenance,
validation, and master gates.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Lean used the existing pinned Lake environment;
no update, build, dependency fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0417/build_obligation_artifacts.py` | 0 | deterministically regenerated registry, node records, seven typed graphs, and structured recipes |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0417/ObligationTree.lean` | 0 | conditional composition and exact root identity elaborated; axiom report was `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0417/check_obligation_tree.py` | 0 | nine unique obligations, denominators, zero exclusions, reciprocal semantic endpoints, proof DAG reachability, aliases, recipes, and substantive ledgers passed |
| `python3 Stage1_Instances/THM-M-0417/check_anchor_audit.py` | 0 | prerequisite pinned source revision, blob/hash, terminal body, placeholder scan, and exact wrapper remained valid |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0417` | 0 | rank 72, planned, legacy artifacts unaccepted, theorem incomplete |
| prohibited-token scan of new Lean and JSON artifacts | 1, expected empty | no proof escape, unsafe declaration, or fake completion marker found |
| `git diff --check -- Stage1_Instances/THM-M-0417` | 0 | no whitespace errors |

## Boundary

This node freezes architecture and typed workflow only. It does not accept the pinned terminal proof
body, complete transitive provenance or TCB analysis, supply H0/R0 independent reviews, perform a
hermetic release build, or establish theorem completion. Those remain later dependency-ordered
nodes and master acceptance remains required.

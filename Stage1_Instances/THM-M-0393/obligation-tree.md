# THM-M-0393 Obligation Tree Freeze

## Scope And Freeze

This artifact completes only `S56-M-0393-OBLIGATION_TREE`. Registry
`THM-M-0393-REGISTRY-v1` fixes 17 root-relevant semantic obligations before any proof closure is
observed. Every obligation is machine-required and remains `M4`; none has a proof body or evidence
receipt. There are no eligibility exclusions. The exact statement input is bound by SHA-256
`456c62756bc035e675135270bf6984c00bb1203bc6687d3495ae7663131d985f`.
The ordered obligation ID/fingerprint denominator is bound by SHA-256
`35ff2262d476ef84a23ade1c047c347a7c51b4271429d291a18e8c5f49f0c5db`.

The prior audit found no terminal Lean candidate. The architecture therefore models the classical
rational-approximation route rather than disguising a statement substrate or documentation entry
as a proof. `M0393-X1`, the deep algebraic-approximation theorem, is explicitly a critical bridge.
Its primary-source crosswalk and formal implementation remain open.

## Proof Architecture

```text
M0393-ROOT  exact ThueStatement
|-- M0393-S1  definitions and ordered-pair solution encoding
|-- M0393-S2  source-to-formal assumptions and transport
|-- M0393-X2  dependency, axiom, placeholder, unsafe, and oracle closure
`-- M0393-T2  finite reconstruction of all integral solutions
    |-- M0393-S3  y = 0 boundary
    |-- M0393-N1  finite common-factor choices from g^n | m
    |-- M0393-N2  primitive normalization
    `-- M0393-T1  primitive-solution finiteness
        |-- M0393-C1  dehomogenization
        |-- M0393-C2  finite algebraic root family and separation data
        |-- M0393-B1  bounded-denominator branch
        `-- M0393-B2  large-denominator approximation branch
            |-- M0393-L1  select a nearby root
            |-- M0393-L2  degree-n approximation upper bound
            |-- M0393-L3  pass to an exponent mu with 2 < mu < n
            `-- M0393-X1  Thue algebraic-approximation bridge
```

All leaves have a planned ledger shorter than 100 substantive steps, but that number grants no
readability or proof credit. Construction invariants, the major imported theorem boundary, the
bounded/large split, normalization, and recomposition own separate IDs. Future implementation must
expand a node again if its actual ledger triggers section 6.5.

## Typed Graph Boundary

`typed-graphs.json` separates proof requirements from refinement, provenance, evidence, trust,
documentation, and workflow relations. Four nonleaf parents have open composition-certificate
specifications whose required-child sets exactly match their proof edges. They are specifications,
not Lean certificates. The evidence graph is deliberately empty. The provenance graph records the
canonical local statement and pinned mathlib substrate without assigning proof credit, plus the
missing terminal-body boundary.

The workflow keeps source pinpointing, proof implementation, composition, and kernel/trust
validation open. Only the registry/graph freeze tasks are proposed as worker-self-tested. Master
acceptance, all proof work, `AUDIT-Z`, and `THEOREM-Z` remain outside this phase.

## Validation Evidence

Commands were run from repository root on base revision
`6646f3026454e24525976ebd54841f85a50d3ba5`:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0393
  exit 0: execution rank 6; planned; theorem_complete=false
python3 Stage1_Instances/THM-M-0393/validate_obligation_tree.py
  exit 0: validates statement digest, unique/full root reachability, acyclic proof/workflow graphs,
  exact composition child sets, typed edge vocabulary, empty evidence, and open M4 root
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0393/Statement.lean
  exit 1: reused canonical cache lacks the Mathlib.olean module root; no build/update/fetch was run
python3 -m json.tool Stage1_Instances/THM-M-0393/obligation-registry.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-0393/typed-graphs.json >/dev/null
  both exit 0
git diff --check -- Stage1_Instances/THM-M-0393 .stage1-worker-selftest.json
  exit 0: no output
```

## Status Boundary

The obligation denominator and typed architecture are self-tested structural work. The unavailable
olean prevents fresh Lean statement replay in this worker and remains a known failure rather than
being repaired by mutating `.lake`. No theorem proof, source acceptance, composition certificate,
kernel receipt, audit completion, theorem completion, or master acceptance is claimed.

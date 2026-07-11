# Statement validation record

Item: `S56-M-0420-STATEMENT`  
Base revision: `7fe8e74dc1d7b1678d428039fd13be71de273dd8`

## Frozen target

`Stage1Instances.THM_M_0420.HilbertClassFieldTarget` is the exact intake-selected claim. It
quantifies over a number field `K`, existentially packages a finite number-field extension `H/K`,
and requires abelian Galoisness, unramifiedness at every nonzero finite prime, the class-group/Galois
group isomorphism, and maximality by `K`-algebra embeddings. Infinite-place conditions are outside
the frozen root. Its only direct imports are the pinned mathlib class-number and unramifiedness
modules.

The checked theorem `hilbertClassFieldTarget_iff_pinnedCandidateSourceShape` relates the target to
a direct local expansion of the historical `S1_M_075.HilbertClassFieldExists` candidate. The
reciprocity isomorphism can be reversed by the independently checked
`reciprocity_orientation_transport`. Neither theorem supplies Hilbert class field existence.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` using its
existing symlink to the canonical pinned `.lake` artifacts; no dependency update or fetch ran.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0420/Statement.lean` | 0 | target, predicates, both transports, four mutations, and explicit target print elaborated |
| `python3 ../../Stage1_Instances/THM-M-0420/check_statement.py` | 0 | expression SHA-256 `e02ce829ff52e7bd576532eb0493f01d2b0053e114babc33d15131fc12db1041`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0420/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `426dd9...b536`, `651c8a...b1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0420` | 0 | rank 75, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

The mutation check rejects loss of reciprocity, maximality, abelianity, or finite-prime
unramifiedness by comparing separately elaborated explicit expressions. This is statement-only
evidence pending master acceptance; it does not advance the anchor, proof, validation, or release
nodes and makes no theorem-completion claim.

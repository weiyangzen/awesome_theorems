# THM-M-1234 proof recheck at `bad90e2e`

Item: `S56-M-1234-PROOF`

Intent: `prove`

Verdict: `blocked`

Worker state proposed: `[ ]` (no transition)

Base revision: `bad90e2e2479d376609447202eb4f437789d0d11`

Base tree: `df3ade7b4d06057f8aac33369c3d69bd391aa05a`

## Exact result

The exact target is `Stage1Rev56.THMM1234.Statement`: every admissible
whole-plane, finite-energy velocity with bounded weak vorticity must have a
global weak Euler solution. No repo-local or pinned declaration inhabits that
universal proposition, and the prerequisite immutable anchor audit found no
exact external body eligible to pin.

The existing sources contain real, placeholder-free bodies, but none closes a
frozen semantic root dependency:

- `root_of_construction_and_closure` is conditional on two explicit packages.
- `candidateConstructionPackage_from_initialData` uses the initial fields at
  every time. It inhabits the formal `CandidateConstructionPackage` interface,
  but that interface consumes none of the graph-required approximation,
  estimate, or compactness children. It therefore cannot close
  `M1234-A-STRUCTURE` under the frozen composition rules.
- `initialCandidateFields_trace` proves the trace only for that constant
  candidate.
- `zero_data_solution` proves only the strict zero-data boundary case.

There is no trivial encoding shortcut. Constant-in-time initial fields leave
the nonlinear weak momentum integral open for arbitrary data, while the zero
solution cannot satisfy the arbitrary initial term and vorticity trace. The
exact root therefore remains `H1/M3/R3`.

## Failed gate

The first failed gate is `M1234-A-APPROX`: the frozen graph requires a checked,
child-consuming construction of smooth global Euler approximants for every
`InitialData` witness, but the registry provides only a planned target and the
available pinned Lean closure has no body for it. The direct frozen root cut
remains `M1234-A-STRUCTURE` plus `M1234-E-CLOSURE`; expanding those two nodes
exposes the approximation, estimate, compactness, linear/nonlinear passage,
and trace packages as missing.

Retry requires an accepted repair of the under-specified package interfaces,
followed by real local bodies for approximation, uniform estimates,
nonlinear-compatible compactness, momentum limit passage, and the one-sided
trace. An immutable exact Lean 4 terminal body could instead be pinned and
checked for exact type and provenance. Assuming either package, adding an
axiom, or substituting the zero-data case is not eligible.

## Validation

All checks used the existing pinned environment. No `lake update`, `lake
build`, dependency clone/fetch, network action, or `.lake` mutation was
performed. The Lean recipe copied the four owned modules into a fresh `/tmp`
directory, selected Lean and `LEAN_PATH` with `lake env`, elaborated at trust
level zero, and removed every generated artifact.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c...34c5d`; root open at M3. |
| Temporary-copy `lake env` Lean replay | 0 | `Statement.lean`, `ObligationTree.lean`, `ConstructionProof.lean`, and `Proof.lean` elaborated at `--trust=0 -t0`. All printed declarations report only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-aware prohibited-construct scan over owned Lean files | 1 | Expected no-match result: no `sorry`, `admit`, declared axiom, `sorryAx`, unsafe/opaque/extern injection, `implemented_by`, or `native_decide`. |
| Exact-topic search in pinned mathlib Lean sources | 1 | Expected no-match result for Yudovich, Yudovitch, incompressible Euler, and bounded vorticity. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The replay produced `Statement.olean` SHA-256
`1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`.
The exact source and output hashes are bound in the paired JSON packet.

The prerequisite obligation-tree item is still worker-provisional `[_]`, not
master-accepted `[x]`. The automation-provided untracked `.lake` symlink also
makes this nonrelease evidence. Because the assigned universal proof phase is
not genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.
This packet is not a proof receipt, state transition, validation or release
decision, audit completion, theorem completion, or master acceptance.

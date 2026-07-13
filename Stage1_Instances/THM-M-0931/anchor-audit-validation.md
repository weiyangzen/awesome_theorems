# THM-M-0931 Anchor-Audit Validation

Item: `S56-M-0931-ANCHOR_AUDIT`

Base revision: `a1c9974d7fb28cd680e6494b968544bf801a93a2`

Base tree: `1fa287bc821355aca2ca9e3ce107830a3eb58e64`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Int.erdos_ginzburg_ziv_multiset` proves the same occurrence-preserving integer selection result as
the frozen target, under a stronger at-least-input-count premise and for all natural `n`. The local
audit adapter retains the target's positive `n` binder and converts only the exact input-cardinality
equality to the candidate's lower bound. It elaborates without changing the carrier, selection
relation, witness cardinality, or divisibility conclusion.

The pinned terminal body enumerates multiset occurrences, applies the indexed integer theorem, and
maps the selected indices back to a submultiset. The indexed theorem is a zero/one/prime/composite
induction; its prime case uses the pinned Chevalley-Warning solution-count theorem. Lean reports
only `propext`, `Classical.choice`, and `Quot.sound` for the four public EGZ declarations, the
Chevalley-Warning boundary, and the exact adapter. `Mathlib.PrintSorries` reports the terminal and
adapter sorry-free. Scoped source scans found no proof-gap, bodyless, unsafe, external-code, native
oracle, or generated-certificate marker in the EGZ or Chevalley-Warning sources.

The indexed integer theorem and the two `ZMod` forms are shared-body dependencies or alternate
encodings, not independent root closures. Repository-local neighboring probes only mention the
same mathlib declarations and receive no cross-target credit. A complete bounded Sourcegraph query
returned only mathlib. GitHub repository metadata returned no project, while other anonymous code
and statement-collection search lanes were rate-limited or checkpointed. Those failures are
recorded explicitly and no exhaustive-discovery claim is made.

The exact mathlib route is an `M0-W` candidate with a local nonrelease `E2` probe. The accepted root
remains `H1/M3/R4` until dependency-ordered master acceptance and downstream obligation, proof,
provenance/trust, composition, validation, and release gates. Neither `AUDIT-Z` nor theorem
completion is claimed.

## Commands And Results

All local validation ran in this worker clone against the automation-provided canonical `.lake`
symlink. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0931` | 0 | rank 1470; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | exact revision `8a1783...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; dependency worktree clean |
| `rg` over repo-local and all manifest-materialized package Lean sources for EGZ aliases and declaration names | 0 | no independent proof body beyond the pinned mathlib module; neighboring probes are discovery-only |
| read-only Sourcegraph search for EGZ aliases in public Lean code | 0 | complete response, `skipped=[]`, 15 matches in mathlib only; response SHA-256 `0f5de56e...b53` |
| read-only GitHub repository metadata searches for ASCII and accented EGZ names with Lean | 0 | both complete zero-result responses; SHA-256 `08c082fd...600b2` |
| read-only GitHub code/formal-conjectures tree queries | 0 transport | anonymous rate-limit response; SHA-256 `1db366a2...386e`; no negative result claimed |
| read-only grep.app query | 0 transport | Vercel Security Checkpoint response; SHA-256 `da0a115f...1938`; no result claim |
| `lake env lean ../../Stage1_Instances/THM-M-0931/AnchorAudit.lean` from `Formalizations/Lean` | 0 | four public types, terminal bodies, exact adapter, six axiom reports, and two sorry-free reports matched; stdout SHA-256 `3ae69c74...53e5` |
| `python3 -B Stage1_Instances/THM-M-0931/check_anchor_audit.py` | 0 | identity, pins, blobs, hashes, source markers, adapter, seven-record classification, receipt, packet, and offline Lean replay matched |
| `python3 -m json.tool` on the three anchor JSON artifacts and root packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` | 1 (expected no match) | no proof gap, axiom declaration, unsafe/opaque body, external code, oracle, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0931 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. The
obligation registry, accepted proof-phase wrapper, full transitive trust and executable TCB closure,
independent source/readability reviews, hermetic and independent validation, deterministic release
bundle, `AUDIT-Z`, and theorem completion remain open.

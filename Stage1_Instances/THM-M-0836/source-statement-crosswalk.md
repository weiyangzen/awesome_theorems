# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6138-6143` supplies exactly six uncited lines: the title "computer
proof of the four-color theorem," Appel/Haken, 1976, the gloss "reducible configurations and the
discharging method for the four-color theorem," high importance, and `已验证`. Git blame places all
six lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record supplies no formula,
domains, definitions, quantifiers, configuration inventory, computation artifact, proof boundary,
bibliography, correction record, or formal declaration.

`Docs/Stage0_Blueprint.md:22820-22845` repeats the gloss while leaving precise definitions and
premises, proof route, dependencies, alternate forms, axioms, machine state, and artifact links
open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets this target to
`L0 / rework_required`.

## Bibliographic source leads

Crossref metadata identifies the following source family:

- Kenneth Appel and Wolfgang Haken, *Every planar map is four colorable*, *Bulletin of the American
  Mathematical Society* 82(5) (1976), 711-712, DOI
  `10.1090/S0002-9904-1976-14122-5`.
- Kenneth Appel and Wolfgang Haken, *Every planar map is four colorable. Part I: Discharging*,
  *Illinois Journal of Mathematics* 21(3) (1977), DOI `10.1215/ijm/1256049011`.
- Kenneth Appel, Wolfgang Haken, and John Koch, *Every planar map is four colorable. Part II:
  Reducibility*, *Illinois Journal of Mathematics* 21(3) (1977), DOI
  `10.1215/ijm/1256049012`.
- Separate 1977 microfiche supplements are indexed under DOI `10.1215/ijm/1256049023` and DOI
  `10.1215/ijm/1256049024`.

The AMS publisher PDF of the 1976 announcement was inspected. The observed two-page PDF has SHA-256
`da6b2598f51ad324055fe366bd36e3f9689f3d0b965893a6ca9accb75adfad64`. Printed pages 711-712
state the theorem "Every planar map can be colored with at most four colors," give the dual
loopless-planar-graph reading, describe configurations, reducibility and unavoidability, and state
that an unavoidable set of reducible configurations immediately proves the theorem. They sketch
discharging by an initial charge, conservation under redistribution, and positive final charge;
report fewer than 2000 configurations of ring size at most fourteen; and say multiple programs by
John Koch and the authors checked every configuration in the unavoidable set as reducible. The
footnote names the later Part I and Part II and their distinct author lists.

This authenticates a strong source-family lead and the intended proof architecture. It still does
not select whether this separate catalog row targets the announcement's ordinary theorem, a
method-level conjunction, program correctness, or full source reconstruction rather than the
neighboring ordinary four-color target. The announcement delegates details and does not provide the
complete configuration inventory, program sources, certificate semantics, or detailed proofs.
Attempts to retrieve the Project Euclid Part I and II PDFs returned anti-bot HTML rather than PDFs.
Exact detailed statements, incorporated definitions, tables, programs, computation artifacts,
proof composition, errata and corrections, immutable preservation of the full suite, and independent
review remain open. The announcement supports discovery and source discrimination only, not `H0`.

## Component crosswalk

| Catalog/source component | Prospective mathematical role | Required Lean component | Intake assessment |
|---|---|---|---|
| "four-color theorem" | terminal map/planar-graph coloring conclusion | source-selected finite map/planarity model and proper four-coloring proposition | ordinary conclusion recognizable; duplicate-target and encoding choice open |
| reducible configurations | local configurations cannot occur in a minimal counterexample after coloring-extension analysis | exact configuration/occurrence/ring definitions plus a fixed inventory and reducibility proof for each member | definitions, list, quantifiers, computation boundary, and composition absent |
| discharging method | prove a fixed configuration family unavoidable by charge assignment and local transfer rules | finite plane-triangulation substrate, charge functions, rules, conservation and contradiction theorem | only generic degree-sum support is pinned; source rules absent |
| computer proof | finite case checking used within the proof | specified program or certificate corpus, verified semantics/checker, coverage and termination proof | no program, tables, certificate, checker, revision, or trust boundary selected |
| Appel/Haken, 1976 | announcement-level historical identity | immutable source and exact selected proposition | bibliography located; no full-text admission or independent review |
| Parts I/II, 1977 | detailed discharging and reducibility sources | source-to-node conjunction and checked child-to-root composition | multipart/author boundary located; exact theorem map open |
| `已验证` | untrusted catalog status | accepted source/kernel receipts | no H or M credit |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SimpleGraph.Coloring` defines `SimpleGraph.Coloring` and
`SimpleGraph.Colorable`; `Mathlib.Combinatorics.SimpleGraph.Finite` exposes finite degree data; and
`Mathlib.Combinatorics.SimpleGraph.DegreeSum` proves
`SimpleGraph.sum_degrees_eq_twice_card_edges`. The coloring module's own TODO list includes
"Planar graphs." The bounded repository-and-mathlib search found no exact-topic Appel-Haken,
four-color, unavoidable-set, reducible-configuration, or discharging-method declaration.

`IntakeProbe.lean` elaborates the adjacent pinned APIs and a tiny concrete coloring example. This
authenticates an available graph/color/degree substrate only. It does not select or elaborate a
canonical statement, define a planar embedding or configuration calculus, verify an Appel-Haken
case, inspect a terminal proof body, or establish global absence. It gives no statement or proof
credit and is not the downstream anchor audit.

Before leaving `H5`, accountable reviewers must choose one stable proposition or exact conjunction,
preserve the primary text and any computational supplements immutably, map every incorporated
definition, hypothesis, conclusion, program/certificate boundary, source transition, correction and
erratum, and independently approve the mapping. Before machine credit, the identical claim must be
encoded in Lean and pass expression identity, transport, mutation, provenance, trust, composition,
and computation-certificate gates.

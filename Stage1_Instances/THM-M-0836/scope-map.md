# Scope map

## Preserved source family

The repository fixes only the title, Appel/Haken attribution, year 1976, and the phrase
"reducible configurations and the discharging method for the four-color theorem." Intake preserves
that Appel-Haken computer-assisted proof family without converting a method description into a
theorem. A later statement decision must explicitly choose one of these materially different roots:

1. the ordinary conclusion that every finite planar map or graph is four-colorable;
2. the exact conjunction of an unavoidable-set result and reducibility of every selected
   configuration, with a checked composition to the four-color conclusion;
3. one source-defined discharging theorem or unavoidable-set theorem;
4. one source-defined reducibility theorem or the conjunction over a fixed configuration list;
5. correctness of the historical case-checking program or of a newly specified checker and
   certificate corpus;
6. a complete source-faithful formal reconstruction of the Appel-Haken proof suite.

These have different binders, conclusions, evidence boundaries, and proof obligations. The catalog
does not select one of them.

## Decisions required at statement freeze

1. Select and lawfully preserve an immutable source edition and one exact truth-valued result or
   conjunction; map the 1976 announcement, 1977 Parts I and II, and relevant supplements without
   conflating their authors, dates, or roles.
2. Choose maps, plane triangulations, embedded planar graphs, abstract finite planar graphs, or a
   dual formulation, then freeze finiteness, connectedness, loop/multiple-edge, embedding, face,
   outer-face, and map-to-graph transport conventions.
3. Define a proper four-coloring and fix whether the conclusion is vertex coloring, face coloring,
   chromatic number at most four, or a checked equivalent form.
4. Define configurations, occurrence, ring/boundary data, contraction or extension, reducibility,
   unavoidable sets, charge, initial charge, local discharge rules, and conservation or final-charge
   invariants exactly as required by the selected source.
5. Freeze the finite configuration inventory and every symmetry, isomorphism, indexing, and
   duplicate-elimination convention. A supplied arbitrary list may not smuggle in unavoidability or
   reducibility as a hypothesis.
6. Specify every computer-assisted boundary: program and language, integer/data encodings,
   enumeration order, finite search space, generated tables, certificate schema, independent
   checker, arithmetic semantics, termination, completeness, and connection to the mathematical
   root.
7. Resolve empty and tiny maps, disconnected graphs, bridges, loops and parallel edges, degenerate
   embeddings, repeated faces, triangulation reductions, minimal-counterexample assumptions, and
   configuration boundary cases.
8. Freeze ordered binders, universes, hypotheses, conclusion, foundation and classical-choice
   policy, computation policy, TCB, minimal imports, expression/environment hashes, transports, and
   required statement mutations.

## Neighbor boundaries

- `THM-M-0833` is the ordinary four-color theorem. Its planar-graph colorability conclusion cannot
  silently replace this row's historical proof-method/computation boundary.
- `THM-M-0834` is the five-color theorem and is strictly weaker.
- `THM-M-0837` names the later Robertson-Sanders-Seymour-Thomas proof, whose configuration set and
  verification route are not the Appel-Haken proof.
- `THM-M-0838` names Gonthier's formal Coq proof. It is a crucial later formalization lead, but it
  cannot be relabeled as a Lean proof of the historical Appel-Haken source suite.

## Explicit exclusions

- A theorem saying an arbitrary planar graph is four-colorable without a source-approved account of
  why that is the selected root rather than `THM-M-0833`.
- A theorem assuming the graph is four-colorable, or a structure/hypothesis that stores the desired
  coloring, unavoidable set, reducibility result, or successful computation.
- The five-color theorem, special graph families, a fixed finite graph, or a finite sample of
  configurations presented as the full result.
- A generic degree-sum identity or abstract potential/charge conservation lemma presented as the
  Appel-Haken discharging theorem.
- A Boolean program run, table, checksum, benchmark, or unchecked certificate without a verified
  specification, checker, completeness argument, and source-to-root composition.
- The RSST proof, Gonthier's Coq theorem, or a modern checker substituted without an explicit checked
  and source-approved relationship.
- The catalog's `已验证` label, a DOI record, a source title, an elaborated `#check`, or a bounded
  search treated as statement, source-fidelity, kernel-closure, or theorem-completion evidence.

No canonical expression, statement fingerprint, checked transport, obligation registry, discovery
protocol, proof state, or completion claim is frozen at intake.

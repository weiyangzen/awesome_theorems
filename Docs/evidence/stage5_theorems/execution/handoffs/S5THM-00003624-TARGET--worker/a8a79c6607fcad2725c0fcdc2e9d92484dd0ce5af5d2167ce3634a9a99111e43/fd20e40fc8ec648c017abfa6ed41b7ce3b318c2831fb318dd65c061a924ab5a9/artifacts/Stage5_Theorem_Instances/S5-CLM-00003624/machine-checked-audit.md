# Machine-checked audit

Root: `AwesomeTheorems.Stage5.S5_CLM_00003624.agp_infinite_proof`.

The root has the exact frozen type `Filter.Tendsto Erdos1057.carmichaelCounting Filter.atTop Filter.atTop` and closes by applying `Erdos1057.erdos_1057.variants.agp_infinite` from the exact imported provider module. The package declares no helper definitions and no proof oracle. Its explicit dependency chain is the local wrapper → frozen provider theorem → `Erdos1057.carmichaelCounting`.

The closure is classified `M0-P`: a pinned-provider theorem through a claim-owned exact wrapper. Cold from-source replay is required with `LAKE_NO_CACHE=1` and `--trust=0`; the worker reports an empty remaining machine cut set and an empty observed-axiom list for the elaborated claim-owned wrappers. This is provisional evidence only. The canonical Master must independently recompute the elaborated root, transitive declarations, bodies, dependencies, and axiom environment.

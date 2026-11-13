# Model and simulator card — Supply Chain Jenga

## Intended use

A synthetic two-product inventory simulator comparing reactive and capacity-constrained replenishment under disruption.

## Implemented methods

- Shared packaging and separate raw-material inventories
- Two-day procurement lead times and bounded supplier capacity
- Disruption injection and observed-demand rolling forecasts
- Linear-program allocation with inventory conservation
- Matched-seed policy comparisons for service, backlog and declared cost

Some projects use deterministic simulators and rules rather than trained neural models. Those distinctions are retained in this card and the source.

## Evaluation

See `docs/EXPERIMENTS.md` and the machine-readable reports. No pretrained foundation-model weights or real-world efficacy certification are included. Parameters, splits and synthetic generators are visible in source.

## Limitations

Two-product synthetic inventory network and capacity-constrained procurement LP. No operational enterprise integration.

## Extensions not implemented in this release

- Multi-tier stochastic supply networks and calibrated demand models
- Real supplier data and operational decision validation

# Synopsis — Supply Chain Jenga

**Ishdeep Singh · 12 November 2026**

## V2 interface release

A dependency atlas with a day scrubber.

- Selectable suppliers and shared product dependencies
- Outage length, start, backup capacity and replenishment policy controls
- Scrub actual zero-based model days to inspect stocks and backlog
- Demand, fulfilment and inventory charts plus policy evaluations

Every shown value comes from the 75-day simulation under declared synthetic assumptions. The underlying domain scope and research-extension boundaries below remain explicit.

## Implemented release

Runnable source: `lab/supply.py`. Interface and backend are included. Tests and benchmark outputs accompany this distribution.

## Limits of the implemented release

Two-product synthetic inventory network and capacity-constrained procurement LP. No operational enterprise integration.

## Measured evaluation

```json
{
  "metrics": [
    {
      "policy": "fixed",
      "fill_rate": 1.0,
      "cost": 12247.21773809524,
      "stockout_days": 28.0,
      "nonnegative_inventory": true
    },
    {
      "policy": "optimized",
      "fill_rate": 1.0,
      "cost": 12029.139166666668,
      "stockout_days": 27.25,
      "nonnegative_inventory": true
    }
  ],
  "seeds": [
    881,
    882,
    883,
    884
  ],
  "note": "Synthetic two-product inventory model; both policies see identical realized demand, never future demand. Costs are declared model units."
}
```

## Original specification and proposed extensions

The material below preserves the design ambitions. Future-tense features and anticipated challenges are not completed-development claims.

Supply Chain Jenga

**Tagline:** We have all the expensive parts. Unfortunately, we do not have the box.

### Concept, problem, and users

Supply Chain Jenga represents products, suppliers, warehouses, and orders as a dependency network. A low-cost component can be essential to completing a high-value product. The project studies how disruptions propagate and which recovery choices improve fulfilment under capacity and lead-time constraints.

Target users are operations students, procurement analysts exploring scenarios, and researchers studying network resilience. The research question is how much additional sourcing or inventory cost buys a measurable improvement under unseen disruption combinations.

### Proposed product and workflow

Load a synthetic network, inspect dependencies, run a demand scenario, and disable a supplier or transport link. The app traces affected inventory and orders, then compares backup sourcing, delayed fulfilment, and inventory policies. Users can inspect why a seemingly available alternative is rejected.

Screens: network explorer, product dependency view, inventory timeline, disruption controls, recovery planner, and cost/service comparison. Show units, lead times, capacities, and confidence bands. A recommendation should identify the binding constraint, not merely name another supplier.

### Data and system design

Records: `Supplier`, `Facility`, `Material`, `BillOfMaterials`, `InventoryLot`, `PurchaseOrder`, `Shipment`, `DemandSeries`, and `Disruption`. Include capacities, substitution rules, yields, order commitments, and lead-time distributions. The bill of materials is part of the authoritative operational model.

Start with one product family and synthetic ground truth. Hold out disruption families, demand periods, and network structures as separate generalization tests. For demand forecasting, use chronological backtesting. A planner cannot use a future disruption schedule unless it is explicitly operating in a labelled perfect-information benchmark.

### Algorithms and experiments

Baseline: fixed reorder rules and predefined backup suppliers. Next: probabilistic demand forecasting and a constrained recovery optimizer. A mixed-integer or stochastic formulation can model sourcing, transport, inventory, and unmet demand; a simpler heuristic is the first implementation. A graph representation may later improve impact prediction, but the graph alone does not solve operational constraints.

The objective balances purchasing, holding, transport, and unmet-demand penalties. Publish those weights and explore service/cost tradeoffs. Enforce material conservation, supplier capacity, production dependencies, and order timing. Correlated disruptions are necessary stress tests because several backups may fail together.

Metrics: unit fill rate, stockout duration, backlog, recovery time, and total declared cost. Compare identical demand/disruption seeds and report solver time or heuristic budget. Ablate correlated events, forecast uncertainty, and multi-tier dependencies. An apparent gain that requires unavailable capacity is an invalid plan.

### Anticipated problems, in my voice

| What could go wrong | My likely reaction | Engineering response |
|---|---|---|
| Backup capacity is counted multiple times | “One supplier has been hired to rescue the entire economy.” | Shared capacity constraints across affected products |
| Material appears from nowhere | “Supply-chain optimization by manifestation.” | Inventory balance checks at every step |
| The cheapest plan causes persistent stockouts | “Saved on procurement. Lost the customers.” | Show service/cost frontier and unmet-demand penalties |

### Demo, milestones, and limits

Remove a small packaging supplier, trace delayed products, and compare an infeasible “obvious backup” with a capacity-aware recovery plan. Milestones: bill of materials; inventory simulator; disruption replay; baseline policies; optimizer; stochastic tests. Deliver network scenarios and recovery reports. Real procurement advice needs reliable operational data and relevant constraints; synthetic performance remains a controlled experiment.




## Problems actually encountered during the makeover

| The problem | In my voice | What changed |
|---|---|---|
| Sample B overwrote the file used by sample A | “Bro, this is an A/B test, why did B steal A’s identity?” | Recordings now get unique file names; a regression test checks both files remain distinct and unchanged. |
| A duplicate highlight followed row positions instead of duplicate evidence | “Apparently every third row had been arrested on vibes.” | Duplicate highlights now use exact record content and jump to a real duplicate. |
| The table displayed a rounded number that search did not match | “I copied the number from your own screen, my guy.” | Search checks both raw values and the formatted values visible in the table. |
| Graph labels became tiny on a phone | “Causal inference, now available to ants.” | Graph workspaces keep readable node widths and scroll within their own viewport. |
| Robot movement and the play button disagreed about whether it was running | “Gordon left the parking spot while the button was still contemplating life.” | The live flag is synchronized after accepted commands and remains off after rejected commands. |
| Fast screenshots caught an interface between renders | “The UI took a smoke break precisely when the camera arrived.” | Captures were inspected, incomplete frames replaced, and videos labelled as edited screenshots. |

These are observed build issues. Proposed research challenges in the original specifications remain proposed; this log does not invent months of model training or real deployments.

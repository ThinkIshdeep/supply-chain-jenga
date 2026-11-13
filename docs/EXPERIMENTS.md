# Experiments and reproduction

Run `python scripts/evaluate_all.py` from this repository. The report is written to `reports/evaluation-results.json`. This executes real calculations; model quality is separate from test success.

## Recorded baseline

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

## Interpretation

Two-product synthetic inventory network and capacity-constrained procurement LP. No operational enterprise integration.

The raw reports describe whether measurements are synthetic benchmarks, controlled regression fixtures or invariants. Do not interpret regression-fixture accuracy as a held-out real-world score. Preserve seeds and splits when comparing changes.

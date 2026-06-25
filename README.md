# Multi-Jurisdiction Sales Tax Calculator

A Python-based financial computation tool for calculating sales tax 
liability across multiple jurisdictions. Processes purchase amounts 
through a structured rate registry, applies banker's rounding at every 
step, and generates a formatted transaction summary.

## Features

- Calculates tax per jurisdiction from a centralized rate registry
- Supports state, county, and federal jurisdictions out of the box
- New jurisdictions can be added in a single line with no logic changes
- Full session ledger with running total across multiple transactions
- Input validation rejects NaN, infinite values, and negative amounts
- Formatted summary report with dynamic rows per active jurisdiction

## How to Run

```bash
python SalesTax.py
```

No external dependencies. Requires Python 3 with a standard installation.

## Jurisdiction Registry

| Jurisdiction | Rate  |
|--------------|-------|
| State        | 5.00% |
| County       | 2.50% |
| Federal      | 0.00% |

## Sample Output

```
sales summary
----------------------------------
  purchase amount:          $120.00
  state tax:                  $6.00
  county tax:                 $3.00
  total tax:                  $9.00
----------------------------------
  total sale:               $129.00
```

## Technical Highlights

- `TaxJurisdiction` enum drives all classification and registry lookups
- `TransactionRecord` dataclass computes total tax and final sale on initialization
- `TaxEngine` maintains a full session ledger and running sale total
- `SalesSummaryRenderer` builds output rows dynamically from active jurisdictions
- Banker's rounding applied at every individual tax computation step

## Tech Stack

Python 3 | dataclasses | enums | functools

# External data sources

This project uses a hybrid approach:

1. **Public real-world financial and actuarial inputs**
2. **A synthetic policy-level portfolio calibrated to realistic aggregate values**

Real individual life-insurance policy data is usually not publicly available because it contains sensitive customer and contract information. Therefore, the model documents public sources and uses processed templates that can be replaced with real extracted values.

## Planned source categories

### 1. Swedbank Försäkring annual reports

Purpose:

- premium income
- assets under management / fund value scale
- insurance liabilities
- claims or benefits paid
- operating expenses
- profit/loss figures
- solvency-related figures

Suggested search terms:

```text
Swedbank Försäkring årsredovisning PDF
Swedbank Försäkring annual report
Swedbank Insurance annual report
```

How it is used in the model:

- calibrate the synthetic portfolio scale
- compare projected premium income and expenses to realistic reported totals
- explain business relevance of profitability and valuation metrics

Processed target file:

```text
data/processed/financial_inputs.csv
```

### 2. Swedish mortality data

Purpose:

- replace a fixed mortality assumption with age/gender-based mortality rates
- make the model more actuarial and assumption-driven

Potential sources:

- Statistics Sweden / SCB mortality tables
- Human Mortality Database

Processed target file:

```text
data/processed/mortality_table_sweden.csv
```

### 3. Swedish interest-rate data

Purpose:

- support discount-rate assumptions
- create investment-return or stress scenarios
- connect valuation to market assumptions

Potential sources:

- Sveriges Riksbank policy-rate data
- Swedish government bond yields
- Swedish yield-curve data

Processed target file:

```text
data/processed/interest_rate_assumptions.csv
```

## Important modelling note

This project should not claim to use internal Swedbank data or real customer policy records. A strong and honest project description is:

> Due to privacy constraints, real policy-level life-insurance data is not publicly available. This project therefore combines public financial reporting data and public actuarial/market assumptions with a synthetic policy-level portfolio calibrated to realistic aggregate values.

## Next development steps

1. Extract selected values from a Swedbank Försäkring annual report.
2. Replace placeholder values in `data/processed/financial_inputs.csv`.
3. Add a mortality-rate lookup by age and gender.
4. Add discount-rate assumptions from real Swedish interest-rate data.
5. Update the dashboard/report to show which assumptions come from public external sources.

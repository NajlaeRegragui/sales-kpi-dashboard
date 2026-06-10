# Power BI File

The main Power BI report file for GitHub is stored here:

```text
powerbi/sales_dashboard.pbix
```

It contains:

- CSV import tables from `data/cleaned`
- Star-schema relationships
- Marked date table `DimDate`
- DAX measures for sales, margin, plan, forecast, targets, pipeline and data quality

The file is intentionally small enough to keep in the GitHub repository for portfolio review.

There may also be local working copies named `powerbi_buis.pbix` if the report was edited directly in Power BI Desktop. The GitHub-facing PBIX is `sales_dashboard.pbix`.

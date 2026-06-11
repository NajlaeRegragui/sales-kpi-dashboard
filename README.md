# Sales KPI Dashboard - Power BI Portfolio Project

![Sales KPI Dashboard](powerbi/screenshots/dashboard_mockup.png)

## Overview

This is a Sales Data Analyst portfolio project built in Power BI.

I created this project to practice the kind of work a data analyst would do in a sales environment: cleaning data, building a data model, creating DAX measures and turning the numbers into a dashboard that can support business decisions.

The dataset is synthetic, but it is designed to feel realistic. It includes sales campaigns, customers, products, regions, sales representatives, targets, forecasts and CRM pipeline data.

The project covers the full workflow:

- raw and cleaned CSV data
- Python data preparation
- SQL analysis questions
- Power BI semantic model
- DAX KPI measures
- dashboard screenshot
- business insights that can be explained in an interview

## Business Questions

- Which regions are generating the most revenue?
- How is actual revenue performing against plan and forecast?
- Which media channels are contributing most to sales?
- How strong is the current sales pipeline?
- Where do data quality issues appear in the sales process?
- Which KPIs would help management understand performance quickly?

## Main KPIs

- Revenue
- Delivery Cost
- Gross Margin
- Gross Margin %
- Actual vs Plan %
- Actual vs Forecast %
- Target Attainment %
- Pipeline Coverage
- Win Rate %
- Digital Revenue Share %
- Inventory Utilization %
- CPM
- Data Quality Issue %

## Repository Structure

```text
sales-kpi-analysis/
|-- README.md
|-- data/
|   |-- raw/
|   |   |-- sales_data_raw.csv
|   |   |-- FactSales.csv
|   |   |-- FactPipeline.csv
|   |   |-- FactPlan.csv
|   |   |-- FactForecast.csv
|   |   |-- FactTargets.csv
|   |   |-- BridgeCampaignProduct.csv
|   |   |-- DimDate.csv
|   |   |-- DimCustomer.csv
|   |   |-- DimProduct.csv
|   |   |-- DimRegion.csv
|   |   `-- DimSalesRep.csv
|   `-- cleaned/
|       |-- sales_data_cleaned.csv
|       |-- FactSales.csv
|       |-- FactPipeline.csv
|       |-- FactPlan.csv
|       |-- FactForecast.csv
|       |-- FactTargets.csv
|       |-- BridgeCampaignProduct.csv
|       |-- DimDate.csv
|       |-- DimCustomer.csv
|       |-- DimProduct.csv
|       |-- DimRegion.csv
|       `-- DimSalesRep.csv
|-- scripts/
|   |-- clean_sales_data.py
|   `-- generate_sales_data.py
|-- sql/
|   `-- sales_analysis_queries.sql
|-- powerbi/
|   |-- sales_dashboard.pbix
|   `-- screenshots/
|       `-- dashboard_mockup.png
|-- dax/
|   `-- measures.md
|-- insights/
|   `-- business_insights.md
`-- docs/
    |-- data_dictionary.md
    `-- project_workflow.md
```

## Power BI File

The main Power BI file is:

```text
powerbi/sales_dashboard.pbix
```

The model is built as a star schema. It includes these main tables:

- `FactSales`
- `FactPipeline`
- `FactPlan`
- `FactForecast`
- `FactTargets`
- `BridgeCampaignProduct`
- `DimDate`
- `DimCustomer`
- `DimProduct`
- `DimRegion`
- `DimSalesRep`

## How to Reproduce the Data

To regenerate the synthetic data, run:

```bash
python scripts/clean_sales_data.py
```

This creates the main raw and cleaned CSV files:

- `data/raw/sales_data_raw.csv`
- `data/cleaned/sales_data_cleaned.csv`

The detailed star-schema CSV files are also kept in `data/raw` and `data/cleaned` so the Power BI model can be rebuilt or reviewed.

## Dashboard Preview

The dashboard is designed as an executive sales overview. It focuses on:

- KPI cards
- Actual vs Plan trend
- Region performance
- Media channel mix
- Pipeline by sales stage

![Dashboard Screenshot](powerbi/screenshots/dashboard_mockup.png)

## Data Privacy

All data in this project is synthetic. It was created only for portfolio and learning purposes, and it does not include real customer, company or personal data.

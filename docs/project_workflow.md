# Project Workflow

## 1. Job-Ad Analysis

The project translates a realistic sales analytics scenario into a BI use case for a Sales Data Analyst supporting Sales, Management, Controlling, IT and Sales Operations.

All data is synthetic and the project is company-neutral.

## 2. Business Questions

The project focuses on revenue steering, margin analysis, planning variance, forecast accuracy, target attainment, pipeline quality, media performance and CRM data quality.

## 3. Data Generation

Synthetic data is generated with `scripts/generate_sales_data.py`.

The generated data includes:

- Campaign bookings
- CRM opportunities
- Customers
- Products and media channels
- Regions
- Sales representatives
- Plan, forecast and target scenarios
- Intentional data quality flags

## 4. Data Preparation

CSV files are written to:

- `data/raw`
- `data/cleaned`

The cleaned tables are structured for Power BI import and relationship modeling.

## 5. Power BI Modeling

The semantic model uses a star schema with:

- Fact tables for sales, pipeline, plan, forecast and targets
- Dimensions for date, customer, product, region and sales rep
- DAX measures stored in a dedicated `_Measures` table

## 6. Dashboard Design

The recommended first Power BI page is an Executive Sales Overview with:

- KPI cards
- Actual vs Plan trend
- Region performance table
- Media channel mix
- Pipeline by sales stage

## 7. Interview Preparation

Use `insights/interview_insights.md` to explain the business story, technical choices and management insights.

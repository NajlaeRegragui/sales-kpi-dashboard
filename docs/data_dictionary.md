# Data Dictionary

## DimDate
Calendar table from 2024-01-01 to 2026-12-31. Use `Date` as date table column.

## DimCustomer
Customer master data with industry, segment, HQ city, strategic account flag and industry demand index.

## DimProduct
Media products across OOH Analog, Digital OOH, Digital Media, Dialog Media and Crossmedia. Includes base cost ratio and list price per day.

## DimRegion
Sales regions and office markets with a market demand index.

## DimSalesRep
Sales representative master data with team, region, seniority and hire date.

## FactSales
Actual campaign bookings. Grain: one row per campaign. Contains booking dates, customer, sales rep, region, primary product, revenue, cost, margin, discounts, impressions, inventory units, CRM source and data quality flag.

## BridgeCampaignProduct
Campaign-to-product bridge. Grain: one row per campaign/product. Supports product mix analysis for bundled campaigns.

## FactPipeline
Salesforce-like opportunity pipeline. Grain: one row per opportunity. Contains sales stage, probability, opportunity amount, weighted pipeline and lost reason.

## FactPlan
Monthly plan by region and product. Scenario: Plan.

## FactForecast
Monthly rolling forecast by region and product. Scenario: Forecast.

## FactTargets
Monthly target by sales representative and region. Scenario: Target.

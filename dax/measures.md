# DAX Measures

Create these measures in the `_Measures` table.

```DAX
Revenue = SUM(FactSales[Revenue])
Delivery Cost = SUM(FactSales[DeliveryCost])
Gross Margin = [Revenue] - [Delivery Cost]
Gross Margin % = DIVIDE([Gross Margin], [Revenue])
Discount Amount = SUM(FactSales[DiscountAmount])
Discount Rate % = DIVIDE([Discount Amount], [Revenue] + [Discount Amount])
Campaigns = DISTINCTCOUNT(FactSales[CampaignKey])
Avg Campaign Revenue = DIVIDE([Revenue], [Campaigns])
Impressions = SUM(FactSales[Impressions])
CPM = DIVIDE([Revenue], [Impressions]) * 1000
Booked Units = SUM(FactSales[BookedUnits])
Available Units = SUM(FactSales[AvailableUnits])
Inventory Utilization % = DIVIDE([Booked Units], [Available Units])
Plan Revenue = SUM(FactPlan[PlanRevenue])
Revenue vs Plan = [Revenue] - [Plan Revenue]
Revenue vs Plan % = DIVIDE([Revenue vs Plan], [Plan Revenue])
Forecast Revenue = SUM(FactForecast[ForecastRevenue])
Revenue vs Forecast = [Revenue] - [Forecast Revenue]
Revenue vs Forecast % = DIVIDE([Revenue vs Forecast], [Forecast Revenue])
Target Revenue = SUM(FactTargets[TargetRevenue])
Target Attainment % = DIVIDE([Revenue], [Target Revenue])
Weighted Pipeline = SUM(FactPipeline[WeightedPipeline])
Pipeline Coverage = DIVIDE([Weighted Pipeline], [Target Revenue])
Open Pipeline = CALCULATE(SUM(FactPipeline[OpportunityAmount]), NOT FactPipeline[SalesStage] IN {"Closed Won", "Closed Lost"})
Win Rate % = DIVIDE(CALCULATE(COUNTROWS(FactPipeline), FactPipeline[SalesStage] = "Closed Won"), CALCULATE(COUNTROWS(FactPipeline), FactPipeline[SalesStage] IN {"Closed Won", "Closed Lost"}))
Data Quality Issues = CALCULATE(COUNTROWS(FactSales), FactSales[DataQualityFlag] <> "OK")
Data Quality Issue % = DIVIDE([Data Quality Issues], COUNTROWS(FactSales))
Digital Revenue = CALCULATE([Revenue], DimProduct[MediaChannel] IN {"Digital OOH", "Digital Media", "Crossmedia"})
Digital Revenue Share % = DIVIDE([Digital Revenue], [Revenue])

-- Optional generic portfolio aliases
Total Sales = [Revenue]
Total Profit = [Gross Margin]
Order Count = [Campaigns]
Total Quantity = [Booked Units]
Average Order Value = [Avg Campaign Revenue]
Profit Margin % = [Gross Margin %]
```

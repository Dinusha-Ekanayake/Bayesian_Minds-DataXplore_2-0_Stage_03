# DASHBOARD HACKATHON
# Customer Revenue and Experience Analytics

**Prepared by:** Dr. Rajitha Navarathna
**Date:** Apr 2026
**Organization:** OCTAVE

---

In this hackathon, your team will take on the role of a business intelligence team working for a live entertainment venue. The venue management wants to better understand customer behavior, revenue performance, and customer experience using the dataset provided.

Your challenge is to transform raw customer-level data into a professional **dashboard** that supports business decision-making. Your final solution should demonstrate strong skills in **data preparation, data modeling, DAX, dashboard design, best visualisation practices and business storytelling**.

The goal is not only to create attractive visuals, but also to build a dashboard that helps management identify meaningful insights and take action.

---

## Business Background

The venue has collected data on customer visits, ticket purchases, additional spending, repeat visit behavior, and feedback scores. Management is interested in understanding which customers generate the most revenue, which seating categories perform best, and how customer satisfaction varies across segments.

They want to use data to answer questions such as:

- Which customer groups contribute the most to total revenue?
- Which seating regions generate the highest value?
- Do repeat visitors spend more than first-time visitors?
- How do satisfaction and recommendation likelihood vary across customer segments?
- What insights can help improve customer experience and business performance?

Your dashboard should help management answer these questions in a clear, interactive, and visually effective way.

---

## Dataset Description

You will work with a customer-level dataset containing the following fields:

| Feature | Description |
|---|---|
| Customer_ID | Unique audience member ID |
| Age | Age of the attendee |
| Gender | Gender of the attendee |
| Country | Country of residence |
| Visit_Date | Date attended concert |
| Seating_Region | VIP / Premium / High Economy / Economy |
| Ticket_Price | Price of ticket (USD) |
| Num_Tickets | Number of tickets purchased in that transaction |
| Merchandise_Spend | Total merchandise spend (USD) |
| Drink_Spend | Spend on beverages (USD) |
| Repeat_Visit | 1 if customer has visited before, else 0 |
| Satisfaction_Score | Post-show rating through a survey (1–10) |
| Recommendation_Likelihood | Likelihood (0–10) to recommend show to others |

---

## Challenge Statement

Your team is required to design and develop a **dashboard solution** that helps venue management monitor and analyze customer revenue and experience.

The dashboard should provide insights into revenue generation, customer behavior, spending patterns, satisfaction levels, and repeat visit tendencies. In addition to dashboard development, your team must demonstrate strong understanding of fact and dimension tables, data relationships, measures, and analytical design choices and dashboard development principles.

---

## Scope of Analysis

Your dashboard should address the following areas of analysis.

### (i) Revenue Analysis

Your solution should include analysis of total ticket revenue, merchandise revenue, drink revenue, and overall revenue. It should also allow management to compare revenue by country, seating region, customer group, and visit date.

### (ii) Customer Analysis

Your dashboard should help identify the number of customers by demographic and geographic segments, customer spending patterns, average number of tickets purchased, and repeat visit rates.

### (iii) Experience Analysis

Your dashboard should include customer satisfaction and recommendation analysis across different segments. It should also examine whether customer spending or repeat visit behavior appears to be associated with better experience scores.

### (iv) Time-Based Analysis

Your team should make meaningful use of the visit date to explore performance over time, such as monthly revenue trends or visit behavior patterns across periods.

---

## Technical Expectations

### A. Data Preparation

Before building the dashboard, your team should prepare the dataset for analysis. This includes ensuring correct data types, transforming date fields properly, checking for inconsistencies, and creating any additional columns needed for reporting.

### B. Data Modeling

Although the provided dataset is flat, you are expected to demonstrate proper business intelligence modeling practices. Your Power BI solution should show how the dataset can be structured into fact and dimension tables. A **star schema** is strongly encouraged.

### C. Measures and KPIs

Your team should build relevant DAX measures that support the dashboard. These may include:

- `TotalTicketRevenue`
- `TotalMerchandiseRevenue`
- `TotalDrinkRevenue`
- `TotalRevenue`
- `Average Spend per Customer`
- `Repeat Visit Rate`
- `Average SatisfactionScore`
- `Average Recommendation Likelihood`

### D. Dashboard Design

Your dashboard should be easy to navigate, visually clean, and interactive. Use appropriate visuals, filters, and slicers to help users explore the data efficiently.

---

## Deliverables

Each team must submit one single folder containing:

- Dashboard code/scripts
- Published dashboard link

**Important:**

- Ensure the dashboard link is accessible and functional.
- Ensure all files are properly named and organized.
- Incomplete submissions may lose marks.
- Multiple submissions may not be considered unless instructed.

---

A successful team will not only show technical skill, but also explain why the analysis matters and how management can act on the findings. Remember that the best dashboard is not simply the most attractive one. It is the one that helps decision-makers understand the business clearly and confidently.

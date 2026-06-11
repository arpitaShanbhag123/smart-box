import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("plots", exist_ok=True)

# toolbox + loss inputs
num_tools = 300
toolbox_value = 4655

# Tools lost estimates
tools_lost_per_week = 1
tools_lost_per_month = tools_lost_per_week * 4

# smart toolbox estimated cost
smart_toolbox_cost = 6000
annual_maintenance = 1000

# labor downtime from missing tools
tech_count = 75
hours_lost_per_tech_week = 1
hourly_rate = 100

weekly_downtime_hours = tech_count * hours_lost_per_tech_week
weekly_downtime_cost = weekly_downtime_hours * hourly_rate
annual_downtime_cost = weekly_downtime_cost * 52

# evaluation period
years = 5

# tool cost distribution (based on actual tools that go missing most often)
# Socket wrenches: $30-$120 (avg $75)
# Allen keys (individual): $3-$12 (avg $8) | Sets: $25-$80 (avg $50)
# Punches: $10-$35 (avg $25)
# Wire snips: $20-$60 (avg $40)
# Scissors: $15-$45 (avg $30)
# Pliers: $25-$60 (avg $40)
tool_cost_distribution = [
    75, 80, 75, 50, 50, 8, 8, 8, 25, 25,
    40, 40, 30, 30, 40, 40, 75, 50, 25, 40
]

# deterministic expected-value tool loss
avg_tool_cost = sum(tool_cost_distribution) / len(tool_cost_distribution)
annual_tool_loss_cost = tools_lost_per_month * 12 * avg_tool_cost

# total annual cost (replacement + downtime)
total_annual_loss = annual_tool_loss_cost + annual_downtime_cost

# cumulative losses over 5 years i.e., list of 100 200 300
cumulative_losses = np.cumsum([total_annual_loss] * years)

# smart toolbox annualized cost (purchase year 1 + maintenance) -- total investment
smart_costs = [smart_toolbox_cost + annual_maintenance * i for i in range(years)]

# ROI calculation (per $ invested)
roi = ((cumulative_losses[-1] - smart_costs[-1]) / smart_costs[-1]) * 100

# break-even analysis
break_even_year = None
for i in range(years):
    if smart_costs[i] <= cumulative_losses[i]:
        break_even_year = i + 1
        break

# output summary
print("COST-BENEFIT SUMMARY")
print("Annual tool replacement cost: $" + format(annual_tool_loss_cost, ",.2f"))
print("Annual downtime cost: $" + format(annual_downtime_cost, ",.2f"))
print("TOTAL annual loss: $" + format(total_annual_loss, ",.2f"))
print("5-year cumulative loss (no tracking): $" + format(cumulative_losses[-1], ",.2f"))
print("5-year smart toolbox cost: $" + format(smart_costs[-1], ",.2f"))
print("ROI over " + str(years) + " years: " + format(roi, ".2f") + "%")

if break_even_year:
    print("Break-even point: Year " + str(break_even_year))
else:
    print("Break-even point not reached within evaluation period.")

# cumulative loss plot
plt.figure(figsize=(8, 5))
plt.plot(range(1, years + 1), cumulative_losses, marker="o", label="Cumulative Losses (Replacement + Downtime)")
plt.title("Cumulative Total Loss Cost Over Time")
plt.xlabel("Years")
plt.ylabel("Cumulative Cost ($)")
plt.grid(True)
plt.legend()
plt.savefig("plots/cumulative_loss.png")
plt.show()

# break-even comparison
plt.figure(figsize=(8, 5))
plt.plot(range(1, years + 1), cumulative_losses, marker="o", label="Losses Without Smart Toolbox")
plt.plot(range(1, years + 1), smart_costs, marker="s", label="Smart Toolbox Cost")
plt.title("Break-Even Comparison: Smart Toolbox vs Current Losses")
plt.xlabel("Years")
plt.ylabel("Cost ($)")
plt.grid(True)
plt.legend()
plt.savefig("plots/break_even_comparison.png")
plt.show()

# histogram of tool category costs
plt.figure(figsize=(8, 5))
plt.hist(tool_cost_distribution, bins=10, color="skyblue", edgecolor="black")
plt.title("Distribution of Tool Category Costs")
plt.xlabel("Category Cost ($)")
plt.ylabel("Frequency")
plt.grid(axis="y")
plt.savefig("plots/tool_cost_distribution.png")
plt.show()

# deterministic sensitivity analysis
loss_rates = range(1, 11)
break_even_years = []

for rate in loss_rates:
    expected_loss = rate * 12 * avg_tool_cost
    total_sim_annual = expected_loss + annual_downtime_cost
    cumulative_sim = np.cumsum([total_sim_annual] * years)

    be_year = None
    for i in range(years):
        if smart_costs[i] <= cumulative_sim[i]:
            be_year = i + 1
            break

    break_even_years.append(be_year)

plt.figure(figsize=(8, 5))
plt.plot(loss_rates, break_even_years, marker="o")
plt.title("Break-Even Year vs Tools Lost per Month (Deterministic)")
plt.xlabel("Tools Lost per Month")
plt.ylabel("Break-Even Year")
plt.grid(True)
plt.savefig("plots/break_even_vs_tools_lost.png")
plt.show()

# annual cost comparison
annual_smart_cost = smart_toolbox_cost / years + annual_maintenance

plt.figure(figsize=(8, 5))
plt.bar(["Annual Tool+Downtime Loss"], [total_annual_loss], color="tomato")
plt.bar(["Smart Toolbox Annual Cost"], [annual_smart_cost], color="green")
plt.title("Annual Cost Comparison (Losses vs Smart Toolbox)")
plt.ylabel("Cost ($)")
plt.savefig("plots/annual_cost_comparison.png")
plt.show()
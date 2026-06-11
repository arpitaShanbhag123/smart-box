import matplotlib.pyplot as plt
import numpy as np
import random

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
tech_count = 65
hours_lost_per_tech_week = 1
hourly_rate = 100 # get a finalized number later

weekly_downtime_hours = tech_count * hours_lost_per_tech_week
weekly_downtime_cost = weekly_downtime_hours * hourly_rate
annual_downtime_cost = weekly_downtime_cost * 52

# evaluation period
years = 5

# tool cost distribution

tool_cost_distribution = [
    150, 300, 75, 250, 120, 450, 150, 200, 600, 120,
    60, 120, 250, 800, 250, 60, 300, 100, 160, 60, 60, 60
]

def simulate_yearly_tool_loss(tools_lost_per_month, cost_distribution):
    losses = []
    for i in range(tools_lost_per_month * 12):
        losses.append(random.choice(cost_distribution))
    return sum(losses)

# tool loss cost 
annual_tool_loss_cost = simulate_yearly_tool_loss(tools_lost_per_month, tool_cost_distribution)

# total annual cost (replacement + downtime)
total_annual_loss = annual_tool_loss_cost + annual_downtime_cost

# cost calculations

cumulative_losses = np.cumsum([total_annual_loss] * years)
smart_costs = [smart_toolbox_cost + annual_maintenance * i for i in range(years)]
roi = ((cumulative_losses[-1] - smart_costs[-1]) / smart_costs[-1]) * 100

break_even_year = None
for i in range(years):
    if smart_costs[i] <= cumulative_losses[i]:
        break_even_year = i + 1
        break

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

# cumulative loss over time

plt.figure(figsize=(8, 5))
plt.plot(range(1, years + 1), cumulative_losses, marker="o", label="Cumulative Losses (Replacement + Downtime)")
plt.title("Cumulative Total Loss Cost Over Time")
plt.xlabel("Years")
plt.ylabel("Cumulative Cost ($)")
plt.grid(True)
plt.legend()
plt.savefig("figure1_cumulative_losses.png", dpi=300)
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
plt.savefig("figure2_break_even.png", dpi=300)
plt.show()

# histogram of tool category costs

plt.figure(figsize=(8, 5))
plt.hist(tool_cost_distribution, bins=10, color="skyblue", edgecolor="black")
plt.title("Distribution of Tool Category Costs")
plt.xlabel("Category Cost ($)")
plt.ylabel("Frequency")
plt.grid(axis="y")
plt.savefig("figure3_category_histogram.png", dpi=300)
plt.show()

# monte carlo simulation (1000 runs)

def simulate_many_years(n_runs, tools_lost_per_month, distribution):
    results = []
    for _ in range(n_runs):
        results.append(simulate_yearly_tool_loss(tools_lost_per_month, distribution))
    return results

mc_tool_only = simulate_many_years(1000, tools_lost_per_month, tool_cost_distribution)
mc_total_losses = [loss + annual_downtime_cost for loss in mc_tool_only]

plt.figure(figsize=(8, 5))
plt.hist(mc_total_losses, bins=30, color="lightgreen", edgecolor="black")
plt.title("Monte Carlo Simulation: Total Annual Loss Distribution (1000 Runs)")
plt.xlabel("Annual Total Loss ($)")
plt.ylabel("Frequency")
plt.grid(axis="y")
plt.savefig("figure4_monte_carlo.png", dpi=300)
plt.show()

# sensitivity: break-even vs loss rate

loss_rates = range(1, 11)
break_even_years = []

for rate in loss_rates:
    simulated_loss = simulate_yearly_tool_loss(rate, tool_cost_distribution)
    total_sim_annual = simulated_loss + annual_downtime_cost
    cumulative_sim = np.cumsum([total_sim_annual] * years)
    
    be_year = None
    for i in range(years):
        if smart_costs[i] <= cumulative_sim[i]:
            be_year = i + 1
            break


    break_even_years.append(be_year if be_year else None)

plt.figure(figsize=(8, 5))
plt.plot(loss_rates, break_even_years, marker="o")
plt.title("Break-Even Year vs Tools Lost per Month (with Downtime)")
plt.xlabel("Tools Lost per Month")
plt.ylabel("Break-Even Year")
plt.grid(True)
plt.savefig("figure5_sensitivity_break_even.png", dpi=300)
plt.show()

# annual cost comparison

annual_smart_cost = smart_toolbox_cost / years + annual_maintenance

plt.figure(figsize=(8, 5))
plt.bar(["Annual Tool+Downtime Loss"], [total_annual_loss], color="tomato")
plt.bar(["Smart Toolbox Annual Cost"], [annual_smart_cost], color="green")
plt.title("Annual Cost Comparison (Losses vs Smart Toolbox)")
plt.ylabel("Cost ($)")
plt.savefig("figure6_annual_cost_comparison.png", dpi=300)
plt.show()
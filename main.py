import matplotlib.pyplot as plt
import numpy as np
import random

# toolbox and loss inputs
# toolbox inventory estimate -- might need to replace
num_tools = 300
toolbox_value = 4655

# tool loss assumptions -- need to replace
tools_lost_per_month = 3

# smart toolbox costs -- need to replace
smart_toolbox_cost = 10000
annual_maintenance = 1000

# usage/time period
years = 5

# real tool cost distribution

tool_cost_distribution = [
    150, 300, 75, 250, 120, 450, 150, 200, 600, 120,
    60, 120, 250, 800, 250, 60, 300, 100, 160, 60, 60, 60
]

# simulate tool loss using real cost categories
def simulate_yearly_tool_loss(tools_lost_per_month, cost_distribution):
    losses = []
    for _ in range(tools_lost_per_month * 12):
        losses.append(random.choice(cost_distribution))
    return sum(losses)

# run single-year simulation
annual_loss_cost = simulate_yearly_tool_loss(tools_lost_per_month, tool_cost_distribution)

# cost calculations

cumulative_losses = np.cumsum([annual_loss_cost] * years)
smart_costs = [smart_toolbox_cost + annual_maintenance * i for i in range(years)]
roi = ((cumulative_losses[-1] - smart_costs[-1]) / smart_costs[-1]) * 100

break_even_year = None
for i in range(years):
    if smart_costs[i] <= cumulative_losses[i]:
        break_even_year = i + 1
        break

print("COST-BENEFIT SUMMARY")
print("Annual tool loss cost: $" + format(annual_loss_cost, ",.2f"))
print("5-year cumulative loss (no tracking): $" + format(cumulative_losses[-1], ",.2f"))
print("5-year smart toolbox cost: $" + format(smart_costs[-1], ",.2f"))
print("ROI over " + str(years) + " years: " + format(roi, ".2f") + "%")

if break_even_year:
    print("Break-even point: Year " + str(break_even_year))
else:
    print("Break-even point not reached within evaluation period.")

# cumulative losses over time

plt.figure(figsize=(8, 5))
plt.plot(range(1, years + 1), cumulative_losses, marker="o", label="Cumulative Losses")
plt.title("Cumulative Tool Loss Cost Over Time")
plt.xlabel("Years")
plt.ylabel("Cumulative Cost ($)")
plt.grid(True)
plt.legend()
plt.savefig("figure_cumulative_losses.png", dpi=300)
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
plt.savefig("figure_break_even.png", dpi=300)
plt.show()

# tool category costs

plt.figure(figsize=(8, 5))
plt.hist(tool_cost_distribution, bins=10, color="skyblue", edgecolor="black")
plt.title("Distribution of Tool Category Costs")
plt.xlabel("Category Cost ($)")
plt.ylabel("Frequency")
plt.grid(axis="y")
plt.savefig("figure_cost_histogram.png", dpi=300)
plt.show()

# monte carlo simulation to show variability in annual losses based on tool cost distribution

def simulate_many_years(n_runs, tools_lost_per_month, distribution):
    results = []
    for _ in range(n_runs):
        results.append(simulate_yearly_tool_loss(tools_lost_per_month, distribution))
    return results

mc_results = simulate_many_years(1000, tools_lost_per_month, tool_cost_distribution)

plt.figure(figsize=(8, 5))
plt.hist(mc_results, bins=30, color="lightgreen", edgecolor="black")
plt.title("Monte Carlo Simulation: Annual Tool Loss Distribution (1000 Runs)")
plt.xlabel("Annual Tool Loss ($)")
plt.ylabel("Frequency")
plt.grid(axis="y")
plt.savefig("figure_monte_carlo.png", dpi=300)
plt.show()

# sensitivity analysis: break-even year vs tools lost per month

loss_rates = range(1, 11)
break_even_years = []

for rate in loss_rates:
    annual_sim_loss = simulate_yearly_tool_loss(rate, tool_cost_distribution)
    cumulative_sim = np.cumsum([annual_sim_loss] * years)

    be_year = None
    for i in range(years):
        if smart_costs[i] <= cumulative_sim[i]:
            be_year = i + 1
            break
    break_even_years.append(be_year if be_year else None)

plt.figure(figsize=(8, 5))
plt.plot(loss_rates, break_even_years, marker="o")
plt.title("Break-Even Year vs Tools Lost per Month")
plt.xlabel("Tools Lost per Month")
plt.ylabel("Break-Even Year")
plt.grid(True)
plt.savefig("figure_sensitivity_break_even.png", dpi=300)
plt.show()

# annual loss vs smart toolbox annual cost

annual_smart_cost = smart_toolbox_cost / years + annual_maintenance

plt.figure(figsize=(8, 5))
plt.bar(["Annual Tool Loss"], [annual_loss_cost], color="tomato")
plt.bar(["Smart Toolbox Annual Cost"], [annual_smart_cost], color="green")
plt.title("Annual Cost Comparison: Tool Loss vs Smart Toolbox")
plt.ylabel("Cost ($)")
plt.savefig("figure_annual_cost_comparison.png", dpi=300)
plt.show()
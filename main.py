import matplotlib.pyplot as plt
import numpy as np

# toolbox inventory estimate
num_tools = 300
toolbox_value = 4655

# tool loss assumptions -- need to replace
tools_lost_per_month = 3

avg_tool_cost = 30

# smart toolbox costs -- need to replace
smart_toolbox_cost = 10000
annual_maintenance = 1000

# usage/time period
years = 5

# annual losses with current toolbox
annual_loss_cost = tools_lost_per_month * 12 * avg_tool_cost

# cumulative losses (years)
cumulative_losses = np.cumsum([annual_loss_cost] * years)

# smart toolbox cumulative cost
smart_costs = [smart_toolbox_cost + annual_maintenance * i for i in range(years)]

# ROI after x years
roi = ((cumulative_losses[-1] - smart_costs[-1]) / smart_costs[-1]) * 100

# break-even point
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

# cumulative loss line graph
plt.figure(figsize=(8, 5))
plt.plot(range(1, years + 1), cumulative_losses, marker="o", label="Cumulative Losses")
plt.title("Cumulative Tool Loss Cost Over Time")
plt.xlabel("Years")
plt.ylabel("Cumulative Cost ($)")
plt.grid(True)
plt.legend()
plt.savefig("cumulative_loss_cost.png")
plt.close()

# smart toolbox vs. current system (break-even)
plt.figure(figsize=(8, 5))
plt.plot(range(1, years + 1), cumulative_losses, marker="o", label="Losses Without Smart Toolbox")
plt.plot(range(1, years + 1), smart_costs, marker="s", label="Smart Toolbox Cost")
plt.title("Break-Even Comparison: Smart Toolbox vs Current Losses")
plt.xlabel("Years")
plt.ylabel("Cost ($)")
plt.grid(True)
plt.legend()
plt.savefig("break_even_comparison.png")
plt.close()
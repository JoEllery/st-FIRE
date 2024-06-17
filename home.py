import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

returns = pd.read_csv("http://www.dsm.business/data/stock_history.csv")

sb = st.text_input("Starting balance: ", 1000000)
aw = st.text_input("Annual withdrawl: ", 70000)
yr = st.text_input("Years of retirement: ", 35)
ps = st.text_input("Percentage stocks: ")

if sb and aw and yr and ps:

  st.write("Working!")

  vanguard_results = np.zeros(1000)

  # Iterate over simulations
  for i in range(1000):

    # Reset withdrawl and balance to starting values
    withdraw = int(aw)
    balance = int(sb)

    # Simulate over 35 years
    for y in range(int(yr)):

      # Choose a random year to use for data (done by choosing a random row of the dataframe)
      random_row = np.random.choice(range(len(returns)))

      # Extract inflation from that year
      inflation = returns.loc[random_row, 'inflation']

      # Scale up withdrawl for cost of living changes
      withdraw = withdraw * (1 + inflation)

      # Extract stock and bond returns from the same year
      stock_ret = returns.loc[random_row, 'stocks']
      bond_ret = returns.loc[random_row, 'bonds']
      ret = (float(ps) * stock_ret) + ((1-float(ps)) * bond_ret)

      # Calculate the new balance given the withdrawl and returns
      balance = (balance - withdraw) * (1 + ret)

      # No debt!
      if balance < 0:

        balance = 0

    vanguard_results[i] = balance

  quants = np.quantile(vanguard_results, [.10, .25, .5, .75, .9])
  prob = np.sum(vanguard_results>0)/1000

  st.write("Your probability of surviving retirement is: " + str(prob))

  fig, ax = plt.subplots(figsize=(5, 5))
  
  ax.hist(vanguard_results)  # Plot transformer sentiment

  ax.set_ylabel('Count')  # Label for the y-axis
  ax.set_title('Simulated Distribution of Account Balances')  # Title of the chart
  ax.set_xlabel("Final Balance") # Label for the x-axis
  
  # Display the plot!
  st.pyplot(fig)

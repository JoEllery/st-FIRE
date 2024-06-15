import streamlit as st
import numpy as np
import pandas as pd

returns = pd.read_csv("http://www.dsm.business/data/stock_history.csv")

sb = st.text_input("Starting balance: ", placeholder = 1000000)
aw = st.text_input("Annual withdrawl: ", placeholder = 70000)
yr = st.text_input("Years of retirement: ", placeholder = 35)
ps = st.text_input("Percentage stocks: ")

if sb and aw and yr and ps:

  vanguard_results = np.zeros(1000)

  # Iterate over simulations
  for i in range(1000):

    # Reset withdrawl and balance to starting values
    withdraw = aw
    balance = sb

    # Simulate over 35 years
    for y in range(yr):

      # Choose a random year to use for data (done by choosing a random row of the dataframe)
      random_row = np.random.choice(range(len(returns)))

      # Extract inflation from that year
      inflation = returns.loc[random_row, 'inflation']

      # Scale up withdrawl for cost of living changes
      withdraw = withdraw * (1 + inflation)

      # Extract stock and bond returns from the same year
      stock_ret = returns.loc[random_row, 'stocks']
      bond_ret = returns.loc[random_row, 'bonds']
      ret = (ps * stock_ret) + ((1-ps) * bond_ret)

      # Calculate the new balance given the withdrawl and returns
      balance = (balance - withdraw) * (1 + ret)

      # No debt!
      if balance < 0:

        balance = 0

    vanguard_results[i] = balance

  quants = np.quantile(vanguard_results, [.10, .25, .5, .75, .9])
  prob = np.sum(vanguard_results>0)/1000

  st.write("The 10th, 25th, 50th, 75th and 90th percentiles of returns are: ")
  st.write(quants)
  st.write("Your probability of surviving retirement is: " + str(prob))

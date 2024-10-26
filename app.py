import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a financial advisor that understands the user's financial condition, then suggests investment options accordingly to reach their long-term and short-term financial goals. "
         "Take into account the choice of time duration and the goal. Now specifically give the answers in pointers tailored towards their preferences and viability"
         "Give the investment option name also .In Indian Rupee Only"),
        ("user", "Question:[Age:{age}, Employment Status:{employment_status}, Invest/Month:{invest}, Goal:{primary_goal}, Term:{time_horizon}, Risk Level:{risk_level}, Target Amount:{target_amount}]")
    ]
)

# Streamlit framework
st.title('FutureFunds')

# Collecting User Inputs
input_age = st.number_input("Enter your age", 0, 100)
input_employment_status = st.selectbox("Choose your Employment Status", ['Select From Below', 'Employed', 'Unemployed', 'Freelancer', 'Student'])

# Savings Input
input_invest = st.number_input("Enter the amount you are willing to invest every month", min_value=0.0, format="%.2f")

# Choosing the approach: Investment or Debt Clearance
input_approach = st.selectbox("Select Investment / Debt Clearance", ('Investment', 'Debt Clearance'))

if input_approach == 'Investment':
    input_primarygoal = st.selectbox("What is your primary investment goal?", ('Wealth Accumulation', 'Retirement Planning', 'Education Funding'))

    # Additional inputs related to investment
    input_time_horizon = st.number_input("Enter the time horizon (in years) for this goal", min_value=1, max_value=50, step=1)
    input_risk_level = st.selectbox("What is your risk tolerance?", ['Low', 'Moderate', 'High'])
    input_target_amount = st.number_input("Enter your target amount for this investment goal", min_value=0.0, format="%.2f")

elif input_approach == 'Debt Clearance':
    # Debt-related inputs
    input_debttype = st.selectbox("What type of debt do you have?", ('Credit Card', 'Student Loan', 'Mortgage'))
    input_debtbalance = st.number_input('Enter the outstanding balance of the debt:')
    input_debtpay = st.number_input('What is the monthly payment for the debt')
    input_debtstrat = st.selectbox("Choose a debt repayment strategy", ('Debt Avalanche', 'Debt Snowball', 'Debt Consolidation', 'Debt Snowflake'))
    input_dependant = st.text_input("Do you have any dependents or responsibilities?")

# Debugging Outputs
st.write("Debugging Info:")
st.write("Age:", input_age)
st.write("Employment Status:", input_employment_status)
st.write("Investible Amount:", input_invest)

if input_approach == 'Investment':
    st.write("Primary Goal:", input_primarygoal)
    st.write("Time Horizon:", input_time_horizon)
    st.write("Risk Level:", input_risk_level)
    st.write("Target Amount:", input_target_amount)
elif input_approach == 'Debt Clearance':
    st.write("Debt Type:", input_debttype)
    st.write("Debt Balance:", input_debtbalance)
    st.write("Monthly Payment:", input_debtpay)
    st.write("Repayment Strategy:", input_debtstrat)
    st.write("Dependants:", input_dependant)

# Button for invoking the chain
clicked = st.button('Get Response')

# LLM interaction - Chain invocation
llm = Ollama(model="llama3.2")
output_parser = StrOutputParser()

# Chain invocation based on inputs
if clicked:
    if input_approach == 'Investment':
        # Ensure all required keys are present
        response = prompt | llm | output_parser
        try:
            result = response.invoke({
                'age': input_age,
                'employment_status': input_employment_status,
                'invest': input_invest,
                'primary_goal': input_primarygoal,
                'time_horizon': input_time_horizon,
                'risk_level': input_risk_level,
                'target_amount': input_target_amount
            })
            st.write(result)
        except KeyError as e:
            st.error(f"Key error: {e}")

    elif input_approach == 'Debt Clearance':
        # Ensure all required keys are present
        response = prompt | llm | output_parser
        try:
            result = response.invoke({
                'age': input_age,
                'employment_status': input_employment_status,
                'invest': input_invest,
                'debttype': input_debttype,
                'debtbalance': input_debtbalance,
                'debtpay': input_debtpay,
                'debtstrat': input_debtstrat,
                'dependants': input_dependant
            })
            st.write(result)
        except KeyError as e:
            st.error(f"Key error: {e}")

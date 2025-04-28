import numpy_financial as npf

EST_ENG_COST = 65 # Hourly rate of an engineer
INITIAL_INVESTMENT = -500000
SUBS = 20000
MAINTENANCE = EST_ENG_COST # Estimated one hour a week of maintenance on average
COST_OF_MISTAKES = (3*EST_ENG_COST) # Estimate three engineers on 4 3-hour calls a year
IQ = (EST_ENG_COST) # Estimate we will save 12 hours a year because of improved quality

# TC (Totoal Cost) includes the initial investment, subscription, and maintenance costs
TC = -INITIAL_INVESTMENT + SUBS + MAINTENANCE
# B (Benefits) includes Engineer Money Saved, Cost of Mistakes, and Improved Quality (IQ)
B = 608 + COST_OF_MISTAKES + IQ
# NB (Net Benefits) is the difference between TC and B
NB = B - TC
# ROI (Return on Investment) is the ratio of NB to TC, expressed as a percentage
ROI = (NB / TC) * 100
# IRR (Internal Rate of Return) is the rate at which the net present value of cash flows equals zero
IRR = npf.irr([INITIAL_INVESTMENT, B, B, B])
# Convert IRR to percentage
IRR = IRR * 100
# Print the results
print(f"Total Cost (TC): {TC}")
print(f"Benefits (B): {B}")
print(f"Net Benefits (NB): {NB}")
print(f"Return on Investment (ROI): {ROI}%")
print(f"Internal Rate of Return (IRR): {IRR}%")
#
# The above code calculates the ROI and IRR for a project based on various cost and benefit factors.
# It uses the numpy financial library to calculate the IRR and prints the results.
# The calculations are based on the following assumptions:

%initial state
user(insurenceCompany).
user(advertismentCompany).
user(retailCompany).

monitor(watchdog). %agant tasked with 



data(govData). 
data(healthRiskData).
data(healthStatistics). %has matching vars with healthRiskModel but no protected attributes
data(housingData).

data(newData1).
data(newData2).

isEmpty(newData1).
isEmpty(newData2).



%govData
citizen('Alex Johnson', 29, single).
citizen('Maria Gonzalez', 34, married).
citizen('Kevin Smith', 42, divorced).
citizen('Emily Davis', 27, married).
citizen('James Brown', 31, single).

%healthRiskData
patient('Alex Johnson', 29, good).
patient('Maria Gonzalez', 34, good).
patient('Kevin Smith', 42, bad).
patient('Emily Davis', 27, good).
patient('James Brown', 31, single).



model(healthRiskModel).
model(happinessModel). %has matching vars with govData (protected with no protected), has matchin vars with healthStatistics (no protected with no protected)


%privacy
private(healthRiskData).

%variables
hasProtectedAttributes(govData).
hasProtectedAttributes(healthRiskData).
hasProtectedAttributes(healthRiskModel).

hasMatchingVars(healthRiskData, healthRiskModel).
hasMatchingVars(govData, healthRiskModel).
hasMatchingVars(healthStatistics, healthRiskModel).
hasMatchingVars(govData, happinessModel).
hasMatchingVars(healthStatistics, happinessModel).
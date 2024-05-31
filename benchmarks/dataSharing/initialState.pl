%initial state
user(insurenceCompany).
user(advertismentCompany).
user(retailCompany).

monitor(watchdog). %agant tasked with 



data(govData). 
data(healthRiskData).
data(healthStatistics). %has matching vars with healthRiskModel but no protected attributes
data(housingData).



%govData
citizen(['Alex Johnson', 29, 'single']).
citizen(['Maria Gonzalez', 34, 'married']).
citizen(['Kevin Smith', 42, 'divorced']).
citizen(['Emily Davis', 27, 'married']).
citizen(['James Brown', 31, 'single']).

%healthRiskData
patient(['Alex Johnson', 29, 'good']).
patient(['Maria Gonzalez', 34, 'good']).
patient(['Kevin Smith', 42, 'bad']).
patient(['Emily Davis', 27, 'good']).
patient(['James Brown', 31, 'good']).




model(healthRiskModel).
model(happinessModel). %has matching vars with govData (protected with no protected), has matchin vars with healthStatistics (no protected with no protected)


varNames(govData, ["name", "age", "status"]).
varNames(healthRiskData, ["name", "age", "health"]).
varNames(healthStatistics, ["name", "age", "health"]).
varNames(housingData, ["propertyType", "price"]).
varNames(healthRiskModel, ["age", "health"]).

nameLink(govData, citizen).
nameLink(healthRiskData, patient).



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
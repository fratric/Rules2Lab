%initial state
user(insurenceCompany).

user(goverment).
user(hospital).
%user(supermarket).
%user(consultancy).

advisor(normativeAdvisor). %agant tasked with 


data(govData). %goverment
data(healthRiskData). %hospital
%data(groceriesData). %supermarket
%data(tradingData). %consultancy
data(auditData). %consultancy
data(electionData). %goverment
%data(advertismentData). %supermarket
data(geriatryData).
data(countryHealthData).
data(surnameMapData).
data(ageMapData).

model(healthRiskModel). %hospital
model(countryHealthModel).
model(ageMapModel).
model(surnameMapModel).

owns(goverment, govData).
owns(goverment, electionData).
owns(hospital, healthRiskData).
owns(hospital, healthRiskModel).
owns(hospital, geriatryData).
owns(goverment, countryHealthData).
owns(goverment, surnameMapData).
owns(goverment, ageMapData).
owns(goverment, countryHealthModel).
owns(goverment, ageMapModel).
owns(goverment, surnameMapModel).

%privacy
private(healthRiskData).
private(auditData).

%data costs
cost(govData, 100).
cost(electionData, 80).
cost(healthRiskData, 1000).
cost(geriatryData, 70).
cost(countryHealthData, 60).
cost(surnameMapData, 40).
cost(ageMapData, 40).
%model costs
cost(healthRiskModel, 900).
cost(countryHealthModel, 40).
cost(ageMapModel, 40).
cost(surnameMapModel, 40).


varName(govData).
varName(healthRiskData).
varName(surnameMapData).
varName(surnameMapModel).

varAge(govData).
varAge(healthRiskData).
varAge(electionData).
varAge(geriatryData).
varAge(healthRiskModel).
varAge(ageMapData).
varAge(ageMapModel).

varHealth(healthRiskData).
varHealth(geriatryData).
varHealth(healthRiskModel).
varHealth(countryHealthData).
varHealth(countryHealthModel).
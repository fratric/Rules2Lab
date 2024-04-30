:- dynamic advisor/1, varName/1, varHealth/1, varAge/1, varCountry/1. 
:- dynamic owns/2, private/1, user/1, data/1, model/1, cost/2. 
:- dynamic hasAccess/2. %user_name, data_address

%
% %Declaration of types
%


%observable facts
isObservable(user,1).
isObservable(data,1).
isObservable(model,1).
isObservable(private,1).
isObservable(owns,2).
isObservable(hasAccess,2).
%isObservable(hasProtectedAttributes,1).
isObservable(varName,1).
isObservable(varHealth,1).
isObservable(varAge,1).
isObservable(varCountry,1).

%agents
isAgent(user).
isAgent(advisor).
isAgent(officer).

%atomic actions
isAction(nullAction, 1).
isAction(gainAccess, 2). %user_name, data_address
isAction(infer, 3). %user_name, data_address
isAction(checkPrivacy, 3).

%
% %Helper predicates
%

agent(X) :- user(X); advisor(X).

hasCredit(X) :- 
    user(X),
    findall(B,hasAccess(X,B),L1),
    length(L1,N1),
    N1 < 2.

%
% %Action preconditions
%


%synactic constraints on actions
sc_nullAction(X) :- agent(X).
sc_gainAccess(X,A) :- user(X), (data(A);model(A)), not(private(A)).
sc_infer(X,A,B) :- user(X), data(A), model(B).

%semantic constraints on actions
nullAction(X) :- sc_nullAction(X).
gainAccess(X,A) :- sc_gainAccess(X,A), not(owns(X,A)), not(hasAccess(X,A)), not(hasAccess(X,A)), hasCredit(X).
infer(X,A,B) :- sc_infer(X,A,B), hasAccess(X,A), hasAccess(X,B). 

gatherData(X) :- advisor(X).
learnNorm(X) :- advisor(X).
integrateNorm(X) :- advisor(X).

%
% %Other predicates
%


solution(Y,A,B) :- 
    user(Y),
    data(A),
    (owns(Y,A);hasAccess(Y,A)),
    model(B),
    (owns(Y,B);hasAccess(Y,B)),
    %hasProtectedAttributes(A),
    %hasProtectedAttributes(B).
    varName(A),
    varAge(A),
    varAge(B),
    varHealth(B).

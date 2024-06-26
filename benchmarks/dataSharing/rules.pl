:- dynamic terminated/1, user/1, enforcer/1.
:- dynamic data/1, model/1, private/1, hasPrivateAttributes/1, hasMatchingVars/2, varNames/2, nameLink/2. 
:- dynamic hasAccess/2, performedInference/3, gainAccess/2.

%
% %Declaration of types
%

isAgent(user).
isAgent(enforcer).


object(A) :- data(A);model(A).

%state variables
isStateVar(user,1).
isStateVar(data,1).
isStateVar(model,1).
isStateVar(private,1).
isStateVar(hasPrivateAttributes,1).
isStateVar(hasMatchingVars,2).
isStateVar(hasAccess,2).
isStateVar(performedInference,3).


%observable facts
%isObservable(hasAccess,2).


%static forms of observables
static_hasAccess(X,A) :- user(X), object(A).

%atomic actions
isAction(nullAction, 1).
isAction(gainAccess, 2).
isAction(infer, 3).

%
% %Helper predicates
%

agent(X) :- user(X); enforcer(X).

hasAccessListData(X, L) :- user(X), findall(B, (data(B),hasAccess(X,B)), L).
hasAccessNumData(X,N) :- hasAccessListData(X,L), length(L,N).
hasCreditData(X) :- hasAccessNumData(X,N), N < 1.

hasAccessListModel(X, L) :- user(X), findall(B, (model(B),hasAccess(X,B)), L).
hasAccessNumModel(X,N) :- hasAccessListModel(X,L), length(L,N).
hasCreditModel(X) :- hasAccessNumModel(X,N), N < 1.

hasCredit(X,A) :- object(A),hasAccessNumModel(X,N1), hasAccessNumData(X,N2), N1 + N2 < 2.

%hasCredit(X,A) :- data(A), hasCreditData(X).
%hasCredit(X,A) :- model(A), hasCreditModel(X).

%hasPrivateAttributes(A) :- data(A), data(B), A /== B, private(B), hasMatchingVars(A,B).


%
% %Action preconditions
%


%synactic constraints on actions
static_nullAction(X) :- user(X).
static_gainAccess(X,A) :- user(X), object(A), not(private(A)).
static_infer(X,A,B) :- user(X), data(A), model(B), hasMatchingVars(A,B).


%semantic constraints on actions
nullAction(X) :- static_nullAction(X).
gainAccess(X,A) :- static_gainAccess(X,A), not(hasAccess(X,A)), hasCredit(X,A).
%gainAccess(X,A) :- static_gainAccess(X,A), not(hasAccess(X,A)), hasCredit(X,A), not(hasAccess(X,B)), hasPrivateAttributes(B).
%restrictionPolicy(X,A) :- not(hasAccess(X,A)), hasPrivateAttributes(A).

infer(X,A,B) :- static_infer(X,A,B), hasAccess(X,A), hasAccess(X,B), not(performedInference(X,A,B)). 



%add here later hasMatchingVars or performedInference so that there's no need to check most of the time until something happens
terminate(X,A,B) :- user(X), not(terminated(X)), data(A), data(B), private(A), A \== B.


%
% %Transitions
% 

%every action is executable depending on the state, hence s -> a
%every action leads to known state fact assertions, hence s -> a ->s_new

transition(nullAction(_X0), [], 0).
transition(gainAccess(X0,X1), [+(hasAccess(X0,X1))], 10).
%transition(infer(X0,X1,X2), [+(performedInference(X0,X1,X2)), -(performInference(X0,X1,X2) )], 500).

%inferredData(govData,healthRiskModel).


%
% %Restriction norm
%

%restriction(X,A) :- user(X),object(A).

%
% %Other predicates
%

restriction_opt(X,B) :- user(X),object(B),object(A),A \== B,hasPrivateAttributes(B),hasAccess(X,A),hasPrivateAttributes(A).

solution(Y,A,B) :- 
    user(Y),
    data(A),
    not(private(A)),
    hasAccess(Y,A),
    model(B),
    not(private(B)),
    hasAccess(Y,B),
    hasPrivateAttributes(A),
    hasPrivateAttributes(B),
    performedInference(Y,A,B).

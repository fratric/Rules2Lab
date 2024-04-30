%enable_pi.

max_clauses(10).
max_vars(15).
max_body(15).

head_pred(norm,2).

body_pred(agent,1).
body_pred(data,1).
body_pred(model,1).
body_pred(private,1).
%body_pred(hasProtectedAttributes,1).

body_pred(varName,1).
body_pred(varAge,1).
body_pred(varHealth,1).

body_pred(hasAccess,2).
body_pred(owns,2).

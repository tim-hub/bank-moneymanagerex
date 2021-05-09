
## Steps

1. Loop each record (Deposit, Withdraw and Transfer out)
    1. Duplication Engine. Tell whether records exist in the DB, 
       1. if so, print and promote to ask manuuel check
    0. Distinguisher, distinguish W/D/T
    1. Inputer, Base on Details try to get payee from DB 
        1. Get payee and Cat SubCat IDs
    2. Payee Checker, Payee not exist, then create payee
        1. Promote to let user input category and subcategory(optional)
    3. Account Checker, For transfer, get account from table `DetailsToAccount`
        1. Promote to user input
    
P.S.
- credit ignore `Autopayment Thanks you`

## Steps

1. Loop each record (Deposit, Withdraw and Transfer out)
    1. Duplication Engine. Tell whether records exist in the DB, 
       1. if so, print and promote to ask manuuel check
    0. Distinguish W/D/T
    1. Base on Details try to get payee from DB 
        1. Get payee and Cat SubCat IDs
    2. Payee not exist, then create payee
        1. Promote to let user input category and subcategory(optional)
    3. For transfer, get account from table `DetailsToAccount`
        1. Promote to user input
    
P.S.
- credit ignore `Autopayment Thanks you`
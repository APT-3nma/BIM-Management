# 🏦 B.I.M.

**Note: Developing in progress**

BIM (Business Inventory Management) is an open-source system designed to help businesses manage their inventory. Instead of relying on manual data entry, BIM integrates AI to make the inventory processes faster, more efficient, and easier to scale.


**Note: Phase 1 in development**

**Changes:** 
New imports added. 
**Safe Password**
If the user has an special character or many special characters in the password of SQL line 28 is to solve that issue. 
**Environment path** Added an env_path to solve the issue of connecting the code chain of SQL and FastAPI.
**Raw Port Integration** Added raw_port to also solve a connection error, in cases in which your env file matches the same variable name in the main code but when trying to run it,  it returns an Error because the port that is being used needs to be cleaned, that's what cause the connection error.

**Note: Version 1.0.0**

**Note: new tables added to the database main code.**

**Update:**
**Supplier table added to both the database and the main code.** In order to provide a better organized experience we added a Supplier table including their contact info and id's. **Note: This can be modified by each user**
**Categories Table added.** To keep track of the category of each item this table is included for that, also to keep an order in each category.
**Transaction Table.** **Just added** This table is to keep track of the transaction Inbound and outbound transactions.
**InventoryItem Table.** This table replace the default base "Product table" that was done a week ago, also it comes with new functions to track the item id's, the category they belong, suppliers, quantity and location of the items and their unit price. **Note: Each user can modify it.**
**New Imports to keep track of the date and times of each transaction.** We forgot to add this earlier.


**Update:**
**requirements.txt** This file store all the requirements in order to make the main code work to activate the dependencies once every file is downloaded, in the terminal write "pip install -r requirements.txt"


**Update:** The SQL Schema is now available. 


**Version 1.0.2 in progress**




# Analyses

-   For each recipient, who added you to the thread?
-   Who has never responded?
-   Who responds the most? Least?
-   Who has been added and removed?
-   Who says fuck the most?
-   Who says Portland the most?

# Components
- Find Messages by Thread
   - Input: subject line
   - Methods
   - Output: message(s), in dictionary format to add to DB
- Data class
   - Create DB
      - message schema
         - subject
         - message id
         - snippet
         - n_recipients
         - sender
         - date
         - internalDate
         - attachments
         - body
      - person schema
         - message id
         - name
         - email address
         - relationship (send, recieve)

   - Add messages to DB
   - Query DB?
- Analysis


# Pre-processing Steps

1.  Populate db [portland_updatedb.py]
    1.  Initialize DB
       1. SQLite file
    2.  Find all messages belonging to Portland
    3.  Loop by messages
        - Parse times
        - Parse headers
        - Store:
           - From
           - To
           - Subject
           - Time/Date
           - (Body)

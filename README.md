# portland
## email analytics of RE: Portland thread

The so-called "Portland thread" is a long-running email chain amongst a group of ~30 friends going for the past 6 years. We've used it to plan events, stay in touch, and share jokes mostly. Many people we've added along the way.

The purpose of this project is to load all of the messages into an SQLite database and perform some data science related actions on them. Currently, the focus is on loading the data efficiently and building up the database.

## Tasks:
1. Store data into SQLite db
2. Parse messages to seek "thread parent" of each person on the email chain (aka 'who added you')
3. Load data into Jupyter notebook and start to look at trends
  - Who responds the most?
  - Who has never responded?
  - Who has the best (largest) vocabulary?

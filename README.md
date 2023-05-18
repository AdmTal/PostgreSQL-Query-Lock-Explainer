# PostgreSQL Query Lock Explainer

Utility to show what locks will be acquired by a given query.

Query is executed but not committed.

> **Warning**
> 
> Don't run this on a production DB.
> 
> The suggested strategy is to run this using a test DB to figure out the locks
> And then use that information later if you need it.

## Installation instructions

```.env
pip install pg_explain_locks
```

## How this thing works

This tool runs a given query like this:

1. `BEGIN`
2. `-- Run given query`
3. `-- Check which locks are taken`
4. `ROLLBACK`

## Example Usage

Examples shown against [dvdrental sample database](http://www.postgresqltutorial.com/postgresql-sample-database/)

```.env
pg_explain_locks \
  --user DB_USER \
  --password DB_PASSWORD \
  --database DATABASE \
  --host HOST \
  --query "DROP table actor CASCADE"
  
+-------------+----------------------------+---------------------+
| Relation ID | Relation Name              | Lock Type           |
+-------------+----------------------------+---------------------+
| 16422       | actor                      | AccessExclusiveLock |
| 16448       | film_actor                 | AccessExclusiveLock |
| 16456       | actor_info                 | AccessExclusiveLock |
| 16487       | film_list                  | AccessExclusiveLock |
| 16506       | nicer_but_slower_film_list | AccessExclusiveLock |
| 16557       | actor_pkey                 | AccessExclusiveLock |
| 16588       | idx_actor_last_name        | AccessExclusiveLock |
+-------------+----------------------------+---------------------+

```

```.env
pg_explain_locks \
  --user DB_USER \
  --password DB_PASSWORD \
  --database DATABASE \
  --host HOST \
  --query "SELECT * FROM film_actor fa JOIN actor a on a.actor_id=fa.actor_id FOR UPDATE"
  
+-------------+---------------------+-----------------+
| Relation ID | Relation Name       | Lock Type       |
+-------------+---------------------+-----------------+
| 16422       | actor               | RowShareLock    |
| 16448       | film_actor          | RowShareLock    |
| 16557       | actor_pkey          | AccessShareLock |
| 16569       | film_actor_pkey     | AccessShareLock |
| 16588       | idx_actor_last_name | AccessShareLock |
| 16593       | idx_fk_film_id      | AccessShareLock |
+-------------+---------------------+-----------------+

```

```.env

pg_explain_locks \
  --user DB_USER \
  --password DB_PASSWORD \
  --database DATABASE \
  --host HOST \
  --query "ALTER TABLE customer ADD COLUMN deleted BOOLEAN"
  
+-------------+---------------+---------------------+
| Relation ID | Relation Name | Lock Type           |
+-------------+---------------+---------------------+
| 16411       | customer      | AccessExclusiveLock |
+-------------+---------------+---------------------+
```

## Example usage with settings file

Create a settings file at `~/.pg_explain_locks_settings` in order to use the same DB settings every time.

Settings file contents :
```.env
USER=your_user
PASSWORD=your_password
DATABASE=your_database
HOST=your_host
PORT=your_post
```

Usage:

```.env
pg_explain_locks "ALTER TABLE customer ADD COLUMN deleted BOOLEAN"

+-------------+---------------+---------------------+
| Relation ID | Relation Name | Lock Type           |
+-------------+---------------+---------------------+
| 16411       | customer      | AccessExclusiveLock |
+-------------+---------------+---------------------+
```



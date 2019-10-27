# PostgreSQL Query Lock Explainer

Utility to show what locks will be acquired by a given query.

Query is executed but not committed.

## Installation instructions

```.env
python3 -m venv venv
source ./venv/bin/activate
(venv) pip install requirements.txt
```

## Example Usage

Examples shown against [dvdrental sample database](http://www.postgresqltutorial.com/postgresql-sample-database/)
```
source ./venv/bin/activate
(venv) python explain_query_locks.py \
  --user DB_USER \
  --password DB_PASSWORD \
  --database DATABASE \
  --host HOST \
  --query "DROP table ACTOR CASCADE"
  
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
(venv) python explain_query_locks.py \
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

(venv) python explain_query_locks.py \
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


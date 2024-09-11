## 1. Backend Configuration

<details>
  <summary><strong>Project Dependencies</strong></summary>

### 1.1 Installing project dependencies

- Install [Python](https://www.python.org/downloads/)

### 1.2 DataBase Configuration

#### 1.2.1 Install and configure database
- Install [MariaDB](https://mariadb.org/download/?t=mariadb&o=true&p=mariadb&r=10.3.13&os=windows&cpu=x86&pkg=msi)
- After that, open the HeidiSQL application and configure with this information:

```sh
User: root
Password: root
Port: 3306
```

- This information can be checked in enviroments variables `vue-challenge\environments\.env.dev`

- These are the variables:

```sh
DATABASE_USER=root
DATABASE_PASSWORD=root
DATABASE_HOST=127.0.0.1:3306
```

- Create two new databases at the root with the name `vue-challenge` and `vue-challenge-test`.
- You don't need create the tables, just the database. More, in the next section

#### 1.2.2 To create database tables it's necessary perform the bellow command
- Open cmd in the `vue-challenge\backend` directory again
- Create a python virtual enviroment with:

```sh
py -m venv venv
```

- Open the virtual enviroment with: (on Windows)

```sh
venv\Scripts\activate
```

- Install the project dependencies with:

```sh
pip install -r requirements.txt
```

- perform `alembic upgrade head` command 
- In case of error, go to the file: `vue-challenge\backend\alembic.ini`, 
and change the code on line 56 according to your bank's credentials.:

```sh
sqlalchemy.url = mysql+pymysql://root:root@localhost:3306/vue-challenge
```

- Finally, run the code below to create the tables:

```sh
alembic upgrade head
```

- For more information about alembic, see the section `2.1 About Alembic`

**obs:** Using this command, the database is filled with some initial data. For example, an user admin and the tables needed to build menu are created.

</details>

<details>
<summary><strong>Start Application individually</strong></summary>

### 1.3 Starting the BackEnd application

- To start backend performing the command

```sh
uvicorn src.api:app --reload
```

- The server will open on http://127.0.0.1:8000
- Open your browser at http://127.0.0.1:8000/docs
- Then, you can create, read, update or delete users (Be happy!)

### 1.3 Endpoint test execution.

- To run the endpoint tests, simply start a new terminal session and place the following codes in sequence:

```sh
cd backend

venv\Scripts\activate

pytest
```

- As a result, 21 endpoint tests will be executed in sequence.

- Obs: The backend must be running on another terminal.

</details>

## 2. Frontend Run

- To run the frontend, simply run the following lines of code in a terminal:

```sh
cd frontend
npm i
npm run dev
```

- Remember to look at the environment variables to confirm that everything is ok.

- This information can be checked in enviroments variables `vue-challenge\environments\.env.dev`

- These are the variables:

```sh
BACKEND_URL=http://localhost:8000/
```

- When starting the project, it will be launched on the login screen. To access the system, simply use the following credentials:

```sh
username: admin
password: admin
```

- In the system, there are only two routes, the login screen defined by `http://localhost:8000/login/`, and the registration screen which is the following route, `http://localhost:8000/registration/`:

- You can only access the project if you are logged in to the system.

## 3. Clarification

This topic is not necessary to start the application, just to understand some technologies used.

<details>
<summary><strong>Clarification</strong></summary>

### 3.1 About Alembic
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
- With this tool, we can add migrations on application

### 2.2 Creating new revisions
- To create a new revision, use this command: `alembic revision -m "name_revision"` 
  (replace the name_revision for the correct name, for example `create users table`)
- The revision will be created in src/migration/versions directory
- On update() and downgrade() functions, make the necessary changes

```sh
alembic revision -m "name_revision"
```

### 3.3 Creating a new table
- To create a new table, add this code on upgrade() function:
```sh
op.create_table(
        'table_name',
        sa.Column('id', sa.Integer, primary_key=True),         # Create an id column of integer type as priority key and auto increment
        sa.Column('column2', sa.String(50), nullable=False),   # Create a column of type String(50), with not null
        sa.Column('column3', sa.Boolean, nullable=False),      # Create an id column of Boolean type, with not null
    )
```

- And to drop table, add this code on downgrade() function:
```sh
op.drop_table('table_name')  # Drop table
```

- To create table, follow the steps in section `1.2.2`
- And to Drop table, perform the command: `alembic downgrade base`

```sh
alembic downgrade base
```

### 3.4 Adding a new column to a table
- Create a new revision as section `2.2`
- To add a new column in a table, add this code on upgrade() funcion:
```sh
op.add_column('table_name', sa.Column('column_name', sa.String(50)))  # Adds a new column in table 'table_name'. Data type can be changed
```
    
- And to Drop Column, add this code on downgrade() function:
```sh
op.drop_column('table_name', 'column_name')  # Drop Column
```

</details>
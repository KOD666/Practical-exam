  

# SQL Queries

  

## 1. Create `Employee` Table

```sql

create table Employee(

  Empid int primary key,

  name varchar(18),

  dept varchar(12),

  hdate date

);

```

  

## 2. Create `Attendence` Table

```sql

create table Attendence(

  aid int primary key,

  Empid int,

  adate date,

  status varchar(10)

);

```

  

## 3. Add Foreign Key Constraint to `Attendence` Table

```sql

alter table Attendence

add constraint fk_att

foreign key (Empid) references Employee(Empid);

```

  

## 4. Create `leave` Table

```sql

create table leave(

  lid int primary key,

  Empid int,

  st_date date,

  end_date date,

  l_type varchar(20)

);

```

  

## 5. Add Check Constraint for `l_type` in `leave` Table

```sql

alter table leave

add constraint ck_leave

check(l_type in('Sick Leave','Vacation Leave', 'Duty Leave'));

```

  

## 6. Insert Data into `Employee` Table

```sql

insert into Employee values (01,'Arya','HR',to_date('2023-06-12','YYYY-MM-DD'));

insert into Employee values (02,'jj','Dean',to_date('2023-01-21','YYYY-MM-DD'));

```

  

## 7. Insert Data into `Attendence` Table

```sql

insert into Attendence values (1, 01, to_date('2025-04-01','YYYY-MM-DD'), 'absent');

insert into Attendence values (2, 02, to_date('2025-04-01','YYYY-MM-DD'), 'present');

```

  

## 8. Insert Data into `leave` Table

```sql

insert into leave (lid, Empid, st_date, end_date, l_type)

values (1, 1, to_date('2023-06-11', 'YYYY-MM-DD'), to_date('2023-06-13', 'YYYY-MM-DD'), 'Sick Leave');

  

insert into leave (lid, Empid, st_date, end_date, l_type)

values (2, 2, to_date('2023-07-09', 'YYYY-MM-DD'), to_date('2023-07-13', 'YYYY-MM-DD'), 'Vacation Leave');

```

  

## 9. Create `EmpAtt` View

```sql

CREATE VIEW EmpAtt AS

SELECT E.name, A.status, A.adate

FROM Employee E

JOIN Attendence A ON E.Empid = A.Empid;

```

  

## 10. Select Data from `EmpAtt` View

```sql

select * from EmpAtt;

```

  

## 11. Select Employees Not in `Leave` Table

```sql

SELECT *

FROM Employee

WHERE EmpID NOT IN (SELECT EmpID FROM leave);

```

  

## 12. Count Employees by Department

```sql

select dept, count(*) as T_Emp

from Employee

group by dept;

```
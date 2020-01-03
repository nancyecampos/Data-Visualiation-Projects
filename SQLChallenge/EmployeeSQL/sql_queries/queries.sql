--Create Employee Table
DROP TABLE IF EXISTS employees;
CREATE TABLE employees
(
	emp_no INT PRIMARY KEY NOT NULL,
	birth_date VARCHAR NOT NULL,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	gender VARCHAR NOT NULL,
	hire_date DATE NOT NULL
);

--Create Department Table
DROP TABLE IF EXISTS departments;
CREATE TABLE departments
(
	dept_no VARCHAR PRIMARY KEY NOT NULL,
	dept_name VARCHAR NOT NULL
);

--Create Department Employee Table
DROP TABLE IF EXISTS dept_emp;
CREATE TABLE dept_emp
(
	emp_no INT NOT NULL,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
	dept_no VARCHAR NOT NULL,
	FOREIGN KEY (dept_no) REFERENCES departments(dept_no),
	from_date VARCHAR NOT NULL,
	to_date VARCHAR NOT NULL
);

--Create Department Manager Table
DROP TABLE IF EXISTS dept_manager;
CREATE TABLE dept_manager
(
	dept_no VARCHAR NOT NULL,
	FOREIGN KEY (dept_no) REFERENCES departments(dept_no),
	emp_no INT NOT NULL,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
	from_date VARCHAR NOT NULL,
	to_date VARCHAR NOT NULL
);

--Create Salaries Table
DROP TABLE IF EXISTS salaries;
CREATE TABLE salaries
(
	emp_no INT NOT NULL,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
	salary INT NOT NULL,
	from_date VARCHAR NOT NULL,
	to_date VARCHAR NOT NULL
);

--Create Titles Table
DROP TABLE IF EXISTS titles;
CREATE TABLE titles
(
	emp_no INT NOT NULL,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
	title VARCHAR NOT NULL,
	from_date VARCHAR NOT NULL,
	to_date VARCHAR NOT NULL
);

--QUERIES

--List the following details of each employee: employee number, last name, first name, gender, and salary.
SELECT emp.emp_no, emp.last_name, emp.first_name, emp.gender, sal.salary
FROM salaries AS sal
INNER JOIN employees AS emp ON
emp.emp_no = sal.emp_no;

--List employees who were hired in 1986.
SELECT * FROM employees
WHERE hire_date BETWEEN '1986-01-01' AND '1987-01-01';

--List the manager of each department with the following information: department number, department name, the manager's employee number, last name, first name, and start and end employment dates.
SELECT dep.dept_no, dep.dept_name, man.emp_no, emp.last_name, emp.first_name, man.from_date, man.to_date
FROM departments AS dep
INNER JOIN dept_manager AS man ON
man.dept_no = dep.dept_no
JOIN employees AS emp ON
emp.emp_no = man.emp_no;

--List the department of each employee with the following information: employee number, last name, first name, and department name.
SELECT emp.emp_no, emp.last_name, emp.first_name, dep.dept_name
FROM employees AS emp
INNER JOIN dept_emp AS de ON
emp.emp_no = de.emp_no
INNER JOIN departments AS dep ON
dep.dept_no = de.dept_no;

--List all employees whose first name is "Hercules" and last names begin with "B."
SELECT * FROM employees
WHERE first_name = 'Hercules' AND last_name LIKE 'B%';

--List all employees in the Sales department, including their employee number, last name, first name, and department name.
SELECT emp.emp_no, emp.last_name, emp.first_name, dep.dept_name
FROM employees AS emp
INNER JOIN dept_emp AS de ON
emp.emp_no = de.emp_no
INNER JOIN departments AS dep ON
dep.dept_no = de.dept_no
WHERE dep.dept_name = 'Sales';

--List all employees in the Sales and Development departments, including their employee number, last name, first name, and department name.
SELECT emp.emp_no, emp.last_name, emp.first_name, dep.dept_name
FROM employees AS emp
INNER JOIN dept_emp AS de ON
emp.emp_no = de.emp_no
INNER JOIN departments AS dep ON
dep.dept_no = de.dept_no
WHERE dep.dept_name = 'Sales' OR dep.dept_name = 'Development';

--In descending order, list the frequency count of employee last names, i.e., how many employees share each last name.
SELECT last_name, COUNT(*) AS frequency
FROM employees
GROUP BY last_name
ORDER BY frequency DESC;
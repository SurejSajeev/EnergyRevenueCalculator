--Write a SQL query to find out Bob's daily rate on 15/06/2010

SELECT daily_rate
FROM Salary
WHERE emp_id = 1002
  AND start_date <= '2010-06-15'
ORDER BY start_date DESC
LIMIT 1;


--Write a SQL query to find everyone’s daily rate for 10/10/2010

SELECT e.emp_id, e.emp_name, s.daily_rate
FROM Employee e
JOIN Salary s ON e.emp_id = s.emp_id
WHERE s.start_date <= '2010-10-10'
  AND (e.end_date IS NULL OR e.end_date >= '2010-10-10')
ORDER BY e.emp_id, s.start_date DESC;


--Write a SQL query to find the daily spend for all employees in 2010

WITH daily_rates AS (
    SELECT e.emp_id, s.daily_rate,
           GREATEST(e.start_date, s.start_date) AS rate_start_date,
           LEAST(e.end_date, '2010-12-31') AS rate_end_date
    FROM Employee e
    JOIN Salary s ON e.emp_id = s.emp_id
    WHERE e.start_date <= '2010-12-31'
      AND (e.end_date IS NULL OR e.end_date >= '2010-01-01')
      AND s.start_date <= '2010-12-31'
)
SELECT SUM(daily_rate * (DATEDIFF(rate_end_date, rate_start_date) + 1)) AS total_spend_2010
FROM daily_rates
WHERE rate_start_date <= '2010-12-31'
  AND rate_end_date >= '2010-01-01';

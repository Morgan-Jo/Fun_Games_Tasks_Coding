-- ==========================================================
-- CLUE #1: The "After-Hours" Anomalies
-- Find all employees who entered the building between 00:00 and 04:00.
-- This narrows our list from 50 suspects down to the night-owls.
-- ==========================================================

SELECT 
    e.name, 
    e.department, 
    b.entry_time
FROM employees e
JOIN badge_access b ON e.emp_id = b.emp_id
WHERE time(b.entry_time) BETWEEN '00:00:00' AND '04:00:00'
ORDER BY b.entry_time DESC;


-- ==========================================================
-- CLUE #2: The Unauthorized Vault Access
-- Which employees entered the 'Server Vault' who are NOT in the 'IT' department?
-- This demonstrates your ability to cross-reference access permissions.
-- ==========================================================

SELECT 
    e.name, 
    e.department, 
    b.room_id, 
    b.entry_time
FROM employees e
JOIN badge_access b ON e.emp_id = b.emp_id
WHERE b.room_id = 'Server Vault'
AND e.department != 'IT';


-- ==========================================================
-- CLUE #3: The Statistical Outlier (The "Smoking Gun")
-- Identify any user whose single file download was 10x larger than 
-- their average download over the previous 30 days.
-- This uses a Window Function to establish a personal baseline for each user.
-- ==========================================================

WITH UserBaselines AS (
    SELECT 
        emp_id,
        file_name,
        file_size_mb,
        timestamp,
        AVG(file_size_mb) OVER(PARTITION BY emp_id) as personal_avg_size
    FROM network_logs
)
SELECT 
    e.name,
    ub.file_name,
    ub.file_size_mb,
    ub.personal_avg_size,
    (ub.file_size_mb / ub.personal_avg_size) as variance_factor
FROM UserBaselines ub
JOIN employees e ON ub.emp_id = e.emp_id
WHERE ub.file_size_mb > (ub.personal_avg_size * 10)
ORDER BY variance_factor DESC;
WITH SuspectList AS (
    -- Step 1: Find employees in the building during the leak
    SELECT DISTINCT emp_id 
    FROM badge_access 
    WHERE entry_time BETWEEN '2026-02-07 00:00:00' AND '2026-02-07 04:00:00'
),
BehavioralAnomalies AS (
    -- Step 2: Calculate rolling average file transfer size per employee
    SELECT 
        emp_id,
        action,
        file_size_mb,
        AVG(file_size_mb) OVER(PARTITION BY emp_id ORDER BY timestamp ROWS BETWEEN 10 PRECEDING AND 1 PRECEDING) as avg_last_10_files
    FROM network_logs
)
-- Step 3: Identify the mole (accessed during leak AND transferred 10x their usual size)
SELECT 
    e.name, 
    e.department, 
    ba.file_size_mb, 
    ba.avg_last_10_files
FROM employees e
JOIN BehavioralAnomalies ba ON e.emp_id = ba.emp_id
WHERE e.emp_id IN (SELECT emp_id FROM SuspectList)
AND ba.file_size_mb > (ba.avg_last_10_files * 10)
AND ba.action = 'FILE_DOWNLOAD';
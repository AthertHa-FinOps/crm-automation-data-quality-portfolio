-- Tables loaded by run_analysis.py:  crm(crm_id, first_name, last_name, email, phone, lead_source, city, province, created_date)
--                                    source(lead_id, first_name, last_name, email, phone, lead_source, city, province, created_date)
-- Dialect: SQLite (portable to Postgres/MySQL with minor changes).

-- Q1 duplicate contacts (same email after normalizing case/whitespace)
SELECT LOWER(TRIM(email)) AS norm_email, COUNT(*) AS records
FROM crm WHERE TRIM(email) <> ''
GROUP BY LOWER(TRIM(email)) HAVING COUNT(*) > 1;

-- Q2 missing email
SELECT crm_id, first_name, last_name FROM crm WHERE TRIM(email) = '';

-- Q3 invalid email format
SELECT crm_id, email FROM crm
WHERE TRIM(email) <> '' AND TRIM(email) NOT LIKE '%_@_%._%' OR TRIM(email) LIKE '%@@%';

-- Q4 email not normalized (uppercase or surrounding spaces)
SELECT crm_id, email FROM crm WHERE TRIM(email) <> '' AND email <> LOWER(TRIM(email));

-- Q5 non-standard phone (expected NNN-NNN-NNNN)
SELECT crm_id, phone FROM crm
WHERE phone NOT GLOB '[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]';

-- Q6 inconsistent province values (expected 'ON')
SELECT province, COUNT(*) AS records FROM crm WHERE province <> 'ON' GROUP BY province;

-- Q7 blank lead source
SELECT crm_id, email FROM crm WHERE TRIM(lead_source) = '';

-- Q8 source leads missing from CRM
SELECT s.lead_id, s.email FROM source s
LEFT JOIN crm c ON LOWER(TRIM(c.email)) = s.email WHERE c.crm_id IS NULL;

-- Q9 CRM records with an email that has no source lead
SELECT c.crm_id, c.email FROM crm c
LEFT JOIN source s ON s.email = LOWER(TRIM(c.email))
WHERE TRIM(c.email) <> '' AND s.lead_id IS NULL;

-- Q10 matched records where CRM and source disagree (last name or phone digits)
SELECT c.crm_id, s.lead_id, c.last_name AS crm_last, s.last_name AS src_last, c.phone AS crm_phone, s.phone AS src_phone
FROM crm c JOIN source s ON s.email = LOWER(TRIM(c.email))
WHERE c.last_name <> s.last_name
   OR REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(c.phone,'-',''),'(',''),')',''),' ',''),'.','') NOT IN (REPLACE(s.phone,'-',''), '1'||REPLACE(s.phone,'-',''), '+1'||REPLACE(s.phone,'-',''));

SELECT 
  DATE_PART('year', (p.resource->>'birthDate')::date) AS birthyear, 
  COUNT(*) AS num_patients 
FROM 
  patient p
GROUP BY 
  birthyear
HAVING 
  COUNT(*) > 1
ORDER BY birthyear;
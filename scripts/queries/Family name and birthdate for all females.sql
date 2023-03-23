SELECT 
  p.resource->>'birthDate' AS birthdate, 
  p.resource->'name'->0->>'family' AS family_name
FROM 
  patient p 
WHERE 
  p.resource->>'gender' = 'female';
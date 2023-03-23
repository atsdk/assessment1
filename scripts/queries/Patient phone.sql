SELECT resource#>>'{name,0,given,0}' as name,
       resource#>>'{name,0,family}' as surname,
       tel->>'value' as phone_number
FROM patient,
     jsonb_array_elements(resource->'telecom') tel
WHERE tel->>'system' = 'phone';
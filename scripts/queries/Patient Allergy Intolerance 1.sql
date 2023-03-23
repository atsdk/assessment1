SELECT p.resource#>>'{name,0,given,0}' as name,
       p.resource#>>'{name,0,family}' as surname
FROM patient p
JOIN patient_allergy_intolerance pai
	ON pai.patient_id = p.id
JOIN allergy a
	ON pai.allergy_code = a.code
WHERE 
	a.display IN ('Lisinopril', 'Tree nut (substance)');
SELECT
	o.id as observation_id,
	o.resource->>'effectiveDateTime' as date_time,
	o.resource#>>'{category,0,coding,0,code}' as obervation_type,
	p.id as patient_id,
	p.resource#>>'{name,0,given,0}' as patient_first_given_name,
	p.resource#>>'{name,0,family}' as patient_family_name
FROM observation o
JOIN patient p ON
RIGHT(
	o.resource#>>'{subject,reference}',
	LENGTH(o.resource#>>'{subject,reference}') - 9  /* Remove urn:uuid: */
) = p.id
ORDER BY patient_id;
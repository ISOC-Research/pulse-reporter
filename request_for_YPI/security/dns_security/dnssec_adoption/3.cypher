// DNSSEC signing check — identifies popular domains in the country that have
// DNSSEC-signed zones based on the 'dnssec' property on DomainName nodes in IYP.
// Domains with DNSSEC signing protect users from DNS cache poisoning attacks.
// The parameter $countryCode must be provided during execution (e.g., 'SN', 'FR', 'JP').
MATCH (c:Country {country_code: $countryCode})<-[q:QUERIED_FROM]-(d:DomainName)
WHERE d.dnssec IS NOT NULL
WITH d, q.value AS queryPercentage, d.dnssec AS dnssecStatus
ORDER BY queryPercentage DESC
LIMIT 25
RETURN d.name         AS domainName,
       queryPercentage AS queryPercentage,
       dnssecStatus    AS dnssecSigned;

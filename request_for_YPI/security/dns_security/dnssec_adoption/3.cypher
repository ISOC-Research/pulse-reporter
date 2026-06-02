MATCH ()-[r]->()
RETURN DISTINCT type(r)
ORDER BY type(r)
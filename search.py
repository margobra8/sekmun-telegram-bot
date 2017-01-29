#! python3
# -*- coding: utf-8 -*

"""
search.py - Módulo de consulta de información para SEKMUN Bot

SEKMUN Bot desarrollado por Marcos Gómez (http://margobra8.ml/)
Distribuido bajo la licencia MIT (ver LICENSE.md)
"""

import re

# Términos de búsqueda e información en Regex
paths = {
	# Mociones
	r"(?i)moci[oó]?n(es)? de (procedimiento)s?": "mociones/mocion_procedimiento.txt",
	r"(?i)moci[oó]?n(es)? de [óo]?rden(es)?": "mociones/mocion_orden.txt",
	r"(?i)moci[oó]?n(es)? de duda(s)?": "mociones/mocion_duda.txt",
	r"(?i)moci[oó]?n(es)? de (privilegio)s?": "mociones/mocion_privilegio.txt",
	r"(?i)moci[oó]?n(es)?": "mociones/mociones.txt",
	# Caucus
	r"(?i)caucus simple(s)?": "caucus/simple.txt",
	r"(?i)caucus moderado(s)?": "caucus/moderado.txt",
	r"(?i)caucus(es)?": "caucus/index.txt",
	# Debates Particulares y Anteproyectos
	r"(?i)debate(s)?( particular(es)?)?( de anteproyectos?)?": "debate_particular/index.txt",
	r"(?i)defender (el|los)? anteproyectos?": "debate_particular/index.txt",
	r"(?i)anteproyectos?": "anteproyecto/index.txt",
}

# Errores de búsqueda
error_notfound = "❌ _*ERROR*_\n\nNo se han encontrado resultados de búsqueda para\n<`{}`> 😕\n\nSi necesitas ejecutar un comando usa /ayuda para ver la lista."
error_empty = "search_empty.txt"

# Main method
def info_query(msg):
	for regex, path in paths.items():	
		if re.search(regex, msg):
			return open(path, "r").read()
			
		else:
			return error_notfound
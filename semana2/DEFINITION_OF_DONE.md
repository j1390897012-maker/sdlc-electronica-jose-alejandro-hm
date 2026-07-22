# Definition of Done (DoD)

Una User Story se considera terminada cuando cumple todos los siguientes criterios:

## Funcionalidad

- La implementación cumple con los criterios de aceptación definidos en la User Story.
- Los escenarios Gherkin asociados funcionan correctamente.
- Los casos de error y casos borde fueron considerados.

## Pruebas

- Existe al menos una prueba automatizada para la funcionalidad implementada.
- Todas las pruebas pasan correctamente con pytest.
- La cobertura del proyecto es igual o superior al 80%.

## Calidad del código

- El código cumple las reglas definidas por Ruff.
- No existen errores reportados por Mypy.
- Las funciones nuevas tienen tipos definidos cuando corresponde.

## Revisión

- La implementación fue revisada mediante Pull Request.
- El desarrollador revisó su propio diff línea por línea antes del merge.
- No existen cambios innecesarios dentro del PR.

## Documentación

- La documentación relacionada fue actualizada.
- README, backlog o archivos de soporte fueron modificados si la funcionalidad lo requiere.

## Control de versiones

- Los commits tienen mensajes claros.
- La rama corresponde a la User Story trabajada.
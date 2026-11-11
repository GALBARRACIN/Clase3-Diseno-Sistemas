# Resolución Tareas Clase 3 - Grupo 12

## Respuestas a Fragmentos de Código (CODIGO.pptx.pdf)
* **CÓDIGO 1 (Singleton)**: a) `True`. b) 1 vez[cite: 4].
* **CÓDIGO 2 (Factory Method)**: (1) `CreadorAvion`. (2) `precio`[cite: 5].
* **CÓDIGO 3 (Abstract Factory)**: a) `Pasaporte en EUR`. b) `FabricaMercado`[cite: 6].
* **CÓDIGO 4 (Builder)**: a) `6.0` (3% de 200). b) `246.0` (200+10+30+6)[cite: 7].
* **CÓDIGO 5 (Prototype)**: a) `2 3`. b) `deepcopy`[cite: 8].
* **CÓDIGO 6 (Adapter)**: a) `4550`. b) `True`[cite: 9].
* **CÓDIGO 7 (Bridge)**: a) `SMS: Vuelo confirmado`. b) `6` clases (3 tipos + 3 canales)[cite: 10].
* **CÓDIGO 8 (Composite)**: a) `620`. b) `precio`[cite: 11].
* **CÓDIGO 9 (Decorator)**: a) `204.0`. b) `216.0`[cite: 12].
* **CÓDIGO 10 (Facade)**: a) `VOUCHER-MDZ-BUE`. b) `4` pasos en el log[cite: 13].
* **CÓDIGO 11 (Flyweight)**: a) `True 2`. b) `_cache`[cite: 14].
* **CÓDIGO 12 (Proxy)**: a) `1` (usa caché). b) `2` (nueva ruta SLA)[cite: 15].
* **CÓDIGO 13 (Chain of Responsibility)**: a) `False`. b) `0` veces (corta en disponibilidad)[cite: 16].
* **CÓDIGO 14 (Command)**: a) `['Vuelo']`. b) `Comando`[cite: 17].
* **CÓDIGO 15 (Interpreter)**: a) `True`. b) `False`[cite: 18].
* **CÓDIGO 16 (Iterator)**: a) `[1, 2, 3, 4, 5]`. b) `yield`[cite: 19].
* **CÓDIGO 17 (Mediator)**: a) `2`. b) `0`[cite: 20].
* **CÓDIGO 18 (Memento)**: a) `4`. b) `3`[cite: 21].
* **CÓDIGO 19 (Observer)**: a) `1`. b) `1`[cite: 22].
* **CÓDIGO 20 (State)**: a) `True True False`. b) `Cancelada`[cite: 23].
* **CÓDIGO 21 (Strategy)**: a) `C`. b) Cliente/Contexto[cite: 24].
* **CÓDIGO 22 (Template Method)**: a) `4`. b) (1) `Voucher`, (2) `generar`[cite: 25].
* **CÓDIGO 23 (Visitor)**: a) `500`. b) `visitar_vuelo`[cite: 26].

---

## Módulo 4: Búsqueda, avisos y estados (Grupo_12.pdf)
* **P17 (Retomar pago interrumpido)**[cite: 27]: 
  * **Patrón elegido**: Memento. 
  * **Por qué**: Permite guardar el estado exacto del formulario (paso 3) y restaurarlo sin exponer su estructura interna.
  * **Descartado**: State, porque maneja comportamiento basado en estado actual, pero no guarda un historial para restaurar.
* **P19 (Ciclo de reserva Pendiente -> Cancelada)**[cite: 27]: 
  * **Patrón elegido**: State. 
  * **Por qué**: Permite que las acciones disponibles (confirmar, cancelar) cambien dinámicamente según el estado interno actual de la reserva.
  * **Descartado**: Strategy, porque aunque cambia el comportamiento, no está diseñado para transiciones en un ciclo de vida definido.
* **T4 (Botón Buscar lanza búsqueda - Trampa)**[cite: 27]: 
  * **Patrón elegido**: Ninguno. 
  * **Por qué**: Es un simple evento de UI que llama a una función. Usar un patrón estructural o de comportamiento aquí sería sobreingeniería.

---

## Escenario D: Ciclo de una reserva (Grupo_12.pdf)
* **Patrones elegidos**[cite: 28]: State (45), Chain of Responsibility (46), Template Method (47), Observer (48).
* **Combinación de patrones**[cite: 28]: El `Template Method` define el esqueleto general de la reserva con pasos fijos. En el paso específico de "validación", el método delega la tarea a un `Chain of Responsibility` que valida secuencialmente (documento -> disponibilidad -> pago) cortando al primer error.
* **Patrón descartado**[cite: 28]: Strategy se descartó para el flujo de reserva porque los pasos son fijos y secuenciales (mejor resuelto por Template Method), no algoritmos completamente intercambiables.

### Dibujo de cajas y flechas (Escenario D)

```mermaid
graph TD
    TM[Template Method] -->|Define los pasos fijos del flujo| CR[Chain of Responsibility]
    CR -->|Valida en secuencia y frena al error| ST[State]
    ST -->|Maneja las transiciones de la reserva| OB[Observer]
    OB -.->|Avisa al viajero en cada cambio| ST
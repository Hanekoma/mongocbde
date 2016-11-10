# CBDE - Laboratori 5
## Document explicatiu

En aquest laboratori de CBDE se'ns presenta un nou tipus de bases de dades no relacionals (NoSQL) anomenat *document stores*.
L'objectiu d'aquesta pràctica és entendre aquest tipus i saber dissenyar els documents de la manera més optima possible.

A l'enunciat d'aquesta pràctica tenim quatre *queries* que accedeixen a un seguit de taules donades, les quals hem de decidir com estructurar els documents per realitzar accessos de manera òptima.

Després d'haver analitzat una per una les quatre consultes donades, hem arribat a la conclusió que l'entitat òptima per dissenyar els documents és emmagatzemar els **LineItem**s com documents separats.
Llavors, d'ara cap endavant, explicarem la justificació analitzant consulta per consulta, finalment extraient la conclusió final.

### Query 1

En aquesta primera consulta disposem d'una *query* que selecciona molts elements, tots ells de l'entitat *LineItem*, agrupats i ordenats per dos atributs de la mateixa entitat, a més a més de filtrar comparant una data donada amb la data dels *lineitems*.
Per tant, hem arribat a la conclusió que tota aquesta consulta només depèn de l'entitat *LineItem*.

En conseqüència, dissenyar en aquest cas els documents per *lineitems* aportaria grans avantatges en conceptes d'eficiència i optimització en l'execució de la consulta. Llavors doncs elegiríem l'entitat *LineItem* com a element base per al disseny d'aquesta *query*.

### Query 2

Si parlem de la segona consulta donada, veiem com es seleccionen i es filtra per atributs de les entitats *PartSupp*, *Part*, *Supplier*, *Nation* i *Region*.
Totes elles, que d'un bon principi hem pensat que no tenien res a veure, tenen un gran tret característic en comú.
Si partim de la idea que tenim una *lineitem*, podem veure com des d'allà tenim només una *partsupplier*, la qual disposa d'una *part* i d'una *supplier*. Llavors des d'aquesta ultima entitat, podem veure que disposem només d'una *nation*, la qual a més a més disposa d'una *region*.

És a dir, dit d'una altra manera, per cada *lineitem* disposarem sempre d'una entitat de les comentades anteriorment. Per tant, partint des d'aquesta idea, hem vist que el disseny més òptim dels documents seria agafar com a entitat base l'entitat *LineItem*.
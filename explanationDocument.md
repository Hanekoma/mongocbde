**GRUP**: Oriol Muñoz i Albert Suàrez

# CBDE - Laboratori 5
## Document explicatiu

### Introducció

En aquest laboratori de CBDE se'ns presenta un nou tipus de bases de dades no relacionals (NoSQL) anomenat *document stores*.
L'objectiu d'aquesta pràctica és entendre aquest tipus i saber dissenyar els documents de la manera més optima possible.

A l'enunciat d'aquesta pràctica tenim quatre *queries* que accedeixen a un seguit de taules donades, les quals hem de decidir com estructurar els documents per realitzar accessos de manera òptima.

Després d'haver analitzat una per una les quatre consultes donades, hem arribat a la conclusió que l'entitat òptima per dissenyar els documents és emmagatzemar els **LineItem**s com documents separats.
Llavors, d'ara cap endavant, explicarem la justificació analitzant consulta per consulta, finalment extraient la conclusió final.



### Query 1

En aquesta primera consulta disposem d'una *query* que selecciona molts elements, tots ells de l'entitat *LineItem*, agrupats i ordenats per dos atributs de la mateixa entitat, a més a més de filtrar comparant una data donada amb la data dels *lineitems*.
Per tant, hem arribat a la conclusió que tota aquesta consulta només depèn de l'entitat *LineItem*.

En conseqüència, dissenyar en aquest cas els documents per *lineitems* aportaria grans avantatges en conceptes d'eficiència i optimització en l'execució de la consulta. Llavors doncs elegiríem l'entitat **LineItem** com a element base per al disseny d'aquesta *query*.

### Query 2

Si parlem de la segona consulta donada, veiem com es seleccionen i es filtra per atributs de les entitats *PartSupp*, *Part*, *Supplier*, *Nation* i *Region*.
Totes elles, que d'un bon principi hem pensat que no tenien res a veure, tenen un gran tret característic en comú.
Si partim de la idea que tenim una *lineitem*, podem veure com des d'allà tenim només una *partsupplier*, la qual disposa d'una *part* i d'una *supplier*. Llavors des d'aquesta ultima entitat, podem veure que disposem només d'una *nation*, la qual a més a més disposa d'una *region*.

És a dir, dit d'una altra manera, per cada *lineitem* disposarem sempre d'una entitat de les comentades anteriorment. Per tant, partint des d'aquesta idea, hem vist que el disseny més òptim dels documents seria agafar com a entitat base l'entitat **LineItem**.

### Query 3

Si ens referim a la tercera consulta, ens adonem que agrupa per tres valors dels quals pertanyen a l'entitat d'*order*, però que tot i així, partint des de l'entitat *lineitem*, només pot tenir un pertinent valor dels tres mencionats, ja que la cardinalitat de *lineitem* a *order* és d'1 a 1.
A més a més, aquesta consulta s'ordena per dos elements. El primer atribut per al qual s'ordena, *revenue*, és una suma d'un conjunt d'atributs de l'entitat *lineitem*. Per altra banda, el segon d'ells, *orderdate*, tot i pertànyer a l'entitat *order*, per cada *lineitem* només tindrà una *orderdate* donada la seva cardinalitat.
I com a últim punt, veure que també es consulten atributs de l'entitat *customer*, però que si partim de *lineitem* la seva cardinalitat seria d'1 a 1.

En conclusió, hem vist que l'entitat base per dissenyar els documents d'aquesta consulta és el **LineItem**.


### Query 4

Si per últim, si decidim analitzar la quarta consulta, veiem com accedim fins a sis entitats diferents: *customer*, *order*, *lineitem*, *supplier*, *nation* i *region*. Tot i així, si parem atenció als atributs seleccionats i per quins atributs s'agrupa i s'ordena, veiem com tots ells depenen o bé de l'entitat *order* o *lineitem*.
És a dir, que partint d'alguna d'aquestes entitats qualsevol, la cardinalitat a les altres entitats sempre seria 1. En conseqüència, aporta gran valor en ser candidata com a entitat base.

Tot i així, hem acabat decidint que el més òptim per elegir com entitat base ha estat el **LineItem**, sobretot pel fet que les altres tres consultes hem decidit *lineitem* com a entitat. Així doncs, les quatre queries coincidirien en la decisió.

### Conclusió

Finalment, després d'haver analitzat consulta per consulta, hem pogut veure com hem coincidit els quatre cops en la decisió de quina seria l'entitat base mes optima. Així doncs, elegim **LineItem** com l'entitat per dissenyar la nostra base de dades no relacional de tipus *document stores*.

Considerem, donades totes les justificacions realitzades, que aquesta opció és la que aporta més valor i millor anirà en la performance de les consultes, ja que obtindrem més eficiència a l'hora de rebre els resultats de la execució de les diferents queries donades.
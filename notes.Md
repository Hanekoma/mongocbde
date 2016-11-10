# Notes

## Sobre la base del document
No és lògic fer servir *Part*, *PartSupp*, *Supplier*, *Nation*, *Customer*, *Nation* ni *Region* com a base del document.

El motiu d'això és que, de fer-ho, s'haurien de fer més updates que inserts, i.e.,
cada vegada que es compri un product (*lineItem*) d'una order, s'hauria d'actualitzar el document dels anteriors. Això és *insanity*,
sobretot considerant que MongoDB és caca a l'hora de fer updates (diapositiva 41 Document Stores).

### Order vs Lineitem
Aquests dos ítems seran només insertats i, en principi, mai updatats. Per tant, són els millors candidats.

Triar (*hard?*) i modelar (*easy*).

Sobre les queries:

##### Primera query -> LineItem
- `Where l_shipdate < '[date]'`
- `Group by l_returnflag, l_linestatus`
- `Order by l_returnflag, l_linestatus`

##### Segona query -> LineItem
 `Where (rellevants, no relatius a joins):
 p_size = [SIZE],
 p_type LIKE '%[TYPE]',
 r_name = '[REGION]',
 ps_supply_cost = (
    SELECT min(ps_supplycost)
    FROM partsupp, supplier, nation, region
    WHERE (joins) AND r_name = ['REGION']
 )
 Order by s_acctbal desc, n_name, s_name, p_partkey`

 ##### Tercera query
- `Where c_mktsegment = '[SEGMENT]', o_orderdate < '[DATE1]', l_shipdate > '[DATE2]'`
- `Group by l_orderkey, o_orderdate, o_shippriority`
- `Order by revenue desc, o_orderdate`


 ##### Quarta query
- `Where (joins...) r_name = '[REGION]', o_orderdate >= date '[DATE]', o_orderdate < date '[DATE]' + blabla`
- `Group by n_name`
- `Order by revenue desc`


 ### Notes
- Revenue depèn de totes les lineitem de una order. Si volem índex, necessitem order com a document.
- Però ho volem...?
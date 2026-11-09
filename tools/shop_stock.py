#!/usr/bin/env python3
"""Genera src/data/shopStock.json: existencias del taller para la tienda (/tienda/).

Lee en solo-lectura la base local de Control Lumo y suma, por SKU, las piezas de
la línea Bestrijes que están en la ubicación «taller». La tienda es estática: esta
foto no se descuenta con cada venta, hay que volver a correr el script cuando
cambie el inventario.

Uso: python3 tools/shop_stock.py [ruta/a/control_lumo.db]
"""
import datetime
import json
import pathlib
import sqlite3
import sys

DB = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path.home() / "lumo_crm/local/control_lumo.db"
OUT = pathlib.Path(__file__).resolve().parent.parent / "src/data/shopStock.json"

SQL = """
select json_extract(c.datos, '$.sku'),
       coalesce((select sum(json_extract(e.datos, '$.cantidad'))
                 from documentos e
                 where e.coleccion = 'existencias'
                   and json_extract(e.datos, '$.sku') = json_extract(c.datos, '$.sku')
                   and json_extract(e.datos, '$.ubicacion') = 'taller'), 0)
from documentos c
where c.coleccion = 'catalogo'
  and json_extract(c.datos, '$.activo') = 1
  and json_extract(c.datos, '$.linea') = 'bestrijes'
  and json_extract(c.datos, '$.variante') in ('libre', 'llavero', 'iman', 'llavero_iman')
order by json_extract(c.datos, '$.orden')
"""


def main():
    if not DB.exists():
        sys.exit(f"No encuentro la base de Control Lumo en {DB}")
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        rows = con.execute(SQL).fetchall()
    finally:
        con.close()
    data = {
        "generado": datetime.date.today().isoformat(),
        "existencias": {sku: max(0, int(qty)) for sku, qty in rows},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(data["existencias"].values())
    print(f"{OUT.relative_to(OUT.parent.parent.parent)}: {len(rows)} SKU, {total} piezas en taller")


if __name__ == "__main__":
    main()

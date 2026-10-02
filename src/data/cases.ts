import type { SegmentId } from "./segments";

/**
 * Trabajos reales para negocios (clientes nombrados con permiso de Adriano,
 * 2026-10-01). Solo cifras confirmadas: si no hay cantidad confirmada, no se
 * pone ninguna — nunca inventar.
 */
export interface BusinessCase {
  client: string;
  sector: SegmentId;
  /** Qué se fabricó, en una línea citable. */
  what: string;
  /** Cantidad confirmada, si existe. */
  quantity?: string;
  technique: string;
  /** Filename in src/assets/{sectores,gallery,catalogo}. */
  image: string;
}

export const cases: BusinessCase[] = [
  {
    client: "Hotel en Cancún",
    sector: "hoteles-y-restaurantes",
    what: "Cuadros enmarcados para las habitaciones de un hotel, producidos y entregados como un solo lote.",
    quantity: "≈ 1,500 piezas",
    technique: "Producción en serie de arte enmarcado",
    image: "hotel-cuadros.jpg",
  },
  {
    client: "La Central Vinos & Licores",
    sector: "hoteles-y-restaurantes",
    what: "Señalética de marca en acrílico negro con grabado dorado, del mismo diseño en cada pieza.",
    technique: "Corte y grabado láser en acrílico",
    image: "hotel-la-central.jpg",
  },
  {
    client: "L'Oréal",
    sector: "marcas-y-corporativos",
    what: "Paletas de madera grabadas con el nombre de cada asistente para un evento corporativo.",
    technique: "Grabado láser personalizado por pieza",
    image: "gal-10.jpg",
  },
  {
    client: "BeStar Generation",
    sector: "eventos-y-bodas",
    what: "Placas de aluminio grabadas con el logo y la fecha del evento.",
    technique: "Grabado láser en aluminio",
    image: "corp-placas.jpg",
  },
  {
    client: "Emerald B2",
    sector: "marcas-y-corporativos",
    what: "Termos de acero grabados con el logo de la marca.",
    technique: "Grabado láser rotativo en acero",
    image: "corp-termo.jpg",
  },
];

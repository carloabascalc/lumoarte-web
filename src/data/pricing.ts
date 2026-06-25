// Contenido de la sección "¿Cómo calculamos tu precio?" por servicio.
// Láser tiene cifras reales (de la Fórmula de Cálculo de Adriano).
// 3D y gran formato describen el MODELO de precio sin cifras exactas
// hasta que Adriano confirme las tarifas — entonces se llena `tarifas`.

export interface PricingTipo {
  n: string;
  title: string;
  desc: string;
  tag: string;
  /** CSS color (token o valor). */
  accent: string;
}

export interface PricingComponente {
  name: string;
  points: string[];
}

/** Una lámina/material de la lista de precios (MXN, sin IVA). */
export interface PriceItem {
  name: string;
  /** Grosor o presentación (ej. "3 mm"). */
  spec?: string;
  /** Tamaño de lámina (ej. "122 × 81 cm"). */
  size?: string;
  /** Precio por lámina completa en MXN, sin IVA. */
  price: number;
}

export interface PriceGroup {
  category: string;
  items: PriceItem[];
}

/** Lista de precios de materiales, en HTML (no solo PDF) para que la IA y los
 *  buscadores puedan leer y citar las cifras. Mantener en sync con el PDF. */
export interface MaterialPricing {
  /** Nota al pie (moneda, IVA, vigencia, condiciones). */
  note: string;
  currency: string; // ISO 4217, ej. "MXN"
  year: number;
  groups: PriceGroup[];
}

/** Una herramienta / complemento (se vende por separado, sin servicio de corte). */
export interface ToolItem {
  name: string;
  /** Medida o presentación (ej. "100 ml", "18 mm", "unidad"). */
  measure?: string;
  /** Precio en MXN, sin IVA. */
  price: number;
}

/** Lista "Herramientas y complementos" (página 2 del PDF de precios). Va en su
 *  propia tabla, fuera del AggregateOffer de materiales del láser. */
export interface ToolsPricing {
  intro: string;
  note: string;
  currency: string;
  year: number;
  items: ToolItem[];
}

export interface PricingContent {
  intro: string;
  tipos: PricingTipo[];
  /** Etiquetas de los "chips" que suman al precio final. */
  flow: string[];
  componentes: PricingComponente[];
  /** Franja oscura de tarifas. Solo cuando hay cifras reales. */
  tarifas?: string; // permite <strong>…</strong>
  /** Si true, muestra el botón a la lista de precios (PDF real existe). */
  hasPriceList?: boolean;
  /** Ruta a la guía/fórmula en PDF, si existe. */
  formulaPdf?: string;
  /** Lista de precios de materiales en HTML (solo cuando hay cifras reales). */
  materiales?: MaterialPricing;
  /** Herramientas y complementos (página 2 del PDF), si existe. */
  herramientas?: ToolsPricing;
}

const TIPOS_GENERICOS = (noun: string): PricingTipo[] => [
  {
    n: "01",
    title: `${noun} listo para producir`,
    desc: "Listo a escala real y sin correcciones. Entra directo a producción.",
    tag: "Cotización inmediata",
    accent: "var(--color-accent)",
  },
  {
    n: "02",
    title: `${noun} con ajustes`,
    desc: "Requiere limpiar, escalar o preparar el archivo antes de producir.",
    tag: "Revisión previa",
    accent: "var(--color-muted)",
  },
  {
    n: "03",
    title: "Diseño a la medida",
    desc: "Proyecto nuevo o concepto desde cero. Lo diseñamos contigo.",
    tag: "Cotización manual",
    accent: "var(--color-accent-honey)",
  },
];

export const PRICING: Record<string, PricingContent> = {
  "corte-laser": {
    intro:
      "Sin sorpresas ni precios inflados. Cobramos por lo que realmente lleva tu pieza: el material que usa y el tiempo que tarda la máquina. Así se arma cada cotización.",
    tipos: [
      {
        n: "01",
        title: "Archivo listo para producir",
        desc: "Vector optimizado, a escala real y sin correcciones. Entra directo a corte.",
        tag: "Cotización inmediata",
        accent: "var(--color-accent)",
      },
      {
        n: "02",
        title: "Archivo con ajustes",
        desc: "Requiere vectorizar, escalar o limpiar duplicados antes de producir.",
        tag: "Revisión previa",
        accent: "var(--color-muted)",
      },
      {
        n: "03",
        title: "Diseño a la medida",
        desc: "Proyecto nuevo o concepto desde cero. Lo diseñamos y rediseñamos contigo.",
        tag: "Cotización manual",
        accent: "var(--color-accent-honey)",
      },
    ],
    flow: ["Material", "Tiempo de máquina", "Manejo", "IVA"],
    componentes: [
      {
        name: "Material",
        points: [
          "Según tipo, grosor y tamaño de lámina",
          "Aprovechamos el corte al máximo",
          "Solo pagas el material que usas",
        ],
      },
      {
        name: "Tiempo de máquina",
        points: [
          "Simulado en software especializado",
          "Redondeado al minuto + 30% de preparación",
          "$14 MXN por minuto de corte",
        ],
      },
      {
        name: "Manejo (4%)",
        points: [
          "Gestión y procesamiento del pedido",
          "Costos administrativos y operativos",
          "Se aplica sobre el subtotal",
        ],
      },
      {
        name: "IVA (16%)",
        points: [
          "Sobre subtotal + manejo",
          "Siempre desglosado en tu cotización",
          "Nunca escondido en el precio base",
        ],
      },
    ],
    tarifas:
      "Máquina <strong>$14 MXN / min</strong> · Diseño y ajustes <strong>$600 MXN / hr</strong> <span class=\"pf-tarifas-note\">(solo cuando el archivo lo requiere)</span>",
    hasPriceList: true,
    formulaPdf: "/como-cotizamos-corte-laser.pdf",
    materiales: {
      currency: "MXN",
      year: 2026,
      note: "Precios por lámina completa en MXN, sin IVA · vigentes 2026 · sobre pedido, disponibilidad sujeta a proveedor local (2 a 5 días hábiles). El precio final de tu pieza depende del material que usa y del tiempo de máquina — esto es solo el costo del material.",
      groups: [
        {
          category: "Acrílico",
          items: [
            { name: "Acrílico transparente", spec: "2 mm", size: "122 × 81 cm", price: 390 },
            { name: "Acrílico blanco", spec: "2 mm", size: "122 × 81 cm", price: 312 },
            { name: "Acrílico transparente", spec: "3 mm", size: "122 × 81 cm", price: 533 },
            { name: "Acrílico blanco", spec: "3 mm", size: "122 × 81 cm", price: 427 },
            { name: "Acrílico negro", spec: "3 mm", size: "122 × 81 cm", price: 515 },
            { name: "Acrílico de color", spec: "3 mm", size: "122 × 81 cm", price: 477 },
            { name: "Acrílico espejo plata", spec: "3 mm", size: "122 × 81 cm", price: 669 },
            { name: "Acrílico espejo oro", spec: "3 mm", size: "122 × 81 cm", price: 669 },
            { name: "Acrílico espejo rosa oro", spec: "3 mm", size: "122 × 81 cm", price: 669 },
            { name: "Acrílico fluorescente", spec: "3 mm", size: "122 × 81 cm", price: 583 },
            { name: "Acrílico transparente", spec: "6 mm", size: "122 × 81 cm", price: 953 },
            { name: "Acrílico blanco", spec: "6 mm", size: "122 × 81 cm", price: 758 },
            { name: "Lamicoid", spec: "1.5 mm", size: "61 × 122 cm", price: 546 },
          ],
        },
        {
          category: "MDF",
          items: [
            { name: "MDF", spec: "2.7 mm", size: "122 × 81 cm", price: 63 },
            { name: "MDF", spec: "3 mm", size: "122 × 81 cm", price: 82 },
            { name: "MDF", spec: "4.7 mm", size: "122 × 81 cm", price: 104 },
            { name: "MDF", spec: "5.5 mm", size: "122 × 81 cm", price: 121 },
            { name: "MDF", spec: "9 mm", size: "122 × 81 cm", price: 171 },
            { name: "MDF", spec: "12 mm", size: "122 × 81 cm", price: 206 },
          ],
        },
        {
          category: "Madera",
          items: [
            { name: "Triplay Okumé", spec: "4 mm", size: "122 × 81 cm", price: 169 },
            { name: "Triplay Okumé", spec: "6 mm", size: "122 × 81 cm", price: 221 },
            { name: "Triplay chapado Tzalam", spec: "6 mm", size: "122 × 81 cm", price: 304 },
            { name: "Chapa de madera", spec: "1 mm", size: "122 × 81 cm", price: 87 },
          ],
        },
        {
          category: "Otros materiales",
          items: [
            { name: "Cartón gris", spec: "2 mm", size: "70 × 100 cm", price: 72 },
            { name: "Cartón caple", spec: "2 mm", size: "70 × 100 cm", price: 98 },
            { name: "Cartón ilustración negro", size: "70 × 100 cm", price: 150 },
            { name: "Cartón ilustración blanco", size: "70 × 100 cm", price: 85 },
            { name: "Cartulina de color", size: "50 × 70 cm", price: 20 },
            { name: "Papel batería · delgada", spec: "1.5 mm", size: "69 × 112 cm", price: 129 },
            { name: "Papel batería · gruesa", spec: "2.5 mm", size: "69 × 112 cm", price: 233 },
            { name: "Coroplast", spec: "3 mm", size: "122 × 81 cm", price: 87 },
            { name: "Foamboard blanco", size: "80 × 120 cm", price: 207 },
            { name: "Foamboard negro", size: "80 × 120 cm", price: 207 },
            { name: "Foamy (EVA)", spec: "3 mm", size: "60 × 90 cm", price: 52 },
            { name: "Corcho", spec: "3 mm", size: "60 × 90 cm", price: 130 },
            { name: "Fieltro", spec: "3 mm", size: "100 × 90 cm", price: 130 },
            { name: "Tela natural", size: "100 × 90 cm", price: 169 },
            { name: "Cuero sintético", size: "100 × 90 cm", price: 195 },
            { name: "Piel natural", size: "por m²", price: 455 },
          ],
        },
      ],
    },
    herramientas: {
      currency: "MXN",
      year: 2026,
      intro:
        "Para maquetas y diseño: vendemos los materiales por separado, sin servicio de corte. Artículos de uso frecuente para arquitectura, diseño y modelismo, disponibles en Cancún.",
      note: "Precios en MXN, sin IVA · vigentes 2026 · precios de referencia · algunos artículos se gestionan sobre pedido, sujetos a disponibilidad local en Cancún.",
      items: [
        { name: "Silicón frío líquido Mil-U", measure: "100 ml", price: 75 },
        { name: "Silicón frío líquido Mil-U", measure: "250 ml", price: 163 },
        { name: "Silicón líquido", measure: "150 ml", price: 98 },
        { name: "Pegamento UHU", measure: "tubo 21 g", price: 52 },
        { name: "Pegamento en barra", measure: "40 g", price: 52 },
        { name: "Cutter Olfa", measure: "18 mm", price: 169 },
        { name: "Repuestos cutter Olfa", measure: "caja 10 pzas", price: 85 },
        { name: "Cutter", measure: "unidad", price: 117 },
        { name: "Regla metálica con corcho", measure: "30 cm", price: 117 },
        { name: "Base de corte", measure: "A3 · 30 × 45 cm", price: 364 },
        { name: "Masking tape", measure: "18 mm", price: 39 },
        { name: "Cinta doble cara", measure: "12 mm", price: 59 },
        { name: "Lápiz HB", measure: "unidad", price: 13 },
        { name: "Portaminas", measure: "0.5 mm", price: 78 },
        { name: "Borrador plástico", measure: "unidad", price: 20 },
        { name: "Pluma técnica", measure: "unidad", price: 104 },
        { name: "Rapidógrafo", measure: "0.5 mm", price: 260 },
        { name: "Escuadra 45°", measure: "25 cm", price: 111 },
        { name: "Escuadra 30°/60°", measure: "25 cm", price: 111 },
        { name: "Compás de dibujo", measure: "metálico", price: 156 },
        { name: "Acetato transparente", measure: "A3 · 0.3 mm", price: 30 },
      ],
    },
  },

  "impresion-3d": {
    intro:
      "Cobramos por lo que realmente consume tu pieza: el material y el tiempo que la impresora está trabajando. Sin mínimos ni precios inflados — así se arma cada cotización.",
    tipos: TIPOS_GENERICOS("Modelo 3D"),
    flow: ["Material", "Tiempo de impresión", "Manejo", "IVA"],
    componentes: [
      {
        name: "Material",
        points: [
          "Gramos de filamento o resina usados",
          "Según tecnología (FDM o resina) y acabado",
          "Solo pagas el material de tu pieza",
        ],
      },
      {
        name: "Tiempo de impresión",
        points: [
          "Calculado en el laminador antes de imprimir",
          "Depende de tamaño, relleno y resolución",
          "Incluye la preparación de la máquina",
        ],
      },
      {
        name: "Manejo",
        points: [
          "Gestión y procesamiento del pedido",
          "Post-proceso: retiro de soportes y limpieza",
          "Se aplica sobre el subtotal",
        ],
      },
      {
        name: "IVA (16%)",
        points: [
          "Sobre subtotal + manejo",
          "Siempre desglosado en tu cotización",
          "Nunca escondido en el precio base",
        ],
      },
    ],
  },

  "impresion-gran-formato": {
    intro:
      "Cobramos por el área que imprimes y el acabado que necesitas — nada más. Sin mínimos sorpresa ni precios inflados; así se arma cada cotización.",
    tipos: TIPOS_GENERICOS("Arte"),
    flow: ["Material", "Tinta", "Acabados", "IVA"],
    componentes: [
      {
        name: "Material",
        points: [
          "Por metro cuadrado de lona o vinil",
          "Según el sustrato y su resistencia",
          "Solo pagas el área que imprimes",
        ],
      },
      {
        name: "Tinta",
        points: [
          "Cobertura de tinta",
          "Resolución hasta 1440 dpi",
          "Depende de la calidad del archivo",
        ],
      },
      {
        name: "Acabados",
        points: [
          "Bastilla, ojillos, laminado o corte",
          "Montaje y terminado según el uso",
          "Se aplica sobre el subtotal",
        ],
      },
      {
        name: "IVA (16%)",
        points: [
          "Sobre subtotal + acabados",
          "Siempre desglosado en tu cotización",
          "Nunca escondido en el precio base",
        ],
      },
    ],
  },
};

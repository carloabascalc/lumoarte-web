// Catálogo general de Lumo — productos que ya se fabrican y se pueden pedir.
// Las fotos viven en src/assets/catalogo/<id>.jpg (mismo id que aquí).
// Precios en MXN (pesos). Crece poco a poco: agrega objetos a este arreglo.

export type CatalogCategory = "cajas" | "huacales" | "dijes" | "senaletica";

export interface CatalogProduct {
  id: string;
  name: string;
  desc: string;
  price: number; // MXN
  unit?: string; // p. ej. "c/u" para dijes
  from?: boolean; // muestra "Desde $X"
  category: CatalogCategory;
}

export const CATALOG_CATEGORIES: { id: CatalogCategory | "todos"; label: string }[] = [
  { id: "todos", label: "Todo" },
  { id: "cajas", label: "Cajas y regalo" },
  { id: "huacales", label: "Huacales y estuches" },
  { id: "dijes", label: "Dijes y llaveros" },
  { id: "senaletica", label: "Señalética" },
];

export const CATALOG: CatalogProduct[] = [
  {
    id: "caja-corazon-acrilico",
    name: "Caja corazón de acrílico",
    desc: "Caja corazón en acrílico cortada a láser. Para florerías, joyerías y eventos, por lote con tu logo.",
    price: 170,
    category: "cajas",
  },
  {
    id: "caja-flores-corazon",
    name: "Caja corazón para flores 20 cm",
    desc: "Caja corazón de 20 cm en MDF cortado a láser, para florerías y arreglos. Por lote, con tu marca.",
    price: 150,
    category: "cajas",
  },
  {
    id: "caja-mdf-dulces",
    name: "Caja MDF para dulces",
    desc: "Caja de MDF con tapa grabada. Dulceros para bodas y eventos, del mismo diseño en todo el lote.",
    price: 150,
    category: "cajas",
  },
  {
    id: "caja-regalo-mdf",
    name: "Caja de regalo MDF",
    desc: "Caja de regalo en MDF grabada con logo, nombre o fecha. Kits de bienvenida y regalo corporativo.",
    price: 200,
    category: "cajas",
  },
  {
    id: "caja-10x10x10",
    name: "Caja usos múltiples 10×10×10",
    desc: "Cubo de MDF de 10 cm para empaque de producto, joyería o amenidades. Personalizable por lote.",
    price: 60,
    category: "cajas",
  },
  {
    id: "caja-15x15x15",
    name: "Caja usos múltiples 15×15×15",
    desc: "Caja de MDF de 15 cm con tapa para empaque y kits. Personalizable por lote.",
    price: 135,
    category: "cajas",
  },
  {
    id: "cajones-personalizables",
    name: "Cajón personalizable",
    desc: "Cajón con compartimentos en triplay cortado a láser, grabado con tu marca. Para amenidades y kits.",
    price: 300,
    from: true,
    category: "cajas",
  },
  {
    id: "estuche-vino",
    name: "Estuche de vino deslizable",
    desc: "Estuche para botella de vino en triplay cortado a láser, con tapa deslizable. Regalo corporativo y amenidad de hotel.",
    price: 250,
    category: "huacales",
  },
  {
    id: "huacal-vintage",
    name: "Huacal vintage",
    desc: "Huacal en triplay cortado a láser, para canastas de regalo, despensas corporativas y exhibición.",
    price: 250,
    from: true,
    category: "huacales",
  },
  {
    id: "dije-triplay-tzalam",
    name: "Dije de marca en triplay Tzalam",
    desc: "Dije o etiqueta en madera Tzalam, grabado con tu marca. Ideal para producto artesanal.",
    price: 18,
    unit: "c/u",
    from: true,
    category: "dijes",
  },
  {
    id: "dijes-corporativos",
    name: "Dijes corporativos acrílico espejo",
    desc: "Dijes en acrílico espejo oro o plata, grabados con tu logo. Para eventos y empresas.",
    price: 10,
    unit: "c/u",
    from: true,
    category: "dijes",
  },
  {
    id: "indicador-estacionamiento",
    name: "Indicador de estacionamiento",
    desc: "Letrero de lugar de estacionamiento personalizado con nombre o logo. Señalética a la medida.",
    price: 600,
    from: true,
    category: "senaletica",
  },
];

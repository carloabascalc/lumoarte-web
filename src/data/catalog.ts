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
    desc: "Caja en forma de corazón en acrílico, ideal para regalo romántico, anillo o flores preservadas.",
    price: 170,
    category: "cajas",
  },
  {
    id: "caja-flores-corazon",
    name: "Caja corazón para flores 20 cm",
    desc: "Caja corazón de 20 cm para arreglo floral, rosas eternas o regalo sorpresa.",
    price: 150,
    category: "cajas",
  },
  {
    id: "caja-mdf-dulces",
    name: "Caja MDF para dulces",
    desc: "Caja de MDF con tapa grabada, perfecta para dulces, detalles o usos múltiples.",
    price: 150,
    category: "cajas",
  },
  {
    id: "caja-regalo-mdf",
    name: "Caja de regalo MDF",
    desc: "Caja de regalo en MDF, lista para personalizar con nombre, fecha o logo.",
    price: 200,
    category: "cajas",
  },
  {
    id: "caja-10x10x10",
    name: "Caja usos múltiples 10×10×10",
    desc: "Cubo de MDF de 10 cm, para detalles, joyería u organización. Personalizable.",
    price: 60,
    category: "cajas",
  },
  {
    id: "caja-15x15x15",
    name: "Caja usos múltiples 15×15×15",
    desc: "Caja de MDF de 15 cm con tapa, para regalo o almacenamiento. Personalizable.",
    price: 135,
    category: "cajas",
  },
  {
    id: "cajones-personalizables",
    name: "Cajón personalizable",
    desc: "Cajón de madera con compartimentos, para regalar a alguien querido. Grabado a la medida.",
    price: 300,
    from: true,
    category: "cajas",
  },
  {
    id: "estuche-vino",
    name: "Estuche de vino deslizable",
    desc: "Estuche de madera para botella de vino, con tapa deslizable. Regalo corporativo premium.",
    price: 250,
    category: "huacales",
  },
  {
    id: "huacal-vintage",
    name: "Huacal vintage",
    desc: "Huacal de madera estilo vintage, para arreglos, despensa de regalo o decoración.",
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

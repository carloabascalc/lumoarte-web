export interface Machine {
  id: "h2c" | "a2l" | "h3c";
  name: string;
  spec: string;
  note: string;
  alt: string;
}

export const MACHINES: Machine[] = [
  {
    id: "h2c",
    name: "Bambu Lab H2C",
    spec: "Volumen 330 × 320 × 320 mm · Multi-color hasta 4 filamentos",
    note: "Nuestra máquina para materiales técnicos: TPU, ASA, ABS, nylon y fibra de carbono. También piezas multicolor, producción por lote y prototipos rápidos.",
    alt: "Modelo animado de la impresora Bambu Lab H2C imprimiendo un engrane, con la unidad AMS y cuatro bobinas encima.",
  },
  {
    id: "a2l",
    name: "Bambu Lab A2L · Varias unidades",
    spec: "Volumen 330 × 320 × 325 mm · Multicolor con AMS",
    note: "Varias impresoras trabajando en paralelo para pedidos en volumen.",
    alt: "Modelo animado de varias impresoras Bambu Lab A2L imprimiendo lotes de piezas iguales al mismo tiempo, con su AMS de cuatro bobinas al lado.",
  },
  {
    id: "h3c",
    name: "Bambu Lab H3C · Próximamente",
    spec: "Volumen 330 × 320 × 325 mm · Hasta 9 materiales y colores con cambiador de herramientas",
    note: "Se suma a nuestro equipo: piezas multicolor y multimaterial por lote, con más capacidad de producción.",
    alt: "Modelo animado de la impresora Bambu Lab H3C cambiando de herramienta en su rack de nueve mientras imprime una pieza por bandas de color.",
  },
];

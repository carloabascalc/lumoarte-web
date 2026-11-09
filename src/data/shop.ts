import stockData from './shopStock.json';

/**
 * Tienda (/tienda/): venta al público de piezas de existencia.
 * Todo lo editable vive aquí: precios por presentación, envío y figuras.
 * Las existencias salen de shopStock.json (python3 tools/shop_stock.py).
 */

export type VariantId = 'libre' | 'llavero' | 'iman' | 'llavero_iman';

export interface ShopVariant {
  id: VariantId;
  label: string;
  desc: string;
  /** MXN, precio final al público. */
  price: number;
}

/** Precio único por presentación, igual para todas las figuras. */
export const VARIANTS: ShopVariant[] = [
  { id: 'libre', label: 'Figura', desc: 'La figura sola, para tenerla en la mano o en el escritorio.', price: 90 },
  { id: 'llavero', label: 'Llavero', desc: 'Con argolla para llaves o mochila.', price: 100 },
  { id: 'iman', label: 'Imán', desc: 'Con imán, para el refri o cualquier superficie metálica.', price: 100 },
  { id: 'llavero_iman', label: 'Llavero con imán', desc: 'Con argolla y con imán.', price: 110 },
];

export const SHIPPING = {
  /** Tarifa única de paquetería a todo México, MXN. */
  flat: 149,
  /** Subtotal desde el que el envío nacional es gratis, MXN. */
  freeFrom: 799,
  /** Recoger en el taller siempre es gratis. */
  pickup: 0,
};

export const SHOP = {
  /** 'whatsapp': el pedido se cierra por WhatsApp. 'mercadopago': cobro en línea (etapa 2). */
  checkout: 'whatsapp' as 'whatsapp' | 'mercadopago',
  /** Tope por renglón del carrito, además de la existencia. */
  maxPerLine: 20,
  /** Días naturales para reportar una pieza que llegó dañada o con defecto. */
  claimDays: 7,
};

export interface ShopFigure {
  /** Clave en Control Lumo: el SKU es `${id}-${variante}`. */
  id: string;
  slug: string;
  num: string;
  name: string;
  epithet: string;
  species: string;
  /** 'venta': tiene página y se puede comprar. 'proximamente': solo se anuncia en la vitrina. */
  status: 'venta' | 'proximamente';
  /** Archivo en src/assets/tienda/. */
  image?: string;
  imageAlt?: string;
  summary?: string;
  story?: string[];
  facts?: [string, string][];
  sayingTitle?: string;
  saying?: string;
}

export const FIGURES: ShopFigure[] = [
  {
    id: 'PINZU',
    slug: 'pinzu',
    num: '01',
    name: 'PINZU',
    epithet: 'El que cuenta las mareas',
    species: 'Cangrejo',
    status: 'venta',
    image: 'pinzu.png',
    imageAlt: 'PINZU, cangrejo articulado rojo de la colección Bestrijes de Lumo Cancún',
    summary:
      'El primero que dejó la Trije en la orilla. Ocho patas que cuelgan solas, dos pinzas que no sueltan y un ruido de cadena cuando lo mueves.',
    story: [
      'PINZU fue el primero que la corriente dejó en la arena, y por eso lleva el 01. No es de agua: es de orilla. Se entierra hasta que sólo le quedan los ojos fuera y espera. Nadie ha averiguado qué espera.',
      'Los que lo han tenido en la mano dicen lo mismo: agarra y no suelta. No por fuerza: por terquedad. Sus dos pinzas cierran y ahí se quedan hasta que a él le parece.',
      'Sus ocho patas cuelgan por su cuenta y suenan al moverlas, como una cadena de ancla corta. Los pescadores dicen que ese ruido es la forma en que un cangrejo cuenta las mareas, y que si lo oyes de noche es porque ya vienen.',
    ],
    facts: [
      ['Especie', 'Cangrejo de orilla'],
      ['Zona', 'La arena de Playa Delfines'],
      ['Carácter', 'Terco, paciente'],
      ['Señal', 'Dos pinzas que no sueltan'],
    ],
    sayingTitle: 'Lo que dicen de él',
    saying:
      'En Playa Delfines cuentan que si lo dejas en el borde de una mesa, al rato está del otro lado. Nadie lo ha visto moverse. Todos conocen a alguien a quien le pasó.',
  },
  {
    id: 'TIBRU',
    slug: 'tibru',
    num: '02',
    name: 'TIBRU',
    epithet: 'El que abre camino',
    species: 'Tiburón',
    status: 'venta',
    image: 'tibru.png',
    imageAlt: 'TIBRU, tiburón articulado gris de la colección Bestrijes de Lumo Cancún',
    summary:
      'El más chico de los tiburones y el más duro de todos. Va adelante: donde cabe TIBRU, cabe el resto.',
    story: [
      'TIBRU nació en el canal, donde el agua dulce de la laguna choca con el mar. Ahí la corriente va en dos direcciones a la vez y no pasa nada que tenga el cuerpo de una sola pieza. El suyo está partido en tres y por eso pudo salir.',
      'Sonríe siempre. Tiene más dientes de los que necesita y bastante menos miedo del que le tocaba, y esa combinación lo puso al frente: es el que entra primero a los lugares angostos y el que regresa a decir si se puede.',
      'Nunca se le ha visto quieto. Ni cuando duerme.',
    ],
    facts: [
      ['Especie', 'Tiburón del canal'],
      ['Zona', 'Entre la laguna y el mar'],
      ['Carácter', 'Sin miedo'],
      ['Señal', 'Más dientes de los que necesita'],
    ],
    sayingTitle: 'Lo que dicen de él',
    saying: 'Que sonríe porque ya sabe lo que va a pasar. Los pescadores del canal no lo encuentran gracioso.',
  },
  {
    id: 'CONTOY',
    slug: 'contoy',
    num: '03',
    name: 'CONTOY',
    epithet: 'El que lleva el mapa',
    species: 'Tiburón ballena',
    status: 'venta',
    image: 'contoy.png',
    imageAlt: 'CONTOY, tiburón ballena articulado con manchas de la colección Bestrijes de Lumo Cancún',
    summary:
      'El más grande de los bestrijes y el más manso. Boca enorme, ni un diente: lo suyo no es morder, es contar.',
    story: [
      'Cada verano, al norte de Isla Contoy, los tiburones ballena se juntan por cientos en el mismo pedazo de mar. Llegan, comen y se van. CONTOY es el que se quedó.',
      'Las manchas de su lomo no son manchas: son posiciones. Cada punto es un bestrije, y cuando aparece uno nuevo en la corriente, a CONTOY le sale un punto más. Por eso la costumbre, cuando se pierde alguno, es preguntarle a él.',
    ],
    facts: [
      ['Especie', 'Tiburón ballena'],
      ['Zona', 'Al norte de Isla Contoy'],
      ['Carácter', 'Manso, callado'],
      ['Señal', 'Manchas que son un mapa'],
    ],
    sayingTitle: 'Lo que dicen de él',
    saying:
      'Que si le hablas de cerca y dices un nombre, la mancha de ese bestrije se aclara un poco. Nadie ha conseguido comprobarlo con luz suficiente.',
  },
  {
    id: 'MENO',
    slug: 'meno',
    num: '04',
    name: 'MENO',
    epithet: 'El que vive al revés',
    species: 'Pez payaso',
    status: 'venta',
    image: 'meno.png',
    imageAlt: 'MENO, pez payaso articulado naranja con franjas blancas de la colección Bestrijes de Lumo Cancún',
    summary:
      'El más chico de carácter y el que más ruido hace. Se esconde cuando lo buscas y aparece cuando dejas de buscarlo.',
    story: [
      'MENO vive metido en una anémona que pica a todo el mundo menos a él. Ese es todo su plan y le ha funcionado: nunca ha tenido que pelear por nada.',
      'Su nombre está al revés, y él también. Nada de cabeza, duerme de lado y tiene la costumbre de desaparecer justo cuando alguien lo quiere ver. En cuanto te distraes, ahí está otra vez, mirándote de frente.',
      'Si tu bestrije es MENO, ya te habrás dado cuenta: no se queda donde lo pones.',
    ],
    facts: [
      ['Especie', 'Pez payaso'],
      ['Zona', 'Dentro de una anémona'],
      ['Carácter', 'Escandaloso y escondido'],
      ['Señal', 'Tres franjas'],
    ],
    sayingTitle: 'Lo que dicen de él',
    saying:
      'Que las franjas ni siquiera son suyas. Que se las puso para que la anémona lo confundiera con una piedra y lo dejara quedarse. Nadie se lo ha preguntado de frente.',
  },
  {
    id: 'IDORI',
    slug: 'idori',
    num: '05',
    name: 'IDORI',
    epithet: 'El que no se deja empujar',
    species: 'Pez cirujano',
    status: 'venta',
    image: 'idori.png',
    imageAlt: 'IDORI, pez cirujano articulado azul con cola amarilla de la colección Bestrijes de Lumo Cancún',
    summary:
      'Azul entero, cola amarilla y un filo a cada lado de la cola que no enseña casi nunca. Es el que menos ruido hace y al que nadie se le atraviesa.',
    story: [
      'IDORI se hizo esperar. La corriente lo trajo hasta Punta Nizuc, el arrecife más somero de todos, el que se ve desde la superficie, y ahí lo dejó dando vueltas un buen rato antes de soltarlo en la orilla.',
      'Es azul de arriba abajo, con una mancha negra que le cruza el lomo como una huella de mano y la cola amarilla. De cerca tiene lo que ninguno: a cada lado de la cola lleva un filo, plegado contra el cuerpo, que sólo asoma cuando alguien se pasa de listo.',
      'Casi nunca lo saca. No le hace falta: en el arrecife todos saben que está ahí, así que a IDORI no lo empujan, no lo corren de su piedra y no le discuten el sitio.',
    ],
    facts: [
      ['Especie', 'Pez cirujano'],
      ['Zona', 'El arrecife de Punta Nizuc'],
      ['Carácter', 'Tranquilo hasta que no'],
      ['Señal', 'Un filo a cada lado de la cola'],
    ],
    sayingTitle: 'Lo que dicen de él',
    saying:
      'Que el agua que deja atrás sale cortada en dos y tarda en volver a juntarse. Los que bucean en Nizuc dicen que se nota; los que no, dicen que son ganas.',
  },
  {
    id: 'TRAJI',
    slug: 'traji',
    num: '07',
    name: 'TRAJI',
    epithet: '',
    species: 'Ajolote',
    status: 'proximamente',
  },
];

const stock = stockData.existencias as Record<string, number>;

export const skuOf = (figure: ShopFigure, variant: VariantId): string => `${figure.id}-${variant}`;

export const stockOf = (figure: ShopFigure, variant: VariantId): number => stock[skuOf(figure, variant)] ?? 0;

export const figureStock = (figure: ShopFigure): number =>
  VARIANTS.reduce((sum, v) => sum + stockOf(figure, v.id), 0);

export const figureUrl = (figure: ShopFigure): string => `/tienda/${figure.slug}/`;

export const forSale = (): ShopFigure[] => FIGURES.filter((f) => f.status === 'venta');

export const minPrice = Math.min(...VARIANTS.map((v) => v.price));

export const mxn = (n: number): string => `$${n.toLocaleString('es-MX')}`;

/** Una línea vendible del catálogo, tal como la necesita el carrito en el navegador. */
export interface ShopLine {
  sku: string;
  name: string;
  variant: string;
  price: number;
  stock: number;
  href: string;
}

export const shopLines = (): ShopLine[] =>
  forSale().flatMap((f) =>
    VARIANTS.map((v) => ({
      sku: skuOf(f, v.id),
      name: f.name,
      variant: v.label,
      price: v.price,
      stock: stockOf(f, v.id),
      href: figureUrl(f),
    })),
  );

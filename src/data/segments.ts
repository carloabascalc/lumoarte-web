/**
 * Sectores (target de volumen / B2B). Single source of truth for the
 * /sectores/* landing pages, the homepage "Para quién fabricamos" grid,
 * footer/nav links, llms.txt and the sitewide OfferCatalog.
 *
 * Copy rules (Adriano): minimal, no hard delivery times, no machine counts,
 * no invented clients or capacities. Product examples only from work that
 * already appears in the gallery/catalog.
 */

export type SegmentId =
  | 'hoteles-y-restaurantes'
  | 'marcas-y-corporativos'
  | 'souvenirs-mayoreo'
  | 'eventos-y-bodas';

export interface SegmentFaq {
  question: string;
  answer: string;
}

export interface Segment {
  id: SegmentId;
  /** Card / nav label. */
  name: string;
  slug: string;
  /** Value preselected in QuoteForm's "Tipo de cliente". */
  cliente: string;
  /** One line for the homepage card. */
  blurb: string;
  eyebrow: string;
  /** H1 — may contain <em>. */
  h1: string;
  subtitle: string;
  metaTitle: string;
  metaDescription: string;
  /** schema.org BusinessAudience.audienceType */
  audience: string;
  /** Hero photos: [back, main, front] — filenames in src/assets/{gallery,catalogo}. */
  images: [string, string, string];
  /** Homepage card photo (distinct per segment). */
  cardImage: string;
  productos: { name: string; desc: string }[];
  faqs: SegmentFaq[];
}

export const segments: Segment[] = [
  {
    id: 'hoteles-y-restaurantes',
    name: 'Hoteles y restaurantes',
    slug: '/sectores/hoteles-y-restaurantes/',
    cliente: 'Hotel o restaurante',
    blurb: 'Posavasos, llaveros de habitación, señalética y amenidades con tu marca, en lotes y con reposición.',
    eyebrow: 'Hoteles y restaurantes',
    h1: 'Piezas con tu marca para hoteles y restaurantes en <em>Cancún</em>',
    subtitle:
      'Fabricamos en serie lo que tu hotel, bar o restaurante usa todos los días: posavasos, llaveros, señalética, estuches y amenidades grabadas con tu logo. Cuando se acaban, reponerlas es un mensaje.',
    metaTitle: 'Proveedor para hoteles y restaurantes en Cancún | Lumo Cancún',
    metaDescription:
      'Posavasos, llaveros de habitación, señalética y amenidades con tu logo para hoteles y restaurantes en Cancún. Lotes de decenas a miles de piezas, precio por volumen.',
    audience: 'Hoteles, bares y restaurantes',
    images: ['hotel-cuadros.jpg', 'hotel-senaletica.jpg', 'hotel-la-central.jpg'],
    cardImage: 'hotel-la-central.jpg',
    productos: [
      { name: 'Posavasos con tu logo', desc: 'Grabados en madera, MDF o acrílico, por cientos.' },
      { name: 'Llaveros de habitación', desc: 'En triplay, acrílico o impresos en 3D, con número y marca.' },
      { name: 'Señalética interior', desc: 'Letreros, numeración de habitaciones y placas en acrílico o madera.' },
      { name: 'Estuches y cajas', desc: 'Estuches de vino, cajas de amenidades y empaques con tu marca.' },
      { name: 'Menús y portamenús', desc: 'Tapas grabadas y soportes para mesa y barra.' },
      { name: 'Cuadros para habitaciones', desc: 'Arte enmarcado producido por lote para todas tus habitaciones.' },
    ],
    faqs: [
      {
        question: '¿Pueden ser proveedores de mi hotel o restaurante?',
        answer:
          'Sí. Lumo Cancún fabrica en serie piezas con la marca de hoteles, bares y restaurantes: posavasos, llaveros de habitación, señalética, estuches y amenidades. Hemos entregado lotes de alrededor de 1,500 cuadros enmarcados para un hotel en Cancún. Guardamos tus archivos, así que cada reposición sale igual a la anterior y se pide con un mensaje por WhatsApp.',
      },
      {
        question: '¿Cómo cobran un pedido grande de posavasos o llaveros?',
        answer:
          'Por pieza, con precio por volumen: el costo unitario baja conforme sube la cantidad, porque el material se aprovecha mejor y la máquina trabaja en corridas continuas. Mándanos tu logo, la medida y cuántas piezas necesitas y te cotizamos el lote.',
      },
      {
        question: '¿Pueden igualar la imagen de varias sucursales?',
        answer:
          'Sí. Al ser fabricación digital, la pieza se produce desde el mismo archivo cada vez, así que la señalética y los artículos salen iguales en todas tus sucursales y en cada pedido.',
      },
    ],
  },
  {
    id: 'marcas-y-corporativos',
    name: 'Marcas y corporativos',
    slug: '/sectores/marcas-y-corporativos/',
    cliente: 'Marca o empresa',
    blurb: 'Regalos corporativos, dijes de marca, placas y displays con tu logo, por cientos.',
    eyebrow: 'Marcas y corporativos',
    h1: 'Regalos corporativos y piezas de marca en <em>Cancún</em>',
    subtitle:
      'Grabamos y fabricamos en serie regalos corporativos, dijes y llaveros de marca, placas, kits de bienvenida y displays con tu logo — para eventos, equipos y clientes.',
    metaTitle: 'Regalos corporativos y merch con logo en Cancún | Lumo Cancún',
    metaDescription:
      'Regalos corporativos, dijes de marca, placas, termos y trofeos con tu logo en Cancún. Producción en serie para empresas, con precio por volumen.',
    audience: 'Marcas, empresas y corporativos',
    images: ['corp-placas.jpg', 'corp-trofeos.jpg', 'corp-termo.jpg'],
    cardImage: 'corp-trofeos.jpg',
    productos: [
      { name: 'Dijes y llaveros de marca', desc: 'En acrílico espejo, triplay o impresos en 3D, con tu logo.' },
      { name: 'Regalos corporativos', desc: 'Piezas grabadas para clientes, equipos y fin de año.' },
      { name: 'Placas y reconocimientos', desc: 'Grabado en aluminio, madera, acrílico, vidrio o mármol.' },
      { name: 'Kits y cajas de bienvenida', desc: 'Cajas de MDF o madera grabadas con tu marca.' },
      { name: 'Trofeos impresos en 3D', desc: 'Trofeos y premios con tu diseño, en lotes para eventos y equipos.' },
      { name: 'Displays y exhibidores', desc: 'Para punto de venta, mostrador y stands.' },
    ],
    faqs: [
      {
        question: '¿Hacen regalos corporativos con logo en Cancún?',
        answer:
          'Sí. Lumo Cancún graba y fabrica en serie regalos corporativos con el logo de tu empresa: dijes y llaveros de marca, placas, cajas y kits de bienvenida, y piezas para activaciones. Hemos trabajado para marcas como L\'Oréal (paletas grabadas con el nombre de cada asistente) y Emerald B2 (termos de acero con logo). Trabajamos en acrílico, MDF, triplay, cuero, aluminio, vidrio y mármol, además de impresión 3D.',
      },
      {
        question: '¿Necesito tener el logo en vector?',
        answer:
          'Lo ideal es un vector (AI, EPS, SVG o PDF). Si solo tienes tu logo en PNG o JPG nítido, lo vectorizamos por ti; cuando es sencillo va incluido en la cotización.',
      },
      {
        question: '¿Envían a otras ciudades?',
        answer:
          'Sí. En Cancún entregamos en la zona metropolitana y al resto de México enviamos por DHL o Estafeta, con el costo agregado a la cotización.',
      },
    ],
  },
  {
    id: 'souvenirs-mayoreo',
    name: 'Souvenirs por mayoreo',
    slug: '/sectores/souvenirs-mayoreo/',
    cliente: 'Tienda o mayoreo',
    blurb: 'Llaveros y recuerdos de Cancún fabricados por lote para tiendas, hoteles y revendedores.',
    eyebrow: 'Souvenirs por mayoreo',
    h1: 'Souvenirs de Cancún por <em>mayoreo</em>',
    subtitle:
      'Fabricamos llaveros, dijes y recuerdos de Cancún por lote para tiendas de souvenirs, hoteles y revendedores — con tu diseño o una línea exclusiva para tu tienda.',
    metaTitle: 'Souvenirs y llaveros de Cancún por mayoreo | Lumo Cancún',
    metaDescription:
      'Fabricante de souvenirs de Cancún por mayoreo: llaveros, dijes y figuras en acrílico, MDF e impresión 3D para tiendas, hoteles y revendedores.',
    audience: 'Tiendas de souvenirs, revendedores y mayoristas',
    images: ['souv-tiburones.jpg', 'souv-llaveros-cancun.jpg', 'souv-peces.jpg'],
    cardImage: 'souv-llaveros-cancun.jpg',
    productos: [
      { name: 'Llaveros de Cancún', desc: 'Grabados en madera o acrílico, o impresos en 3D a color.' },
      { name: 'Figuras y llaveros articulados', desc: 'Peces, tiburones y animales impresos en 3D a color, por lote.' },
      { name: 'Línea exclusiva para tu tienda', desc: 'Tu diseño, producido solo para ti.' },
      { name: 'Empaque para souvenirs', desc: 'Cajas y estuches cortados a láser.' },
    ],
    faqs: [
      {
        question: '¿Venden souvenirs de Cancún por mayoreo?',
        answer:
          'Sí. Lumo Cancún fabrica en Cancún llaveros, dijes y recuerdos por lote para tiendas de souvenirs, hoteles y revendedores, en madera, acrílico e impresión 3D. El precio por pieza baja conforme sube la cantidad.',
      },
      {
        question: '¿Pueden hacer un diseño exclusivo para mi tienda?',
        answer:
          'Sí. Producimos tu propio diseño o desarrollamos uno contigo; el diseño desde cero se cotiza por separado. Guardamos el archivo para que reponer inventario sea un solo mensaje.',
      },
    ],
  },
  {
    id: 'eventos-y-bodas',
    name: 'Eventos y bodas',
    slug: '/sectores/eventos-y-bodas/',
    cliente: 'Evento, boda o agencia',
    blurb: 'Recuerdos, números de mesa, cajas y señalética para eventos de cientos de invitados.',
    eyebrow: 'Eventos, bodas y agencias',
    h1: 'Recuerdos y decoración para eventos y bodas en <em>Cancún</em>',
    subtitle:
      'Para wedding planners, agencias y empresas: recuerdos para invitados, números de mesa, cajas, señalética y decoración — iguales pieza a pieza, para eventos de cientos de personas.',
    metaTitle: 'Recuerdos para bodas y eventos en Cancún | Lumo Cancún',
    metaDescription:
      'Recuerdos para invitados, números de mesa, cajas y placas para bodas y eventos en Cancún. Producción en serie para wedding planners y agencias.',
    audience: 'Wedding planners, agencias de eventos y organizadores',
    images: ['evento-cajas.jpg', 'evento-recuerdos.jpg', 'evento-cajas-corazon.jpg'],
    cardImage: 'evento-cajas.jpg',
    productos: [
      { name: 'Recuerdos para invitados', desc: 'Llaveros, dijes y piezas grabadas con nombres o fecha.' },
      { name: 'Cajas y dulceros', desc: 'Cajas de MDF y acrílico para regalos y mesas de dulces.' },
      { name: 'Números de mesa y señalética', desc: 'Del mismo diseño para todo el evento.' },
      { name: 'Piezas con nombre', desc: 'Paletas, gafetes y lugares de mesa personalizados por invitado.' },
      { name: 'Invitaciones', desc: 'Invitaciones cortadas o grabadas a láser en papel, madera o acrílico.' },
      { name: 'Decoración', desc: 'Paneles, centros de mesa y piezas decorativas cortadas a láser.' },
    ],
    faqs: [
      {
        question: '¿Hacen recuerdos para bodas y eventos en Cancún?',
        answer:
          'Sí. Lumo Cancún fabrica en serie recuerdos para invitados, cajas y dulceros, números de mesa, señalética y decoración para bodas y eventos corporativos. Trabajamos con wedding planners y agencias en lotes de decenas a miles de piezas; por ejemplo, placas de aluminio grabadas para el evento BeStar Generation.',
      },
      {
        question: '¿Pueden personalizar cada pieza con un nombre distinto?',
        answer:
          'Sí. Grabamos nombres distintos en cada pieza a partir de una lista (por ejemplo, lugares de mesa o paletas con nombre), manteniendo el mismo diseño en todo el lote.',
      },
      {
        question: '¿Con cuánto tiempo debo pedir para mi evento?',
        answer:
          'Habitualmente entregamos en menos de una semana; cuando hay disponibilidad, el mismo día. Para eventos grandes conviene cotizar en cuanto tengas la cantidad de invitados, y calendarizamos la producción contigo.',
      },
    ],
  },
];

export const getSegment = (id: SegmentId): Segment => {
  const segment = segments.find((s) => s.id === id);
  if (!segment) throw new Error(`Unknown segment: ${id}`);
  return segment;
};

import type { SegmentId } from './segments';

/**
 * Páginas por producto (/productos/*): capturan búsquedas de producto
 * ("llaveros con logo", "trofeos impresos en 3D") que las páginas de sector
 * no cubren. Same copy rules as segments.ts: no minimums, no delivery
 * promises, no invented clients or capacities. Only products with real
 * production photos get a page.
 */

export type ProductId = 'llaveros-con-logo' | 'trofeos-impresos-3d' | 'placas-y-senaletica';

export interface Product {
  id: ProductId;
  /** Card / breadcrumb label. */
  name: string;
  slug: string;
  /** One line for the hub table and cards. */
  blurb: string;
  eyebrow: string;
  /** H1 — may contain <em>. */
  h1: string;
  subtitle: string;
  metaTitle: string;
  metaDescription: string;
  /** schema.org BusinessAudience.audienceType */
  audience: string;
  service: 'laser' | '3d';
  serviceType: string;
  /** Hero photos: [back, main, front] — filenames in src/assets/{sectores,gallery,catalogo}. */
  images: [string, string, string];
  variantes: { name: string; desc: string }[];
  /** Sectors that buy it — links to /sectores/*. */
  sectors: SegmentId[];
  /** Named clients from cases.ts to show as proof. */
  cases?: string[];
  faqs: { question: string; answer: string }[];
}

export const products: Product[] = [
  {
    id: 'llaveros-con-logo',
    name: 'Llaveros con logo',
    slug: '/productos/llaveros-con-logo/',
    blurb: 'Llaveros de habitación, de marca y souvenir, grabados a láser o impresos en 3D a color.',
    eyebrow: 'Llaveros por mayoreo',
    h1: 'Llaveros con logo por mayoreo en <em>Cancún</em>',
    subtitle:
      'Llaveros de habitación para hoteles, llaveros de marca para empresas y llaveros souvenir para tiendas: grabados a láser en madera o acrílico, o impresos en 3D a color, en lotes de decenas a miles.',
    metaTitle: 'Llaveros con logo por mayoreo en Cancún | Lumo Cancún',
    metaDescription:
      'Llaveros personalizados con logo por mayoreo en Cancún: de habitación, de marca y souvenir. Grabados en madera o acrílico, o impresos en 3D a color.',
    audience: 'Hoteles, marcas, tiendas de souvenirs y eventos',
    service: '3d',
    serviceType: 'Fabricación de llaveros personalizados en serie',
    images: ['dije-triplay-tzalam.jpg', 'gal-16.jpg', 'souv-peces.jpg'],
    variantes: [
      { name: 'Grabados en madera', desc: 'Triplay o Tzalam con tu logo grabado a láser. Cálidos y ligeros.' },
      { name: 'De acrílico', desc: 'Transparente, de color o espejo oro y plata, cortados y grabados a láser.' },
      { name: 'Impresos en 3D a color', desc: 'Con volumen y varios colores en la misma pieza, como los llaveros Cancún tricolor.' },
      { name: 'Llaveros de habitación', desc: 'Con el número de cada habitación y la marca del hotel, del mismo diseño en todo el lote.' },
      { name: 'Figuras y llaveros articulados', desc: 'Peces, tiburones y animales impresos en 3D, para souvenir.' },
      { name: 'Dijes y etiquetas de marca', desc: 'Para producto artesanal, empaque y kits corporativos.' },
    ],
    sectors: ['hoteles-y-restaurantes', 'marcas-y-corporativos', 'souvenirs-mayoreo', 'eventos-y-bodas'],
    faqs: [
      {
        question: '¿Hacen llaveros con logo por mayoreo en Cancún?',
        answer:
          'Sí. Lumo Cancún fabrica en Cancún llaveros con logo en serie: grabados a láser en madera o acrílico, o impresos en 3D a color. Los producimos para hoteles (llaveros de habitación), empresas (llaveros de marca), tiendas de souvenirs y eventos, en lotes de decenas a miles de piezas. El precio por pieza baja conforme sube la cantidad.',
      },
      {
        question: '¿Cuál es la diferencia entre un llavero grabado a láser y uno impreso en 3D?',
        answer:
          'El llavero grabado a láser es una pieza plana de madera o acrílico con el diseño marcado en la superficie; toma el color del material. El llavero impreso en 3D tiene volumen y puede llevar varios colores en la misma pieza, como letras de un color sobre una base de otro. El grabado conviene para logos sobrios y el 3D para formas y colores de marca.',
      },
      {
        question: '¿Cada llavero puede llevar un número o nombre distinto?',
        answer:
          'Sí. A partir de una lista grabamos un número o nombre distinto en cada pieza (por ejemplo, el número de cada habitación) manteniendo el mismo diseño en todo el lote.',
      },
      {
        question: '¿Pueden reponer llaveros que se pierden?',
        answer:
          'Sí. Guardamos el archivo de tu llavero, así que reponer piezas perdidas o hacer otro lote sale igual al anterior y se pide con un mensaje por WhatsApp.',
      },
    ],
  },
  {
    id: 'trofeos-impresos-3d',
    name: 'Trofeos impresos en 3D',
    slug: '/productos/trofeos-impresos-3d/',
    blurb: 'Trofeos y premios con tu propio diseño, sin molde, en lotes para eventos, torneos y empresas.',
    eyebrow: 'Trofeos y premios',
    h1: 'Trofeos impresos en 3D con tu diseño en <em>Cancún</em>',
    subtitle:
      'Trofeos y premios con la forma de tu logo o tu idea, impresos en 3D en Cancún: para eventos corporativos, torneos, equipos y premiaciones. Sin molde, así que tu diseño propio es viable desde lotes medianos.',
    metaTitle: 'Trofeos impresos en 3D personalizados en Cancún | Lumo Cancún',
    metaDescription:
      'Trofeos y premios personalizados impresos en 3D en Cancún, con tu diseño y sin molde. Lotes para eventos corporativos, torneos y equipos.',
    audience: 'Empresas, organizadores de eventos, torneos y equipos',
    service: '3d',
    serviceType: 'Fabricación de trofeos personalizados por impresión 3D',
    images: ['gal-19.jpg', 'corp-trofeos.jpg', 'corp-placas.jpg'],
    variantes: [
      { name: 'Trofeo con tu diseño', desc: 'La figura, el logo o la forma que quieras, modelada e impresa en 3D.' },
      { name: 'Premios para eventos corporativos', desc: 'Reconocimientos para equipos, ventas y aniversarios.' },
      { name: 'Trofeos para torneos', desc: 'Lotes para primero, segundo y tercer lugar, del mismo diseño.' },
      { name: 'Placas grabadas', desc: 'Placas de aluminio, madera o acrílico grabadas a láser con nombre y fecha.' },
    ],
    sectors: ['marcas-y-corporativos', 'eventos-y-bodas'],
    faqs: [
      {
        question: '¿Hacen trofeos impresos en 3D en Cancún?',
        answer:
          'Sí. Lumo Cancún imprime en 3D trofeos y premios con tu propio diseño, en lotes para eventos corporativos, torneos, equipos y premiaciones. Hemos producido lotes de trofeos dorados para eventos corporativos en Cancún. Imprimimos en Bambu Lab, con filamento de un color o multicolor.',
      },
      {
        question: '¿Por qué un trofeo impreso en 3D en lugar de uno de catálogo?',
        answer:
          'Porque puede tener la forma exacta de tu logo o tu idea, y no necesita molde. Un trofeo de catálogo es igual al de cualquier otro evento; uno inyectado con diseño propio exige un molde que solo se paga en tirajes muy grandes. La impresión 3D produce tu diseño propio directamente desde el archivo, así que es viable en lotes medianos.',
      },
      {
        question: '¿Necesito tener un modelo 3D?',
        answer:
          'No es indispensable. Si tienes el archivo (STL, OBJ, 3MF o STEP) lo imprimimos directo; si solo tienes tu logo o un boceto, lo modelamos contigo y el modelado se cotiza por separado.',
      },
      {
        question: '¿Pueden llevar el nombre del ganador o la fecha?',
        answer:
          'Sí. Los combinamos con placas grabadas a láser en aluminio, madera o acrílico, con el nombre, el lugar o la fecha de cada premio.',
      },
    ],
  },
  {
    id: 'placas-y-senaletica',
    name: 'Placas y señalética',
    slug: '/productos/placas-y-senaletica/',
    blurb: 'Placas de reconocimiento, letreros de marca y señalética interior grabados a láser.',
    eyebrow: 'Placas y señalética',
    h1: 'Placas y señalética grabada a láser en <em>Cancún</em>',
    subtitle:
      'Placas de reconocimiento, letreros de marca y señalética interior para hoteles, restaurantes, oficinas y eventos — grabados a láser en acrílico, madera o aluminio, del mismo diseño en cada pieza.',
    metaTitle: 'Placas y señalética grabada a láser en Cancún | Lumo Cancún',
    metaDescription:
      'Placas de reconocimiento, letreros de marca y señalética interior grabados a láser en Cancún, en acrílico, madera o aluminio. Producción en serie.',
    audience: 'Hoteles, restaurantes, oficinas y organizadores de eventos',
    service: 'laser',
    serviceType: 'Placas y señalética grabadas con láser',
    images: ['hotel-senaletica.jpg', 'hotel-la-central.jpg', 'corp-placas.jpg'],
    variantes: [
      { name: 'Placas de reconocimiento', desc: 'Grabadas en aluminio, madera, acrílico, vidrio o mármol.' },
      { name: 'Letreros de marca', desc: 'Acrílico negro con grabado dorado, como los de La Central Vinos & Licores.' },
      { name: 'Señalética interior', desc: 'Números de habitación, baños, áreas y avisos, del mismo diseño en todo el inmueble.' },
      { name: 'Señalética de reciclaje', desc: 'Letreros de separación de residuos en madera grabada.' },
      { name: 'Indicadores de estacionamiento', desc: 'Con nombre, número o logo para cada lugar.' },
      { name: 'Placas conmemorativas para eventos', desc: 'Con el logo y la fecha del evento, para cada asistente.' },
    ],
    sectors: ['hoteles-y-restaurantes', 'marcas-y-corporativos', 'eventos-y-bodas'],
    cases: ['La Central Vinos & Licores', 'BeStar Generation'],
    faqs: [
      {
        question: '¿Hacen placas y señalética grabada en Cancún?',
        answer:
          'Sí. Lumo Cancún graba a láser placas de reconocimiento, letreros de marca y señalética interior en acrílico, madera, aluminio, vidrio y mármol. Hemos hecho los letreros de marca de La Central Vinos & Licores y las placas de aluminio del evento BeStar Generation. Producimos lotes del mismo diseño para todo un hotel, restaurante u oficina.',
      },
      {
        question: '¿El grabado láser se despega o se borra?',
        answer:
          'No se despega: el láser marca el material mismo, no es una calcomanía ni un vinil pegado. Por eso el grabado láser dura más que un rótulo de vinil en señalética de uso diario.',
      },
      {
        question: '¿Pueden hacer toda la señalética de un hotel con el mismo diseño?',
        answer:
          'Sí. Cada pieza sale del mismo archivo, así que números de habitación, letreros de áreas y avisos quedan iguales en todo el inmueble. Guardamos los archivos para que agregar o reponer una pieza salga idéntica.',
      },
    ],
  },
];

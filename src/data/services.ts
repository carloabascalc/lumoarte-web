/**
 * EMD (exact-match-domain) strategy: when true, service tiles, nav drawer,
 * footer Servicios column and CrossServices link out to the EMD domain
 * (e.g. cortelasercancun.com) instead of the internal /servicios/* slug.
 *
 * Flip to true once cortelasercancun.com and impresion3dcancun.com have
 * been registered and added to the Vercel project.
 */
export const EMD_ENABLED = false;

export type ServiceId = 'corte-laser' | 'impresion-3d' | 'impresion-gran-formato' | 'recuerdos-cancun';

export interface Service {
  id: ServiceId;
  name: string;
  shortName: string;
  slug: string;
  blurb: string;
  metaDescription: string;
  icon: string;
  /** External EMD domain (no protocol). When set, ServicesGrid tiles link here instead of slug. */
  emdDomain?: string;
  /** Internal Astro route for the EMD one-pager (if the service has an EMD). */
  emdRoute?: string;
  manualPdf: string;
  preciosPdf: string;
}

export const services: Service[] = [
  {
    id: 'corte-laser',
    name: 'Corte Láser',
    shortName: 'Láser',
    slug: '/servicios/corte-laser',
    blurb: 'Cortamos y grabamos MDF, acrílico, papel y cuero; grabamos vidrio, mármol y cerámica. Precisión milimétrica.',
    metaDescription: 'Servicio de corte láser y grabado en Cancún. MDF, acrílico, papel, cuero, vidrio, mármol y cerámica. Cotización inmediata por WhatsApp.',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v3"/><rect x="8" y="5" width="8" height="3.5" rx="1"/><path d="M12 8.5v4.5"/><path d="M4 17h16"/><circle cx="12" cy="14.5" r="1"/><path d="M9.4 13.4 8 16"/><path d="m14.6 13.4 1.4 2.6"/></svg>`,
    emdDomain: 'cortelasercancun.com',
    emdRoute: '/cortelasercancun',
    manualPdf: '/manual-corte-laser.pdf',
    preciosPdf: '/precios-corte-laser.pdf',
  },
  {
    id: 'impresion-3d',
    name: 'Impresión 3D',
    shortName: '3D',
    slug: '/servicios/impresion-3d',
    blurb: 'Prototipos y piezas finales en FDM (multi-color, gran formato) y resina de alta definición.',
    metaDescription: 'Servicio de impresión 3D en Cancún. FDM multi-color con Bambu Lab H2C y Artillery Sidewinder XL, y resina de alta definición con Anycubic. Prototipos, repuestos, miniaturas, joyería.',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>`,
    emdDomain: 'impresion3dcancun.com',
    emdRoute: '/impresion3dcancun',
    manualPdf: '/manual-impresion-3d.pdf',
    preciosPdf: '/precios-impresion-3d.pdf',
  },
  {
    id: 'impresion-gran-formato',
    name: 'Impresión Gran Formato',
    shortName: 'Gran Formato',
    slug: '/servicios/impresion-gran-formato',
    blurb: 'Lonas, vinil y sublimación hasta 1.80 m de ancho para eventos, retail, vehículos y textiles.',
    metaDescription: 'Impresión gran formato en Cancún hasta 1.80 m de ancho. Lonas para eventos, vinil para wraps y rotulación, sublimación textil. Tintas eco-solventes y de sublimación.',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="1"/><path d="M6 10h12"/><path d="M6 14h8"/></svg>`,
    manualPdf: '/manual-impresion-gran-formato.pdf',
    preciosPdf: '/precios-impresion-gran-formato.pdf',
  },
  {
    id: 'recuerdos-cancun',
    name: 'Regalos y Recuerdos Cancún',
    shortName: 'Regalos',
    slug: '/servicios/recuerdos-cancun',
    blurb: 'Llaveros de Cancún impresos en 3D. Mándanos tu propio modelo o elige uno de nuestro catálogo.',
    metaDescription: 'Impresión 3D de llaveros en Cancún. Mándanos tu propio modelo 3D (.stl, .3mf, .obj) o elige uno de nuestro catálogo. También diseños a la medida para bodas, eventos y empresas.',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="3"/><path d="M12 8v3"/><rect x="9" y="11" width="6" height="10" rx="2"/></svg>`,
    manualPdf: '/manual-recuerdos-cancun.pdf',
    preciosPdf: '/precios-recuerdos-cancun.pdf',
  },
];

export const getService = (id: ServiceId): Service => {
  const service = services.find((s) => s.id === id);
  if (!service) throw new Error(`Unknown service: ${id}`);
  return service;
};

/**
 * Returns the public-facing URL for a service.
 * If EMDs are enabled and the service has an EMD domain, returns the absolute
 * EMD URL. Otherwise returns the internal Astro slug.
 */
export const getServiceUrl = (service: Service): string => {
  if (EMD_ENABLED && service.emdDomain) return `https://${service.emdDomain}`;
  return service.slug;
};

/** True when clicking this service link will leave the umbrella site. */
export const isExternalService = (service: Service): boolean =>
  EMD_ENABLED && !!service.emdDomain;

export const SITE = {
  name: 'Lumo Cancún',
  tagline: 'Fabricación digital en Cancún',
  url: 'https://lumocancun.com',
  description: 'Corte láser, impresión 3D e impresión gran formato en Cancún. Un solo taller, tres servicios. Cotización inmediata por WhatsApp.',
  // Primary line — WhatsApp + calls all route here (998).
  whatsapp: '529981888048',
  whatsappDisplay: '+52 998 188 8048',
  phone: '529981888048',
  phoneDisplay: '+52 998 188 8048',
  // Secondary line — call-only, shown after the primary number (813).
  phoneSecondary: '528138913891',
  phoneSecondaryDisplay: '+52 813 891 3891',
  email: 'lumocancun@gmail.com',
  instagram: 'https://www.instagram.com/_lumoarte',
  instagramHandle: '@_lumoarte',
  gbp: 'https://www.google.com/maps?cid=2574885880611067538',
  geo: { lat: 21.1546364, lng: -86.8257604 },
  // Horario oficial del Google Business Profile (Lun–Sáb 9–18, Dom cerrado)
  hours: {
    days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    opens: '09:00',
    closes: '18:00',
  },
  address: {
    street: 'Retorno Tejón, Mz 3, Lt 2, Sm 20',
    city: 'Cancún',
    state: 'Quintana Roo',
    postalCode: '77500',
    country: 'MX',
  },
  ogDefault: '/og/default.jpg',
};

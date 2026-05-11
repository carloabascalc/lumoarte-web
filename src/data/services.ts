/**
 * EMD (exact-match-domain) strategy: when true, service tiles, nav drawer,
 * footer Servicios column and CrossServices link out to the EMD domain
 * (e.g. cortelasercancun.com) instead of the internal /servicios/* slug.
 *
 * Flip to true once cortelasercancun.com and impresion3dcancun.com have
 * been registered and added to the Vercel project.
 */
export const EMD_ENABLED = false;

export type ServiceId = 'corte-laser' | 'impresion-3d' | 'impresion-gran-formato';

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
    blurb: 'Cortamos y grabamos en MDF, acrílico, papel, cuero, vidrio, mármol y más con precisión milimétrica.',
    metaDescription: 'Servicio de corte láser y grabado en Cancún. MDF, acrílico, papel, cuero, vidrio, mármol y cerámica. Cotización por WhatsApp en menos de 24 horas.',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4"/><path d="M12 18v4"/><path d="m4.93 4.93 2.83 2.83"/><path d="m16.24 16.24 2.83 2.83"/><path d="M2 12h4"/><path d="M18 12h4"/><path d="m4.93 19.07 2.83-2.83"/><path d="m16.24 7.76 2.83-2.83"/><circle cx="12" cy="12" r="3"/></svg>`,
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
  name: 'Lumo Arte',
  tagline: 'Fabricación digital en Cancún',
  url: 'https://lumocancun.com',
  description: 'Corte láser, impresión 3D e impresión gran formato en Cancún. Un solo taller, tres servicios. Cotización por WhatsApp en menos de 24 horas.',
  whatsapp: '528138913891',
  whatsappDisplay: '+52 813 891 3891',
  email: 'contacto@lumocancun.com',
  instagram: 'https://www.instagram.com/_lumoarte',
  instagramHandle: '@_lumoarte',
  address: {
    street: 'Retorno Tejón, Mz 3, Lt 2, Sm 20',
    city: 'Cancún',
    state: 'Quintana Roo',
    postalCode: '77500',
    country: 'MX',
  },
  ogDefault: '/og/default.jpg',
};

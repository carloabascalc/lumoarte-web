export type ServiceId = 'corte-laser' | 'impresion-3d' | 'impresion-gran-formato';

export interface Service {
  id: ServiceId;
  name: string;
  shortName: string;
  slug: string;
  blurb: string;
  metaDescription: string;
  icon: string;
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
  },
  {
    id: 'impresion-3d',
    name: 'Impresión 3D',
    shortName: '3D',
    slug: '/servicios/impresion-3d',
    blurb: 'Prototipos y piezas finales en FDM (multi-color, gran formato) y resina de alta definición.',
    metaDescription: 'Servicio de impresión 3D en Cancún. FDM multi-color con Bambu Lab H2C y Artillery Sidewinder XL, y resina de alta definición con Anycubic. Prototipos, repuestos, miniaturas, joyería.',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>`,
  },
  {
    id: 'impresion-gran-formato',
    name: 'Impresión Gran Formato',
    shortName: 'Gran Formato',
    slug: '/servicios/impresion-gran-formato',
    blurb: 'Lonas, vinil y sublimación hasta 1.80 m de ancho para eventos, retail, vehículos y textiles.',
    metaDescription: 'Impresión gran formato en Cancún hasta 1.80 m de ancho. Lonas para eventos, vinil para wraps y rotulación, sublimación textil. Tintas eco-solventes y de sublimación.',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="1"/><path d="M6 10h12"/><path d="M6 14h8"/></svg>`,
  },
];

export const getService = (id: ServiceId): Service => {
  const service = services.find((s) => s.id === id);
  if (!service) throw new Error(`Unknown service: ${id}`);
  return service;
};

export const SITE = {
  name: 'Lumo Arte',
  tagline: 'Fabricación digital en Cancún',
  url: 'https://lumoarte.com',
  description: 'Corte láser, impresión 3D e impresión gran formato en Cancún. Un solo taller, tres servicios. Cotización por WhatsApp en menos de 24 horas.',
  whatsapp: '528138913891',
  whatsappDisplay: '+52 813 891 3891',
  email: 'contacto@lumoarte.com',
  instagram: 'https://www.instagram.com/_lumoarte',
  instagramHandle: '@_lumoarte',
  address: {
    street: 'Ave 20 de Noviembre #125, Lt 9, Mz 30, Sm 76, L1',
    city: 'Cancún',
    state: 'Quintana Roo',
    postalCode: '',
    country: 'MX',
  },
  ogDefault: '/og/default.jpg',
};

/**
 * Contenido de /califica/: la página que Adriano manda por WhatsApp al
 * entregar un pedido. Con 5 estrellas lleva a la reseña de Google; con
 * menos, abre esta encuesta y las respuestas llegan por WhatsApp.
 */

export const RATING_LABELS = ['Mal', 'Regular', 'Bien', 'Muy bien', '¡Excelente!'] as const;

interface BaseQuestion {
  id: string;
  /** Pregunta tal como la ve el cliente. */
  label: string;
  /** Versión corta que encabeza la respuesta en el mensaje de WhatsApp. */
  short: string;
  required: boolean;
}

interface ChoiceQuestion extends BaseQuestion {
  kind: 'multi' | 'single';
  options: string[];
}

interface TextQuestion extends BaseQuestion {
  kind: 'text';
  placeholder: string;
}

export type SurveyQuestion = ChoiceQuestion | TextQuestion;

export const SURVEY: SurveyQuestion[] = [
  {
    id: 'que-fallo',
    kind: 'multi',
    label: '¿Qué fue lo que no te gustó?',
    short: 'Lo que no me gustó',
    required: true,
    options: [
      'Calidad o acabado de la pieza',
      'La pieza no quedó como esperaba',
      'Tiempo de entrega',
      'Precio',
      'Atención y comunicación',
      'Otra cosa',
    ],
  },
  {
    id: 'entrega',
    kind: 'single',
    label: '¿Te entregamos en la fecha que quedamos?',
    short: 'Entrega',
    required: true,
    options: ['Sí, a tiempo', 'Con un poco de retraso', 'No, tardamos bastante'],
  },
  {
    id: 'atencion',
    kind: 'single',
    label: '¿Cómo fue la atención por WhatsApp?',
    short: 'Atención por WhatsApp',
    required: true,
    options: ['Rápida y clara', 'Regular', 'Lenta o confusa'],
  },
  {
    id: 'mejorar',
    kind: 'text',
    label: '¿Qué tendríamos que cambiar para que la próxima vez sea de 5 estrellas?',
    short: 'Para que sea de 5 estrellas',
    required: false,
    placeholder: 'Escríbelo con confianza, lo leemos todo.',
  },
  {
    id: 'volveria',
    kind: 'single',
    label: '¿Nos volverías a encargar un trabajo?',
    short: '¿Volvería a encargar?',
    required: true,
    options: ['Sí', 'Tal vez', 'No'],
  },
];

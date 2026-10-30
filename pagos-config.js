/* =====================================================================
   CONFIGURACIÓN DE PAGOS Y ENVÍOS  (este archivo es SOLO tuyo)
   ---------------------------------------------------------------------
   Aquí pones los datos de tus cuentas y las tarifas de envío.
   Respeta comas, comillas y llaves. Si algo se rompe, pídele ayuda a Claude.
   NO pongas aquí claves secretas de Wompi ni de Addi: esas van en el servidor.
   ===================================================================== */

const AJ_PAGOS = {
  /* true  = el carrito lleva a la página "Finalizar compra".
     false = el pedido sale directo por WhatsApp (como antes). */
  checkout: true,

  /* (Opcional) dirección que recibe cada pedido para avisarte por correo.
     Ejemplo con Formspree:  "https://formspree.io/f/xxxxxxxx"   (vacío = no se envía) */
  pedidosEndpoint: "",

  /* TRANSFERENCIA, NEQUI Y LLAVE. Los datos aparecen cuando el cliente confirma su pedido.
     Si los dejas vacíos, el cliente verá "Te enviamos los datos de pago por WhatsApp". */
  transferencia: {
    activo: true,
    titular: "",                 // nombre del titular de las cuentas (ej. "Nicolas Gonzalez")
    bancos: [
      /* { banco: "Bancolombia", tipo: "Ahorros", numero: "000-000000-00" }, */
    ],
    nequi: "",                   // número de Nequi, ej. "3001523568"
    llave: ""                    // tu Llave, ej. "@nikotech"
  },

  /* WOMPI. Mientras "activo" sea false, el cliente recibe un link de pago de Wompi por WhatsApp o correo.
     Cuando tengas el servidor listo, pon activo: true y en endpoint la dirección de tu servidor. */
  wompi: { activo: false, endpoint: "" },

  /* ADDI. Igual que Wompi. */
  addi: { activo: false, endpoint: "" }
};

const AJ_ENVIOS = {
  /* Ciudades con envío gratis (escribe en minúsculas y sin tildes). */
  gratis: ["bogota"],

  /* Tarifa de envío NACIONAL por tamaño de paquete, en pesos. 0 = sin definir → se muestra "Por confirmar".
     Cómo definirlas: cotiza con tu transportadora un paquete pequeño, uno mediano y uno grande
     a una ciudad principal, y pon ese valor. Más abajo puedes sumar recargos por ciudad. */
  tarifas: { pequeno: 0, mediano: 0, grande: 0 },

  /* Recargo adicional por ciudad (minúsculas, sin tildes). Ej.: { "leticia": 25000, "san andres": 40000 } */
  recargos: {},

  /* Porcentaje del valor del pedido que sumas como seguro en envíos nacionales. 0 = no cobrar. Ej.: 0.01 = 1 % */
  seguroPct: 0,

  /* Tamaño de paquete por categoría (pequeno, mediano o grande). Cambia solo si hace falta. */
  tamanos: {
    celulares: "pequeno", audio: "pequeno", smartwatch: "pequeno", cargadores: "pequeno", fundas: "pequeno",
    accesorios: "pequeno", computacion: "pequeno", estilo: "pequeno", hogar: "pequeno", redes: "pequeno",
    almacenamiento: "pequeno", perifericos: "mediano", tablets: "mediano", portatiles: "mediano",
    impresion: "grande", monitores: "grande", televisores: "grande", computadores: "grande", energia: "grande"
  }
};

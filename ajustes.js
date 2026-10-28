/* =====================================================================
   AJUSTES DE TU TIENDA  (este archivo es SOLO tuyo: yo no lo piso)
   ---------------------------------------------------------------------
   Lo más fácil: abre  nikotechsolutions.github.io/panel.html , haz clic
   en lo que quieras cambiar y copia el texto que te genera aquí.
   También puedes editarlo a mano: respeta comas, llaves y comillas.
   ===================================================================== */

/* 1) PRODUCTOS DESTACADOS de la portada, en el orden que quieras.
      Pon los números (ID) separados por coma. Entre 4 y 12 productos. */
const AJ_DESTACADOS = [769, 18, 26, 30, 85, 207, 211, 221];

/* 2) CAMBIAR PRECIOS.  Ejemplos (quita las // para activarlos):
      787: { precio: 1800000 },                       // precio nuevo
      787: { precio: 1800000, antes: 2100000 },       // con precio anterior tachado (y % de descuento)
      787: { antes: 0 },                              // quita el precio tachado
      769: { opciones: { "256 GB · eSIM (virtual)": { precio: 4170000, antes: 6999000 } } },   // producto con opciones */
const AJ_PRECIOS = {
};

/* 3) OCULTAR productos (no aparecen en la tienda). Pon los ID separados por coma. */
const AJ_OCULTOS = [];

/* 4) CAMBIAR EL NOMBRE de un producto.  Ejemplo:  769: "iPhone 17 Pro Max Nuevo", */
const AJ_NOMBRES = {
};

/* 5) CAMBIAR UNA IMAGEN.  Sube la foto a la carpeta img (puede ser .jpg, .png o .webp)
      y escribe su nombre.  Ejemplo:  769: "mi-iphone.jpg", */
const AJ_IMAGENES = {
};

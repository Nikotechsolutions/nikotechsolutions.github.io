/* =========================================================
   NIKOTECHSOLUTIONS - CATÁLOGO Y LÓGICA COMPARTIDA
   Este archivo se usa en TODAS las páginas (index, catalogo,
   ofertas, contacto) para que el menú, el buscador y el
   carrito funcionen exactamente igual en todas partes.
   ========================================================= */

/* ---------------------------------------------------------
   1. CATÁLOGO DE PRODUCTOS
   --------------------------------------------------------- */
const products = [
    {
        id: 1,
        title: "Audífonos Gamer Aura Pro",
        category: "audio",
        price: 173.90,
        badge: "Más Vendido",
        rating: 5,
        image: "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500",
        description: "Audífonos de alta fidelidad con cancelación activa de ruido, micrófono omnidireccional retráctil y sonido envolvente 7.1. Diseñados para largas sesiones de juego con sus almohadillas de espuma viscoelástica súper cómodas."
    },
    {
        id: 2,
        title: "Laptop ZenBook Nova 14",
        category: "laptops",
        price: 899.00,
        badge: "OLED 2.8K",
        rating: 5,
        image: "https://images.unsplash.com/photo-1664575196412-ed801e8333a1?w=500",
        description: "Laptop ultraligera equipada con pantalla OLED 2.8K de 90Hz, procesador de última generación, 16GB RAM y 512GB SSD NVMe. Ideal para creadores de contenido y profesionales en movimiento."
    },
    {
        id: 3,
        title: "Smart Speaker Voice-AI",
        category: "smarthome",
        price: 119.90,
        badge: "Novedad",
        rating: 4,
        image: "https://images.unsplash.com/photo-1543512214-318c7553f230?w=500",
        description: "Altavoz inteligente con asistente de voz integrado, audio omnidireccional de 360 grados y control de dispositivos del hogar inteligente. Compatible con Alexa y Google Assistant."
    },
    {
        id: 4,
        title: "Smartwatch Pro Cyber-X",
        category: "smarthome",
        price: 79.90,
        oldPrice: 115.00,
        badge: "-30% OFF",
        rating: 5,
        image: "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=500",
        description: "Reloj inteligente resistente al agua (IP68) con monitor de ritmo cardíaco, oxímetro, seguimiento del sueño y más de 30 modos deportivos. Batería de larga duración de hasta 10 días."
    },
    {
        id: 5,
        title: "Teclado Mecánico RGB Switch Blue",
        category: "perifericos",
        price: 65.00,
        badge: "Gamer",
        rating: 4,
        image: "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500",
        description: "Teclado mecánico completo con switches azules de respuesta táctil y sonora rápida, retroiluminación RGB personalizable con múltiples efectos y chasis de aluminio duradero."
    },
    {
        id: 6,
        title: "Mouse Gamer Precision 16000 DPI",
        category: "perifericos",
        price: 45.00,
        badge: "Precisión",
        rating: 4,
        image: "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500",
        description: "Mouse ergonómico para eSports con sensor óptico ajustable hasta 16,000 DPI, 7 botones programables e iluminación RGB customizable mediante software."
    },
    {
        id: 7,
        title: "Laptop UltraSlim Vector 15",
        category: "laptops",
        price: 749.00,
        badge: "Nuevo",
        rating: 4,
        image: "https://images.unsplash.com/photo-1664575196412-ed801e8333a1?w=500",
        description: "Diseño elegante en aluminio de solo 1.3kg de peso, pantalla Full HD IPS de 15.6 pulgadas, batería de hasta 12 horas de duración y carga rápida mediante USB-C."
    },
    {
        id: 8,
        title: "Audífonos InEar BassLine X",
        category: "audio",
        price: 39.90,
        badge: "Económico",
        rating: 4,
        image: "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500",
        description: "Audífonos inalámbricos Bluetooth 5.3 compactos con bajos potentes, resistencia al sudor IPX5 y hasta 24 horas de reproducción total con el estuche de carga."
    },
    {
        id: 9,
        title: "Bombillo Smart RGB WiFi",
        category: "smarthome",
        price: 19.90,
        badge: "Hogar Inteligente",
        rating: 4,
        image: "https://images.unsplash.com/photo-1543512214-318c7553f230?w=500",
        description: "Foco inteligente LED regulable con 16 millones de colores. No requiere hub, se conecta directamente a tu red WiFi y se controla mediante App o comandos de voz."
    },
    {
        id: 10,
        title: "Cámara de Seguridad WiFi 360°",
        category: "smarthome",
        price: 54.90,
        oldPrice: 69.90,
        badge: "-20% OFF",
        rating: 4,
        image: "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=500",
        description: "Cámara de vigilancia para interiores con visión nocturna por infrarrojos, detección de movimiento con IA, audio bidireccional y rotación horizontal de 360°."
    },
    {
        id: 11,
        title: "Mousepad XL Gamer Pro",
        category: "perifericos",
        price: 22.00,
        badge: "XL",
        rating: 5,
        image: "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500",
        description: "Alfombrilla de mouse de tamaño extendido (900x400mm) con base de goma antideslizante, bordes cosidos reforzados y superficie de microfibra de alta velocidad."
    },
    {
        id: 12,
        title: "Silla Gamer ErgoMax",
        category: "gaming",
        price: 249.00,
        badge: "Nuevo",
        rating: 5,
        image: "https://images.unsplash.com/photo-1636487658609-28282bb5a3a0?w=500",
        description: "Silla ergonómica de alta calidad con cojín lumbar y cervical ajustables, reposabrazos 3D, reclinación de hasta 160° y pistón de gas Clase 4 de alta resistencia."
    },
    {
        id: 13,
        title: "Micrófono USB StreamCast",
        category: "audio",
        price: 89.90,
        oldPrice: 109.90,
        badge: "-18% OFF",
        rating: 4,
        image: "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500",
        description: "Micrófono condensador de estudio ideal para streaming, podcasting y llamadas. Inclución de patrón polar cardioide, botón de silenciamiento rápido (tap-to-mute) y filtro pop incorporado."
    },
    {
        id: 14,
        title: "Monitor Curvo 27\" 165Hz",
        category: "monitores",
        price: 289.00,
        badge: "Nuevo",
        rating: 5,
        image: "https://images.unsplash.com/photo-1636487658609-28282bb5a3a0?w=500",
        description: "Monitor de juegos curvo 1500R de 27 pulgadas, tasa de refresco ultra rápida de 165Hz, tiempo de respuesta de 1ms y compatibilidad con FreeSync / G-Sync."
    },
    {
        id: 15,
        title: "Hub USB-C 7 en 1",
        category: "perifericos",
        price: 34.90,
        badge: "Multipuerto",
        rating: 4,
        image: "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500",
        description: "Adaptador multipuerto USB-C fabricado en aluminio con salida HDMI 4K, 3 puertos USB 3.0, lector de tarjetas SD/MicroSD y puerto de carga Power Delivery de hasta 100W."
    }
];

/* ---------------------------------------------------------
   2. CARRITO (con memoria entre páginas usando localStorage)
   --------------------------------------------------------- */
let cart = JSON.parse(localStorage.getItem('nikotech_cart') || '[]');

function saveCart() {
    localStorage.setItem('nikotech_cart', JSON.stringify(cart));
}

function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    cart.push(product);
    saveCart();
    updateCartUI();
    toggleCart(true);
}

function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
    updateCartUI();
}

function updateCartUI() {
    const cartCountEl = document.getElementById('cartCount');
    if (cartCountEl) cartCountEl.innerText = cart.length;

    const container = document.getElementById('cartItems');
    if (!container) return;
    container.innerHTML = '';

    let total = 0;
    cart.forEach((item, index) => {
        total += item.price;
        container.innerHTML += `
            <div class="cart-item">
                <img src="${item.image}" alt="${item.title}">
                <div class="cart-item-details">
                    <div class="cart-item-title">${item.title}</div>
                    <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                </div>
                <i class="fa-solid fa-trash remove-item" onclick="removeFromCart(${index})"></i>
            </div>
        `;
    });

    const totalEl = document.getElementById('cartTotal');
    if (totalEl) totalEl.innerText = `$${total.toFixed(2)}`;
}

function toggleCart(forceOpen = false) {
    const modal = document.getElementById('cartModal');
    if (!modal) return;
    if (forceOpen) {
        modal.classList.add('open');
    } else {
        modal.classList.toggle('open');
    }
}

function checkoutWhatsApp() {
    if (cart.length === 0) {
        alert('Tu carrito está vacío.');
        return;
    }

    const phoneNumber = "573000000000";

    let message = "¡Hola NikotechSolution! Quisiera realizar el siguiente pedido:\n\n";
    let total = 0;

    cart.forEach((item, i) => {
        message += `${i + 1}. ${item.title} - $${item.price.toFixed(2)}\n`;
        total += item.price;
    });

    message += `\n*Total a pagar: $${total.toFixed(2)}*`;

    const encodedMessage = encodeURIComponent(message);
    window.open(`https://wa.me/${phoneNumber}?text=${encodedMessage}`, '_blank');
}

/* ---------------------------------------------------------
   3. RENDERIZADO, FILTRADO Y ORDENAMIENTO DE PRODUCTOS
   --------------------------------------------------------- */
let currentCategory = 'all';
let currentProducts = [...products];

function renderProducts(items, gridId = 'productsGrid') {
    const grid = document.getElementById(gridId);
    if (!grid) return;

    if (items.length === 0) {
        grid.innerHTML = `<p style="color: var(--text-muted); grid-column: 1/-1; text-align:center; padding: 40px 0;">No encontramos productos que coincidan con tu búsqueda.</p>`;
        return;
    }

    grid.innerHTML = '';
    items.forEach(product => {
        const oldPriceHtml = product.oldPrice
            ? `<span style="text-decoration:line-through; color:var(--text-muted); font-size:14px; margin-right:6px;">$${product.oldPrice.toFixed(2)}</span>`
            : '';
        grid.innerHTML += `
            <div class="product-card">
                <span class="product-badge">${product.badge}</span>
                <a href="producto.html?id=${product.id}" class="product-link">
                    <img src="${product.image}" alt="${product.title}" class="product-img">
                    <div>
                        <div class="product-rating">${'★'.repeat(product.rating)}${'☆'.repeat(5 - product.rating)}</div>
                        <h3 class="product-title">${product.title}</h3>
                    </div>
                </a>
                <div class="product-bottom">
                    <span>${oldPriceHtml}<span class="product-price">$${product.price.toFixed(2)}</span></span>
                    <button class="add-cart-btn" onclick="event.stopPropagation(); addToCart(${product.id})">
                        <i class="fa-solid fa-cart-plus"></i> Agregar
                    </button>
                </div>
            </div>
        `;
    });
}

function filterCategory(category, btnElement, gridId = 'productsGrid') {
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    currentCategory = category;

    if (category === 'all') {
        currentProducts = [...products];
    } else {
        currentProducts = products.filter(p => p.category === category);
    }

    applySorting(gridId);
}

function filterProducts(gridId = 'productsGrid') {
    const input = document.getElementById('searchInput');
    if (!input) return;
    const query = input.value.toLowerCase();
    
    currentProducts = products.filter(p => p.title.toLowerCase().includes(query));
    applySorting(gridId);
}

function applySorting(gridId = 'productsGrid') {
    const sortSelect = document.getElementById('sortSelect');
    const sortOption = sortSelect ? sortSelect.value : 'default';

    let sortedList = [...currentProducts];

    if (sortOption === 'price-low') {
        sortedList.sort((a, b) => a.price - b.price);
    } else if (sortOption === 'price-high') {
        sortedList.sort((a, b) => b.price - a.price);
    } else if (sortOption === 'name-asc') {
        sortedList.sort((a, b) => a.title.localeCompare(b.title));
    }

    renderProducts(sortedList, gridId);
}

/* ---------------------------------------------------------
   4. MENÚ HAMBURGUESA (móvil)
   --------------------------------------------------------- */
function toggleMobileMenu() {
    const navLinks = document.getElementById('navLinks') || document.querySelector('.nav-links');
    const menuBtnIcon = document.querySelector('.mobile-menu-btn i');

    if (navLinks) {
        navLinks.classList.toggle('active');
        if (navLinks.classList.contains('active')) {
            if (menuBtnIcon) { menuBtnIcon.classList.remove('fa-bars'); menuBtnIcon.classList.add('fa-xmark'); }
        } else {
            if (menuBtnIcon) { menuBtnIcon.classList.remove('fa-xmark'); menuBtnIcon.classList.add('fa-bars'); }
        }
    }
}

/* ---------------------------------------------------------
   5. BUSCADOR (lupita que se abre/cierra)
   --------------------------------------------------------- */
function toggleSearch() {
    const searchBox = document.getElementById('searchBox');
    if (!searchBox) return;
    searchBox.classList.toggle('active');
    if (searchBox.classList.contains('active')) {
        document.getElementById('searchInput').focus();
    }
}

/* ---------------------------------------------------------
   6. INICIALIZACIÓN COMÚN
   --------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();
});

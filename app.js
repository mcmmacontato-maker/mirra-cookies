const body = document.body;
const cartDrawer = document.querySelector('.cart-drawer');
const cartItems = document.querySelector('[data-cart-items]');
const cartCount = document.querySelector('.cart-count');
const total = document.querySelector('[data-total]');
const shippingGap = document.querySelector('[data-shipping-gap]');
const toast = document.querySelector('.toast');
const quickViewModal = document.querySelector('[data-quick-view-modal]');
const modalName = document.querySelector('[data-modal-name]');
const modalDescription = document.querySelector('[data-modal-description]');
const modalPrice = document.querySelector('[data-modal-price]');
const modalPhoto = document.querySelector('[data-modal-photo]');
let cart = [];
let modalProduct = null;

lucide.createIcons();

function renderCart() {
  cartCount.textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  total.textContent = `R$ ${subtotal}`;
  shippingGap.textContent = subtotal >= 120 ? 'frete grátis' : `R$ ${120 - subtotal}`;
  if (!cart.length) {
    cartItems.innerHTML = '<div class="empty-cart"><i data-lucide="cookie"></i><p>Sua sacola está esperando<br />por algo gostoso.</p><a href="#sabores" data-close-cart>ver sabores</a></div>';
    lucide.createIcons();
    cartItems.querySelector('[data-close-cart]').addEventListener('click', closeCart);
    return;
  }
  cartItems.innerHTML = cart.map((item, index) => `<div class="cart-item"><div class="cart-item-thumb ${item.className}"></div><div class="cart-item-info"><h4>${item.name}</h4><div class="cart-item-controls"><button class="quantity-button" type="button" data-quantity="decrease" data-index="${index}">−</button><span>${item.quantity}</span><button class="quantity-button" type="button" data-quantity="increase" data-index="${index}">+</button></div></div><strong class="cart-item-price">R$ ${item.price * item.quantity}</strong><button class="cart-item-remove" type="button" aria-label="Remover ${item.name}" data-remove-item data-index="${index}">×</button></div>`).join('');
  cartItems.querySelectorAll('[data-quantity]').forEach((button) => button.addEventListener('click', () => updateQuantity(Number(button.dataset.index), button.dataset.quantity)));
  cartItems.querySelectorAll('[data-remove-item]').forEach((button) => button.addEventListener('click', () => { cart.splice(Number(button.dataset.index), 1); renderCart(); }));
}

function addProduct(product) {
  const existing = cart.find((item) => item.name === product.name);
  if (existing) existing.quantity += 1;
  else cart.push({ ...product, quantity: 1 });
  renderCart();
}

function updateQuantity(index, action) {
  const item = cart[index];
  if (action === 'increase') item.quantity += 1;
  if (action === 'decrease') item.quantity -= 1;
  if (item.quantity <= 0) cart.splice(index, 1);
  renderCart();
}

function openCart() {
  body.classList.add('cart-open');
  cartDrawer.setAttribute('aria-hidden', 'false');
}
function closeCart() {
  body.classList.remove('cart-open');
  cartDrawer.setAttribute('aria-hidden', 'true');
}
function showToast(message = 'Adicionado à sua sacola') {
  toast.querySelector('span').textContent = message;
  toast.classList.add('show');
  window.setTimeout(() => toast.classList.remove('show'), 2200);
}

document.querySelectorAll('[data-open-cart]').forEach((button) => button.addEventListener('click', openCart));
document.querySelectorAll('[data-close-cart]').forEach((button) => button.addEventListener('click', closeCart));
document.querySelector('[data-cart-overlay]').addEventListener('click', closeCart);

document.querySelectorAll('[data-add]').forEach((button) => button.addEventListener('click', () => {
  const card = button.closest('.product-card');
  addProduct({ name: card.dataset.name, price: Number(card.dataset.price), className: card.querySelector('.product-image').classList[1] });
  showToast();
}));

document.querySelector('[data-combo]').addEventListener('click', () => {
  addProduct({ name: 'Combo para dividir', price: 89, className: 'image-chocolate' });
  openCart();
});

function openQuickView(card) {
  modalProduct = { name: card.dataset.name, price: Number(card.dataset.price), className: card.querySelector('.product-image').classList[1], description: card.querySelector('.product-info p').textContent };
  modalName.textContent = modalProduct.name;
  modalPrice.textContent = `R$ ${modalProduct.price}`;
  modalDescription.textContent = `${modalProduct.description}. Textura macia no centro e bordas douradas, assado em pequenos lotes.`;
  modalPhoto.className = `quick-view-photo ${modalProduct.className}`;
  quickViewModal.classList.add('is-open');
  quickViewModal.setAttribute('aria-hidden', 'false');
}
function closeQuickView() {
  quickViewModal.classList.remove('is-open');
  quickViewModal.setAttribute('aria-hidden', 'true');
}

document.querySelectorAll('.quick-view').forEach((button) => button.addEventListener('click', () => openQuickView(button.closest('.product-card'))));
document.querySelectorAll('[data-close-quick-view]').forEach((button) => button.addEventListener('click', closeQuickView));
document.querySelector('[data-modal-add]').addEventListener('click', () => { addProduct(modalProduct); closeQuickView(); showToast(); });
document.querySelector('[data-checkout]').addEventListener('click', () => { if (!cart.length) { showToast('Escolha um cookie para continuar'); return; } closeCart(); showToast('Checkout em breve'); });

document.querySelectorAll('.filter').forEach((filter) => filter.addEventListener('click', () => {
  document.querySelectorAll('.filter').forEach((item) => item.classList.remove('active'));
  filter.classList.add('active');
  const selected = filter.dataset.filter;
  document.querySelectorAll('.product-card').forEach((card) => {
    card.hidden = selected !== 'todos' && card.dataset.category !== selected;
  });
}));

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeCart();
  if (event.key === 'Escape') closeQuickView();
});

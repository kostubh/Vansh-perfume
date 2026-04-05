// Product Data
const PRODUCTS = [
    { id: 1, name: 'Mystic Rose', price: 29500, category: 'Floral', mood: 'Romantic', image: 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400', description: 'A timeless blend of Bulgarian rose and oud wood.' },
    { id: 2, name: 'Velvet Noir', price: 32500, category: 'Oriental', mood: 'Mysterious', image: 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=400', description: 'Dark, sensual, and captivating. A sophisticated blend.' },
    { id: 3, name: 'Citrus Symphony', price: 24500, category: 'Citrus', mood: 'Fresh', image: 'https://images.unsplash.com/photo-1588405748880-12d1d2a59cfc?w=400', description: 'A vibrant celebration of Mediterranean citrus groves.' },
    { id: 4, name: 'Ocean Breeze', price: 26500, category: 'Aquatic', mood: 'Clean', image: 'https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=400', description: 'Experience the crisp, refreshing essence of coastal winds.' },
    { id: 5, name: 'Golden Amber', price: 35000, category: 'Amber', mood: 'Warm', image: 'https://images.unsplash.com/photo-1594035910387-fea47794261f?w=400', description: 'Warm, luxurious, and utterly captivating.' },
    { id: 6, name: 'Ethereal Bloom', price: 28000, category: 'Floral', mood: 'Light', image: 'https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=400', description: 'A delicate dance of white petals in the morning dew.' },
    { id: 7, name: 'Spice Caravan', price: 31000, category: 'Spicy', mood: 'Bold', image: 'https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=400', description: 'An exotic journey through ancient spice markets.' },
    { id: 8, name: 'Lunar Garden', price: 34000, category: 'Floral', mood: 'Mystical', image: 'https://images.unsplash.com/photo-1547887537-6158d64c35b3?w=400', description: 'Night-blooming jasmine under a silver moon.' }
];

const NOTES = {
    top: ['Bergamot', 'Lemon', 'Mandarin', 'Pink Pepper', 'Sea Salt'],
    middle: ['Rose', 'Jasmine', 'Lavender', 'Neroli', 'Sage'],
    base: ['Oud', 'Amber', 'Musk', 'Vanilla', 'Sandalwood']
};

const QUIZ_QUESTIONS = [
    {
        question: "How would you describe your ideal atmosphere?",
        options: [
            { text: "A sun-drenched citrus grove", mood: "Fresh" },
            { text: "A mysterious moonlit garden", mood: "Mysterious" },
            { text: "A warm, candle-lit library", mood: "Warm" },
            { text: "A vibrant, blooming meadow", mood: "Romantic" }
        ]
    },
    {
        question: "Choose a favorite time of day:",
        options: [
            { text: "Dewy morning", mood: "Fresh" },
            { text: "Golden hour", mood: "Warm" },
            { text: "Twilight", mood: "Mystical" },
            { text: "Midnight", mood: "Bold" }
        ]
    }
];

// State Management
let cart = [];
let quizStep = 0;
let quizAnswers = [];
let customBlend = { top: [], middle: [], base: [] };

// DOM Elements
const productGrid = document.getElementById('product-grid');
const filterBtns = document.querySelectorAll('.filter-btn');
const quizContent = document.getElementById('quiz-content');
const topNotesContainer = document.getElementById('top-notes');
const middleNotesContainer = document.getElementById('middle-notes');
const baseNotesContainer = document.getElementById('base-notes');
const blendPrice = document.getElementById('blend-price');
const cartCount = document.getElementById('cart-count');

// Initialize App
function init() {
    renderProducts(PRODUCTS);
    setupFilters();
    setupQuiz();
    setupBlendCreator();
    setupCart();
}

// Product Functions
function renderProducts(products) {
    productGrid.innerHTML = products.map(p => `
        <div class="product-card fade-in" onclick="openProductModal(${p.id})">
            <img src="${p.image}" alt="${p.name}" class="product-image">
            <div class="product-info">
                <span class="product-category">${p.category}</span>
                <h3>${p.name}</h3>
                <p class="product-price">₹${p.price.toLocaleString('en-IN')}</p>
            </div>
        </div>
    `).join('');
}

function setupFilters() {
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const category = btn.dataset.filter;
            const filtered = category === 'all' ? PRODUCTS : PRODUCTS.filter(p => p.category === category);
            renderProducts(filtered);
        });
    });
}

// Quiz Functions
function setupQuiz() {
    const startBtn = document.getElementById('start-quiz');
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            renderQuizStep(0);
        });
    }
}

function renderQuizStep(step) {
    if (step >= QUIZ_QUESTIONS.length) {
        showQuizResults();
        return;
    }

    const q = QUIZ_QUESTIONS[step];
    quizContent.innerHTML = `
        <div class="quiz-step fade-in">
            <h3 class="text-center">${q.question}</h3>
            <div class="quiz-options">
                ${q.options.map((opt, i) => `
                    <div class="quiz-option" onclick="selectQuizOption(${step}, '${opt.mood}')">
                        ${opt.text}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

window.selectQuizOption = (step, mood) => {
    quizAnswers.push(mood);
    renderQuizStep(step + 1);
};

function showQuizResults() {
    // Basic logic: pick first product that matches a mood from answers
    const recommended = PRODUCTS.find(p => quizAnswers.includes(p.mood)) || PRODUCTS[0];
    quizContent.innerHTML = `
        <div class="quiz-results text-center fade-in">
            <h3>Your Signature Scent is: ${recommended.name}</h3>
            <div class="gold-divider"></div>
            <img src="${recommended.image}" style="width: 200px; margin: 20px 0;">
            <p>${recommended.description}</p>
            <button class="cta-btn" onclick="addToCart(${recommended.id})">Add to Cart</button>
            <button class="cta-btn" style="background: var(--secondary); margin-left: 10px;" onclick="resetQuiz()">Retake Quiz</button>
        </div>
    `;
}

window.resetQuiz = () => {
    quizStep = 0;
    quizAnswers = [];
    quizContent.innerHTML = `
        <div class="quiz-start text-center">
            <h3>Find Your Signature Scent</h3>
            <p>Answer 5 questions to find your perfect match.</p>
            <button id="start-quiz" class="cta-btn" onclick="renderQuizStep(0)">Start Quiz</button>
        </div>
    `;
};

// Blend Creator Functions
function setupBlendCreator() {
    renderNotes('top', topNotesContainer);
    renderNotes('middle', middleNotesContainer);
    renderNotes('base', baseNotesContainer);
}

function renderNotes(layer, container) {
    container.innerHTML = NOTES[layer].map(note => `
        <div class="note-badge" onclick="toggleNote('${layer}', '${note}', this)">
            ${note}
        </div>
    `).join('');
}

window.toggleNote = (layer, note, element) => {
    const index = customBlend[layer].indexOf(note);
    if (index > -1) {
        customBlend[layer].splice(index, 1);
        element.classList.remove('selected');
    } else if (customBlend[layer].length < 2) {
        customBlend[layer].push(note);
        element.classList.add('selected');
    }
    updateBlendPreview();
};

function updateBlendPreview() {
    document.getElementById('preview-top').textContent = customBlend.top.join(', ') || 'Top';
    document.getElementById('preview-middle').textContent = customBlend.middle.join(', ') || 'Middle';
    document.getElementById('preview-base').textContent = customBlend.base.join(', ') || 'Base';
    
    const count = customBlend.top.length + customBlend.middle.length + customBlend.base.length;
    const price = (count * 50 + 100) * 100;
    blendPrice.textContent = `₹${price.toLocaleString('en-IN')}`;
}

// Cart Functions
function setupCart() {
    const addBlendBtn = document.getElementById('add-blend-to-cart');
    if (addBlendBtn) {
        addBlendBtn.addEventListener('click', () => {
            const count = customBlend.top.length + customBlend.middle.length + customBlend.base.length;
            if (count === 0) return alert('Select some notes first!');
            const price = (count * 50 + 100) * 100;
            addToCart({ name: 'Custom Blend', price: price });
            // Reset blend
            customBlend = { top: [], middle: [], base: [] };
            updateBlendPreview();
            document.querySelectorAll('.note-badge').forEach(b => b.classList.remove('selected'));
        });
    }
}

window.addToCart = (item) => {
    const product = typeof item === 'number' ? PRODUCTS.find(p => p.id === item) : item;
    cart.push(product);
    cartCount.textContent = cart.length;
    alert(`${product.name} added to cart!`);
};

// Modal Functions
window.openProductModal = (id) => {
    const p = PRODUCTS.find(prod => prod.id === id);
    const modal = document.getElementById('product-modal');
    const modalBody = document.getElementById('modal-body');
    
    modalBody.innerHTML = `
        <div class="modal-product-layout" style="display: flex; gap: 40px; align-items: center;">
            <img src="${p.image}" style="width: 40%; height: auto;">
            <div class="modal-info">
                <span class="product-category">${p.category}</span>
                <h2>${p.name}</h2>
                <div class="gold-divider" style="margin: 20px 0;"></div>
                <p style="margin-bottom: 20px;">${p.description}</p>
                <p class="product-price">₹${p.price.toLocaleString('en-IN')}</p>
                <button class="cta-btn" style="margin-top: 20px;" onclick="addToCart(${p.id})">Add to Cart</button>
            </div>
        </div>
    `;
    modal.style.display = "block";
};

document.querySelector('.close-modal').onclick = function() {
    document.getElementById('product-modal').style.display = "none";
};

window.onclick = function(event) {
    const modal = document.getElementById('product-modal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

// Run init
document.addEventListener('DOMContentLoaded', init);

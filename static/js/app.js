/* ============================================================
   LOYOLA ERP — Main JavaScript
   ============================================================ */

// ==================== SIDEBAR TOGGLE ====================
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    sidebar.classList.toggle('active');
    if (sidebar.classList.contains('active')) {
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    } else {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// ==================== DARK / LIGHT MODE ====================
function toggleTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('themeIcon');
    const current = html.getAttribute('data-theme');

    if (current === 'dark') {
        html.setAttribute('data-theme', 'light');
        icon.className = 'bi bi-moon-stars-fill';
        localStorage.setItem('theme', 'light');
    } else {
        html.setAttribute('data-theme', 'dark');
        icon.className = 'bi bi-sun-fill';
        localStorage.setItem('theme', 'dark');
    }
}

// Load saved theme
document.addEventListener('DOMContentLoaded', function () {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        const icon = document.getElementById('themeIcon');
        if (icon) icon.className = 'bi bi-sun-fill';
    }

    // Auto-dismiss flash messages
    setTimeout(() => {
        document.querySelectorAll('.flash-msg').forEach(msg => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(() => msg.remove(), 300);
        });
    }, 5000);

    // Close sidebar on window resize (if desktop)
    window.addEventListener('resize', () => {
        if (window.innerWidth > 1024) {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebarOverlay');
            if (sidebar) sidebar.classList.remove('active');
            if (overlay) overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
});

// ==================== CONFIRM DELETE ====================
function confirmDelete(url, itemName) {
    if (confirm(`Are you sure you want to delete "${itemName}"? This cannot be undone.`)) {
        window.location.href = url;
    }
}

// ==================== MODAL FUNCTIONS ====================
function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// ==================== RESUME FORM HELPERS ====================
function addArrayItem(fieldName, template) {
    const container = document.getElementById(fieldName + '-container');
    const div = document.createElement('div');
    div.className = 'array-item';
    div.innerHTML = template + '<button type="button" class="btn btn-danger btn-sm mt-1" onclick="this.parentElement.remove(); updateJsonField(\'' + fieldName + '\')">Remove</button>';
    container.appendChild(div);
}

function updateJsonField(fieldName) {
    const container = document.getElementById(fieldName + '-container');
    const items = container.querySelectorAll('.array-item');
    const data = [];

    items.forEach(item => {
        const inputs = item.querySelectorAll('input, textarea');
        const obj = {};
        inputs.forEach(input => {
            if (input.name && input.name.startsWith('item_')) {
                obj[input.name.replace('item_', '')] = input.value;
            }
        });
        if (Object.keys(obj).length > 0) {
            data.push(obj);
        }
    });

    const hiddenInput = document.getElementById(fieldName + '-json');
    if (hiddenInput) {
        hiddenInput.value = JSON.stringify(data);
    }
}

// ==================== FILE UPLOAD PREVIEW ====================
function previewFile(input, previewId) {
    const preview = document.getElementById(previewId);
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            if (preview.tagName === 'IMG') {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// ==================== GLOBAL SEARCH ====================
const searchInput = document.getElementById('globalSearch');
if (searchInput) {
    searchInput.addEventListener('keyup', function (e) {
        const query = this.value.toLowerCase();
        // Search visible table rows
        document.querySelectorAll('.data-table tbody tr').forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(query) ? '' : 'none';
        });
        // Search cards
        document.querySelectorAll('.gallery-card, .placement-card').forEach(card => {
            const text = card.textContent.toLowerCase();
            card.style.display = text.includes(query) ? '' : 'none';
        });
    });
}

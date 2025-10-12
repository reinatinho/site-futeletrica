// Smooth scrolling para links de navegação
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar efeito de scroll suave
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Configurar Intersection Observer para animações
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -100px 0px'
    };

    // Observer para títulos de seção
    const titleObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.style.transition = 'all 0.8s ease-out';
            }
        });
    }, observerOptions);

    // Observer para texto da história
    const historyObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                entry.target.classList.add('animated');
                const paragraphs = entry.target.querySelectorAll('p');
                paragraphs.forEach((p, index) => {
                    setTimeout(() => {
                        p.style.opacity = '1';
                        p.style.transform = 'translateY(0)';
                        p.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
                    }, index * 300);
                });
            }
        });
    }, observerOptions);

    // Observer para itens da galeria
    const galleryObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const items = entry.target.querySelectorAll('.galeria-item');
                items.forEach((item, index) => {
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                        item.style.transition = 'all 0.8s ease-out';
                    }, index * 150);
                });
            }
        });
    }, observerOptions);

    // Observer para regras
    const rulesObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const rules = entry.target.querySelectorAll('.regra-item');
                rules.forEach((rule, index) => {
                    setTimeout(() => {
                        rule.style.opacity = '1';
                        rule.style.transform = 'translateX(0)';
                        rule.style.transition = 'all 0.8s ease-out';
                    }, index * 100);
                });
            }
        });
    }, observerOptions);

    // Observer para seção de uniformes
    const uniformesObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                entry.target.classList.add('animated');
                const img = entry.target.querySelector('.uniformes-img');
                const text = entry.target.querySelector('.uniformes-text');
                const features = entry.target.querySelectorAll('.uniformes-features .feature');
                const solicitar = entry.target.querySelector('.uniformes-solicitar');
                
                if (img) {
                    setTimeout(() => {
                        img.style.opacity = '1';
                        img.style.transform = 'translateX(0)';
                        img.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
                    }, 200);
                }
                
                if (text) {
                    setTimeout(() => {
                        text.style.opacity = '1';
                        text.style.transform = 'translateX(0)';
                        text.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
                    }, 400);
                }
                
                features.forEach((feature, index) => {
                    setTimeout(() => {
                        feature.style.opacity = '1';
                        feature.style.transform = 'translateY(0)';
                        feature.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
                    }, 600 + (index * 150));
                });
                
                if (solicitar) {
                    setTimeout(() => {
                        solicitar.style.opacity = '1';
                        solicitar.style.transform = 'translateY(0)';
                        solicitar.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
                    }, 1000);
                }
            }
        });
    }, observerOptions);

    // Observer para seção do parceiro
    const partnerObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.style.transition = 'all 0.8s ease-out';
            }
        });
    }, observerOptions);

    // Preparar elementos para animação
    const sectionTitles = document.querySelectorAll('.section-title');
    const historyText = document.querySelector('.historia-text');
    const galleryGrid = document.querySelector('.galeria-grid');
    const rulesGrid = document.querySelector('.regras-grid');
    const uniformesContent = document.querySelector('.uniformes-content');
    const partnerContent = document.querySelector('.parceiro-content');
    
    // Definir estados iniciais
    sectionTitles.forEach(title => {
        title.style.opacity = '0';
        title.style.transform = 'translateY(30px)';
        titleObserver.observe(title);
    });

    if (historyText) {
        const paragraphs = historyText.querySelectorAll('p');
        paragraphs.forEach(p => {
            p.style.opacity = '0';
            p.style.transform = 'translateY(30px)';
        });
        historyObserver.observe(historyText);
    }

    if (galleryGrid) {
        const items = galleryGrid.querySelectorAll('.galeria-item');
        items.forEach(item => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(30px)';
        });
        galleryObserver.observe(galleryGrid);
    }

    if (rulesGrid) {
        const rules = rulesGrid.querySelectorAll('.regra-item');
        rules.forEach((rule, index) => {
            rule.style.opacity = '0';
            rule.style.transform = index % 2 === 0 ? 'translateX(-30px)' : 'translateX(30px)';
        });
        rulesObserver.observe(rulesGrid);
    }

    if (uniformesContent) {
        const img = uniformesContent.querySelector('.uniformes-img');
        const text = uniformesContent.querySelector('.uniformes-text');
        const features = uniformesContent.querySelectorAll('.uniformes-features .feature');
        const solicitar = uniformesContent.querySelector('.uniformes-solicitar');
        
        if (img) {
            img.style.opacity = '0';
            img.style.transform = 'translateX(-30px)';
        }
        
        if (text) {
            text.style.opacity = '0';
            text.style.transform = 'translateX(30px)';
        }
        
        features.forEach(feature => {
            feature.style.opacity = '0';
            feature.style.transform = 'translateY(20px)';
        });
        
        if (solicitar) {
            solicitar.style.opacity = '0';
            solicitar.style.transform = 'translateY(20px)';
        }
        
        uniformesObserver.observe(uniformesContent);
    }

    if (partnerContent) {
        partnerContent.style.opacity = '0';
        partnerContent.style.transform = 'translateY(30px)';
        partnerObserver.observe(partnerContent);
    }

    // Menu mobile toggle
    const navMenu = document.querySelector('.nav-menu');
    const navToggle = document.createElement('button');
    navToggle.innerHTML = '<i class="fas fa-bars"></i>';
    navToggle.className = 'nav-toggle';
    navToggle.style.cssText = `
        display: none;
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0.5rem;
    `;

    // Adicionar botão de toggle ao nav
    const navContainer = document.querySelector('.nav-container');
    navContainer.appendChild(navToggle);

    // Função para toggle do menu mobile
    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('mobile-active');
    });

    // Adicionar estilos para mobile
    const style = document.createElement('style');
    style.textContent = `
        @media (max-width: 768px) {
            .nav-toggle {
                display: block !important;
            }
            
            .nav-menu {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: var(--black);
                flex-direction: column;
                padding: 1rem;
                transform: translateY(-100%);
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }
            
            .nav-menu.mobile-active {
                transform: translateY(0);
                opacity: 1;
                visibility: visible;
            }
        }
    `;
    document.head.appendChild(style);
});

// Função para fullscreen do Power BI
function toggleFullscreen() {
    const container = document.getElementById('powerbi-container');
    if (!container) return;
    
    const iframe = container.querySelector('iframe');
    
    if (!document.fullscreenElement) {
        container.requestFullscreen().then(() => {
            iframe.style.height = '100vh';
            iframe.style.width = '100vw';
        }).catch(err => {
            console.log('Erro ao entrar em fullscreen:', err);
        });
    } else {
        document.exitFullscreen().then(() => {
            iframe.style.height = '600px';
            iframe.style.width = '100%';
        });
    }
}

// Adicionar listener para mudanças de fullscreen
document.addEventListener('fullscreenchange', function() {
    const container = document.getElementById('powerbi-container');
    if (!container) return;
    
    const iframe = container.querySelector('iframe');
    
    if (!document.fullscreenElement) {
        iframe.style.height = '600px';
        iframe.style.width = '100%';
    }
});

// Lazy loading para imagens
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});

// Efeito de parallax removido para evitar sobreposição de conteúdo
// O parallax pode causar problemas de z-index e sobreposição durante o scroll

// Melhorar transições durante o scroll
let ticking = false;

function updateOnScroll() {
    const scrolled = window.pageYOffset;
    const sections = document.querySelectorAll('.section');
    
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
        
        if (isVisible && !section.classList.contains('in-view')) {
            section.classList.add('in-view');
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }
    });
    
    ticking = false;
}

function requestTick() {
    if (!ticking) {
        requestAnimationFrame(updateOnScroll);
        ticking = true;
    }
}

window.addEventListener('scroll', requestTick);

// Contador animado para estatísticas
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent.replace('+', ''));
        const increment = target / 100;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = counter.textContent.includes('+') ? target + '+' : target;
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current);
            }
        }, 20);
    });
}

// Executar contador quando a seção hero aparecer
const heroObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounters();
            heroObserver.unobserve(entry.target);
        }
    });
});

const heroSection = document.querySelector('.hero');
if (heroSection) {
    heroObserver.observe(heroSection);
}
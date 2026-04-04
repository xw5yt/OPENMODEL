Create a stunning, production-grade AI landing page in a single HTML file.
No frameworks. Pure HTML, CSS, JavaScript.

---

## 🎯 CONCEPT & TONE

Design direction: Dark luxury meets technical precision.
Think deep space, neural networks, glowing data streams.
Primary palette: Near-black (#07080f), electric blue (#0066ff),
neon cyan (#00d4ff), soft white (#e8edf5).
Accent: subtle violet (#7c3aed) for depth.

One unforgettable element: an animated particle canvas in the hero
that reacts to mouse movement (particles form constellation-like neural nets).

---

## 🔤 TYPOGRAPHY

Display font: "Syne" (import from Google Fonts) — geometric, futuristic.
Body font: "DM Sans" — clean, readable, modern.
Monospace accents: "JetBrains Mono" — for code snippets, stats, labels.
Use dramatic scale contrast: hero headline 96px → body 16px.

---

## 📐 LAYOUT BLOCKS (in order)

### 1. NAVIGATION (sticky, glassmorphism)
- Left: Logo — small glowing dot + "NeuralX" wordmark in Syne font
- Center: links — Возможности · Примеры · Тарифы · Документация
- Right: two buttons — "Войти" (ghost border) + "Попробовать бесплатно"
  (gradient blue→cyan, pill shape, subtle glow on hover)
- Background: blur(20px) + rgba(7,8,15,0.7) on scroll
- Thin cyan line (1px) at bottom on scroll-triggered

### 2. HERO SECTION (full viewport height)
- Background: animated canvas with ~120 moving particles connected
  by lines when close (neural network effect). Particles are small dots,
  connections fade with distance. Mouse parallax: particles gently
  drift toward cursor.
- Large badge above headline: small pill — "✦ ИИ нового поколения"
  with animated gradient border
- Headline (2 lines):
  Line 1: "Интеллект без" — white, 96px
  Line 2: "границ." — gradient text (blue→cyan), italic, 96px
  Text reveals with staggered letter animation on load.
- Subline (max 320px wide, centered):
  "Генеративный ИИ, который понимает контекст, создаёт, анализирует
  и решает задачи любой сложности."
- CTA buttons (centered):
  Primary: "Начать бесплатно →" (large, pill, gradient bg, shimmer
  animation on hover)
  Secondary: "Смотреть демо ▷" (ghost, with play-circle icon)
- Below buttons: trust micro-line —
  "★★★★★  Более 2 млн пользователей · Без кредитной карты"
  in small monospace, muted color
- Bottom: animated scroll-indicator chevron

### 3. LOGOS / SOCIAL PROOF (infinite marquee strip)
- Section label: "Используют команды из" (small caps, muted)
- Marquee of 8–10 company logo placeholders (SVG text logos,
  monochrome white 30% opacity, scale to 100% on hover)
- Two rows moving in opposite directions
- Gradient fade on left/right edges

### 4. FEATURES SECTION — "Что умеет ИИ"
- Section header centered:
  Eyebrow: "ВОЗМОЖНОСТИ" (monospace, cyan, letter-spaced)
  Headline: "Один инструмент — безграничные задачи"
- Bento grid layout (asymmetric):
  Card 1 (wide, 2-col span): "Умный чат" — live typing animation
    showing a demo Q&A exchange. Icon: animated brain pulse.
  Card 2: "Анализ данных" — mini animated bar chart SVG.
  Card 3: "Генерация кода" — code snippet in JetBrains Mono with
    syntax highlight (manual, CSS classes).
  Card 4 (tall): "Работа с документами" — drag-drop zone visual,
    PDF/DOCX icons floating.
  Card 5: "Многоязычность" — rotating flags + text.
  Card 6 (wide): "API интеграция" — code block showing fetch() call.
- Cards: dark glass (#0d0f1a bg), 1px border rgba(0,212,255,0.15),
  radius 20px, hover: border glows, subtle lift transform.

### 5. HOW IT WORKS — "Как это работает"
- Background: slightly lighter #0d0f1a
- Three steps in horizontal row with connecting animated dotted line:
  Step 1 — "Опиши задачу" · icon: keyboard
  Step 2 — "ИИ анализирует" · icon: rotating gear/cog
  Step 3 — "Получи результат" · icon: lightning bolt
- Each step: large number (01 02 03) in huge muted font behind icon,
  short description below.
- Scroll-triggered reveal: steps slide in left→right with delay.

### 6. LIVE DEMO BLOCK
- Full-width section with dark bg + subtle grid texture
- Left half: fake chat UI — messages animate in sequence
  (user asks → AI responds, typewriter effect)
  Use 3–4 exchanges showing different capabilities
- Right half: rotating feature tabs
  Tab buttons: "Чат" / "Код" / "Анализ" / "Перевод"
  Content area switches on click with fade transition
- Section headline: "Убедись сам — прямо сейчас"

### 7. STATS / NUMBERS SECTION
- Dark gradient background
- 4 large animated counters (count up on scroll into view):
  "99.9%" — Uptime SLA
  "< 1s" — Время ответа
  "2M+" — Активных пользователей
  "50+" — Языков и диалектов
- Numbers: 72px, Syne Bold, gradient
- Labels: DM Sans, muted

### 8. PRICING — "Тарифы"
- Eyebrow: "ТАРИФЫ" monospace
- Headline: "Начни бесплатно. Расти без ограничений."
- Three cards in a row, middle card elevated + "Популярный" badge:
  Free:
    - 0₽/мес
    - 100 запросов/день
    - GPT-4o уровень
    - Базовые инструменты
    - [Начать бесплатно]
  Pro (highlighted, glowing border, slightly larger):
    - 990₽/мес
    - Безлимитные запросы
    - Приоритетная очередь
    - API доступ
    - История диалогов
    - [Выбрать Pro]
  Enterprise:
    - Индивидуально
    - Выделенный кластер
    - SLA гарантии
    - Командный доступ
    - Кастомные модели
    - [Связаться]
- Toggle: monthly / annual (annual = -20%, animate price change)

### 9. TESTIMONIALS — "Что говорят пользователи"
- 3-column card grid (or horizontal scroll on mobile)
- Each card: avatar circle (gradient initials), name, role, company,
  5 stars, quote text
- Cards tilt slightly on hover (CSS perspective transform)
- Background: subtle noise texture overlay

### 10. FAQ — "Частые вопросы"
- Accordion style, 6–8 questions
- Open/close with smooth max-height CSS transition
- Active item: left border 2px cyan, bg slightly lighter
- Sample questions:
  · Нужна ли кредитная карта для бесплатного тарифа?
  · Могу ли я использовать API?
  · Как защищены мои данные?
  · Есть ли мобильное приложение?

### 11. FINAL CTA SECTION
- Full-width dark section with large glowing orb/blob in center (radial gradient)
- Headline (large, centered): "Начни работать с ИИ прямо сейчас"
- Subline: "Бесплатно. Без ограничений по времени."
- Single large CTA button: "Создать аккаунт →"
- Below button: "Уже есть аккаунт? Войти"

### 12. FOOTER
- 4-column grid:
  Col 1: Logo + short tagline + social icons (TG, GitHub, Twitter/X)
  Col 2: Продукт — Возможности · Документация · Changelog · API
  Col 3: Компания — О нас · Блог · Карьера · Пресс-кит
  Col 4: Поддержка — FAQ · Контакты · Статус системы · Политика
- Bottom bar: © 2025 NeuralX · Политика конфиденциальности · Условия
- Thin cyan top border (1px gradient)

---

## ✨ GLOBAL EFFECTS & POLISH

- Custom cursor: small glowing dot that follows mouse with 100ms lag
- Smooth scroll (scroll-behavior: smooth)
- All sections: fade + translate-Y(30px) reveal on IntersectionObserver
- Glassmorphism cards throughout (backdrop-filter: blur)
- Grain overlay (SVG filter or pseudo-element) for texture
- Mobile responsive: stack all grids to single column, hamburger nav
- No external libraries except Google Fonts
- All animations: prefer CSS transitions/keyframes
- Keep HTML semantic (header, nav, main, section, footer)
- No lorem ipsum — all text in Russian, realistic and specific

---

## 🚫 AVOID

- Purple gradient on white (cliché AI look)
- Generic Inter/Roboto fonts
- Flat, boring card designs with no depth
- Placeholder gray boxes instead of real visual content
- Cookie-cutter layouts that look like every other SaaS site
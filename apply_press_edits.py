#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, sys

with open('/home/user/contraco-ru/press.html', 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)

def replace_once(c, old, new, label):
    count = c.count(old)
    if count == 0:
        print(f'ERROR [{label}]: string not found', file=sys.stderr)
        sys.exit(1)
    if count > 1:
        print(f'WARN [{label}]: found {count} times, replacing first', file=sys.stderr)
    return c.replace(old, new, 1)

# ============================================================
# EDIT 2a: og:title
# ============================================================
content = replace_once(content,
    '<meta property="og:title" content="Метод Резонанса™: Глобальная стратегия ИИ для российского бизнеса | contraco">',
    '<meta property="og:title" content="Пресса и СМИ | contraco">',
    'og:title'
)

# ============================================================
# EDIT 2b: CollectionPage name (no "| contraco" suffix)
# ============================================================
content = replace_once(content,
    '"name": "Метод Резонанса™: Глобальная стратегия ИИ для российского бизнеса",\n  "description":',
    '"name": "Пресса и СМИ | contraco",\n  "description":',
    'CollectionPage name'
)

# ============================================================
# EDIT 2c: Second WebPage block name (has "| contraco" suffix)
# ============================================================
content = replace_once(content,
    '"name": "Метод Резонанса™: Глобальная стратегия ИИ для российского бизнеса | contraco",',
    '"name": "Пресса и СМИ | contraco",',
    'WebPage block name'
)

# ============================================================
# EDIT 1+2d: Remove all marketing sections, add simple page header with h1
# Matches from <main> opening through end of Global Perspective section
# ============================================================
pattern = r'    <main class="main-content">\n        <section class="page-header">.*?        <!-- Press Coverage -->'
replacement = (
    '    <main class="main-content">\n'
    '        <section class="page-header">\n'
    '            <div class="container">\n'
    '                <h1 class="page-title">Пресса и СМИ</h1>\n'
    '            </div>\n'
    '        </section>\n\n'
    '        <!-- Press Coverage -->'
)
new_content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
if new_content == content:
    print('ERROR [marketing block]: regex not matched', file=sys.stderr)
    sys.exit(1)
content = new_content

# ============================================================
# EDIT 3: Reorder + insert new press cards
# Replace block [CIO.com card][Medium card][Informatics start]
# with [Medium card][4 new cards][CIO.com card][Informatics start]
# ============================================================
OLD_CIOCOM_MEDIUM = (
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">CIO.com</p>\n'
    '                        <p class="press-date">7 апреля 2026</p>\n'
    '                        <span class="press-tag">Экспертный источник</span>\n'
    '                        <h3 class="press-title">Organizations often don\'t measure the cost of IT inefficiency, but it can be huge</h3>\n'
    '                        <p class="press-excerpt">Ведущее мировое издание для CIO цитирует Frank Meltke как эксперта по скрытым затратам неэффективности ИТ. Его фреймворк разграничения необходимого и излишнего трения лёг в основу аналитики статьи и вызвал волну международных публикаций на восьми языках.</p>\n'
    '                        <a href="https://www.cio.com/article/4152626/organizations-often-dont-measure-the-cost-of-it-inefficiency-but-it-can-be-huge.html" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Medium</p>\n'
    '                        <p class="press-date">24 апреля 2026</p>\n'
    '                        <span class="press-tag">Экспертный вклад</span>\n'
    '                        <h3 class="press-title">AI and the New Workload: 21 Experts on What\'s Getting Easier, and What\'s Not</h3>\n'
    '                        <p class="press-excerpt">Frank Meltke участвует в обзоре 21 эксперта о реальном опыте внедрения ИИ: где ИИ действительно снижает нагрузку, а где создаёт новые слои проверки, валидации и принятия решений.</p>\n'
    '                        <a href="https://medium.com/@yarawriting/ai-and-the-new-workload-20-experts-on-whats-getting-easier-and-what-s-not-8f6ebd055921" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Informatics Magazine</p>'
)

NEW_ORDER_THROUGH_INFORMATICS = (
    '                    <!-- Medium - AI and the New Workload -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Medium</p>\n'
    '                        <p class="press-date">24 апреля 2026</p>\n'
    '                        <span class="press-tag">Экспертный вклад</span>\n'
    '                        <h3 class="press-title">AI and the New Workload: 21 Experts on What\'s Getting Easier, and What\'s Not</h3>\n'
    '                        <p class="press-excerpt">Frank Meltke участвует в обзоре 21 эксперта о реальном опыте внедрения ИИ: где ИИ действительно снижает нагрузку, а где создаёт новые слои проверки, валидации и принятия решений.</p>\n'
    '                        <a href="https://medium.com/@yarawriting/ai-and-the-new-workload-20-experts-on-whats-getting-easier-and-what-s-not-8f6ebd055921" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- Le Monde Informatique -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Le Monde Informatique</p>\n'
    '                        <p class="press-date">20 апреля 2026</p>\n'
    '                        <span class="press-tag">Экспертный источник</span>\n'
    '                        <h3 class="press-title">Les lenteurs du support IT grèvent la productivité des salariés</h3>\n'
    '                        <p class="press-excerpt">Ведущее французское корпоративное ИТ-издание освещает исследование Atera по неэффективности ИТ с экспертным анализом Frank Meltke. Статья рассматривает, как трение в ИТ-поддержке обходится организациям в миллионы ежегодно.</p>\n'
    '                        <a href="https://www.lemondeinformatique.fr/actualites/lire-les-lenteurs-du-support-it-grevent-la-productivite-des-salaries-99962.html" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- CIO Online -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">CIO Online</p>\n'
    '                        <p class="press-date">17 апреля 2026</p>\n'
    '                        <span class="press-tag">Экспертный источник</span>\n'
    '                        <h3 class="press-title">Les coûts cachés de l\'inefficacité du support IT</h3>\n'
    '                        <p class="press-excerpt">Французское издание CIO Online публикует экспертный анализ Frank Meltke. Статья исследует, как трение в ИТ-поддержке обходится организациям в миллионы ежегодно.</p>\n'
    '                        <a href="https://www.cio-online.com/actualites/lire-les-couts-caches-de-l-inefficacite-du-support-it-16966.html" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- CIO Korea -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">CIO Korea</p>\n'
    '                        <p class="press-date">9 апреля 2026</p>\n'
    '                        <span class="press-tag">Экспертный источник</span>\n'
    '                        <h3 class="press-title">IT 비효율, 기업에 연간 수백만 달러 손실 초래…해법은 무엇인가</h3>\n'
    '                        <p class="press-excerpt">Ведущее южнокорейское корпоративное ИТ-издание цитирует Frank Meltke как генерального директора консалтинговой компании contraco по цифровой трансформации. Его вывод о том, что полностью безупречная ИТ-среда является либо угрозой безопасности, либо несоразмерно дорогостоящей, составляет аналитическую основу статьи.</p>\n'
    '                        <a href="https://www.cio.com/article/4156938/it-%EB%B9%84%ED%9A%A8%EC%9C%A8-%EA%B8%B0%EC%97%85%EC%97%90-%EC%97%B0%EA%B0%84-%EC%88%98%EB%B0%B1%EB%A7%8C-%EB%8B%AC%EB%9F%AC-%EC%86%90%EC%8B%A4-%EC%B4%88%EB%9E%98%ED%95%B4%EB%B2%95%EC%9D%80.html" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- CIO Japan -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">CIO Japan</p>\n'
    '                        <p class="press-date">Апрель 2026</p>\n'
    '                        <span class="press-tag">Экспертный источник</span>\n'
    '                        <h3 class="press-title">ITの非効率は見えないコストをもたらしている</h3>\n'
    '                        <p class="press-excerpt">Японское издание CIO.com публикует анализ Frank Meltke о скрытых затратах неэффективности ИТ для японской аудитории топ-менеджеров.</p>\n'
    '                        <a href="https://www.cio.com/article/4157518/it%E3%81%AE%E9%9D%9E%E5%8A%B9%E7%8E%87%E3%81%AF%E8%A6%8B%E3%81%88%E3%81%AA%E3%81%84%E3%82%B3%E3%82%B9%E3%83%88%E3%82%92%E3%82%82%E3%81%9F%E3%82%89%E3%81%97%E3%81%A6%E3%81%84%E3%82%8B.html" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- CIO.com -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">CIO.com</p>\n'
    '                        <p class="press-date">7 апреля 2026</p>\n'
    '                        <span class="press-tag">Экспертный источник</span>\n'
    '                        <h3 class="press-title">Organizations often don\'t measure the cost of IT inefficiency, but it can be huge</h3>\n'
    '                        <p class="press-excerpt">Ведущее мировое издание для CIO цитирует Frank Meltke как эксперта по скрытым затратам неэффективности ИТ. Его фреймворк разграничения необходимого и излишнего трения лёг в основу аналитики статьи и вызвал волну международных публикаций на восьми языках.</p>\n'
    '                        <a href="https://www.cio.com/article/4152626/organizations-often-dont-measure-the-cost-of-it-inefficiency-but-it-can-be-huge.html" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Informatics Magazine</p>'
)

content = replace_once(content, OLD_CIOCOM_MEDIUM, NEW_ORDER_THROUGH_INFORMATICS, 'CIOcom+Medium reorder')

# Insert Consultant Magazine + LinkedIn BEFORE Syndications card
OLD_BEFORE_SYNDICATIONS = (
    '                        <a href="https://informaticsmagazine.com/qa/15-predictions-about-the-future-of-ai-regulation-and-the-factors-driving-change/" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Международные синдикации</p>'
)

NEW_WITH_EXTRA_CARDS = (
    '                        <a href="https://informaticsmagazine.com/qa/15-predictions-about-the-future-of-ai-regulation-and-the-factors-driving-change/" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- Consultant Magazine -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Consultant Magazine</p>\n'
    '                        <p class="press-date">30 марта 2026</p>\n'
    '                        <span class="press-tag">Экспертный вклад</span>\n'
    '                        <h3 class="press-title">High-Impact Project Kickoffs in Professional Services</h3>\n'
    '                        <p class="press-excerpt">Frank Meltke вносит вклад в обзор 12 экспертов по методологии запуска проектов. Его анализ разрыва готовности и фреймворк единого условия победы является опорным материалом статьи.</p>\n'
    '                        <a href="https://consultantmagazine.co/qa/high-impact-project-kickoffs-in-professional-services/" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- LinkedIn contraco -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">LinkedIn contraco</p>\n'
    '                        <p class="press-date">16 марта 2026</p>\n'
    '                        <span class="press-tag">Опубликованная статья</span>\n'
    '                        <h3 class="press-title">73% of AI Transformations Fail. Here Is the One Thing They All Got Wrong.</h3>\n'
    '                        <p class="press-excerpt">После 28 лет и более 50 корпоративных трансформаций закономерность неизменна: провалы внедрения ИИ носят не технический, а психологический характер. Статья выявляет четыре барьера принятия, невидимых в стандартных дорожных картах внедрения.</p>\n'
    '                        <a href="https://www.linkedin.com/pulse/73-ai-transformations-fail-here-one-thing-all-got-wrong-contraco-forwf" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Международные синдикации</p>'
)

content = replace_once(content, OLD_BEFORE_SYNDICATIONS, NEW_WITH_EXTRA_CARDS, 'Consultant+LinkedIn insert')

# ============================================================
# EDIT 4: Add I-COM cards after existing I-COM keynote card
# ============================================================
OLD_AFTER_KEYNOTE = (
    '                        <a href="https://youtu.be/8vgMahvshUI" class="press-link" target="_blank" rel="noopener">\n'
    '                            Смотреть презентацию <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">BBC Global Minds</p>'
)

NEW_WITH_ICOM_CARDS = (
    '                        <a href="https://youtu.be/8vgMahvshUI" class="press-link" target="_blank" rel="noopener">\n'
    '                            Смотреть презентацию <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- I-COM Global Summit 2018 Speaker Feature -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">I-COM Global Summit</p>\n'
    '                        <p class="press-date">Апрель 2018, Сан-Себастьян, Испания</p>\n'
    '                        <span class="press-tag">Speaker Feature</span>\n'
    '                        <h3 class="press-title">I-COM Global Summit 2018 Speaker Invitation</h3>\n'
    '                        <p class="press-excerpt">Персональное приглашение спикера и промо-материал для I-COM Global Summit в Сан-Себастьяне. Frank Meltke был выбран в качестве основного докладчика по стратегии многоканальных данных и персонализации.</p>\n'
    '                        <a href="https://youtu.be/8vgMahvshUI" class="press-link" target="_blank" rel="noopener">\n'
    '                            Смотреть\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- I-COM Data Startup Challenge - Jury Board -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">I-COM Global</p>\n'
    '                        <p class="press-date">Март 2018</p>\n'
    '                        <span class="press-tag">Член жюри</span>\n'
    '                        <h3 class="press-title">I-COM Data Startup Challenge: Jury Board</h3>\n'
    '                        <p class="press-excerpt">Frank Meltke в составе международного жюри I-COM Data Startup Challenge. Оценка и наставничество стартапов, управляемых данными, со всего мира.</p>\n'
    '                        <a href="https://www.i-com.org/awards/data-startup-challenge/board-jury" class="press-link" target="_blank" rel="noopener">\n'
    '                            Подробнее\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">BBC Global Minds</p>'
)

content = replace_once(content, OLD_AFTER_KEYNOTE, NEW_WITH_ICOM_CARDS, 'I-COM cards insert')

# ============================================================
# EDIT 5: Replace syndications list body (title + excerpt + ul)
# ============================================================
OLD_SYNDICATIONS_BODY = (
    '<h3 class="press-title">Освещение неэффективности ИТ: 6 дополнительных рынков</h3>\n'
    '                        <p class="press-excerpt">После первой публикации в CIO.com аналитика Frank Meltke была подхвачена шестью дополнительными рынками.</p>\n'
    '                        <ul style="list-style:none; margin: 0 0 24px; padding: 0;">\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://computersweden.se/article/4157029/organisationer-mater-ofta-inte-kostnaden-for-ineffektivitet-inom-it-men-den-kan-vara-enorm.html" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">Computer Sweden</a> <span style="color: var(--warm-gray-medium);">(шведский)</span></li>\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://www.lemondeinformatique.fr/actualites/lire-les-lenteurs-du-support-it-grevent-la-productivite-des-salaries-99962.html" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">Le Monde Informatique</a> <span style="color: var(--warm-gray-medium);">(французский)</span></li>\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://www.cio.com/article/4157518/it%E3%81%AE%E9%9D%9E%E5%8A%B9%E7%8E%87%E3%81%AF%E8%A6%8B%E3%81%88%E3%81%AA%E3%81%84%E3%82%B3%E3%82%B9%E3%83%88%E3%82%92%E3%82%82%E3%81%9F%E3%82%89%E3%81%97%E3%81%A6%E3%81%84%E3%82%8B.html" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">CIO Japan</a> <span style="color: var(--warm-gray-medium);">(японский)</span></li>\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://www.cio.com/article/4156938/it-%EB%B9%84%ED%9A%A8%EC%9C%A8-%EA%B8%B0%EC%97%85%EC%97%90-%EC%97%B0%EA%B0%84-%EC%88%98%EB%B0%B1%EB%A7%8C-%EB%8B%AC%EB%9F%AC-%EC%86%90%EC%8B%A4-%EC%B4%88%EB%9E%98%ED%95%B4%EB%B2%95%EC%9D%80.html" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">CIO Korea</a> <span style="color: var(--warm-gray-medium);">(корейский)</span></li>\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://fjcio.cn/Item/18311.aspx" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">CIO China</a> <span style="color: var(--warm-gray-medium);">(китайский)</span></li>\n'
    '                            <li style="padding: 7px 0; font-size: 0.88rem;"><a href="https://www.cio-online.com/actualites/lire-les-couts-caches-de-l-inefficacite-du-support-it-16966.html" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">CIO Online</a> <span style="color: var(--warm-gray-medium);">(французский)</span></li>\n'
    '                        </ul>'
)

NEW_SYNDICATIONS_BODY = (
    '<h3 class="press-title">Освещение неэффективности ИТ: 8 дополнительных рынков</h3>\n'
    '                        <p class="press-excerpt">После первой публикации в CIO.com аналитика Frank Meltke была подхвачена восемью дополнительными рынками.</p>\n'
    '                        <ul style="list-style:none; margin: 0 0 24px; padding: 0;">\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://computersweden.se/article/4157029/organisationer-mater-ofta-inte-kostnaden-for-ineffektivitet-inom-it-men-den-kan-vara-enorm.html" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">Computer Sweden</a> <span style="color: var(--warm-gray-medium);">(шведский)</span></li>\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://trendhornan.se/teknik/kostnaden-for-it-ineffektivitet-kan-leda-till-stora-forluster-for-foretag" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">Trendhornan</a> <span style="color: var(--warm-gray-medium);">(шведский)</span></li>\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://csirt-universitaire.sn/publications/actualites/les-lenteurs-du-support-it-grevent-la-productivite-des-salaries" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">CSIRT Universitaire</a> <span style="color: var(--warm-gray-medium);">(Сенегал)</span></li>\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://www.iatechauquotidien.com/pme-en-peril-quand-linefficacite-informatique-coute-des-millions/" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">IA Tech au Quotidien</a> <span style="color: var(--warm-gray-medium);">(французский)</span></li>\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://lesenjeuxeco.dz/wp-content/uploads/2026/04/N%C2%B0885-21-04-2026-.pdf" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">Les Enjeux Éco</a> <span style="color: var(--warm-gray-medium);">(Алжир, печать)</span></li>\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://fjcio.cn/Item/18311.aspx" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">CIO China</a> <span style="color: var(--warm-gray-medium);">(китайский)</span></li>\n'
    '                            <li style="padding: 7px 0; border-bottom: 1px solid var(--warm-gray-light); font-size: 0.88rem;"><a href="https://tiatra.com/it%E3%81%AE%E9%9D%9E%E5%8A%B9%E7%8E%87%E3%81%AF%E8%A6%8B%E3%81%88%E3%81%AA%E3%81%84%E3%82%B3%E3%82%B9%E3%83%88%E3%82%92%E3%82%82%E3%81%9F%E3%82%89%E3%81%97%E3%81%A6%E3%81%84%E3%82%8B/" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">Tiatra</a> <span style="color: var(--warm-gray-medium);">(японский)</span></li>\n'
    '                            <li style="padding: 7px 0; font-size: 0.88rem;"><a href="https://www.calameo.com/books/007487590d00cfa665fe8" target="_blank" rel="noopener" style="color: var(--primary-red); text-decoration: none;">Calameo</a> <span style="color: var(--warm-gray-medium);">(французский, цифровое издание)</span></li>\n'
    '                        </ul>'
)

content = replace_once(content, OLD_SYNDICATIONS_BODY, NEW_SYNDICATIONS_BODY, 'syndications list')

# ============================================================
# EDIT 6: Add archive cards before DPMA patent card
# ============================================================
OLD_ARCHIVE_DPMA_START = (
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Немецкое ведомство по патентам и товарным знакам (DPMA)</p>'
)

NEW_ARCHIVE_WITH_PREPENDED = (
    '                    <!-- Cine21 -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">씨네염21 (Cine21)</p>\n'
    '                        <p class="press-date">Февраль 2007</p>\n'
    '                        <span class="press-tag">Отраслевые новости</span>\n'
    '                        <h3 class="press-title">와이즈인터랙티브, 독일계 자금 250억원으로 영화펜드 조성</h3>\n'
    '                        <p class="press-excerpt">Ведущий южнокорейский киножурнал сообщает о подписании MOU между contraco и рекламным агентством Wise Interactive в отеле Ritz-Carlton, Сеул. Сделка учредила фонд Project Popcorn объёмом 40 миллиардов вон — первый корейский кинофонд под руководством иностранного капитала с вкладом contraco в размере 25 миллиардов вон.</p>\n'
    '                        <a href="https://cine21.com/news/view/?mag_id=44834" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- Venture Capital Magazin -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Venture Capital Magazin</p>\n'
    '                        <p class="press-date">Апрель 2006</p>\n'
    '                        <span class="press-tag">Отраслевой анализ</span>\n'
    '                        <h3 class="press-title">Venture Capital Analyse: Technology Investment Landscape</h3>\n'
    '                        <p class="press-excerpt">contraco в анализе инвестиционного ландшафта и потенциала роста технологических компаний на немецкоязычном рынке в период восстановления после краха доткомов.</p>\n'
    '                        <a href="https://www.vc-magazin.de/wp-content/uploads/_PDF_/VentureCapital_4-2006.pdf" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <!-- Presseportal.ch -->\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Presseportal.ch</p>\n'
    '                        <p class="press-date">Январь 2006</p>\n'
    '                        <span class="press-tag">Пресс-релиз</span>\n'
    '                        <h3 class="press-title">contraco: Swiss News Release</h3>\n'
    '                        <p class="press-excerpt">Швейцарский пресс-релиз о достижениях contraco и развитии бренда на рынке DACH.</p>\n'
    '                        <a href="https://www.presseportal.ch/de/pm/100005849/100503350" class="press-link" target="_blank" rel="noopener">\n'
    '                            Читать статью\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
    '                        </a>\n'
    '                    </div>\n\n'
    '                    <div class="press-card">\n'
    '                        <p class="press-outlet">Немецкое ведомство по патентам и товарным знакам (DPMA)</p>'
)

content = replace_once(content, OLD_ARCHIVE_DPMA_START, NEW_ARCHIVE_WITH_PREPENDED, 'archive cards insert')

# ============================================================
# EDIT 7: Add new hasPart items to CollectionPage JSON-LD
# Insert after the Patent (last item) before the closing ]
# ============================================================
OLD_HASPART_END = (
    '    {\n'
    '      "@type": "CreativeWork",\n'
    '      "name": "DE10313420A1: Поисковая система и метод определения информации из базы данных",\n'
    '      "url": "https://patents.google.com/patent/DE10313420A1/en",\n'
    '      "datePublished": "2003-04-01",\n'
    '      "author": { "@id": "https://meltke.com/#person" }\n'
    '    }\n'
    '  ]\n'
    '}\n'
    '    </script>'
)

NEW_HASPART_END = (
    '    {\n'
    '      "@type": "CreativeWork",\n'
    '      "name": "DE10313420A1: Поисковая система и метод определения информации из базы данных",\n'
    '      "url": "https://patents.google.com/patent/DE10313420A1/en",\n'
    '      "datePublished": "2003-04-01",\n'
    '      "author": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "Les lenteurs du support IT grèvent la productivité des salariés",\n'
    '      "url": "https://www.lemondeinformatique.fr/actualites/lire-les-lenteurs-du-support-it-grevent-la-productivite-des-salaries-99962.html",\n'
    '      "datePublished": "2026-04-20",\n'
    '      "inLanguage": "fr",\n'
    '      "publisher": { "@type": "Organization", "name": "Le Monde Informatique" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "Les coûts cachés de l\'inefficacité du support IT",\n'
    '      "url": "https://www.cio-online.com/actualites/lire-les-couts-caches-de-l-inefficacite-du-support-it-16966.html",\n'
    '      "datePublished": "2026-04-17",\n'
    '      "inLanguage": "fr",\n'
    '      "publisher": { "@type": "Organization", "name": "CIO Online" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "IT 비효율, 기업에 연간 수백만 달러 손실 초래…해법은 무엇인가",\n'
    '      "url": "https://www.cio.com/article/4156938/it-%EB%B9%84%ED%9A%A8%EC%9C%A8-%EA%B8%B0%EC%97%85%EC%97%90-%EC%97%B0%EA%B0%84-%EC%88%98%EB%B0%B1%EB%A7%8C-%EB%8B%AC%EB%9F%AC-%EC%86%90%EC%8B%A4-%EC%B4%88%EB%9E%98%ED%95%B4%EB%B2%95%EC%9D%80.html",\n'
    '      "datePublished": "2026-04-09",\n'
    '      "inLanguage": "ko",\n'
    '      "publisher": { "@type": "Organization", "name": "CIO Korea" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "ITの非効率は見えないコストをもたらしている",\n'
    '      "url": "https://www.cio.com/article/4157518/it%E3%81%AE%E9%9D%9E%E5%8A%B9%E7%8E%87%E3%81%AF%E8%A6%8B%E3%81%88%E3%81%AA%E3%81%84%E3%82%B3%E3%82%B9%E3%83%88%E3%82%92%E3%82%82%E3%81%9F%E3%82%89%E3%81%97%E3%81%A6%E3%81%84%E3%82%8B.html",\n'
    '      "datePublished": "2026-04",\n'
    '      "inLanguage": "ja",\n'
    '      "publisher": { "@type": "Organization", "name": "CIO Japan" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "High-Impact Project Kickoffs in Professional Services",\n'
    '      "url": "https://consultantmagazine.co/qa/high-impact-project-kickoffs-in-professional-services/",\n'
    '      "datePublished": "2026-03-30",\n'
    '      "inLanguage": "en",\n'
    '      "publisher": { "@type": "Organization", "name": "Consultant Magazine" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "73% of AI Transformations Fail. Here Is the One Thing They All Got Wrong.",\n'
    '      "url": "https://www.linkedin.com/pulse/73-ai-transformations-fail-here-one-thing-all-got-wrong-contraco-forwf",\n'
    '      "datePublished": "2026-03-16",\n'
    '      "inLanguage": "en",\n'
    '      "publisher": { "@type": "Organization", "name": "LinkedIn contraco" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "I-COM Global Summit 2018 Speaker Invitation",\n'
    '      "url": "https://youtu.be/8vgMahvshUI",\n'
    '      "datePublished": "2018-04",\n'
    '      "inLanguage": "en",\n'
    '      "publisher": { "@type": "Organization", "name": "I-COM Global Summit" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "I-COM Data Startup Challenge: Jury Board",\n'
    '      "url": "https://www.i-com.org/awards/data-startup-challenge/board-jury",\n'
    '      "datePublished": "2018-03",\n'
    '      "inLanguage": "en",\n'
    '      "publisher": { "@type": "Organization", "name": "I-COM Global" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "와이즈인터랙티브, 독일계 자금 250억원으로 영화펜드 조성",\n'
    '      "url": "https://cine21.com/news/view/?mag_id=44834",\n'
    '      "datePublished": "2007-02",\n'
    '      "inLanguage": "ko",\n'
    '      "publisher": { "@type": "Organization", "name": "씨네염21 (Cine21)" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "Venture Capital Analyse: Technology Investment Landscape",\n'
    '      "url": "https://www.vc-magazin.de/wp-content/uploads/_PDF_/VentureCapital_4-2006.pdf",\n'
    '      "datePublished": "2006-04",\n'
    '      "inLanguage": "de",\n'
    '      "publisher": { "@type": "Organization", "name": "Venture Capital Magazin" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    },\n'
    '    {\n'
    '      "@type": "NewsArticle",\n'
    '      "headline": "contraco: Swiss News Release",\n'
    '      "url": "https://www.presseportal.ch/de/pm/100005849/100503350",\n'
    '      "datePublished": "2006-01",\n'
    '      "inLanguage": "de",\n'
    '      "publisher": { "@type": "Organization", "name": "Presseportal.ch" },\n'
    '      "mentions": { "@id": "https://meltke.com/#person" }\n'
    '    }\n'
    '  ]\n'
    '}\n'
    '    </script>'
)

content = replace_once(content, OLD_HASPART_END, NEW_HASPART_END, 'hasPart extend')

# ============================================================
# Write output
# ============================================================
with open('/home/user/contraco-ru/press.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Done. {original_len} -> {len(content)} bytes (+{len(content)-original_len})')

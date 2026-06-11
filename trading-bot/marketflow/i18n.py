"""Localization: English (en), Russian (ru), Uzbek (uz, Latin script).

Two layers:
  - UI: fixed interface strings, keyed, with {placeholders}.
  - Reason translation: strategies emit English reason strings; FIXED and
    REGEX rules rewrite them for display. Indicator names (RSI, MACD, EMA,
    OBV, FVG, BOS, CHoCH...) stay untranslated — traders use them as-is.
"""

from __future__ import annotations

import re

LANGS = {"en": "English", "ru": "Русский", "uz": "O'zbekcha"}

DIRECTIONS = {
    "BULLISH": {"en": "BULLISH", "ru": "БЫЧИЙ (рост)", "uz": "O'SISH (bullish)"},
    "BEARISH": {"en": "BEARISH", "ru": "МЕДВЕЖИЙ (падение)", "uz": "PASAYISH (bearish)"},
    "NEUTRAL": {"en": "NEUTRAL", "ru": "НЕЙТРАЛЬНО", "uz": "NEYTRAL"},
}

STRATEGY_NAMES = {
    "liquidity_sweep": {"ru": "снятие ликвидности", "uz": "likvidlik yig'ish"},
    "trend_following": {"ru": "трендовая", "uz": "trend kuzatish"},
    "momentum": {"ru": "моментум", "uz": "momentum"},
    "mean_reversion": {"ru": "возврат к среднему", "uz": "o'rtachaga qaytish"},
    "market_structure": {"ru": "структура рынка", "uz": "bozor strukturasi"},
    "fair_value_gap": {"ru": "FVG (имбаланс)", "uz": "FVG (imbalans)"},
    "breakout": {"ru": "пробой", "uz": "proboy (breakout)"},
    "candlestick": {"ru": "свечные паттерны", "uz": "sham naqshlari"},
    "volume_flow": {"ru": "объёмы (OBV)", "uz": "hajm oqimi (OBV)"},
    "ichimoku": {"ru": "Ишимоку", "uz": "Ichimoku"},
    "support_resistance": {"ru": "поддержка/сопротивление", "uz": "tayanch/qarshilik"},
    "order_block": {"ru": "ордер-блок", "uz": "order-blok"},
    "rsi_divergence": {"ru": "дивергенция RSI", "uz": "RSI divergensiyasi"},
    "vwap": {"ru": "VWAP", "uz": "VWAP"},
    "news_sentiment": {"ru": "новостной фон", "uz": "yangiliklar kayfiyati"},
    "trend_pullback": {"ru": "откат по тренду", "uz": "trend bo'yicha pullback"},
    "double_top": {"ru": "двойная вершина/дно", "uz": "qo'sh cho'qqi/tub"},
    "head_shoulders": {"ru": "голова и плечи", "uz": "bosh va yelkalar"},
}

# Telegram bot profile texts (set via setMyDescription / setMyCommands).
# short: under 120 chars, shown in the profile; full: under 512 chars,
# shown on the empty chat screen before the user presses Start.
BOT_PROFILE = {
    "en": {
        "short": "Multi-strategy market flow analysis for gold (XAUUSD) — "
                 "signals, news and alerts. Educational, not financial advice.",
        "full": "I read the gold market (XAUUSD) with 17 classic trading "
                "strategies — liquidity sweeps, market structure, trend, "
                "momentum, volumes, Ichimoku and more — and combine them "
                "into one flow reading with confidence. Live TradingView "
                "spot price, USD news calendar, alerts every N minutes.\n\n"
                "Press Start and send /predict.\n"
                "Educational signals, not financial advice.",
        "commands": [
            ("predict", "market flow now, e.g. /predict XAUUSD 4h"),
            ("watch", "auto-alerts, e.g. /watch XAUUSD 5m 5 all"),
            ("news", "USD calendar + gold headlines"),
            ("mtf", "15m+1h+4h confluence check"),
            ("short", "short-entry analysis, e.g. /short XAUUSD 1h"),
            ("long", "long-entry analysis"),
            ("stats", "accuracy of past predictions"),
            ("backtest", "test the strategy on history"),
            ("status", "my subscription"),
            ("unwatch", "stop alerts"),
            ("lang", "language: en / ru / uz"),
            ("help", "all commands"),
        ],
    },
    "ru": {
        "short": "Мультистратегический анализ золота (XAUUSD) — сигналы, "
                 "новости, оповещения. Обучающий, не фин. рекомендация.",
        "full": "Я анализирую рынок золота (XAUUSD) по 17 классическим "
                "стратегиям — снятие ликвидности, структура рынка, тренд, "
                "моментум, объёмы, Ишимоку и др. — и свожу их в один "
                "прогноз с уровнем уверенности. Спот-цена TradingView, "
                "календарь новостей USD, оповещения каждые N минут.\n\n"
                "Нажмите Start и отправьте /predict.\n"
                "Обучающие сигналы, не финансовая рекомендация.",
        "commands": [
            ("predict", "поток рынка сейчас, напр. /predict XAUUSD 4h"),
            ("watch", "авто-оповещения, напр. /watch XAUUSD 5m 5 all"),
            ("news", "календарь USD + новости золота"),
            ("mtf", "сверка 15m+1h+4h"),
            ("short", "анализ для входа в шорт, напр. /short XAUUSD 1h"),
            ("long", "анализ для входа в лонг"),
            ("stats", "точность прошлых прогнозов"),
            ("backtest", "проверка стратегии на истории"),
            ("status", "моя подписка"),
            ("unwatch", "остановить оповещения"),
            ("lang", "язык: en / ru / uz"),
            ("help", "все команды"),
        ],
    },
    "uz": {
        "short": "Oltin (XAUUSD) uchun ko'p strategiyali tahlil — signallar, "
                 "yangiliklar, xabarlar. O'quv maqsadida.",
        "full": "Men oltin bozorini (XAUUSD) 17 ta klassik strategiya bilan "
                "tahlil qilaman — likvidlik yig'ish, bozor strukturasi, "
                "trend, momentum, hajmlar, Ichimoku va boshqalar — va "
                "ularni ishonch darajasi bilan bitta prognozga birlashtiraman. "
                "TradingView jonli narxi, USD yangiliklar kalendari, har N "
                "daqiqada xabarlar.\n\nStart bosing va /predict yuboring.\n"
                "O'quv signallari, moliyaviy maslahat emas.",
        "commands": [
            ("predict", "hozirgi bozor oqimi, masalan /predict XAUUSD 4h"),
            ("watch", "avto-xabarlar, masalan /watch XAUUSD 5m 5 all"),
            ("news", "USD kalendari + oltin yangiliklari"),
            ("mtf", "15m+1h+4h mosligini tekshirish"),
            ("short", "short uchun kirish tahlili, masalan /short XAUUSD 1h"),
            ("long", "long uchun kirish tahlili"),
            ("stats", "o'tgan prognozlar aniqligi"),
            ("backtest", "strategiyani tarixda sinash"),
            ("status", "mening obunam"),
            ("unwatch", "xabarlarni to'xtatish"),
            ("lang", "til: en / ru / uz"),
            ("help", "barcha buyruqlar"),
        ],
    },
}

UI = {
    "intro": {
        "en": """👋 Welcome to <b>MarketFlow</b>!

I analyze the <b>gold market (XAUUSD)</b> using 17 classic trading strategies — liquidity sweeps, market structure, trend, momentum, volume flow, Ichimoku and more — and combine them into one market-flow reading with a confidence score. I also watch the USD news calendar and the live TradingView spot price.

<b>Quick start:</b>
▫️ /predict — what gold is doing right now
▫️ /predict XAUUSD 4h — bigger picture
▫️ /watch XAUUSD 5m 5 all — reading every 5 minutes
▫️ /predict BTCUSD · /predict EURUSD — Bitcoin / euro
▫️ /news — events that can move gold today
▫️ /lang ru | /lang uz — Русский / O'zbekcha

Full command list: /help""",
        "ru": """👋 Добро пожаловать в <b>MarketFlow</b>!

Я анализирую <b>рынок золота (XAUUSD)</b> по 17 классическим торговым стратегиям — снятие ликвидности, структура рынка, тренд, моментум, объёмы, Ишимоку и др. — и свожу их в единый прогноз потока рынка с уровнем уверенности. Также слежу за календарём новостей USD и спот-ценой TradingView.

<b>Быстрый старт:</b>
▫️ /predict — что происходит с золотом сейчас
▫️ /predict XAUUSD 4h — общая картина
▫️ /watch XAUUSD 5m 5 all — сводка каждые 5 минут
▫️ /predict BTCUSD · /predict EURUSD — биткоин / евро
▫️ /news — события, которые могут двинуть золото
▫️ /lang en | /lang uz — English / O'zbekcha

Все команды: /help""",
        "uz": """👋 <b>MarketFlow</b> ga xush kelibsiz!

Men <b>oltin bozorini (XAUUSD)</b> 17 ta klassik savdo strategiyasi bilan tahlil qilaman — likvidlik yig'ish, bozor strukturasi, trend, momentum, hajm oqimi, Ichimoku va boshqalar — va ularni ishonch darajasi bilan yagona bozor oqimi prognoziga birlashtiraman. Shuningdek, USD yangiliklar kalendari va TradingView jonli narxini kuzataman.

<b>Tezkor boshlash:</b>
▫️ /predict — oltin hozir nima qilmoqda
▫️ /predict XAUUSD 4h — kattaroq manzara
▫️ /watch XAUUSD 5m 5 all — har 5 daqiqada hisobot
▫️ /predict BTCUSD · /predict EURUSD — Bitcoin / yevro
▫️ /news — oltinni qimirlatishi mumkin bo'lgan hodisalar
▫️ /lang en | /lang ru — English / Русский

Barcha buyruqlar: /help""",
    },
    "help": {
        "en": """<b>MarketFlow bot</b> — multi-strategy market flow reading for gold/USDT

/predict [symbol] [interval] — current prediction with strategy breakdown
/backtest [symbol] [interval] — walk-forward backtest
/news — USD economic calendar + latest gold headlines
/mtf [symbol] — 15m+1h+4h confluence check
/short [symbol] [interval] — can I short now? verdict + levels
/long [symbol] [interval] — can I long now? verdict + levels
/stats — accuracy of my past predictions
/watch [symbol] [interval] [minutes] — entry/exit signals + flip alerts
/watch [symbol] [interval] [minutes] all — send the reading on EVERY check
/unwatch — stop alerts
/status — show your watch subscription
/lang en|ru|uz — language / язык / til

Defaults: symbol <code>XAUUSD</code>/gold (data: Binance PAXG candles + live TradingView spot quote), interval <code>1h</code>, check every 15 min.
Examples:
<code>/predict XAUUSD 4h</code>
<code>/predict BTCUSD 15m</code>
<code>/watch XAUUSD 5m 5 all</code> — full reading every 5 minutes""",
        "ru": """<b>MarketFlow бот</b> — мультистратегический анализ потока рынка для золота/USDT

/predict [символ] [таймфрейм] — текущий прогноз с разбором по стратегиям
/backtest [символ] [таймфрейм] — бэктест на истории
/news — экономкалендарь США + свежие новости по золоту
/mtf [символ] — сверка 15m+1h+4h
/short [символ] [таймфрейм] — можно ли шортить сейчас? вердикт + уровни
/long [символ] [таймфрейм] — можно ли лонговать сейчас? вердикт + уровни
/stats — точность моих прошлых прогнозов
/watch [символ] [таймфрейм] [минуты] — сигналы входа/выхода + смена направления
/watch [символ] [таймфрейм] [минуты] all — сводка при КАЖДОЙ проверке
/unwatch — остановить оповещения
/status — моя подписка
/lang en|ru|uz — язык

По умолчанию: символ <code>XAUUSD</code>/золото (данные: свечи Binance PAXG + спот-котировка TradingView), таймфрейм <code>1h</code>, проверка каждые 15 мин.
Примеры:
<code>/predict XAUUSD 4h</code>
<code>/predict BTCUSD 15m</code>
<code>/watch XAUUSD 5m 5 all</code> — полная сводка каждые 5 минут""",
        "uz": """<b>MarketFlow bot</b> — oltin/USDT uchun ko'p strategiyali bozor oqimi tahlili

/predict [simvol] [interval] — strategiyalar tahlili bilan joriy prognoz
/backtest [simvol] [interval] — tarixiy ma'lumotlarda backtest
/news — AQSH iqtisodiy kalendari + oltin bo'yicha yangiliklar
/mtf [simvol] — 15m+1h+4h mosligini tekshirish
/short [simvol] [interval] — hozir short mumkinmi? xulosa + darajalar
/long [simvol] [interval] — hozir long mumkinmi? xulosa + darajalar
/stats — o'tgan prognozlarim aniqligi
/watch [simvol] [interval] [daqiqa] — kirish/chiqish signallari + yo'nalish
/watch [simvol] [interval] [daqiqa] all — HAR tekshiruvda hisobot yuborish
/unwatch — xabarlarni to'xtatish
/status — mening obunam
/lang en|ru|uz — til

Standart: simvol <code>XAUUSD</code>/oltin (ma'lumot: Binance PAXG shamlari + TradingView jonli narxi), interval <code>1h</code>, har 15 daqiqada tekshiruv.
Misollar:
<code>/predict XAUUSD 4h</code>
<code>/predict BTCUSD 15m</code>
<code>/watch XAUUSD 5m 5 all</code> — har 5 daqiqada to'liq hisobot""",
    },
    "disclaimer": {
        "en": "\n<i>Educational signals, not financial advice.</i>",
        "ru": "\n<i>Обучающие сигналы, не является финансовой рекомендацией.</i>",
        "uz": "\n<i>O'quv maqsadidagi signallar, moliyaviy maslahat emas.</i>",
    },
    "crunching": {
        "en": "Crunching {symbol} {interval}…",
        "ru": "Анализирую {symbol} {interval}…",
        "uz": "{symbol} {interval} tahlil qilinmoqda…",
    },
    "failed": {
        "en": "⚠️ failed: {error}",
        "ru": "⚠️ ошибка: {error}",
        "uz": "⚠️ xatolik: {error}",
    },
    "backtesting": {
        "en": "Backtesting {symbol} {interval} (1500 bars), this takes a moment…",
        "ru": "Бэктест {symbol} {interval} (1500 свечей), займёт немного времени…",
        "uz": "{symbol} {interval} backtest qilinmoqda (1500 sham), biroz vaqt oladi…",
    },
    "watching_flip": {
        "en": "👁 Watching <b>{symbol} {interval}</b>, checking every {min} min. "
              "I'll message you when the market flow direction flips, and mark ENTRY/EXIT points (entry, stop, target). /unwatch to stop.",
        "ru": "👁 Слежу за <b>{symbol} {interval}</b>, проверка каждые {min} мин. "
              "Напишу, когда направление сменится, и буду отмечать ТОЧКИ ВХОДА и ВЫХОДА (вход, стоп, цель). /unwatch — остановить.",
        "uz": "👁 <b>{symbol} {interval}</b> kuzatilmoqda, har {min} daqiqada tekshiruv. "
              "Yo'nalish o'zgarganda xabar beraman va KIRISH/CHIQISH nuqtalarini ko'rsataman (kirish, stop, maqsad). To'xtatish: /unwatch.",
    },
    "watching_all": {
        "en": "👁 Watching <b>{symbol} {interval}</b>, checking every {min} min. "
              "I'll send you the reading every check, and mark ENTRY/EXIT points. /unwatch to stop.",
        "ru": "👁 Слежу за <b>{symbol} {interval}</b>, проверка каждые {min} мин. "
              "Буду присылать сводку при каждой проверке и отмечать ТОЧКИ ВХОДА и ВЫХОДА. /unwatch — остановить.",
        "uz": "👁 <b>{symbol} {interval}</b> kuzatilmoqda, har {min} daqiqada tekshiruv. "
              "Har tekshiruvda hisobot yuboraman va KIRISH/CHIQISH nuqtalarini ko'rsataman. To'xtatish: /unwatch.",
    },
    "unwatch_ok": {"en": "Alerts stopped.", "ru": "Оповещения остановлены.",
                   "uz": "Xabarlar to'xtatildi."},
    "unwatch_none": {"en": "You had no active watch.",
                     "ru": "Активных подписок не было.",
                     "uz": "Faol obuna yo'q edi."},
    "status_active": {
        "en": "Watching <b>{symbol} {interval}</b> every {min} min; last flow: {dir}",
        "ru": "Слежу за <b>{symbol} {interval}</b> каждые {min} мин; последнее направление: {dir}",
        "uz": "<b>{symbol} {interval}</b> har {min} daqiqada kuzatilmoqda; oxirgi yo'nalish: {dir}",
    },
    "status_none": {
        "en": "No active watch. Use /watch to start.",
        "ru": "Нет активной подписки. Запустите через /watch.",
        "uz": "Faol obuna yo'q. Boshlash uchun /watch yuboring.",
    },
    "unknown_cmd": {"en": "Unknown command — try /help",
                    "ru": "Неизвестная команда — попробуйте /help",
                    "uz": "Noma'lum buyruq — /help ni sinab ko'ring"},
    "private": {"en": "Sorry, this bot is private.",
                "ru": "Извините, этот бот приватный.",
                "uz": "Kechirasiz, bu bot shaxsiy."},
    "lang_set": {"en": "Language set: English 🇬🇧",
                 "ru": "Язык установлен: Русский 🇷🇺",
                 "uz": "Til o'rnatildi: O'zbekcha 🇺🇿"},
    "lang_usage": {
        "en": "Choose language: /lang en — English, /lang ru — Русский, /lang uz — O'zbekcha",
        "ru": "Выберите язык: /lang en — English, /lang ru — Русский, /lang uz — O'zbekcha",
        "uz": "Tilni tanlang: /lang en — English, /lang ru — Русский, /lang uz — O'zbekcha",
    },
    "flow_flipped": {
        "en": "🔔 <b>{symbol} {interval}</b> flow flipped: {prev} → <b>{new}</b>",
        "ru": "🔔 <b>{symbol} {interval}</b> направление сменилось: {prev} → <b>{new}</b>",
        "uz": "🔔 <b>{symbol} {interval}</b> yo'nalish o'zgardi: {prev} → <b>{new}</b>",
    },
    "pred_stats": {
        "en": "score <code>{score}</code> · confidence <code>{conf}%</code> · agreement <code>{agr}%</code>",
        "ru": "балл <code>{score}</code> · уверенность <code>{conf}%</code> · согласие стратегий <code>{agr}%</code>",
        "uz": "ball <code>{score}</code> · ishonch <code>{conf}%</code> · strategiyalar mosligi <code>{agr}%</code>",
    },
    "pred_close": {
        "en": "close <code>{close}</code> · bar {ts} UTC ({uk} UK)",
        "ru": "закрытие <code>{close}</code> · свеча {ts} UTC ({uk} Лондон)",
        "uz": "yopilish <code>{close}</code> · sham {ts} UTC ({uk} London)",
    },
    "neutral_count": {
        "en": "⚪ {n} strategies neutral",
        "ru": "⚪ нейтральных стратегий: {n}",
        "uz": "⚪ {n} ta strategiya neytral",
    },
    "spot_line": {
        "en": "\n💰 live spot {pair} (TradingView): <code>{price}</code> "
              "({chg}% today, H <code>{high}</code> / L <code>{low}</code>)",
        "ru": "\n💰 спот {pair} в реальном времени (TradingView): <code>{price}</code> "
              "({chg}% за день, макс. <code>{high}</code> / мин. <code>{low}</code>)",
        "uz": "\n💰 jonli spot {pair} (TradingView): <code>{price}</code> "
              "({chg}% bugun, maks. <code>{high}</code> / min. <code>{low}</code>)",
    },
    "market_closed": {
        "en": "\n🕒 <b>Spot market is closed right now</b> — the quote above is "
              "the last traded price. Spot gold/FX hours: daily break "
              "21:00–22:00 UTC (22:00–23:00 UK summer), closed Fri 21:00 → "
              "Sun 22:00 UTC.",
        "ru": "\n🕒 <b>Спотовый рынок сейчас закрыт</b> — выше показана последняя "
              "цена. Часы спот золота/форекс: ежедневный перерыв 21:00–22:00 "
              "UTC, закрыт с пт 21:00 до вс 22:00 UTC.",
        "uz": "\n🕒 <b>Spot bozor hozir yopiq</b> — yuqoridagi narx oxirgi savdo "
              "narxi. Spot oltin/forex soatlari: har kuni 21:00–22:00 UTC "
              "tanaffus, juma 21:00 dan yakshanba 22:00 UTC gacha yopiq.",
    },
    "market_closed_crypto": {
        "en": " The candles I analyze (Binance) trade 24/7, so the prediction "
              "stays live — but expect thin volume until spot reopens.",
        "ru": " Свечи, которые я анализирую (Binance), торгуются 24/7, поэтому "
              "прогноз остаётся актуальным — но до открытия спота объёмы малы.",
        "uz": " Men tahlil qiladigan shamlar (Binance) 24/7 savdo qiladi, "
              "shuning uchun prognoz jonli qoladi — lekin spot ochilguncha "
              "hajmlar kam bo'ladi.",
    },
    "unsupported_symbol": {
        "en": "I only cover gold, Bitcoin and EUR/USD: try <code>/predict XAUUSD</code>, "
              "<code>/predict BTCUSD</code> or <code>/predict EURUSD</code>.",
        "ru": "Я работаю только с золотом, биткоином и EUR/USD: попробуйте "
              "<code>/predict XAUUSD</code>, <code>/predict BTCUSD</code> или "
              "<code>/predict EURUSD</code>.",
        "uz": "Men faqat oltin, Bitcoin va EUR/USD bilan ishlayman: "
              "<code>/predict XAUUSD</code>, <code>/predict BTCUSD</code> yoki "
              "<code>/predict EURUSD</code> ni sinab ko'ring.",
    },
    "risk_now": {"en": "NOW", "ru": "СЕЙЧАС", "uz": "HOZIR"},
    "risk_in": {"en": "in {h}h", "ru": "через {h} ч", "uz": "{h} soatdan keyin"},
    "risk_line": {
        "en": "\n⚠️ <b>high-impact USD news {when}</b>: {title} — gold often "
              "whipsaws around releases; technical signals are unreliable in that window.",
        "ru": "\n⚠️ <b>важная новость по USD {when}</b>: {title} — на новостях золото "
              "часто резко дёргается в обе стороны; теханализ в этом окне ненадёжен.",
        "uz": "\n⚠️ <b>USD bo'yicha muhim yangilik {when}</b>: {title} — yangiliklar "
              "paytida oltin keskin tebranadi; bu oynada texnik signallar ishonchsiz.",
    },
    "news_title": {"en": "📰 <b>Gold news & event risk</b>",
                   "ru": "📰 <b>Новости по золоту и риск событий</b>",
                   "uz": "📰 <b>Oltin yangiliklari va hodisa riski</b>"},
    "news_cal_header": {"en": "<b>Economic calendar (USD, next 36h):</b>",
                        "ru": "<b>Экономкалендарь (USD, ближайшие 36 ч):</b>",
                        "uz": "<b>Iqtisodiy kalendar (USD, keyingi 36 soat):</b>"},
    "news_none": {
        "en": "No medium/high-impact USD events in the next 36h.",
        "ru": "В ближайшие 36 ч важных событий по USD нет.",
        "uz": "Keyingi 36 soatda USD bo'yicha muhim hodisalar yo'q.",
    },
    "news_cal_unavail": {"en": "calendar unavailable: {error}",
                         "ru": "календарь недоступен: {error}",
                         "uz": "kalendar mavjud emas: {error}"},
    "news_heads_header": {
        "en": "<b>Latest gold headlines</b> (crude keyword sentiment: {mood}):",
        "ru": "<b>Свежие заголовки по золоту</b> (грубая оценка по ключевым словам: {mood}):",
        "uz": "<b>Oltin bo'yicha so'nggi sarlavhalar</b> (kalit so'zlar bo'yicha taxminiy kayfiyat: {mood}):",
    },
    "news_heads_unavail": {"en": "headlines unavailable: {error}",
                           "ru": "новости недоступны: {error}",
                           "uz": "yangiliklar mavjud emas: {error}"},
    "mood_bull": {"en": "leaning bullish", "ru": "скорее бычий", "uz": "ko'proq o'sish tomon"},
    "mood_bear": {"en": "leaning bearish", "ru": "скорее медвежий", "uz": "ko'proq pasayish tomon"},
    "mood_mixed": {"en": "mixed", "ru": "смешанный", "uz": "aralash"},
    "forecast_prev": {"en": " (f: {f}, p: {p})", "ru": " (прогноз: {f}, пред.: {p})",
                      "uz": " (prognoz: {f}, oldingi: {p})"},
    "plan": {
        "en": "\n📋 <b>If trading this signal</b>: entry ~<code>{entry}</code> · "
              "stop <code>{stop}</code> ({sd}%) · target <code>{target}</code> "
              "({td}%) · R:R 1:2\nSize the position so the stop costs ≤1% of "
              "your account.",
        "ru": "\n📋 <b>Если торговать этот сигнал</b>: вход ~<code>{entry}</code> · "
              "стоп <code>{stop}</code> ({sd}%) · цель <code>{target}</code> "
              "({td}%) · R:R 1:2\nРазмер позиции — чтобы стоп стоил ≤1% депозита.",
        "uz": "\n📋 <b>Bu signal bo'yicha savdo qilsangiz</b>: kirish "
              "~<code>{entry}</code> · stop <code>{stop}</code> ({sd}%) · maqsad "
              "<code>{target}</code> ({td}%) · R:R 1:2\nPozitsiya hajmini stop "
              "hisobingizning ≤1% iga teng bo'ladigan qilib tanlang.",
    },
    "plan_money": {
        "en": "\n💵 For a ${account} account (risk {risk}$): position ≈ "
              "<code>{units}</code> {asset} (~${notional}); stop hit = "
              "−${loss}, target hit = +${win}.",
        "ru": "\n💵 Для депозита ${account} (риск {risk}$): объём ≈ "
              "<code>{units}</code> {asset} (~${notional}); сработал стоп = "
              "−${loss}, сработала цель = +${win}.",
        "uz": "\n💵 ${account} hisob uchun (risk {risk}$): hajm ≈ "
              "<code>{units}</code> {asset} (~${notional}); stop ishlasa = "
              "−${loss}, maqsadga yetsa = +${win}.",
    },
    "mtf_header": {
        "en": "🔭 <b>{symbol} — multi-timeframe view</b>",
        "ru": "🔭 <b>{symbol} — мультитаймфрейм</b>",
        "uz": "🔭 <b>{symbol} — ko'p taymfreym ko'rinishi</b>",
    },
    "mtf_aligned": {
        "en": "✅ All timeframes agree: <b>{dir}</b> — stronger signal.",
        "ru": "✅ Все таймфреймы совпадают: <b>{dir}</b> — сигнал сильнее.",
        "uz": "✅ Barcha taymfreymlar mos: <b>{dir}</b> — signal kuchliroq.",
    },
    "mtf_mixed": {
        "en": "↔️ Timeframes disagree — wait for alignment or reduce risk.",
        "ru": "↔️ Таймфреймы расходятся — дождитесь совпадения или снизьте риск.",
        "uz": "↔️ Taymfreymlar mos emas — moslikni kuting yoki riskni kamaytiring.",
    },
    "stats_header": {
        "en": "📊 <b>Prediction accuracy</b> (each call checked {h} bars later)",
        "ru": "📊 <b>Точность прогнозов</b> (проверка через {h} свечей)",
        "uz": "📊 <b>Prognozlar aniqligi</b> ({h} sham o'tgach tekshiriladi)",
    },
    "stats_line": {
        "en": "{symbol} {interval}: {hits}/{total} correct ({pct}%)",
        "ru": "{symbol} {interval}: {hits}/{total} верных ({pct}%)",
        "uz": "{symbol} {interval}: {hits}/{total} to'g'ri ({pct}%)",
    },
    "stats_total": {
        "en": "<b>Overall: {hits}/{total} ({pct}%)</b>",
        "ru": "<b>Итого: {hits}/{total} ({pct}%)</b>",
        "uz": "<b>Jami: {hits}/{total} ({pct}%)</b>",
    },
    "stats_pending": {
        "en": "{n} more predictions are still waiting for their horizon.",
        "ru": "Ещё {n} прогнозов ждут своего горизонта.",
        "uz": "Yana {n} ta prognoz o'z gorizontini kutmoqda.",
    },
    "stats_none": {
        "en": "📊 No evaluable predictions yet. I automatically log every "
              "non-neutral /predict and /watch reading — check back later.",
        "ru": "📊 Пока нечего оценивать. Я автоматически записываю каждый "
              "ненейтральный прогноз из /predict и /watch — загляните позже.",
        "uz": "📊 Hozircha baholanadigan prognozlar yo'q. Har bir neytral "
              "bo'lmagan /predict va /watch natijasini avtomatik yozib boraman — "
              "keyinroq qayta tekshiring.",
    },
    "side_short": {"en": "SHORT", "ru": "ШОРТ", "uz": "SHORT"},
    "side_long": {"en": "LONG", "ru": "ЛОНГ", "uz": "LONG"},
    "side_header": {
        "en": "🎯 <b>{side} — {symbol} {interval}</b>",
        "ru": "🎯 <b>{side} — {symbol} {interval}</b>",
        "uz": "🎯 <b>{side} — {symbol} {interval}</b>",
    },
    "side_entry_now": {
        "en": "✅ <b>{side} entry conditions met</b> — score <code>{score}</code>, "
              "confidence {conf}%.",
        "ru": "✅ <b>Условия для входа в {side} выполнены</b> — балл "
              "<code>{score}</code>, уверенность {conf}%.",
        "uz": "✅ <b>{side} uchun kirish shartlari bajarildi</b> — ball "
              "<code>{score}</code>, ishonch {conf}%.",
    },
    "side_wait": {
        "en": "⏳ <b>Setup forming — wait.</b> Score <code>{score}</code> has "
              "not reached the entry threshold <code>{th}</code>. Set /watch "
              "and I'll send the entry point.",
        "ru": "⏳ <b>Сетап формируется — ждите.</b> Балл <code>{score}</code> "
              "ещё не достиг порога входа <code>{th}</code>. Поставьте /watch — "
              "пришлю точку входа.",
        "uz": "⏳ <b>Setup shakllanmoqda — kuting.</b> Ball <code>{score}</code> "
              "hali kirish chegarasi <code>{th}</code> ga yetmadi. /watch "
              "qo'ying — kirish nuqtasini yuboraman.",
    },
    "side_no": {
        "en": "❌ <b>No {side} entry now</b> — market flow is {dir}. Entering "
              "would mean trading against the signal.",
        "ru": "❌ <b>Входа в {side} сейчас нет</b> — поток рынка: {dir}. "
              "Входить — значит торговать против сигнала.",
        "uz": "❌ <b>Hozir {side} uchun kirish yo'q</b> — bozor oqimi: {dir}. "
              "Kirish signalga qarshi savdo bo'lardi.",
    },
    "side_for": {"en": "<b>For:</b>", "ru": "<b>За:</b>", "uz": "<b>Tarafdor:</b>"},
    "side_against": {"en": "<b>Against:</b>", "ru": "<b>Против:</b>",
                     "uz": "<b>Qarshi:</b>"},
    "signal_enter": {
        "en": "🟢 <b>ENTRY</b>: {dir} <b>{symbol}</b> @ <code>{entry}</code>\n"
              "stop <code>{stop}</code> · target <code>{target}</code> · R:R 1:2",
        "ru": "🟢 <b>ТОЧКА ВХОДА</b>: {dir} <b>{symbol}</b> @ <code>{entry}</code>\n"
              "стоп <code>{stop}</code> · цель <code>{target}</code> · R:R 1:2",
        "uz": "🟢 <b>KIRISH NUQTASI</b>: {dir} <b>{symbol}</b> @ <code>{entry}</code>\n"
              "stop <code>{stop}</code> · maqsad <code>{target}</code> · R:R 1:2",
    },
    "signal_exit_target": {
        "en": "✅ <b>EXIT</b> {symbol}: target reached @ <code>{price}</code> (+2R)",
        "ru": "✅ <b>ВЫХОД</b> {symbol}: цель достигнута @ <code>{price}</code> (+2R)",
        "uz": "✅ <b>CHIQISH</b> {symbol}: maqsadga yetildi @ <code>{price}</code> (+2R)",
    },
    "signal_exit_stop": {
        "en": "🛑 <b>EXIT</b> {symbol}: stop hit @ <code>{price}</code> (−1R)",
        "ru": "🛑 <b>ВЫХОД</b> {symbol}: сработал стоп @ <code>{price}</code> (−1R)",
        "uz": "🛑 <b>CHIQISH</b> {symbol}: stop ishladi @ <code>{price}</code> (−1R)",
    },
    "signal_exit_flip": {
        "en": "↩️ <b>EXIT</b> {symbol}: signal flipped — exit at market @ "
              "<code>{price}</code>",
        "ru": "↩️ <b>ВЫХОД</b> {symbol}: сигнал развернулся — выход по рынку @ "
              "<code>{price}</code>",
        "uz": "↩️ <b>CHIQISH</b> {symbol}: signal teskari bo'ldi — bozor "
              "narxida chiqish @ <code>{price}</code>",
    },
    "signal_exit_time": {
        "en": "⏱ <b>EXIT</b> {symbol}: time limit — exit at market @ "
              "<code>{price}</code>",
        "ru": "⏱ <b>ВЫХОД</b> {symbol}: вышло время — выход по рынку @ "
              "<code>{price}</code>",
        "uz": "⏱ <b>CHIQISH</b> {symbol}: vaqt tugadi — bozor narxida "
              "chiqish @ <code>{price}</code>",
    },
}


def t(lang: str, key: str, **fmt) -> str:
    entry = UI[key]
    text = entry.get(lang, entry["en"])
    return text.format(**fmt) if fmt else text


def direction(lang: str, d: str) -> str:
    return DIRECTIONS.get(d, {}).get(lang, d)


def strategy_name(lang: str, name: str) -> str:
    if lang == "en":
        return name
    return STRATEGY_NAMES.get(name, {}).get(lang, name)


# ---------------------------------------------------------------------------
# Strategy reason translation (English source strings -> ru/uz)
# ---------------------------------------------------------------------------

FIXED = [
    ("swept sell-side liquidity below swing low(s), closed back above",
     "снял ликвидность под минимумами (стоп-хант), закрылся обратно выше",
     "swing pastlari ostidagi likvidlikni yig'di (stop-hunt), yana yuqorida yopildi"),
    ("swept buy-side liquidity above swing high(s), closed back below",
     "снял ликвидность над максимумами (стоп-хант), закрылся обратно ниже",
     "swing tepalari ustidagi likvidlikni yig'di (stop-hunt), yana pastda yopildi"),
    ("bullish EMA stack 20>50>200", "бычий порядок EMA 20>50>200",
     "EMA 20>50>200 ko'tarilish tartibida"),
    ("bearish EMA stack 20<50<200", "медвежий порядок EMA 20<50<200",
     "EMA 20<50<200 pasayish tartibida"),
    ("price above EMA200", "цена выше EMA200", "narx EMA200 dan yuqori"),
    ("price below EMA200", "цена ниже EMA200", "narx EMA200 dan past"),
    ("MACD above signal", "MACD выше сигнальной", "MACD signal chizig'idan yuqori"),
    ("MACD below signal", "MACD ниже сигнальной", "MACD signal chizig'idan past"),
    ("histogram expanding up", "гистограмма растёт", "gistogramma o'smoqda"),
    ("histogram expanding down", "гистограмма падает", "gistogramma pasaymoqda"),
    ("close below lower Bollinger band", "закрытие ниже нижней полосы Боллинджера",
     "yopilish Bollinger pastki chizig'idan past"),
    ("close above upper Bollinger band", "закрытие выше верхней полосы Боллинджера",
     "yopilish Bollinger yuqori chizig'idan yuqori"),
    ("stochastic oversold", "стохастик в перепроданности", "stoxastik o'ta sotilgan"),
    ("stochastic overbought", "стохастик в перекупленности", "stoxastik o'ta sotib olingan"),
    (" (damped: strong opposing trend)", " (ослаблено: сильный встречный тренд)",
     " (susaytirildi: kuchli qarama-qarshi trend)"),
    ("uptrend structure (HH+HL)", "восходящая структура (HH+HL)",
     "ko'tarilish strukturasi (HH+HL)"),
    ("downtrend structure (LH+LL)", "нисходящая структура (LH+LL)",
     "pasayish strukturasi (LH+LL)"),
    ("CHoCH: broke swing high against downtrend",
     "CHoCH: пробой максимума против нисходящего тренда",
     "CHoCH: pasayish trendiga qarshi maksimum buzildi"),
    ("CHoCH: broke swing low against uptrend",
     "CHoCH: пробой минимума против восходящего тренда",
     "CHoCH: ko'tarilish trendiga qarshi minimum buzildi"),
    ("BOS above last swing high", "BOS: пробой последнего максимума",
     "BOS: oxirgi maksimum yuqoriga buzildi"),
    ("BOS below last swing low", "BOS: пробой последнего минимума",
     "BOS: oxirgi minimum pastga buzildi"),
    ("close above 20-bar high", "закрытие выше максимума 20 свечей",
     "yopilish 20 sham maksimumidan yuqori"),
    ("close below 20-bar low", "закрытие ниже минимума 20 свечей",
     "yopilish 20 sham minimumidan past"),
    (" on elevated volume", " на повышенном объёме", " yuqori hajm bilan"),
    ("bullish engulfing after decline", "бычье поглощение после снижения",
     "pasayishdan so'ng bullish engulfing"),
    ("bearish engulfing after advance", "медвежье поглощение после роста",
     "o'sishdan so'ng bearish engulfing"),
    ("hammer (long lower wick) after decline",
     "молот (длинная нижняя тень) после снижения",
     "pasayishdan so'ng bolg'a (uzun pastki soya)"),
    ("shooting star (long upper wick) after advance",
     "падающая звезда (длинная верхняя тень) после роста",
     "o'sishdan so'ng otuvchi yulduz (uzun yuqori soya)"),
    ("morning star reversal", "разворот «утренняя звезда»",
     "«tong yulduzi» burilishi"),
    ("evening star reversal", "разворот «вечерняя звезда»",
     "«oqshom yulduzi» burilishi"),
    ("rising price confirmed by rising OBV",
     "рост цены подтверждён ростом OBV",
     "narx o'sishi OBV o'sishi bilan tasdiqlangan"),
    ("falling price confirmed by falling OBV",
     "падение цены подтверждено падением OBV",
     "narx pasayishi OBV pasayishi bilan tasdiqlangan"),
    ("bullish divergence: price down, OBV up (accumulation)",
     "бычья дивергенция: цена вниз, OBV вверх (накопление)",
     "bullish divergensiya: narx pastga, OBV yuqoriga (to'planish)"),
    ("bearish divergence: price up, OBV down (distribution)",
     "медвежья дивергенция: цена вверх, OBV вниз (распределение)",
     "bearish divergensiya: narx yuqoriga, OBV pastga (taqsimlash)"),
    ("price above Kumo cloud", "цена выше облака Кумо", "narx Kumo bulutidan yuqori"),
    ("price below Kumo cloud", "цена ниже облака Кумо", "narx Kumo bulutidan past"),
    ("price inside cloud (indecision)", "цена внутри облака (неопределённость)",
     "narx bulut ichida (noaniqlik)"),
    ("Tenkan above Kijun", "Тенкан выше Киджун", "Tenkan Kijundan yuqori"),
    ("Tenkan below Kijun", "Тенкан ниже Киджун", "Tenkan Kijundan past"),
    ("no setup", "нет сетапа", "setup yo'q"),
    ("bullish RSI divergence: lower low in price, higher low in RSI",
     "бычья дивергенция RSI: цена ниже, RSI выше",
     "bullish RSI divergensiya: narx pastroq, RSI yuqoriroq"),
    ("bearish RSI divergence: higher high in price, lower high in RSI",
     "медвежья дивергенция RSI: цена выше, RSI ниже",
     "bearish RSI divergensiya: narx yuqoriroq, RSI pastroq"),
    ("stretched far above VWAP (mean-revert)",
     "сильно выше VWAP (ожидается возврат)",
     "VWAP dan ancha yuqori (qaytish kutiladi)"),
    ("stretched far below VWAP (mean-revert)",
     "сильно ниже VWAP (ожидается возврат)",
     "VWAP dan ancha past (qaytish kutiladi)"),
    ("price above rolling VWAP", "цена выше VWAP", "narx VWAP dan yuqori"),
    ("price below rolling VWAP", "цена ниже VWAP", "narx VWAP dan past"),
    ("pullback into EMA zone rejected in downtrend",
     "откат в зону EMA отбит в нисходящем тренде",
     "EMA zonasiga pullback pasayish trendida rad etildi"),
    ("pullback into EMA zone rejected in uptrend",
     "откат в зону EMA отбит в восходящем тренде",
     "EMA zonasiga pullback ko'tarilish trendida rad etildi"),
]

REGEX = [
    (re.compile(r"RSI stretched at (\d+)"),
     r"RSI перегрет: \1", r"RSI haddan tashqari: \1"),
    (re.compile(r"RSI oversold (\d+)"),
     r"RSI перепродан (\1)", r"RSI o'ta sotilgan (\1)"),
    (re.compile(r"RSI overbought (\d+)"),
     r"RSI перекуплен (\1)", r"RSI o'ta sotib olingan (\1)"),
    (re.compile(r"price inside unfilled bullish FVG \(([\d.]+)-([\d.]+)\)"),
     r"цена в незаполненном бычьем FVG (\1–\2)",
     r"narx to'ldirilmagan bullish FVG ichida (\1–\2)"),
    (re.compile(r"price inside unfilled bearish FVG \(([\d.]+)-([\d.]+)\)"),
     r"цена в незаполненном медвежьем FVG (\1–\2)",
     r"narx to'ldirilmagan bearish FVG ichida (\1–\2)"),
    (re.compile(r"at support ([\d.]+) \((\d+) touches\)"),
     r"у поддержки \1 (касаний: \2)", r"tayanchda \1 (tegishlar: \2)"),
    (re.compile(r"at resistance ([\d.]+) \((\d+) touches\)"),
     r"у сопротивления \1 (касаний: \2)", r"qarshilikda \1 (tegishlar: \2)"),
    (re.compile(r"price inside bullish order block \(([\d.]+)-([\d.]+)\)"),
     r"цена в бычьем ордер-блоке (\1–\2)",
     r"narx bullish order-blok ichida (\1–\2)"),
    (re.compile(r"price inside bearish order block \(([\d.]+)-([\d.]+)\)"),
     r"цена в медвежьем ордер-блоке (\1–\2)",
     r"narx bearish order-blok ichida (\1–\2)"),
    (re.compile(r"headlines lean bullish \((\d+)/(\d+)\)"),
     r"заголовки скорее бычьи (\1/\2)",
     r"sarlavhalar ko'proq bullish (\1/\2)"),
    (re.compile(r"headlines lean bearish \((\d+)/(\d+)\)"),
     r"заголовки скорее медвежьи (\1/\2)",
     r"sarlavhalar ko'proq bearish (\1/\2)"),
    (re.compile(r"double top broke neckline \(([\d.]+)\)"),
     r"двойная вершина: пробита линия шеи (\1)",
     r"qo'sh cho'qqi: bo'yin chizig'i buzildi (\1)"),
    (re.compile(r"double bottom broke neckline \(([\d.]+)\)"),
     r"двойное дно: пробита линия шеи (\1)",
     r"qo'sh tub: bo'yin chizig'i buzildi (\1)"),
    (re.compile(r"^head and shoulders broke neckline \(([\d.]+)\)"),
     r"голова и плечи: пробита линия шеи (\1)",
     r"bosh va yelkalar: bo'yin chizig'i buzildi (\1)"),
    (re.compile(r"inverse head and shoulders broke neckline \(([\d.]+)\)"),
     r"перевёрнутые голова и плечи: пробита линия шеи (\1)",
     r"teskari bosh va yelkalar: bo'yin chizig'i buzildi (\1)"),
]


def translate_reason(reason: str, lang: str) -> str:
    if lang == "en":
        return reason
    idx = 1 if lang == "ru" else 2
    for rule in FIXED:
        reason = reason.replace(rule[0], rule[idx])
    for rule in REGEX:
        reason = rule[0].sub(rule[idx], reason)
    return reason

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
}

UI = {
    "help": {
        "en": """<b>MarketFlow bot</b> — multi-strategy market flow reading for gold/USDT

/predict [symbol] [interval] — current prediction with strategy breakdown
/backtest [symbol] [interval] — walk-forward backtest
/news — USD economic calendar + latest gold headlines
/watch [symbol] [interval] [minutes] — alert when the flow direction flips
/watch [symbol] [interval] [minutes] all — send the reading on EVERY check
/unwatch — stop alerts
/status — show your watch subscription
/lang en|ru|uz — language / язык / til

Defaults: symbol <code>XAUUSD</code>/gold (data: Binance PAXG candles + live TradingView spot quote), interval <code>1h</code>, check every 15 min.
Examples:
<code>/predict XAUUSD 4h</code>
<code>/watch XAUUSD 5m 5 all</code> — full reading every 5 minutes""",
        "ru": """<b>MarketFlow бот</b> — мультистратегический анализ потока рынка для золота/USDT

/predict [символ] [таймфрейм] — текущий прогноз с разбором по стратегиям
/backtest [символ] [таймфрейм] — бэктест на истории
/news — экономкалендарь США + свежие новости по золоту
/watch [символ] [таймфрейм] [минуты] — оповещение при смене направления
/watch [символ] [таймфрейм] [минуты] all — сводка при КАЖДОЙ проверке
/unwatch — остановить оповещения
/status — моя подписка
/lang en|ru|uz — язык

По умолчанию: символ <code>XAUUSD</code>/золото (данные: свечи Binance PAXG + спот-котировка TradingView), таймфрейм <code>1h</code>, проверка каждые 15 мин.
Примеры:
<code>/predict XAUUSD 4h</code>
<code>/watch XAUUSD 5m 5 all</code> — полная сводка каждые 5 минут""",
        "uz": """<b>MarketFlow bot</b> — oltin/USDT uchun ko'p strategiyali bozor oqimi tahlili

/predict [simvol] [interval] — strategiyalar tahlili bilan joriy prognoz
/backtest [simvol] [interval] — tarixiy ma'lumotlarda backtest
/news — AQSH iqtisodiy kalendari + oltin bo'yicha yangiliklar
/watch [simvol] [interval] [daqiqa] — yo'nalish o'zgarganda xabar berish
/watch [simvol] [interval] [daqiqa] all — HAR tekshiruvda hisobot yuborish
/unwatch — xabarlarni to'xtatish
/status — mening obunam
/lang en|ru|uz — til

Standart: simvol <code>XAUUSD</code>/oltin (ma'lumot: Binance PAXG shamlari + TradingView jonli narxi), interval <code>1h</code>, har 15 daqiqada tekshiruv.
Misollar:
<code>/predict XAUUSD 4h</code>
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
              "I'll message you when the market flow direction flips. /unwatch to stop.",
        "ru": "👁 Слежу за <b>{symbol} {interval}</b>, проверка каждые {min} мин. "
              "Напишу, когда направление потока рынка сменится. /unwatch — остановить.",
        "uz": "👁 <b>{symbol} {interval}</b> kuzatilmoqda, har {min} daqiqada tekshiruv. "
              "Bozor oqimi yo'nalishi o'zgarganda xabar beraman. To'xtatish: /unwatch.",
    },
    "watching_all": {
        "en": "👁 Watching <b>{symbol} {interval}</b>, checking every {min} min. "
              "I'll send you the reading every check. /unwatch to stop.",
        "ru": "👁 Слежу за <b>{symbol} {interval}</b>, проверка каждые {min} мин. "
              "Буду присылать сводку при каждой проверке. /unwatch — остановить.",
        "uz": "👁 <b>{symbol} {interval}</b> kuzatilmoqda, har {min} daqiqada tekshiruv. "
              "Har tekshiruvda hisobot yuboraman. To'xtatish: /unwatch.",
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
        "en": "close <code>{close}</code> · bar {ts} UTC",
        "ru": "закрытие <code>{close}</code> · свеча {ts} UTC",
        "uz": "yopilish <code>{close}</code> · sham {ts} UTC",
    },
    "neutral_count": {
        "en": "⚪ {n} strategies neutral",
        "ru": "⚪ нейтральных стратегий: {n}",
        "uz": "⚪ {n} ta strategiya neytral",
    },
    "spot_line": {
        "en": "\n💰 live spot XAU/USD (TradingView/OANDA): <code>{price}</code> "
              "({chg}% today, H <code>{high}</code> / L <code>{low}</code>)",
        "ru": "\n💰 спот XAU/USD в реальном времени (TradingView/OANDA): <code>{price}</code> "
              "({chg}% за день, макс. <code>{high}</code> / мин. <code>{low}</code>)",
        "uz": "\n💰 jonli spot XAU/USD (TradingView/OANDA): <code>{price}</code> "
              "({chg}% bugun, maks. <code>{high}</code> / min. <code>{low}</code>)",
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

/** Localization strings for English and Burmese. */
export type Lang = "en" | "mm";

const strings: Record<string, Record<Lang, string>> = {
  // Township selector
  "township.overline": { en: "Township", mm: "မြို့နယ်" },
  "township.heading": { en: "Choose Your Region", mm: "ဒေသရွေးချယ်ပါ" },
  "township.subtitle": {
    en: "Select an agricultural township in Myanmar to analyze",
    mm: "မြန်မာနိုင်ငံရှိ စိုက်ပျိုးရေးမြို့နယ်ကို ရွေးချယ်ပါ",
  },
  "township.search": { en: "Search townships...", mm: "မြို့နယ်ရှာဖွေပါ..." },
  "season.monsoon": { en: "Monsoon Season", mm: "မိုးရာသီ" },
  "season.dry": { en: "Dry Season", mm: "ဆောင်းရာသီ" },

  // Climate risk
  "climate.overlineMonsoon": {
    en: "Monsoon Season Forecast",
    mm: "မိုးရာသီ ခန့်မှန်းချက်",
  },
  "climate.overlineDry": {
    en: "Dry Season Forecast",
    mm: "ဆောင်းရာသီ ခန့်မှန်းချက်",
  },
  "climate.drought": { en: "Drought Risk", mm: "မိုးခေါင်ရေရှားအန္တရာယ်" },
  "climate.flood": { en: "Flood Risk", mm: "ရေကြီးအန္တရာယ်" },
  "climate.rainfall": {
    en: "Forecast Rainfall",
    mm: "မိုးရေချိန် ခန့်မှန်းချက်",
  },
  "climate.tempAnomaly": { en: "Temp Anomaly", mm: "အပူချိန် ကွဲလွဲမှု" },
  "climate.overallRisk": { en: "Overall Risk:", mm: "အလုံးစုံ အန္တရာယ်:" },
  "climate.cta": {
    en: "Optimize Crop Portfolio",
    mm: "သီးနှံ ခွဲဝေစိုက်ပျိုးမှု ပိုကောင်းအောင်လုပ်ပါ",
  },

  // Optimizer
  "optimizer.overline": { en: "Portfolio", mm: "စိုက်ပျိုးမှု အစီအစဉ်" },
  "optimizer.heading": {
    en: "Optimize Crop Allocation",
    mm: "သီးနှံ ခွဲဝေမှုကို ပိုကောင်းအောင်လုပ်ပါ",
  },
  "optimizer.selectCrops": { en: "Select Crops", mm: "သီးနှံများ ရွေးချယ်ပါ" },
  "optimizer.minCrops": {
    en: "Choose at least 2 crops to diversify",
    mm: "အနည်းဆုံး သီးနှံ ၂ မျိုး ရွေးချယ်ပါ",
  },
  "optimizer.riskTolerance": { en: "Risk Tolerance", mm: "စွန့်စားနိုင်မှု" },
  "optimizer.conservative": { en: "Conservative", mm: "ဘေးကင်း" },
  "optimizer.balanced": { en: "Balanced", mm: "ညီတူညီမျှ" },
  "optimizer.aggressive": { en: "Aggressive", mm: "စွန့်စားသူ" },
  "optimizer.cta": { en: "Optimize Portfolio", mm: "ပိုကောင်းအောင်လုပ်ပါ" },
  "optimizer.monocrop": { en: "Monocrop", mm: "တစ်မျိုးတည်း" },
  "optimizer.optimized": { en: "Optimized", mm: "အကောင်းဆုံး" },
  "optimizer.expectedIncome": {
    en: "Expected Income",
    mm: "မျှော်မှန်းဝင်ငွေ",
  },
  "optimizer.risk": { en: "Risk (Std Dev)", mm: "အန္တရာယ်" },
  "optimizer.sharpe": { en: "Sharpe Ratio", mm: "ရှာ့ပ် အချိုး" },
  "optimizer.riskReduction": {
    en: "Risk Reduction",
    mm: "အန္တရာယ် လျှော့ချမှု",
  },

  // Monte Carlo
  "sim.overline": { en: "Simulation", mm: "ပုံစံတူလုပ်ခြင်း" },
  "sim.heading": {
    en: "Monte Carlo Analysis",
    mm: "မွန်တီကာလို ပိုင်းခြမ်းစိတ်ဖြာမှု",
  },
  "sim.cta": { en: "Run Simulation", mm: "ပုံစံတူ စတင်ပါ" },
  "sim.meanIncome": { en: "Mean Income", mm: "ပျမ်းမျှဝင်ငွေ" },
  "sim.worstCase": { en: "Worst Case (P5)", mm: "အဆိုးဆုံး" },
  "sim.bestCase": { en: "Best Case (P95)", mm: "အကောင်းဆုံး" },
  "sim.catastrophicLoss": { en: "Catastrophic Loss", mm: "ဆုံးရှုံးမှုကြီး" },

  // Common
  "common.back": { en: "Back", mm: "နောက်သို့" },
  "common.loading": { en: "Loading...", mm: "ဖတ်နေသည်..." },
};

/** Get translated string by key. */
export function t(key: string, lang: Lang): string {
  return strings[key]?.[lang] ?? key;
}

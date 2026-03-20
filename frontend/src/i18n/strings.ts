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

  // B2B Dashboard
  "nav.overview": { en: "Overview", mm: "ခြုံငုံသုံးသပ်ချက်" },
  "nav.groupPlan": { en: "Plan", mm: "စီစဉ်ခြင်း" },
  "nav.groupAnalyze": { en: "Analyze", mm: "ပိုင်းခြမ်းစိတ်ဖြာ" },
  "nav.groupMonitor": { en: "Monitor", mm: "စောင့်ကြည့်" },
  "nav.recommend": { en: "Recommend", mm: "အကြံပြုချက်" },
  "nav.demoRoi": { en: "Demo ROI", mm: "သရုပ်ပြ ROI" },
  "nav.reports": { en: "Reports", mm: "အစီရင်ခံစာ" },
  "nav.backToHome": { en: "Back to Home", mm: "ပင်မစာမျက်နှာ" },
  "nav.language": { en: "Language", mm: "ဘာသာစကား" },
  "nav.lightMode": { en: "Light Mode", mm: "အလင်းမုဒ်" },
  "nav.darkMode": { en: "Dark Mode", mm: "အမှောင်မုဒ်" },

  "dashboard.title": { en: "CropFolio Pro", mm: "CropFolio Pro" },
  "dashboard.subtitle": {
    en: "Data-driven crop-fertilizer recommendations for distributors",
    mm: "ဖြန့်ဖြူးသူများအတွက် အချက်အလက်အခြေခံ သီးနှံ-ဓာတ်မြေသြဇာ အကြံပြုချက်များ",
  },
  "dashboard.townships": { en: "Townships", mm: "မြို့နယ်များ" },
  "dashboard.cropProfiles": { en: "Crop Profiles", mm: "သီးနှံပရိုဖိုင်များ" },
  "dashboard.fertilizers": { en: "Fertilizers", mm: "ဓာတ်မြေသြဇာများ" },
  "dashboard.monteCarloSims": {
    en: "Monte Carlo Sims",
    mm: "မွန်တီကာလို ပုံစံတူများ",
  },
  "dashboard.perRecommendation": {
    en: "Per recommendation",
    mm: "အကြံပြုချက်တစ်ခုလျှင်",
  },
  "dashboard.regionsFormat": {
    en: "{count} regions covered",
    mm: "ဒေသ {count} ခု ပါဝင်သည်",
  },
  "dashboard.generateRec": {
    en: "Generate Recommendations",
    mm: "အကြံပြုချက်များ ထုတ်ပါ",
  },
  "dashboard.generateRecDesc": {
    en: "Select townships and crops to get optimized crop-fertilizer pairings with confidence scores from 1,000 Monte Carlo simulations.",
    mm: "မြို့နယ်နှင့် သီးနှံများရွေးချယ်ပြီး Monte Carlo ပုံစံတူ ၁,၀၀၀ ခုမှ ယုံကြည်မှုအမှတ်များဖြင့် အကောင်းဆုံး သီးနှံ-ဓာတ်မြေသြဇာ တွဲဖက်မှုများ ရယူပါ။",
  },
  "dashboard.startRec": {
    en: "Start Recommendation",
    mm: "အကြံပြုချက် စတင်ပါ",
  },
  "dashboard.demoCalc": {
    en: "Demo ROI Calculator",
    mm: "သရုပ်ပြ ROI တွက်ချက်စက်",
  },
  "dashboard.demoCalcDesc": {
    en: "Before committing to a demo farm, calculate expected costs, revenue, and reimbursement risk for any crop-township combination.",
    mm: "သရုပ်ပြခြံ မစတင်မီ မည်သည့်သီးနှံ-မြို့နယ် တွဲဖက်မှုအတွက်မဆို ကုန်ကျစရိတ်၊ ဝင်ငွေနှင့် ပြန်လည်ပေးချေမှု အန္တရာယ်ကို တွက်ချက်ပါ။",
  },
  "dashboard.calcRoi": { en: "Calculate ROI", mm: "ROI တွက်ချက်ပါ" },
  "dashboard.coverageByRegion": {
    en: "Coverage by Region",
    mm: "ဒေသအလိုက် လွှမ်းခြုံမှု",
  },
  "dashboard.faostatWfp": {
    en: "FAOSTAT + WFP data",
    mm: "FAOSTAT + WFP အချက်အလက်",
  },
  "dashboard.npkFormulations": {
    en: "NPK formulations",
    mm: "NPK ဖော်မြူလာများ",
  },

  // Recommend page
  "recommend.title": {
    en: "Recommendation Engine",
    mm: "အကြံပြုချက် အင်ဂျင်",
  },
  "recommend.subtitle": {
    en: "Select townships and crops to generate optimized crop-fertilizer recommendations",
    mm: "အကောင်းဆုံး သီးနှံ-ဓာတ်မြေသြဇာ အကြံပြုချက်များ ထုတ်လုပ်ရန် မြို့နယ်နှင့် သီးနှံများ ရွေးချယ်ပါ",
  },
  "recommend.selectTownships": {
    en: "Select Townships",
    mm: "မြို့နယ်များ ရွေးချယ်ပါ",
  },
  "recommend.selectCrops": {
    en: "Select Crops (min. 2)",
    mm: "သီးနှံများ ရွေးချယ်ပါ (အနည်းဆုံး ၂)",
  },
  "recommend.parameters": { en: "Parameters", mm: "ကန့်သတ်ချက်များ" },
  "recommend.season": { en: "Season", mm: "ရာသီ" },
  "recommend.dry": { en: "Dry", mm: "ခြောက်သွေ့" },
  "recommend.monsoon": { en: "Monsoon", mm: "မိုးရာသီ" },
  "recommend.riskTolerance": {
    en: "Risk Tolerance",
    mm: "စွန့်စားနိုင်မှု",
  },
  "recommend.conservative": { en: "Conservative", mm: "ဘေးကင်း" },
  "recommend.aggressive": { en: "Aggressive", mm: "စွန့်စားသူ" },
  "recommend.generate": {
    en: "Generate Recommendations",
    mm: "အကြံပြုချက်များ ထုတ်ပါ",
  },
  "recommend.generating": { en: "Generating...", mm: "ထုတ်လုပ်နေသည်..." },
  "recommend.running": {
    en: "Running portfolio optimization + 1,000 Monte Carlo simulations...",
    mm: "အကောင်းဆုံး ခွဲဝေမှုနှင့် Monte Carlo ပုံစံတူ ၁,၀၀၀ ခု လုပ်ဆောင်နေသည်...",
  },
  "recommend.expectedIncome": {
    en: "Expected Income/ha",
    mm: "မျှော်မှန်းဝင်ငွေ/ဟက်တာ",
  },
  "recommend.riskReduction": {
    en: "Risk Reduction",
    mm: "အန္တရာယ် လျှော့ချမှု",
  },
  "recommend.vsMonocrop": { en: "vs. monocrop", mm: "တစ်မျိုးတည်းနှင့်" },
  "recommend.successProb": {
    en: "Success Probability",
    mm: "အောင်မြင်နိုင်ခြေ",
  },
  "recommend.worstCase": {
    en: "Worst Case (5th pctl)",
    mm: "အဆိုးဆုံး (၅%)",
  },
  "recommend.soilProfile": { en: "Soil Profile", mm: "မြေဆီလွှာ ပရိုဖိုင်" },
  "recommend.allocation": { en: "Allocation", mm: "ခွဲဝေမှု" },
  "recommend.expectedIncomeLabel": {
    en: "Expected Income",
    mm: "မျှော်မှန်းဝင်ငွေ",
  },
  "recommend.recommendedFert": {
    en: "Recommended Fertilizers",
    mm: "အကြံပြုထားသော ဓာတ်မြေသြဇာများ",
  },

  // Demo ROI
  "demo.title": {
    en: "Demo ROI Calculator",
    mm: "သရုပ်ပြ ROI တွက်ချက်စက်",
  },
  "demo.subtitle": {
    en: "Calculate costs, expected returns, and reimbursement risk before committing to a demo farm",
    mm: "သရုပ်ပြခြံ မစတင်မီ ကုန်ကျစရိတ်၊ မျှော်မှန်းအမြတ်နှင့် ပြန်လည်ပေးချေမှု အန္တရာယ်ကို တွက်ချက်ပါ",
  },
  "demo.scenario": { en: "Scenario", mm: "အခြေအနေ" },
  "demo.township": { en: "Township", mm: "မြို့နယ်" },
  "demo.crop": { en: "Crop", mm: "သီးနှံ" },
  "demo.area": { en: "Area (hectares)", mm: "ဧရိယာ (ဟက်တာ)" },
  "demo.calculate": { en: "Calculate ROI", mm: "ROI တွက်ချက်ပါ" },
  "demo.calculating": { en: "Calculating...", mm: "တွက်ချက်နေသည်..." },
  "demo.totalInputCost": {
    en: "Total Input Cost",
    mm: "စုစုပေါင်း ကုန်ကျစရိတ်",
  },
  "demo.expectedRevenue": { en: "Expected Revenue", mm: "မျှော်မှန်းဝင်ငွေ" },
  "demo.expectedProfit": { en: "Expected Profit", mm: "မျှော်မှန်းအမြတ်" },
  "demo.reimbursementRisk": {
    en: "Reimbursement Risk",
    mm: "ပြန်လည်ပေးချေမှု အန္တရာယ်",
  },
  "demo.riskAssessment": { en: "Risk Assessment", mm: "အန္တရာယ် အကဲဖြတ်ခြင်း" },
  "demo.successProb": { en: "Success Probability", mm: "အောင်မြင်နိုင်ခြေ" },
  "demo.catastrophicLoss": {
    en: "Catastrophic Loss Risk",
    mm: "ကြီးမားသော ဆုံးရှုံးမှု အန္တရာယ်",
  },
  "demo.recommendedFert": {
    en: "Recommended Fertilizer",
    mm: "အကြံပြုထားသော ဓာတ်မြေသြဇာ",
  },

  // Region names for expanded township coverage
  "region.mandalay": { en: "Mandalay", mm: "မန္တလေး" },
  "region.sagaing": { en: "Sagaing", mm: "စစ်ကိုင်း" },
  "region.magway": { en: "Magway", mm: "မကွေး" },
  "region.bago": { en: "Bago", mm: "ပဲခူး" },
  "region.ayeyarwady": { en: "Ayeyarwady", mm: "ဧရာဝတီ" },
  "region.yangon": { en: "Yangon", mm: "ရန်ကုန်" },
  "region.nayPyiTaw": { en: "Nay Pyi Taw", mm: "နေပြည်တော်" },
  "region.shan": { en: "Shan", mm: "ရှမ်း" },
  "region.mon": { en: "Mon", mm: "မွန်" },
  "region.kayin": { en: "Kayin", mm: "ကရင်" },
  "region.tanintharyi": { en: "Tanintharyi", mm: "တနင်္သာရီ" },
  "region.chin": { en: "Chin", mm: "ချင်း" },
  "region.kachin": { en: "Kachin", mm: "ကချင်" },
  "region.rakhine": { en: "Rakhine", mm: "ရခိုင်" },

  // Navigation — new engines
  "nav.bayesian": {
    en: "Bayesian Analyzer",
    mm: "ဘေးစီးယန်း ပိုင်းခြမ်းစိတ်ဖြာမှု",
  },
  "nav.sar": { en: "SAR Verification", mm: "SAR အတည်ပြုခြင်း" },

  // Fertilizer Plan
  "fertPlan.title": {
    en: "Optimized Fertilizer Plan",
    mm: "အကောင်းဆုံး ဓာတ်မြေသြဇာ အစီအစဉ်",
  },
  "fertPlan.optimized": { en: "LP Optimized", mm: "LP အကောင်းဆုံး" },
  "fertPlan.fallback": { en: "Fallback", mm: "အရန်" },
  "fertPlan.totalCost": { en: "Total Cost", mm: "စုစုပေါင်း ကုန်ကျစရိတ်" },
  "fertPlan.yieldIncrease": {
    en: "Yield Increase",
    mm: "အထွက်နှုန်း တိုးမြင့်မှု",
  },
  "fertPlan.returnRatio": { en: "Return Ratio", mm: "ပြန်လည်ရရှိမှု အချိုး" },
  "fertPlan.nutrientDelivery": {
    en: "NPK Delivery (kg/ha)",
    mm: "NPK ပေးပို့မှု (kg/ha)",
  },
  "fertPlan.applicationSchedule": {
    en: "Application Schedule",
    mm: "သုံးစွဲမှု အချိန်ဇယား",
  },
  "fertPlan.day": { en: "Day", mm: "ရက်" },
  "fertPlan.micronutrientAlerts": {
    en: "Micronutrient Alerts",
    mm: "အာဟာရဓာတ်သတိပေးချက်များ",
  },
  "fertPlan.nutrientBalance": { en: "Nutrient Balance", mm: "အာဟာရ ညီမျှမှု" },

  // Bayesian Dashboard
  "bayesian.title": {
    en: "Bayesian Analyzer",
    mm: "ဘေးစီးယန်း ပိုင်းခြမ်းစိတ်ဖြာစက်",
  },
  "bayesian.subtitle": {
    en: "Input field observations to update yield predictions with Bayesian inference",
    mm: "ကွင်းဆင်းလေ့လာမှုများ ထည့်သွင်းပြီး ဘေးစီးယန်း ခန့်မှန်းချက်ဖြင့် အထွက်နှုန်း ခန့်မှန်းချက်များ အပ်ဒိတ်လုပ်ပါ",
  },
  "bayesian.setup": { en: "Setup", mm: "ပြင်ဆင်မှု" },
  "bayesian.evidence": { en: "Field Evidence", mm: "ကွင်းဆင်း အထောက်အထား" },
  "bayesian.evidenceDesc": {
    en: "Set observed conditions to update predictions. Leave unset for prior estimates.",
    mm: "ခန့်မှန်းချက်များ အပ်ဒိတ်လုပ်ရန် တွေ့ရှိထားသော အခြေအနေများ သတ်မှတ်ပါ။",
  },
  "bayesian.run": {
    en: "Run Bayesian Analysis",
    mm: "ဘေးစီးယန်း ပိုင်းခြမ်းစိတ်ဖြာမှု လုပ်ပါ",
  },
  "bayesian.running": {
    en: "Running Bayesian inference...",
    mm: "ဘေးစီးယန်း ခန့်မှန်းနေသည်...",
  },
  "bayesian.predictions": {
    en: "Yield Predictions",
    mm: "အထွက်နှုန်း ခန့်မှန်းချက်များ",
  },
  "bayesian.portfolioWeights": {
    en: "Bayesian Portfolio Weights",
    mm: "ဘေးစီးယန်း ခွဲဝေမှု အလေးချိန်များ",
  },

  // SAR Dashboard
  "sar.title": {
    en: "SAR Planting Verification",
    mm: "SAR စိုက်ပျိုးမှု အတည်ပြုခြင်း",
  },
  "sar.subtitle": {
    en: "Sentinel-1 radar analysis for rice paddy detection and crop monitoring",
    mm: "လယ်ယာ စိုက်ပျိုးမှု စောင့်ကြည့်ရန် Sentinel-1 ရေဒါ ပိုင်းခြမ်းစိတ်ဖြာမှု",
  },
  "sar.selectArea": {
    en: "Select Analysis Area",
    mm: "ပိုင်းခြမ်းစိတ်ဖြာမည့် ဧရိယာ ရွေးချယ်ပါ",
  },
  "sar.analyze": { en: "Analyze", mm: "ပိုင်းခြမ်းစိတ်ဖြာပါ" },
  "sar.analyzing": {
    en: "Analyzing satellite data...",
    mm: "ဂြိုလ်တု အချက်အလက် ပိုင်းခြမ်းစိတ်ဖြာနေသည်...",
  },
  "sar.riceStatus": { en: "Rice Detection", mm: "စပါး ရှာဖွေတွေ့ရှိမှု" },
  "sar.confidence": { en: "Confidence", mm: "ယုံကြည်မှု" },
  "sar.estimatedArea": { en: "Estimated Area", mm: "ခန့်မှန်း ဧရိယာ" },
  "sar.analysisDate": {
    en: "Analysis Date",
    mm: "ပိုင်းခြမ်းစိတ်ဖြာသည့် ရက်စွဲ",
  },
  "sar.phenologySignals": {
    en: "Phenology Signals",
    mm: "ဖီနိုလိုဂျီ အချက်ပြမှုများ",
  },
  "sar.backscatterTimeSeries": {
    en: "Backscatter Time Series",
    mm: "Backscatter အချိန်စီးရီး",
  },
  "sar.analysisArea": {
    en: "Analysis Area",
    mm: "ပိုင်းခြမ်းစိတ်ဖြာမည့် ဧရိယာ",
  },

  // Field Monitor
  "nav.fieldMonitor": {
    en: "Field Monitor",
    mm: "ကွင်းဆင်း စောင့်ကြည့်မှု",
  },
  "fieldMonitor.title": {
    en: "Field Monitor Dashboard",
    mm: "ကွင်းဆင်း စောင့်ကြည့်မှု ဒက်ရှ်ဘုတ်",
  },
  "fieldMonitor.subtitle": {
    en: "Monitor plot compliance from satellite imagery — liability shield for distributors",
    mm: "ဂြိုလ်တုပုံရိပ်မှ စိုက်ကွက် လိုက်နာမှု စောင့်ကြည့်ခြင်း — ဖြန့်ဖြူးသူများအတွက် တာဝန်ယူမှု အကာအကွယ်",
  },
  "fieldMonitor.selectArea": {
    en: "Select Monitoring Area",
    mm: "စောင့်ကြည့်မည့် ဧရိယာ ရွေးချယ်ပါ",
  },
  "fieldMonitor.monitor": { en: "Monitor", mm: "စောင့်ကြည့်ပါ" },
  "fieldMonitor.monitoring": {
    en: "Monitoring...",
    mm: "စောင့်ကြည့်နေသည်...",
  },
  "fieldMonitor.totalPlots": { en: "Total Plots", mm: "စုစုပေါင်း စိုက်ကွက်" },
  "fieldMonitor.complianceRate": {
    en: "Compliance Rate",
    mm: "လိုက်နာမှု နှုန်း",
  },
  "fieldMonitor.activeAlerts": {
    en: "Active Alerts",
    mm: "တက်ကြွသော သတိပေးချက်များ",
  },
  "fieldMonitor.verifiedArea": {
    en: "Verified Area",
    mm: "အတည်ပြုထားသော ဧရိယာ",
  },
  "fieldMonitor.plotMap": { en: "Plot Map", mm: "စိုက်ကွက် မြေပုံ" },
  "fieldMonitor.complianceBreakdown": {
    en: "Compliance Breakdown",
    mm: "လိုက်နာမှု ခွဲခြမ်းစိတ်ဖြာမှု",
  },
  "fieldMonitor.compliant": { en: "Compliant", mm: "လိုက်နာ" },
  "fieldMonitor.warning": { en: "Warning", mm: "သတိပေးချက်" },
  "fieldMonitor.deviation": { en: "Deviation", mm: "သွေဖည်မှု" },
  "fieldMonitor.alerts": { en: "Alerts", mm: "သတိပေးချက်များ" },
  "fieldMonitor.allAlerts": { en: "All", mm: "အားလုံး" },
  "fieldMonitor.noAlerts": {
    en: "No alerts matching filter",
    mm: "စစ်ထုတ်မှုနှင့် ကိုက်ညီသော သတိပေးချက် မရှိပါ",
  },
  "fieldMonitor.score": { en: "Score", mm: "အမှတ်" },
  "fieldMonitor.recommendedCrop": {
    en: "Recommended Crop",
    mm: "အကြံပြုထားသော သီးနှံ",
  },
  "fieldMonitor.plantingDetected": {
    en: "Planting Detected",
    mm: "စိုက်ပျိုးမှု တွေ့ရှိ",
  },
  "fieldMonitor.cropMatch": { en: "Crop Match", mm: "သီးနှံ ကိုက်ညီမှု" },
  "fieldMonitor.phenologyMatch": {
    en: "Phenology Match",
    mm: "ဖီနိုလိုဂျီ ကိုက်ညီမှု",
  },
  "fieldMonitor.sarComparison": {
    en: "SAR: Expected vs Observed",
    mm: "SAR: မျှော်မှန်း vs တွေ့ရှိ",
  },
  "fieldMonitor.expectedVH": { en: "Expected VH", mm: "မျှော်မှန်း VH" },
  "fieldMonitor.observedVH": { en: "Observed VH", mm: "တွေ့ရှိ VH" },
  "fieldMonitor.plotAlerts": {
    en: "Plot Alerts",
    mm: "စိုက်ကွက် သတိပေးချက်များ",
  },

  // Advisory
  "nav.advisory": {
    en: "AI Advisory",
    mm: "AI အကြံပြုချက်",
  },
  "advisory.title": {
    en: "AI Advisory",
    mm: "AI အကြံပြုချက်",
  },
  "advisory.subtitle": {
    en: "AI-powered township intelligence — ask questions and get bilingual answers backed by satellite, climate, and market data",
    mm: "AI စွမ်းအားသုံး မြို့နယ် ထိုးထွင်းသိမြင်မှု — ဂြိုလ်တု၊ ရာသီဥတု နှင့် ဈေးကွက် အချက်အလက်များဖြင့် အထောက်အကူပြု နှစ်ဘာသာ အဖြေများ ရယူပါ",
  },
  "advisory.selectArea": {
    en: "Select Township",
    mm: "မြို့နယ် ရွေးချယ်ပါ",
  },
  "advisory.generate": {
    en: "Generate Advisory",
    mm: "အကြံပြုချက် ထုတ်ပါ",
  },
  "advisory.generating": {
    en: "Generating advisory...",
    mm: "အကြံပြုချက် ထုတ်လုပ်နေသည်...",
  },
  "advisory.askTitle": {
    en: "Ask CropFolio",
    mm: "CropFolio ကို မေးမြန်းပါ",
  },
  "advisory.queryPlaceholder": {
    en: "Ask a question about this township...",
    mm: "ဤမြို့နယ်အကြောင်း မေးခွန်းတစ်ခု မေးပါ...",
  },
  "advisory.ask": {
    en: "Ask",
    mm: "မေးပါ",
  },
  "advisory.noAiFallback": {
    en: "AI features are unavailable. Showing static data summary. Configure a Gemini API key to enable AI advisories.",
    mm: "AI လုပ်ဆောင်ချက်များ မရရှိနိုင်ပါ။ Gemini API key ကို ပြင်ဆင်သတ်မှတ်ပြီး AI အကြံပြုချက်များ ဖွင့်ပါ။",
  },

  // Reports
  "reports.title": { en: "Reports", mm: "အစီရင်ခံစာများ" },
  "reports.subtitle": {
    en: "AI-generated distributor advisory briefs and PDF reports",
    mm: "AI ဖန်တီးထားသော ဖြန့်ဖြူးသူ အကြံဉာဏ်စာများနှင့် PDF အစီရင်ခံစာများ",
  },
};

/** Get translated string by key. */
export function t(key: string, lang: Lang): string {
  return strings[key]?.[lang] ?? key;
}

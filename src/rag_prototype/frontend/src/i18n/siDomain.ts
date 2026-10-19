// Sinhala display text for research and intake content.
//
// DISPLAY ONLY. Every table is keyed by a canonical identifier (branch ID,
// model ID, profile key, variable name, sector code) or by the exact English
// string the backend already uses as the canonical value (skills, q2–q5,
// answer labels). Nothing here is ever sent to the backend; a missing entry
// falls back to the original English text.

export const SI_BRANCH_OPTIONS: Record<string, string> = {
  D: "දැනට අධ්‍යාපනය ලබමින් සිටී (පාසල, විශ්වවිද්‍යාලය හෝ පුහුණු වැඩසටහනක්)",
  E: "අධ්‍යාපනය අවසන් කර හෝ අතහැර, රැකියා විරහිතව හෝ රැකියා සොයමින් සිටී",
  F: "දැනට රැකියාවක නියුතුය (වැටුප් ලබන රැකියාවක්)",
  G: "රැකියාවක නියුතු නොවේ, අධ්‍යාපනය නොලබයි, දැනට රැකියා සොයන්නේද නැත",
};

export const SI_BRANCH_LABELS: Record<string, string> = {
  D: "අධ්‍යාපනය හෝ පුහුණුව ලබමින්",
  E: "රැකියා සොයමින්",
  F: "දැනට රැකියාවේ නියුතු",
  G: "රැකියාවෙන් සහ අධ්‍යාපනයෙන් බැහැරව",
};

export const SI_MODEL_LABELS: Record<string, string> = {
  D_motivation: "අධ්‍යයන අභිප්‍රේරණය",
  D_economic: "ගෘහස්ථ සම්පත්",
  D_educational_cultural: "අධ්‍යාපන පසුබිම",
  E_learning_orientation: "අධ්‍යාපනය සහ වැඩිදුර ඉගෙනීම",
  F_employment_security: "රැකියා සුරක්ෂිතභාවය",
  G_economic_role: "ගෘහස්ථ ආර්ථික භූමිකාව",
  G_future_engagement: "අනාගත රැකියා සහ අධ්‍යාපනය",
};

export const SI_MODEL_DESCRIPTIONS: Record<string, string> = {
  D_motivation: "මෙම ආකෘතිය මඟින් වත්මන් සිසුන්, ඔවුන් ප්‍රකාශ කළ අධ්‍යයන අභිප්‍රේරණය, තේරීමේ නිදහස පිළිබඳ හැඟීම, අධ්‍යයන ක්ෂේත්‍රය පිළිබඳ ආත්මවිශ්වාසය සහ තම ආයතනය සමඟ ඇති බැඳීම අනුව කණ්ඩායම් කරයි.",
  D_economic: "මෙම ආකෘතිය මඟින් වත්මන් සිසුන්, ඔවුන්ගේ නිරීක්ෂිත ගෘහස්ථ ආර්ථික තත්ත්වය සහ අධ්‍යාපන අරමුදල් තත්ත්වය අනුව කණ්ඩායම් කරයි.",
  D_educational_cultural: "මෙම ආකෘතිය මඟින් වත්මන් සිසුන්, පවුලේ අධ්‍යාපන මට්ටම, අපේක්ෂිත අධ්‍යාපනය, ආයතන වර්ගය, ඉගෙනුම ලබන අතරතුර රැකියා කිරීම සහ නැවත අධ්‍යාපනයට පිවිසීම අනුව කණ්ඩායම් කරයි.",
  E_learning_orientation: "මෙම ආකෘතිය මඟින් රැකියා සොයන තරුණයින්, ඔවුන්ගේ පෙර අධ්‍යාපනය කෙතරම් ප්‍රයෝජනවත් වූයේද යන්න, වැඩිදුර ඉගෙනුම් සැලසුම් සහ අපේක්ෂිත අධ්‍යාපන මට්ටම අනුව කණ්ඩායම් කරයි.",
  F_employment_security: "මෙම ආකෘතිය මඟින් රැකියාවල නියුතු තරුණයින්, ඔවුන්ගේ ගිවිසුම් වර්ගය, අපේක්ෂිත රැකියා සුරක්ෂිතභාවය සහ රැකියාවේ විධිමත්භාවය අනුව කණ්ඩායම් කරයි.",
  G_economic_role: "මෙම ආකෘතිය මඟින් රැකියාවෙන් සහ අධ්‍යාපනයෙන් බැහැරව සිටින තරුණයින්, නිවස තුළ ඔවුන්ගේ ආර්ථික භූමිකාව, ආදායම් මාර්ගය සහ නිවසේ අයගේ රැකියා තත්ත්වය අනුව කණ්ඩායම් කරයි.",
  G_future_engagement: "මෙම ආකෘතිය මඟින් රැකියාවෙන් සහ අධ්‍යාපනයෙන් බැහැරව සිටින තරුණයින්, පෙර රැකියා අත්දැකීම් සහ අනාගත රැකියා හා අධ්‍යාපනය පිළිබඳ ඔවුන් ප්‍රකාශ කළ අභිප්‍රායන් අනුව කණ්ඩායම් කරයි.",
};

// The 17 retained profiles. Names and "what distinguishes this profile"
// summaries are translated sentence-for-sentence from the English canonical
// text; comparison direction (more/less often) is preserved in every case.
export const SI_PROFILES: Record<string, { name: string; summary: string }> = {
  D_motivation_p1: {
    name: "සුදුසුකම් ලබාගැනීම මූලික කරගත් අධ්‍යයනය",
    summary: "අධ්‍යයන අභිප්‍රේරණ පිළිබඳ අනෙක් කාණ්ඩ සමඟ සසඳන විට, රැකියා හෝ පුහුණු අවස්ථා සඳහා උදව් ඉල්ලිය හැකි ප්‍රයෝජනවත් කෙනෙකු තමන්ට නොමැති බව මෙම පෙර සමීක්ෂණ කණ්ඩායම වඩාත් බහුලව වාර්තා කළේය.",
  },
  D_motivation_p2: {
    name: "වර්ධනය වන ආත්මවිශ්වාසය සහිත, ඉලක්ක මූලික අධ්‍යයනය",
    summary: "අධ්‍යයන අභිප්‍රේරණ පිළිබඳ අනෙක් කාණ්ඩ සමඟ සසඳන විට, රැකියා හෝ පුහුණු අවස්ථා සඳහා ප්‍රයෝජනවත් සම්බන්ධතා ඇති පුද්ගලයින් කිහිප දෙනෙකු හඳුනන බව මෙම පෙර සමීක්ෂණ කණ්ඩායම වාර්තා කළේ අඩුවෙනි.",
  },
  D_motivation_p3: {
    name: "ඉලක්ක මූලික, ආත්මවිශ්වාසී සහ සබඳතා සහිත අධ්‍යයනය",
    summary: "අධ්‍යයන අභිප්‍රේරණ පිළිබඳ අනෙක් කාණ්ඩ සමඟ සසඳන විට, රැකියා හෝ පුහුණු අවස්ථා සඳහා ප්‍රයෝජනවත් සම්බන්ධතා ඇති පුද්ගලයින් කිහිප දෙනෙකු හඳුනන බව මෙම පෙර සමීක්ෂණ කණ්ඩායම වඩාත් බහුලව වාර්තා කළේය.",
  },
  D_economic_p1: {
    name: "පවුලේ සහාය ලබන, රජයේ අරමුදල් සහිත අධ්‍යයනය",
    summary: "“නිවසේ වැඩි ආදායම් උපයන්නන් සහිත, පවුල අරමුදල් සපයන අධ්‍යයනය” කාණ්ඩය සමඟ සසඳන විට, මෙම පෙර සමීක්ෂණ කණ්ඩායමේ තොරතුරු හා සන්නිවේදන තාක්ෂණය (ICT) හැදෑරීමට කැමති අය සහ පෞද්ගලික ආයතනවල ඉගෙනුම ලබන අය අඩුවෙන් සිටි අතර, වත්මන් පාඨමාලාවට යොමු වීමේදී පවුලෙන් මඟපෙන්වීමක් ලැබුණු බව පැවසූ අයද අඩු විය.",
  },
  D_economic_p2: {
    name: "නිවසේ වැඩි ආදායම් උපයන්නන් සහිත, පවුල අරමුදල් සපයන අධ්‍යයනය",
    summary: "“පවුලේ සහාය ලබන, රජයේ අරමුදල් සහිත අධ්‍යයනය” කාණ්ඩය සමඟ සසඳන විට, මෙම පෙර සමීක්ෂණ කණ්ඩායමේ තොරතුරු හා සන්නිවේදන තාක්ෂණය (ICT) හැදෑරීමට කැමති අය සහ පෞද්ගලික ආයතනවල ඉගෙනුම ලබන අය වැඩියෙන් සිටි අතර, වත්මන් පාඨමාලාවට යොමු වීමේදී පවුලෙන් මඟපෙන්වීමක් ලැබුණු බව පැවසූ අයද වැඩි විය.",
  },
  D_educational_cultural_p1: {
    name: "උපාධිධාරී පවුල් පසුබිමක් සහිතව නැවත අධ්‍යාපනයට පිවිසීම",
    summary: "අධ්‍යාපන පසුබිම පිළිබඳ අනෙක් කාණ්ඩ සමඟ සසඳන විට, මෙම පෙර සමීක්ෂණ කණ්ඩායම දැනටමත් රැකියා සොයමින් සිටියේ වඩාත් බහුලව වන අතර, ප්‍රධාන පුද්ගලික ආදායම් මාර්ගය හෝ අධ්‍යාපන අරමුදල් මූලාශ්‍රය ලෙස දෙමාපියන් හෝ පවුල මත යැපුණේ අඩුවෙනි.",
  },
  D_educational_cultural_p2: {
    name: "රාජ්‍ය අධ්‍යාපනය හරහා පශ්චාත් උපාධි මාර්ගය",
    summary: "අධ්‍යාපන පසුබිම පිළිබඳ අනෙක් කාණ්ඩ සමඟ සසඳන විට, තවමත් රැකියා සෙවීම ආරම්භ නොකිරීම, පුද්ගලික ආදායම සඳහා දෙමාපියන් හෝ පවුල මත යැපීම සහ රජයේ අරමුදල් සහිත හෝ නොමිලේ ලැබෙන අධ්‍යාපනය හරහා ඉගෙනීම මෙම පෙර සමීක්ෂණ කණ්ඩායම තුළ වඩාත් බහුලව දක්නට ලැබිණි.",
  },
  D_educational_cultural_p3: {
    name: "රැකියා අත්දැකීම් රහිත, පෞද්ගලික අධ්‍යාපන මාර්ගය",
    summary: "අධ්‍යාපන පසුබිම පිළිබඳ අනෙක් කාණ්ඩ සමඟ සසඳන විට, තවමත් රැකියා සෙවීම ආරම්භ කර නැති බව මෙම පෙර සමීක්ෂණ කණ්ඩායම පැවසුවේ අඩුවෙන් වන අතර, පුද්ගලික ආදායම සහ අධ්‍යාපන අරමුදල් යන දෙකටම මූලාශ්‍රය ලෙස දෙමාපියන් හෝ පවුල වඩාත් කැපී පෙනුණි.",
  },
  D_educational_cultural_p4: {
    name: "රැකියා අත්දැකීම් සහිත, පෞද්ගලික අධ්‍යාපන මාර්ගය",
    summary: "අධ්‍යාපන පසුබිම පිළිබඳ අනෙක් කාණ්ඩ සමඟ සසඳන විට, තවමත් රැකියා සෙවීම ආරම්භ කර නැති බව මෙම පෙර සමීක්ෂණ කණ්ඩායම පැවසුවේ අඩුවෙනි; ප්‍රධාන පුද්ගලික ආදායම් මාර්ගය ලෙස දෙමාපියන් හෝ පවුල මත යැපුණේද අඩුවෙන් වන අතර, ඉහළම ගෘහස්ථ ආදායම් පරාසය වාර්තා කළේ වඩාත් බහුලවය.",
  },
  E_learning_orientation_p1: {
    name: "අධ්‍යාපනයට ඉහළ වටිනාකමක් සහ ශක්තිමත් ඉගෙනුම් අභිලාෂයක්",
    summary: "“අධ්‍යාපනයට මධ්‍යස්ථ වටිනාකමක් සහ මිශ්‍ර ඉගෙනුම් සැලසුම්” කාණ්ඩය සමඟ සසඳන විට, මෙම පෙර සමීක්ෂණ කණ්ඩායම ස්ථාවර, හොඳ වැටුපක් සහිත සහ තම සුදුසුකම්වලට ගැළපෙන රැකියාවක් අපේක්ෂා කළේ වඩාත් බහුලවය; රැකියා සෙවීමේදී වඩා ප්‍රයෝජනවත් සම්බන්ධතා සහ වඩා ශක්තිමත් සහාය ලැබුණු බව වාර්තා කළ අතර, වැඩි අයදුම්පත් සංඛ්‍යාවක් ඉදිරිපත් කළේය.",
  },
  E_learning_orientation_p2: {
    name: "අධ්‍යාපනයට මධ්‍යස්ථ වටිනාකමක් සහ මිශ්‍ර ඉගෙනුම් සැලසුම්",
    summary: "“අධ්‍යාපනයට ඉහළ වටිනාකමක් සහ ශක්තිමත් ඉගෙනුම් අභිලාෂයක්” කාණ්ඩය සමඟ සසඳන විට, දැඩි රැකියා කොන්දේසි, ඉතා ප්‍රයෝජනවත් සම්බන්ධතා හෝ ශක්තිමත් රැකියා සෙවීමේ සහාය ගැන මෙම පෙර සමීක්ෂණ කණ්ඩායම වාර්තා කළේ අඩුවෙන් වන අතර, ඉදිරිපත් කළ අයදුම්පත් සංඛ්‍යාවද අඩු විය.",
  },
  F_employment_security_p1: {
    name: "අවිනිශ්චිත සුරක්ෂිතභාවයක් සහිත තාවකාලික රැකියා",
    summary: "“වඩා ශක්තිමත් සුරක්ෂිතභාවයක් සහිත ස්ථිර රැකියා” කාණ්ඩය සමඟ සසඳන විට, මෙම පෙර සමීක්ෂණ කණ්ඩායමට අඩු රැකියා ආදායමක් තිබීමටත්, ප්‍රධාන ආදායම් මාර්ගය ලෙස නිත්‍ය රැකියාව මත අඩුවෙන් යැපීමටත්, වත්මන් රැකියාවේ රැඳී සිටීමට අඩු කැමැත්තක් දැක්වීමටත් නැඹුරුවක් තිබිණි.",
  },
  F_employment_security_p2: {
    name: "වඩා ශක්තිමත් සුරක්ෂිතභාවයක් සහිත ස්ථිර රැකියා",
    summary: "“අවිනිශ්චිත සුරක්ෂිතභාවයක් සහිත තාවකාලික රැකියා” කාණ්ඩය සමඟ සසඳන විට, මෙම පෙර සමීක්ෂණ කණ්ඩායමට ඉහළ රැකියා ආදායමක් තිබීමටත්, ප්‍රධාන ආදායම් මාර්ගය ලෙස නිත්‍ය රැකියාව මත වැඩියෙන් යැපීමටත්, වත්මන් රැකියාවේ රැඳී සිටීමට වැඩි කැමැත්තක් දැක්වීමටත් නැඹුරුවක් තිබිණි.",
  },
  G_economic_role_p1: {
    name: "පවුලේ සහාය මත යැපෙන, ආදායම් නොසපයන්නා",
    summary: "“තමන්ගේ ආදායමෙන් නිවසට සපයන්නා හෝ දායක වන්නා” කාණ්ඩය සමඟ සසඳන විට, ප්‍රයෝජනවත් රැකියා සම්බන්ධතා කිහිපයක්, රැකියා අවස්ථා පිළිබඳ තොරතුරු සඳහා නිතිපතා ප්‍රවේශය, හෝ සුදුසු රැකියාවක් හෝ පුහුණුවක් සොයාගැනීම පිළිබඳ ඉහළ ආත්මවිශ්වාසය ඇති බව මෙම පෙර සමීක්ෂණ කණ්ඩායම වාර්තා කළේ අඩුවෙනි.",
  },
  G_economic_role_p2: {
    name: "තමන්ගේ ආදායමෙන් නිවසට සපයන්නා හෝ දායක වන්නා",
    summary: "“පවුලේ සහාය මත යැපෙන, ආදායම් නොසපයන්නා” කාණ්ඩය සමඟ සසඳන විට, ප්‍රයෝජනවත් රැකියා සම්බන්ධතා කිහිපයක්, රැකියා අවස්ථා පිළිබඳ තොරතුරු සඳහා නිතිපතා ප්‍රවේශය සහ සුදුසු රැකියාවක් හෝ පුහුණුවක් සොයාගැනීම පිළිබඳ ඉහළ ආත්මවිශ්වාසය ඇති බව මෙම පෙර සමීක්ෂණ කණ්ඩායම වඩාත් බහුලව වාර්තා කළේය.",
  },
  G_future_engagement_p1: {
    name: "රැකියා සහ අධ්‍යාපනයට සම්බන්ධ වීමට නැඹුරු",
    summary: "“අනාගත රැකියා/අධ්‍යාපන අපේක්ෂා අඩු හෝ අවිනිශ්චිත” කාණ්ඩය සමඟ සසඳන විට, ඉහළ ආත්මවිශ්වාසය, ශක්තිමත් සහාය සහ රැකියා අවස්ථා පිළිබඳ තොරතුරු සඳහා නිතිපතා ප්‍රවේශය ඇති බව මෙම පෙර සමීක්ෂණ කණ්ඩායම වඩාත් බහුලව වාර්තා කළ අතර, අනාගතය ගැන අතරමං වූ හෝ අවිනිශ්චිත හැඟීමක් ඇති වූයේ අඩුවෙනි.",
  },
  G_future_engagement_p2: {
    name: "අනාගත රැකියා/අධ්‍යාපන අපේක්ෂා අඩු හෝ අවිනිශ්චිත",
    summary: "“රැකියා සහ අධ්‍යාපනයට සම්බන්ධ වීමට නැඹුරු” කාණ්ඩය සමඟ සසඳන විට, ඉහළ ආත්මවිශ්වාසය, ශක්තිමත් සහාය හෝ රැකියා අවස්ථා පිළිබඳ තොරතුරු සඳහා නිතිපතා ප්‍රවේශය ඇති බව මෙම පෙර සමීක්ෂණ කණ්ඩායම වාර්තා කළේ අඩුවෙන් වන අතර, අනාගතය ගැන අතරමං වූ හෝ අවිනිශ්චිත හැඟීමක් ඇති වූයේ වඩාත් බහුලවය.",
  },
};

// Cluster-forming question wording as shown to officers (by variable name).
export const SI_QUESTIONS: Record<string, string> = {
  household_size: "ඔබේ නිවසේ (ඔබද ඇතුළුව) ජීවත් වන්නේ කී දෙනෙක්ද?",
  household_workers: "ඔබේ නිවසේ දැනට රැකියාවක නියුතු (ආදායම් උපයන) අය කී දෙනෙක්ද?",
  household_unemployed: "ඔබේ නිවසේ දැනට රැකියා විරහිත අය කී දෙනෙක්ද?",
  study_motivation_type: "ඔබ ඔබේ වත්මන් විෂය හදාරන්නේ ඇයි?",
  autonomy_in_study: "ඔබ හදාරන දේ සහ හදාරන ආකාරය පිළිබඳ ඔබට කොපමණ තේරීමක් සහ පාලනයක් තිබේද?",
  competence_in_study_field: "ඔබේ අධ්‍යයන ක්ෂේත්‍රයේ ඔබ කෙතරම් දක්ෂ යැයි ඔබට හැඟේද?",
  relatedness_at_institution: "ඔබේ ආයතනයේ ප්‍රජාව සමඟ ඔබ කෙතරම් බැඳී සිටින බවක් ඔබට හැඟේද?",
  household_income: "ඔබේ නිවසේ මාසික ආදායම කොපමණද?",
  primary_earner_status: "ඔබ නිවසේ ප්‍රධාන ආදායම් සපයන්නාද?",
  primary_income_source: "ඔබේම ප්‍රධාන පුද්ගලික ආදායම් මාර්ගය කුමක්ද?",
  edu_funding_source: "ඔබේ වත්මන් හෝ නවතම අධ්‍යාපනය සඳහා අරමුදල් සැපයෙන්නේ කෙසේද?",
  father_edu: "ඔබේ පියා සම්පූර්ණ කළ ඉහළම අධ්‍යාපන මට්ටම කුමක්ද?",
  mother_edu: "ඔබේ මව සම්පූර්ණ කළ ඉහළම අධ්‍යාපන මට්ටම කුමක්ද?",
  expected_highest_edu_d: "ඔබ සම්පූර්ණ කිරීමට අපේක්ෂා කරන ඉහළම අධ්‍යාපන මට්ටම කුමක්ද?",
  expected_highest_edu_e: "ඔබ සම්පූර්ණ කිරීමට අපේක්ෂා කරන ඉහළම අධ්‍යාපන මට්ටම කුමක්ද?",
  institution_type: "ඔබ දැනට ඉගෙනුම ලබන්නේ කුමන වර්ගයේ ආයතනයකද?",
  worked_while_studying: "ඉගෙනුම ලබන අතරතුර ඔබ වැටුපක් සඳහා රැකියා කර තිබේද?",
  re_entered_education: "විවේකයකින් පසු ඔබ නැවත අධ්‍යාපනයට පිවිසියාද?",
  past_edu_usefulness: "රැකියාවක් සොයාගැනීමට ඔබේ අධ්‍යාපනය කෙතරම් ප්‍රයෝජනවත් වී තිබේද?",
  plans_further_edu: "ඔබ වැඩිදුර අධ්‍යාපනය හෝ පුහුණුව ලැබීමට සැලසුම් කරනවාද?",
  contract_type: "ඔබේ වත්මන් රැකියා ගිවිසුමේ වර්ගය කුමක්ද?",
  job_security_12months: "මාස 12කට පසුවත් ඔබට මෙම රැකියාව තිබීමට ඇති ඉඩකඩ කොපමණද?",
  sector_formality: "ඔබේ වත්මන් සේවායෝජකයා කෙතරම් විධිමත්ද?",
  reason_not_in_labour_force: "ඔබ දැනට රැකියාවක නොයෙදීමට හේතුව වඩාත් හොඳින් විස්තර කරන්නේ කුමක්ද?",
  ever_worked: "ඔබ මීට පෙර කවදා හෝ වැටුපක් හෝ ලාභයක් සඳහා රැකියා කර තිබේද?",
  wants_to_work_future: "අනාගතයේ කිසියම් අවස්ථාවක රැකියා කිරීමට ඔබ කැමතිද?",
  wants_further_edu: "ඔබ වැඩිදුර අධ්‍යාපනය ලැබීමට කැමතිද?",
};

// Short display names for cluster-forming variables (by variable name).
export const SI_VARIABLES: Record<string, string> = {
  autonomy_in_study: "අධ්‍යයනයේදී තේරීමේ නිදහස සහ පාලනය",
  competence_in_study_field: "අධ්‍යයන ක්ෂේත්‍රය පිළිබඳ ආත්මවිශ්වාසය",
  contract_type: "රැකියා ගිවිසුම් වර්ගය",
  edu_funding_source: "අධ්‍යාපන අරමුදල් මූලාශ්‍රය",
  ever_worked: "පෙර රැකියා අත්දැකීම්",
  expected_highest_edu_d: "අපේක්ෂිත ඉහළම අධ්‍යාපන මට්ටම",
  expected_highest_edu_e: "අපේක්ෂිත ඉහළම අධ්‍යාපන මට්ටම",
  father_edu: "පියාගේ අධ්‍යාපනය",
  household_income: "ගෘහස්ථ ආදායම",
  household_size: "නිවසේ සාමාජික සංඛ්‍යාව",
  household_unemployed: "රැකියා සොයන නිවසේ සාමාජිකයින්",
  household_workers: "රැකියාවල නියුතු නිවසේ සාමාජිකයින්",
  institution_type: "ආයතන වර්ගය",
  job_security_12months: "ඉදිරි මාස 12 තුළ රැකියා සුරක්ෂිතභාවය",
  mother_edu: "මවගේ අධ්‍යාපනය",
  past_edu_usefulness: "පෙර අධ්‍යාපනයේ ප්‍රයෝජනවත්භාවය",
  plans_further_edu: "වැඩිදුර අධ්‍යාපන හෝ පුහුණු සැලසුම්",
  primary_earner_status: "ප්‍රධාන ආදායම් උපයන්නාගේ තත්ත්වය",
  primary_income_source: "ප්‍රධාන පුද්ගලික ආදායම් මාර්ගය",
  re_entered_education: "නැවත අධ්‍යාපනයට පිවිසීම",
  reason_not_in_labour_force: "රැකියාවේ නොයෙදීමට හෝ රැකියා නොසෙවීමට හේතුව",
  relatedness_at_institution: "ආයතනය සමඟ ඇති බැඳීම",
  sector_formality: "රැකියාවේ විධිමත්භාවය",
  study_motivation_type: "අධ්‍යයන අභිප්‍රේරණය",
  wants_further_edu: "අනාගත අධ්‍යාපන අභිප්‍රාය",
  wants_to_work_future: "අනාගත රැකියා අභිප්‍රාය",
  worked_while_studying: "ඉගෙනුම ලබන අතරතුර රැකියා කිරීම",
};

// Answer-option labels, keyed by the exact English label the backend serves.
export const SI_ANSWERS: Record<string, string> = {
  Median: "මධ්‍යස්ථය",
  "Intrinsic: genuinely passionate about the subject": "ස්වයං උනන්දුව (Intrinsic): විෂයට සැබෑ ආශාවක් ඇත",
  "Identified: aligned with own goals": "පුද්ගලික ඉලක්ක (Identified): තමන්ගේම ඉලක්කවලට ගැළපේ",
  "Introjected: avoid guilt or disappointing family": "අභ්‍යන්තර පීඩනය (Introjected): වරදකාරී හැඟීමක් හෝ පවුල කලකිරවීම වළක්වා ගැනීමට",
  "External: qualification required for a job": "බාහිර හේතු (External): රැකියාවකට අවශ්‍ය සුදුසුකමක් ලබාගැනීමට",
  "Amotivated/uncertain: following the path ended up on": "පැහැදිලි අරමුණක් නැත (Amotivated): අහම්බෙන් ලැබුණු මඟේ යමින් සිටී",
  "A great deal of choice and control": "තේරීමේ සහ පාලනයේ විශාල නිදහසක් ඇත",
  "Some flexibility within a mostly fixed curriculum": "බොහෝ දුරට ස්ථිර විෂය නිර්දේශයක් තුළ යම් නම්‍යශීලී බවක් ඇත",
  "Very little choice; prescribed and fixed": "ඉතා අඩු තේරීමක්; නියම කර ඇති, වෙනස් කළ නොහැකි",
  "No choice or control": "තේරීමක් හෝ පාලනයක් නැත",
  "Very capable and confident": "ඉතා දක්ෂ සහ ආත්මවිශ්වාසයෙන් යුතුයි",
  "Fairly capable with some gaps": "යම් අඩුපාඩු තිබුණත් හොඳින් කළ හැකියි",
  "Somewhat capable; struggles in some areas": "තරමක් දක්ෂයි; සමහර අංශවල අපහසුතා ඇත",
  "Not very capable; frequently out of depth": "එතරම් දක්ෂ නැත; නිතර දුෂ්කරතාවලට මුහුණ දෙයි",
  "Strongly connected and part of the community": "ශක්තිමත්ව බැඳී ඇති අතර ප්‍රජාවේ කොටසකි",
  "Some connections but not deeply involved": "යම් සම්බන්ධතා ඇති නමුත් ගැඹුරින් සම්බන්ධ නැත",
  "Weakly connected or isolated": "දුර්වල ලෙස බැඳී ඇත හෝ හුදෙකලායි",
  "No sense of belonging": "අයත් බවක් නොහැඟේ",
  "Below LKR 30,000": "රු. 30,000ට අඩු",
  "LKR 30,000 – 60,000": "රු. 30,000 – 60,000",
  "LKR 60,000 – 120,000": "රු. 60,000 – 120,000",
  "LKR 120,000 – 200,000": "රු. 120,000 – 200,000",
  "Above LKR 200,000": "රු. 200,000ට වැඩි",
  "Prefer not to say": "පැවසීමට අකමැතියි",
  "No — someone else is the main provider": "නැත — ප්‍රධාන ආදායම් සපයන්නා වෙනත් අයෙකි",
  "Shared — several people contribute roughly equally": "බෙදාගත් — කිහිප දෙනෙකු ආසන්න වශයෙන් සමානව දායක වෙති",
  "Yes — I provide the main household income": "ඔව් — නිවසේ ප්‍රධාන ආදායම මා සපයමි",
  "My regular job or business": "මගේ නිත්‍ය රැකියාව හෝ ව්‍යාපාරය",
  "Unemployment or social security benefits": "රැකියා විරහිත හෝ සමාජ ආරක්ෂණ ප්‍රතිලාභ",
  "An education grant, scholarship, or training allowance": "අධ්‍යාපන ප්‍රදානයක්, ශිෂ්‍යත්වයක් හෝ පුහුණු දීමනාවක්",
  "My parents or family": "මගේ දෙමාපියන් හෝ පවුල",
  "My partner or spouse": "මගේ ජීවන සහකරු/සහකාරිය",
  "Casual or informal work": "අනියම් හෝ අවිධිමත් රැකියා",
  "Other source": "වෙනත් මූලාශ්‍රයක්",
  "Government-funded or free of charge": "රජයේ අරමුදල් සහිත හෝ නොමිලේ",
  "Scholarship or grant": "ශිෂ්‍යත්වයක් හෝ ප්‍රදානයක්",
  "Paid for by my family": "මගේ පවුල විසින් ගෙවනු ලැබේ",
  "I pay from my own earnings": "මගේම ඉපැයීම්වලින් ගෙවමි",
  "Employer-sponsored": "සේවායෝජකයාගේ අනුග්‍රහයෙන්",
  "Other arrangement": "වෙනත් ක්‍රමයක්",
  "No schooling": "පාසල් අධ්‍යාපනයක් නැත",
  "Primary/Elementary (Grade 1–5)": "ප්‍රාථමික (1–5 ශ්‍රේණි)",
  "O/L level (Grade 9–11)": "සාමාන්‍ය පෙළ (O/L) (9–11 ශ්‍රේණි)",
  "A/L level (Grade 12–13)": "උසස් පෙළ (A/L) (12–13 ශ්‍රේණි)",
  "Vocational certificate / NVQ": "වෘත්තීය සහතිකය / NVQ",
  "Vocational certificate or NVQ": "වෘත්තීය සහතිකය හෝ NVQ",
  "Diploma": "ඩිප්ලෝමාව",
  "Bachelor's degree": "ප්‍රථම උපාධිය",
  "Post-graduate (Masters/PhD)": "පශ්චාත් උපාධි (ශාස්ත්‍රපති/දර්ශනසූරි)",
  "Post-graduate degree": "පශ්චාත් උපාධිය",
  "Do not know / prefer not to say": "නොදනී / පැවසීමට අකමැතියි",
  "Primary school": "ප්‍රාථමික පාසල",
  "O/L level": "සාමාන්‍ය පෙළ (O/L)",
  "A/L level": "උසස් පෙළ (A/L)",
  "Government school or state university": "රජයේ පාසලක් හෝ රාජ්‍ය විශ්වවිද්‍යාලයක්",
  "Government vocational/technical institute (NYSC, NAITA, VTA, etc.)": "රජයේ වෘත්තීය/තාක්ෂණික ආයතනයක් (NYSC, NAITA, VTA ආදිය)",
  "Private school or private degree-awarding institute": "පෞද්ගලික පාසලක් හෝ උපාධි පිරිනමන පෞද්ගලික ආයතනයක්",
  "International school or foreign university programme": "ජාත්‍යන්තර පාසලක් හෝ විදේශ විශ්වවිද්‍යාල වැඩසටහනක්",
  "Online or distance learning programme": "මාර්ගගත හෝ දුරස්ථ අධ්‍යාපන වැඩසටහනක්",
  "Other": "වෙනත්",
  "No": "නැත",
  "Yes": "ඔව්",
  "Very useful — directly relevant, employers value it": "ඉතා ප්‍රයෝජනවත් — සෘජුවම අදාළයි, සේවායෝජකයින් එය අගය කරති",
  "Somewhat useful — helps to some extent": "තරමක් ප්‍රයෝජනවත් — යම් ප්‍රමාණයකට උපකාරී වේ",
  "Not useful — little relevance to jobs I am looking for": "ප්‍රයෝජනවත් නැත — මා සොයන රැකියාවලට අදාළත්වය අඩුයි",
  "Do not know": "නොදනී",
  "Do not know yet": "තවම නොදනී",
  "No contract at all": "කිසිදු ගිවිසුමක් නැත",
  "Oral contract — permanent/unlimited": "වචනයෙන් කළ ගිවිසුම — ස්ථිර/කාල සීමාවක් නැති",
  "Oral contract — temporary (12–36 months)": "වචනයෙන් කළ ගිවිසුම — තාවකාලික (මාස 12–36)",
  "Oral contract — temporary (under 12 months)": "වචනයෙන් කළ ගිවිසුම — තාවකාලික (මාස 12ට අඩු)",
  "Written contract — permanent/unlimited": "ලිඛිත ගිවිසුම — ස්ථිර/කාල සීමාවක් නැති",
  "Written contract — temporary (12–36 months)": "ලිඛිත ගිවිසුම — තාවකාලික (මාස 12–36)",
  "Written contract — temporary (under 12 months)": "ලිඛිත ගිවිසුම — තාවකාලික (මාස 12ට අඩු)",
  "Very likely — my job is secure": "ඉතා ඉඩ ඇත — මගේ රැකියාව සුරක්ෂිතයි",
  "Likely but not certain — I have some concern": "ඉඩ ඇත, නමුත් නිශ්චිත නැත — මට යම් සැකයක් ඇත",
  "Not likely — I doubt I will still have this job": "ඉඩකඩ අඩුයි — මෙම රැකියාව තවදුරටත් තිබේදැයි මට සැකයි",
  "I do not know": "මම නොදනිමි",
  "Fully formal — registered employer, written contract, statutory benefits": "සම්පූර්ණයෙන්ම විධිමත් — ලියාපදිංචි සේවායෝජකයා, ලිඛිත ගිවිසුම, EPF/ETF වැනි නීතිමය ප්‍රතිලාභ",
  "Mostly formal — some documentation but not fully compliant": "බොහෝ දුරට විධිමත් — යම් ලියකියවිලි ඇති නමුත් සම්පූර්ණයෙන් අනුකූල නොවේ",
  "Mixed — some formal, some informal aspects": "මිශ්‍ර — සමහර අංග විධිමත්, සමහර අංග අවිධිමත්",
  "Fully informal — no documentation, cash only": "සම්පූර්ණයෙන්ම අවිධිමත් — ලියකියවිලි නැත, මුදලින් පමණි",
  "Own illness, injury, or pregnancy": "තමාගේ අසනීපය, තුවාලයක් හෝ ගැබ්ගැනීම",
  "Personal or family responsibilities (caring for children, elderly, etc.)": "පුද්ගලික හෝ පවුලේ වගකීම් (දරුවන්, වැඩිහිටියන් රැකබලා ගැනීම ආදිය)",
  "Currently in education or training": "දැනට අධ්‍යාපනය හෝ පුහුණුව ලබමින් සිටී",
  "Already found work to start in the future": "අනාගතයේ ආරම්භ කිරීමට රැකියාවක් දැනටමත් සොයාගෙන ඇත",
  "Already arranged self-employment to start in the future": "අනාගතයේ ආරම්භ කිරීමට ස්වයං රැකියාවක් දැනටමත් සූදානම් කර ඇත",
  "Awaiting recall to a former job": "පෙර රැකියාවට නැවත කැඳවනු ලැබීම බලාපොරොත්තුවෙන් සිටී",
  "Awaiting the busy season (seasonal worker)": "කාර්යබහුල කන්නය එනතුරු රැඳී සිටී (කන්නයට පමණක් වැඩ කරන අය)",
  "Believe there is no suitable work available in this area": "මෙම ප්‍රදේශයේ සුදුසු රැකියා නොමැති බව විශ්වාස කරයි",
  "I do not meet employers' requirements — feel I lack qualifications": "සේවායෝජකයින්ගේ අවශ්‍යතා සපුරන්නේ නැත — සුදුසුකම් මදි බව හැඟේ",
  "Could not find suitable work after trying": "උත්සාහ කළද සුදුසු රැකියාවක් සොයාගත නොහැකි විය",
  "Do not know how or where to look for work": "රැකියා සොයන්නේ කෙසේද හෝ කොතැනදැයි නොදනී",
  "Have not started looking yet": "තවම රැකියා සෙවීම ආරම්භ කර නැත",
  "Other reason": "වෙනත් හේතුවක්",
  "No — I have never worked": "නැත — මම කිසිදා රැකියා කර නැත",
  "Yes — I have worked before": "ඔව් — මම මීට පෙර රැකියා කර ඇත",
  "No — I do not want to work": "නැත — මට රැකියා කිරීමට අවශ්‍ය නැත",
  "Yes — I want to work at some point": "ඔව් — කිසියම් අවස්ථාවක රැකියා කිරීමට මට අවශ්‍යයි",
  "Not sure yet": "තවම විශ්වාස නැත",
};

export const SI_SECTORS: Record<string, string> = {
  "information technology and communications": "තොරතුරු තාක්ෂණය සහ සන්නිවේදනය",
  "manufacturing or production": "නිෂ්පාදන කර්මාන්තය",
  "agriculture, forestry, and fishing": "කෘෂිකර්මය, වන වගාව සහ ධීවර",
  "personal services (beauty, fitness, wellness)": "පුද්ගලික සේවා (රූපලාවණ්‍ය, ශාරීරික යෝග්‍යතාව, සුවතාව)",
  "hotels, restaurants, and hospitality": "හෝටල්, ආපනශාලා සහ ආගන්තුක සත්කාරය",
  "construction and building": "ඉදිකිරීම් සහ ගොඩනැගිලි",
  "creative, media, and arts": "නිර්මාණශීලී, මාධ්‍ය සහ කලා",
  "transport, storage, and logistics": "ප්‍රවාහනය, ගබඩා කිරීම සහ සැපයුම් කළමනාකරණය (logistics)",
  "wholesale, retail, or repair": "තොග, සිල්ලර හෝ අලුත්වැඩියා",
  "finance, banking, and insurance": "මූල්‍ය, බැංකු සහ රක්ෂණ",
  "education and teaching": "අධ්‍යාපනය සහ ඉගැන්වීම",
  "not sure": "තවම විශ්වාස නැත",
};

export const SI_SKILL_AREAS: Record<string, string> = {
  "ICT & Computing": "තොරතුරු තාක්ෂණය සහ පරිගණක",
  "Languages & Communication": "භාෂා සහ සන්නිවේදනය",
  "Automotive & Mechanical Engineering": "මෝටර් රථ සහ යාන්ත්‍රික ඉංජිනේරු",
  "Hospitality & Culinary Arts": "ආගන්තුක සත්කාරය සහ සූපවේදය",
  "Beauty, Fashion & Personal Care": "රූපලාවණ්‍ය, විලාසිතා සහ පුද්ගලික සත්කාරය",
  "Electrical & Electronics": "විදුලි සහ ඉලෙක්ට්‍රොනික",
  "Creative Arts, Design & Media": "නිර්මාණ කලා, සැලසුම් සහ මාධ්‍ය",
  "Construction & Surveying": "ඉදිකිරීම් සහ මිනින්දෝරු",
  "Agriculture & Environment": "කෘෂිකර්මය සහ පරිසරය",
  "Business, Management & Administration": "ව්‍යාපාර, කළමනාකරණ සහ පරිපාලන",
};

// Only skills with a reliable, widely used Sinhala trade name. All others
// (brand names, certification titles, national-diploma titles) stay English.
export const SI_SKILLS: Record<string, string> = {
  "Baker": "බේකරි ශිල්පී",
  "Beautician": "රූපලාවණ්‍ය ශිල්පී",
  "Hair Dresser": "කොණ්ඩ මෝස්තර ශිල්පී",
  "Tailor": "ඇඳුම් මසන්නා",
  "Electrician": "විදුලි කාර්මික",
  "Plumber": "ජලනල කාර්මික",
  "Welder": "වෑල්ඩින් කාර්මික",
  "Automobile Mechanic": "මෝටර් රථ කාර්මික",
  "Automobile Electrician": "මෝටර් රථ විදුලි කාර්මික",
  "Motorcycle Mechanic": "යතුරුපැදි කාර්මික",
  "Three Wheeler Mechanic": "ත්‍රිරෝද රථ කාර්මික",
  "Mobile Phone Repair Technician": "ජංගම දුරකථන අලුත්වැඩියා කාර්මික",
  "Refrigeration & Air Conditioning Technician": "ශීතකරණ සහ වායුසමීකරණ කාර්මික",
  "Electronic Appliances Technician": "ඉලෙක්ට්‍රොනික උපකරණ කාර්මික",
  "Computer Hardware Technician": "පරිගණක දෘඪාංග කාර්මික",
  "Computer Network Technician": "පරිගණක ජාල කාර්මික",
  "Computer Hardware And Network Technician": "පරිගණක දෘඪාංග සහ ජාල කාර්මික",
  "Web Designing": "වෙබ් අඩවි නිර්මාණය",
  "Professional Cookery": "වෘත්තීය සූපවේදය",
  "Cake Decorator": "කේක් සැරසිලි ශිල්පී",
  "Handycraft": "අත්කම් ශිල්පය",
  "Sinhala Language": "සිංහල භාෂාව",
  "Tamil Language": "දෙමළ භාෂාව",
  "Japanese Language": "ජපන් භාෂාව",
  "Korean Language": "කොරියානු භාෂාව",
  "French Language": "ප්‍රංශ භාෂාව",
  "Professional English": "වෘත්තීය ඉංග්‍රීසි",
  "Mass Communication": "ජනසන්නිවේදනය",
  "Preschool Teacher (Early Childhood Development)": "පෙරපාසල් ගුරු (මුල් ළමාවිය සංවර්ධනය)",
  "Graphics Designer": "ග්‍රැෆික් නිර්මාණ ශිල්පී",
  "Business Management": "ව්‍යාපාර කළමනාකරණය",
  "Human Resources Management": "මානව සම්පත් කළමනාකරණය",
  "Store Management": "ගබඩා කළමනාකරණය",
  "Construction Site Supervisor": "ඉදිකිරීම් භූමි අධීක්ෂක",
  "Quantity Surveying Assistant": "ප්‍රමාණ සමීක්ෂණ සහායක",
  "Survey Field Assistant": "මිනින්දෝරු ක්ෂේත්‍ර සහායක",
  "Field Assistant (Agricultural)": "කෘෂිකාර්මික ක්ෂේත්‍ර සහායක",
  "Landscape Development Assistant": "භූ දර්ශන සංවර්ධන සහායක",
  "Plant Nursery Development Assistant": "පැළ තවාන් සංවර්ධන සහායක",
  "Not sure yet": "තවම විශ්වාස නැත",
};

// q2–q5 option labels, keyed by the English value that is submitted unchanged.
export const SI_PROGRAMME_OPTIONS: Record<string, string> = {
  "Get a job": "රැකියාවක් ලබාගැනීමට",
  "Improve skills in my current job": "වත්මන් රැකියාවේ කුසලතා වර්ධනය කරගැනීමට",
  "Start my own business": "ස්වයං ව්‍යාපාරයක් ආරම්භ කිරීමට",
  "Continue on to further education": "වැඩිදුර අධ්‍යාපනය දිගටම කරගෙන යාමට",
  "Build general skills, not sure about the next step yet": "සාමාන්‍ය කුසලතා වර්ධනයට — ඊළඟ පියවර ගැන තවම විශ්වාස නැත",
  "Full-time, weekdays": "පූර්ණ කාලීන, සතියේ දිනවල",
  "Part-time, weekends": "අර්ධ කාලීන, සති අන්තයේ",
  "No strong preference": "විශේෂ කැමැත්තක් නැත",
  "Sinhala": "සිංහල",
  "English": "ඉංග්‍රීසි",
  "Yes, I want a formal NVQ or qualification": "ඔව්, නිල NVQ සහතිකයක් හෝ සුදුසුකමක් අවශ්‍යයි",
  "Not necessarily — I mainly want the practical skills": "අනිවාර්යයෙන්ම නැත — ප්‍රධාන වශයෙන් අවශ්‍ය ප්‍රායෝගික කුසලතායි",
  "Not sure": "විශ්වාස නැත",
};

export const SI_LANGUAGE_NAMES: Record<string, string> = {
  sinhala: "සිංහල",
  english: "ඉංග්‍රීසි",
  tamil: "දෙමළ",
};

export const SI_FINDING_TITLES: Record<string, string> = {
  "Already searching for work/business": "දැනටමත් රැකියා/ව්‍යාපාර අවස්ථා සොයමින්",
  "Connection to labour-market information/opportunities": "රැකියා අවස්ථා සහ තොරතුරු සමඟ ඇති සම්බන්ධතාව",
  "Current institution type": "වත්මන් ආයතන වර්ගය",
  "Current or preferred field of study": "වත්මන් හෝ කැමති අධ්‍යයන ක්ෂේත්‍රය",
  "Employment/training self-efficacy": "රැකියාවක්/පුහුණුවක් සොයාගැනීමට තමා කෙරෙහි ඇති විශ්වාසය (self-efficacy)",
  "Ever worked for pay/profit": "කවදා හෝ වැටුප්/ලාභ සඳහා රැකියා කර තිබීම",
  "Expected support for work/study engagement": "රැකියා/අධ්‍යයන කටයුතු සඳහා අපේක්ෂිත සහාය",
  "Future orientation": "අනාගතය පිළිබඳ නැඹුරුව",
  "Helpfulness of job-search contacts": "රැකියා සෙවීමේ සම්බන්ධතාවල ප්‍රයෝජනවත්භාවය",
  "Hopes to change job": "රැකියාව වෙනස් කිරීමේ බලාපොරොත්තුව",
  "Household income band": "ගෘහස්ථ ආදායම් පරාසය",
  "Household size": "නිවසේ සාමාජික සංඛ්‍යාව",
  "How current programme was accessed": "වත්මන් පාඨමාලාවට පිවිසි ආකාරය",
  "Ideal sector": "කැමතිම රැකියා ක්ෂේත්‍රය",
  "Job-acceptance conditions": "රැකියාවක් පිළිගැනීමේ කොන්දේසි",
  "Lives in the same area where they grew up": "හැදී වැඩුණු ප්‍රදේශයේම ජීවත් වීම",
  "Main education funding source": "ප්‍රධාන අධ්‍යාපන අරමුදල් මූලාශ්‍රය",
  "Main job-search method while studying": "ඉගෙනුම ලබන අතරතුර ප්‍රධාන රැකියා සෙවීමේ ක්‍රමය",
  "Minimum acceptable wage band": "පිළිගත හැකි අවම වැටුප් පරාසය",
  "Minimum education believed necessary for a decent job": "යහපත් රැකියාවකට අවශ්‍ය යැයි විශ්වාස කරන අවම අධ්‍යාපනය",
  "Monthly work-income band": "මාසික රැකියා ආදායම් පරාසය",
  "Most important life goal": "වඩාත් වැදගත් ජීවිත ඉලක්කය",
  "Number of applications": "ඉදිරිපත් කළ අයදුම්පත් සංඛ්‍යාව",
  "Overall job satisfaction": "සමස්ත රැකියා තෘප්තිය",
  "Primary personal income source": "ප්‍රධාන පුද්ගලික ආදායම් මාර්ගය",
  "Primary recent search method": "මෑත කාලයේ ප්‍රධාන රැකියා සෙවීමේ ක්‍රමය",
  "Primary-earner status": "ප්‍රධාන ආදායම් උපයන්නාගේ තත්ත්වය",
  "Received training for current job": "වත්මන් රැකියාව සඳහා පුහුණුව ලැබීම",
  "Recent education status": "මෑත අධ්‍යාපන තත්ත්වය",
  "Social support for job search": "රැකියා සෙවීම සඳහා සමාජ සහාය",
  "Type of work while studying": "ඉගෙනුම ලබන අතරතුර කළ රැකියා වර්ගය",
  "Useful employment/training contacts": "ප්‍රයෝජනවත් රැකියා/පුහුණු සම්බන්ධතා",
  "Who paid for training": "පුහුණුව සඳහා ගෙවූයේ කවුද",
};

// Fixed explanatory notes and cautions from the bundled evidence libraries.
export const SI_EVIDENCE_TEXT: Record<string, string> = {
  "The final comparison output retained this answer-level contrast but did not store the complete answer-category distribution. Only the verified comparison is shown.":
    "අවසන් විශ්ලේෂණයේ සුරැකුණේ මෙම පිළිතුර සඳහා වූ සංසන්දනය පමණි; සියලු පිළිතුරුවල සම්පූර්ණ බෙදීම සුරැකී නැත. එබැවින් තහවුරු කළ සංසන්දනය පමණක් දැක්වේ.",
  "Complete observed response distributions were available for every profile in this model.":
    "මෙම ආකෘතියේ සෑම කාණ්ඩයක් සඳහාම සියලු පිළිතුරු බෙදී ගිය ආකාරය සම්පූර්ණයෙන් ලබාගත හැකි විය.",
  "The final analysis stored medians and interquartile ranges rather than answer-category percentages.":
    "අවසන් විශ්ලේෂණයේ සුරැකුණේ එක් එක් පිළිතුරේ ප්‍රතිශත නොව, මධ්‍යස්ථ අගය (median) සහ IQR පරාසය පමණි.",
  "Numeric values are shown as profile summaries; no arbitrary bins were created.":
    "සංඛ්‍යාත්මක අගයන් එක් එක් කාණ්ඩයේ සාරාංශයක් ලෙස දැක්වේ; අගයන් අහඹු ලෙස කොටස්වලට බෙදා නැත.",
  "Percentages are within-profile percentages from the final model population.":
    "ප්‍රතිශත ගණනය කර ඇත්තේ එක් එක් කාණ්ඩයේ සිටි අය අතරින් ය.",
  "This is a retained descriptive pattern, not an FDR-supported result.":
    "මෙය විස්තරාත්මක රටාවක් පමණි; සංඛ්‍යානමය වශයෙන් (FDR) තහවුරු කළ ප්‍රතිඵලයක් නොවේ.",
  "Some response cells were sparse; interpret the pattern cautiously.":
    "සමහර පිළිතුරු තෝරාගත්තේ ඉතා ස්වල්ප දෙනෙකි; මෙම රටාව ප්‍රවේශමෙන් තේරුම් ගන්න.",
  "This question used an eligible-subgroup denominator.":
    "මෙම ප්‍රශ්නයේ ප්‍රතිශත ගණනය කළේ ප්‍රශ්නය අදාළ වූ අය අතරින් පමණි.",
  "The eligible sample was small.":
    "ප්‍රශ්නය අදාළ වූ අයගේ සංඛ්‍යාව කුඩා විය.",
};

export const SI_MODEL_JUDGMENTS: Record<string, string> = {
  "NEEDS REVIEW": "සමාලෝචනය අවශ්‍යයි (NEEDS REVIEW)",
  "SAFE for new-user nearest-medoid assignment": "නව සාමාජිකයින් පැවරීමට ආරක්ෂිතයි (SAFE)",
};

// Fixed backend messages (public error strings and the deterministic
// no-recommendation reason). AI-written reasons are not listed and stay English.
export const SI_SERVICE_MESSAGES: Record<string, string> = {
  "Programme recommendation service is temporarily unavailable.":
    "වැඩසටහන් නිර්දේශ සේවාව තාවකාලිකව ලබාගත නොහැක.",
  "Programme recommendation service timed out. Please try again.":
    "වැඩසටහන් නිර්දේශ සේවාවේ ප්‍රතිචාර කාලය ඉක්මවිය. කරුණාකර නැවත උත්සාහ කරන්න.",
  "Programme recommendation service returned an invalid response.":
    "වැඩසටහන් නිර්දේශ සේවාවෙන් වලංගු නොවන ප්‍රතිචාරයක් ලැබිණි.",
  "No programme remained after checking the model output against the member's answers and governed course evidence.":
    "AI ප්‍රතිඵල සාමාජිකයාගේ පිළිතුරු සහ අනුමත පාඨමාලා තොරතුරු සමඟ පරීක්ෂා කිරීමෙන් පසු සුදුසු වැඩසටහනක් ඉතිරි නොවීය.",
};

// Entries a native Sinhala speaker should confirm before wider use. Keys
// reference the tables above; this list is informational only.
export const SI_REVIEW_FLAGS: string[] = [
  "SI_PROFILES.D_motivation_p3.name — 'connected' rendered neutrally as 'සබඳතා සහිත'",
  "SI_PROFILES.G_economic_role_p2.name — 'Self-income provider or contributor'",
  "SI_PROFILES.G_future_engagement_p1.name — 'Work-and-education engaged'",
  "SI_PROFILES.G_future_engagement_p2.name — 'Low or uncertain future engagement'",
  "SI_ANSWERS — five SDT study-motivation options (Intrinsic/Identified/Introjected/External/Amotivated)",
  "SI_FINDING_TITLES — 'Employment/training self-efficacy'",
  "SI_SECTORS — 'transport, storage, and logistics'",
  "SI_SKILLS — all trade-name translations",
  "messages.si — statistical labels (silhouette/ARI/PAC, FDR, effect size, IQR)",
];

// Sinhala rendering of the teaching library's simple_conclusion sentences.
// The library generates them from a small set of fixed English templates, so
// each sentence is parsed and rebuilt in Sinhala with the quoted answer and
// profile names translated by the caller (answers come from the original
// survey's Sinhala wording). A sentence that does not match a known template
// returns null so the caller can fall back to the English text.

export interface ConclusionTranslators {
  answer: (english: string) => string;
  profileName: (english: string) => string;
}

const DEGREES: Record<string, string> = {
  slightly: "ස්වල්ප වශයෙන්",
  somewhat: "තරමක්",
  noticeably: "කැපී පෙනෙන ලෙස",
  much: "බෙහෙවින්",
};

const MEDIAN_SUBJECTS: Record<string, string> = {
  "household size": "නිවසේ සාමාජික සංඛ්‍යාවේ",
  "number of applications": "රැකියා අයදුම්පත් සංඛ්‍යාවේ",
};

// Short work-type phrases used by the worked-while-studying conclusions,
// mapped to the survey's own Sinhala option wording.
const WORK_TYPES: Record<string, string> = {
  "a private-company internship or apprenticeship": "පෞද්ගලික සමාගමක සීමාවාසික පුහුණුවක්",
  "ordinary paid work in a private company": "සමාගමේ වැටුප් සහිත රැකියාවක් (ඉන්ටර්න් නොවේ)",
};

function firstSentence(sentence: string, t: ConclusionTranslators): string | null {
  let m = sentence.match(/^None of the (\d+) (eligible )?members \(([\d.]+)%\) selected “(.+)”\.$/);
  if (m) {
    const [, n, eligible, pct, answer] = m;
    return `${eligible ? "ප්‍රශ්නයට අදාළ " : ""}සාමාජිකයින් ${n} දෙනාගෙන් කිසිවෙකු (${pct}%) “${t.answer(answer)}” තෝරා නැත.`;
  }
  m = sentence.match(/^(Only )?(\d+) of (\d+) (eligible )?members \(([\d.]+)%\) selected “(.+)”\.$/);
  if (m) {
    const [, only, count, n, eligible, pct, answer] = m;
    const who = `${eligible ? "ප්‍රශ්නයට අදාළ " : ""}සාමාජිකයින් ${n} දෙනාගෙන්`;
    return `${who} ${count} දෙනෙකු${only ? " පමණක්" : ""} (${pct}%) “${t.answer(answer)}” තෝරා ඇත.`;
  }
  return null;
}

function comparisonSentence(sentence: string, t: ConclusionTranslators): string | null {
  let m = sentence.match(/^In the other profiles in this model collectively, ([\d.]+)% selected the same answer\.$/);
  if (m) return `මෙම ආකෘතියේ අනෙක් කාණ්ඩ සියල්ල එකට ගත් විට, ${m[1]}% ක් එම පිළිතුරම තෝරා ඇත.`;
  m = sentence.match(/^In the “(.+)” profile, ([\d.]+)% selected the same answer\.$/);
  if (m) return `“${t.profileName(m[1])}” කාණ්ඩයේ ${m[2]}% ක් එම පිළිතුරම තෝරා ඇත.`;
  return null;
}

function strengthSentence(sentence: string): string | null {
  const m = sentence.match(/^This response was (slightly|somewhat|noticeably|much) (more|less) common in this historical profile\.$/);
  if (!m) return null;
  const direction = m[2] === "more" ? "වැඩියෙන්" : "අඩුවෙන්";
  return `මෙම පිළිතුර මෙම ඓතිහාසික කාණ්ඩයේ ${DEGREES[m[1]]} ${direction} දක්නට ලැබිණි.`;
}

function translateMedian(text: string, t: ConclusionTranslators): string | null {
  const m = text.match(
    /^The median (.+?) was ([\d.]+) in this profile and ([\d.]+) in the “(.+)” profile\. The typical value was (higher|lower) here\.$/,
  );
  if (!m || !MEDIAN_SUBJECTS[m[1]]) return null;
  const [, subject, here, there, profile, direction] = m;
  return (
    `මෙම කාණ්ඩයේ ${MEDIAN_SUBJECTS[subject]} මධ්‍යස්ථය ${here} වූ අතර “${t.profileName(profile)}” කාණ්ඩයේ එය ${there} විය. ` +
    `සාමාන්‍ය අගය මෙහි ${direction === "higher" ? "වැඩි" : "අඩු"} විය.`
  );
}

function translateWorkedWhileStudying(text: string): string | null {
  const prefix = "Among members who worked while studying, ";
  if (!text.startsWith(prefix)) return null;
  const body = text.slice(prefix.length);
  const work = (phrase: string) => WORK_TYPES[phrase] ?? null;

  let m = body.match(/^(\d+) of (\d+) \(([\d.]+)%\) had (.+?)\. This was the main form of earlier work experience in this historical profile\.$/);
  if (m && work(m[4])) {
    return (
      `ඉගෙනුම ලබන අතරතුර වැඩ කළ සාමාජිකයින් ${m[2]} දෙනාගෙන් ${m[1]} දෙනෙකුට (${m[3]}%) තිබුණේ “${work(m[4])}” ය. ` +
      "මෙම ඓතිහාසික කාණ්ඩයේ පෙර වැඩ අත්දැකීමේ ප්‍රධාන ආකාරය මෙය විය."
    );
  }
  m = body.match(/^(\d+) of (\d+) \(([\d.]+)%\) had (.+?), while (\d+) of \d+ \(([\d.]+)%\) had (.+?)\.$/);
  if (m && work(m[4]) && work(m[7])) {
    return (
      `ඉගෙනුම ලබන අතරතුර වැඩ කළ සාමාජිකයින් ${m[2]} දෙනාගෙන් ${m[1]} දෙනෙකුට (${m[3]}%) “${work(m[4])}” තිබූ අතර, ` +
      `${m[5]} දෙනෙකුට (${m[6]}%) “${work(m[7])}” තිබුණි.`
    );
  }
  return null;
}

export function translateConclusionToSinhala(text: string, t: ConclusionTranslators): string | null {
  const special = translateMedian(text, t) ?? translateWorkedWhileStudying(text);
  if (special) return special;

  const sentences = text.trim().split(/(?<=\.)\s+(?=[A-Z])/);
  if (sentences.length !== 3) return null;
  const first = firstSentence(sentences[0], t);
  const second = comparisonSentence(sentences[1], t);
  const third = strengthSentence(sentences[2]);
  return first && second && third ? `${first} ${second} ${third}` : null;
}

import fs from "node:fs/promises";
import vm from "node:vm";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const sourcePath = new URL("../index.html", import.meta.url);
const outputDir = new URL("../outputs/card_catalog/", import.meta.url);
const outputPath = new URL("iron_and_gears_card_catalog.xlsx", outputDir);

function extractTemplates(html) {
  const marker = "const TEMPLATES =";
  const markerIndex = html.indexOf(marker);
  if (markerIndex < 0) throw new Error("Could not find TEMPLATES in HTML.");

  const arrayStart = html.indexOf("[", markerIndex);
  if (arrayStart < 0) throw new Error("Could not find TEMPLATES array start.");

  let depth = 0;
  let inString = false;
  let stringQuote = "";
  let escaped = false;
  let inLineComment = false;
  let inBlockComment = false;

  for (let i = arrayStart; i < html.length; i++) {
    const ch = html[i];
    const next = html[i + 1];

    if (inLineComment) {
      if (ch === "\n") inLineComment = false;
      continue;
    }
    if (inBlockComment) {
      if (ch === "*" && next === "/") {
        inBlockComment = false;
        i++;
      }
      continue;
    }
    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (ch === "\\") {
        escaped = true;
      } else if (ch === stringQuote) {
        inString = false;
      }
      continue;
    }

    if (ch === "/" && next === "/") {
      inLineComment = true;
      i++;
      continue;
    }
    if (ch === "/" && next === "*") {
      inBlockComment = true;
      i++;
      continue;
    }
    if (ch === '"' || ch === "'" || ch === "`") {
      inString = true;
      stringQuote = ch;
      continue;
    }
    if (ch === "[") depth++;
    if (ch === "]") {
      depth--;
      if (depth === 0) {
        const arrayLiteral = html.slice(arrayStart, i + 1);
        return vm.runInNewContext(`(${arrayLiteral})`, Object.create(null), {
          timeout: 1000,
        });
      }
    }
  }

  throw new Error("Could not find TEMPLATES array end.");
}

function abilityTags(card) {
  const tags = [];
  if (card.taunt) tags.push("攔截");
  if (card.battlecry) tags.push("部署");
  if (card.deathrattle) tags.push("報廢");
  if (card.endOfTurn) tags.push("回合結束");
  return tags.join("、");
}

function countBy(cards, key) {
  const counts = new Map();
  for (const card of cards) {
    const value = card[key] ?? "";
    counts.set(value, (counts.get(value) ?? 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => Number(a[0]) - Number(b[0]));
}

const html = await fs.readFile(sourcePath, "utf8");
const cards = extractTemplates(html);

const rows = cards.map((card, index) => [
  index + 1,
  card.name,
  card.cost,
  card.atk,
  card.hp,
  card.text || "",
  abilityTags(card),
  card.portrait || "",
  card.battlecry ? "是" : "",
  card.bcType || "",
  card.deathrattle ? "是" : "",
  card.drType || "",
  card.endOfTurn ? "是" : "",
  card.eotType || "",
]);

const workbook = Workbook.create();
const cardsSheet = workbook.worksheets.getOrAdd("卡牌清單", {
  renameFirstIfOnlyNewSpreadsheet: true,
});
cardsSheet.reset();

cardsSheet.getRange("A1:N1").values = [["Iron & Gears 目前卡牌清單", "", "", "", "", "", "", "", "", "", "", "", "", ""]];
cardsSheet.getRange("A2:N2").values = [[
  `來源：index.html｜卡牌總數：${cards.length}`,
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
]];
cardsSheet.getRange("A4:N4").values = [[
  "序號",
  "卡牌名稱",
  "費用",
  "攻擊",
  "生命",
  "卡牌效果",
  "能力標籤",
  "圖像代碼",
  "部署",
  "部署代碼",
  "報廢",
  "報廢代碼",
  "回合結束",
  "回合結束代碼",
]];
cardsSheet.getRange(`A5:N${rows.length + 4}`).values = rows;

cardsSheet.getRange("A1:N1").format = {
  fill: "#2B1A0D",
  font: { name: "Microsoft JhengHei", size: 16, bold: true, color: "#F4D48A" },
  verticalAlignment: "center",
};
cardsSheet.getRange("A2:N2").format = {
  fill: "#3B2611",
  font: { name: "Microsoft JhengHei", size: 10, color: "#E8CFA2" },
};
cardsSheet.getRange("A4:N4").format = {
  fill: "#B07830",
  font: { name: "Microsoft JhengHei", size: 10, bold: true, color: "#1E1006" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "outside", style: "thin", color: "#6D431A" },
};
cardsSheet.getRange(`A5:N${rows.length + 4}`).format = {
  font: { name: "Microsoft JhengHei", size: 10, color: "#22160E" },
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "inside", style: "thin", color: "#E2D3BF" },
};
cardsSheet.getRange(`A5:A${rows.length + 4}`).format.horizontalAlignment = "center";
cardsSheet.getRange(`C5:E${rows.length + 4}`).format.horizontalAlignment = "center";
cardsSheet.getRange(`I5:I${rows.length + 4}`).format.horizontalAlignment = "center";
cardsSheet.getRange(`K5:K${rows.length + 4}`).format.horizontalAlignment = "center";
cardsSheet.getRange(`M5:M${rows.length + 4}`).format.horizontalAlignment = "center";
cardsSheet.getRange("A:A").format.columnWidthPx = 54;
cardsSheet.getRange("B:B").format.columnWidthPx = 150;
cardsSheet.getRange("C:E").format.columnWidthPx = 54;
cardsSheet.getRange("F:F").format.columnWidthPx = 290;
cardsSheet.getRange("G:G").format.columnWidthPx = 110;
cardsSheet.getRange("H:H").format.columnWidthPx = 90;
cardsSheet.getRange("I:N").format.columnWidthPx = 96;
cardsSheet.freezePanes.freezeRows(4);

const summarySheet = workbook.worksheets.add("統計摘要");
summarySheet.getRange("A1:F1").values = [["Iron & Gears 卡牌統計", "", "", "", "", ""]];
summarySheet.getRange("A3:B8").values = [
  ["項目", "數量"],
  ["卡牌總數", cards.length],
  ["有攔截", cards.filter((c) => c.taunt).length],
  ["有部署效果", cards.filter((c) => c.battlecry).length],
  ["有報廢效果", cards.filter((c) => c.deathrattle).length],
  ["有回合結束效果", cards.filter((c) => c.endOfTurn).length],
];
summarySheet.getRange("D3:E3").values = [["費用", "張數"]];
const costRows = countBy(cards, "cost");
summarySheet.getRange(`D4:E${costRows.length + 3}`).values = costRows;
summarySheet.getRange("A1:F1").format = {
  fill: "#2B1A0D",
  font: { name: "Microsoft JhengHei", size: 16, bold: true, color: "#F4D48A" },
};
summarySheet.getRange("A3:B3").format = summarySheet.getRange("D3:E3").format = {
  fill: "#B07830",
  font: { name: "Microsoft JhengHei", size: 10, bold: true, color: "#1E1006" },
  horizontalAlignment: "center",
};
summarySheet.getRange("A4:B8").format = {
  font: { name: "Microsoft JhengHei", size: 10, color: "#22160E" },
  borders: { preset: "inside", style: "thin", color: "#E2D3BF" },
};
summarySheet.getRange(`D4:E${costRows.length + 3}`).format = {
  font: { name: "Microsoft JhengHei", size: 10, color: "#22160E" },
  horizontalAlignment: "center",
  borders: { preset: "inside", style: "thin", color: "#E2D3BF" },
};
summarySheet.getRange("A:A").format.columnWidthPx = 160;
summarySheet.getRange("B:B").format.columnWidthPx = 80;
summarySheet.getRange("D:E").format.columnWidthPx = 80;

await fs.mkdir(outputDir, { recursive: true });

const lastDataRow = rows.length + 4;

const catalogInspect = await workbook.inspect({
  kind: "table",
  range: `卡牌清單!A4:N${lastDataRow}`,
  include: "values",
  tableMaxRows: rows.length + 1,
  tableMaxCols: 14,
});
console.log(catalogInspect.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "formula error scan",
});
console.log(errors.ndjson);

await workbook.render({ sheetName: "卡牌清單", range: `A1:N${lastDataRow}`, scale: 0.8 });
await workbook.render({ sheetName: "統計摘要", range: "A1:F12", scale: 1 });

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath.pathname);

console.log(`Saved ${outputPath.pathname}`);

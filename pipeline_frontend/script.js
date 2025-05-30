async function loadDictionaries() {
  console.log("📥 Загрузка справочников...");

  const industrySelect = document.getElementById("industry");
  const goalSelect = document.getElementById("goalSelect");
  const sourcesContainer = document.getElementById("sourcesContainer");

  const [industriesRes, sourcesRes, goalsRes] = await Promise.all([
    fetch("http://127.0.0.1:8002/dictionaries/industries"),
    fetch("http://127.0.0.1:8002/dictionaries/sources"),
    fetch("http://127.0.0.1:8002/goals/")
  ]);

  const industries = await industriesRes.json();
  const sources = await sourcesRes.json();
  const goals = await goalsRes.json();

  industries.forEach(industry => {
    const option = document.createElement("option");
    option.value = industry.name;
    option.textContent = industry.name;
    industrySelect.appendChild(option);
  });

  goals.forEach(goal => {
    const option = document.createElement("option");
    option.value = goal.id;
    option.textContent = goal.name;
    goalSelect.appendChild(option);
  });

  sourcesContainer.innerHTML = "";
sources.forEach(source => {
  const div = document.createElement("div");
  div.classList.add("source-item");
  div.textContent = source.name;
  div.dataset.name = source.name;

  div.addEventListener("click", () => {
    div.classList.toggle("selected");
  });

  sourcesContainer.appendChild(div);
});

  console.log("✅ Справочники загружены");
}

document.addEventListener("DOMContentLoaded", loadDictionaries);

document.getElementById("recommendationForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const selectedSources = Array.from(document.querySelectorAll('.source-item.selected'))
                             .map(el => el.dataset.name);

  const data = {
    goal_id: parseInt(document.getElementById("goalSelect").value),
    industry: form.industry.value,
    scale: form.scale.value,
    budget_level: form.budget_level.value,
    sources: selectedSources
  };

  console.log("🔍 Отправляем данные:", data);

  const response = await fetch("http://127.0.0.1:8002/recommendations/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  // 🔧 Инструменты по категориям
  const toolsList = document.getElementById("toolsList");
toolsList.innerHTML = "";

const categorized = {};
result.tools.forEach(tool => {
  const [name, category] = tool.split("::");
  if (!categorized[category]) categorized[category] = [];
  categorized[category].push(name);
});

for (const category in categorized) {
  const catHeader = document.createElement("h4");
  catHeader.textContent = category;
  toolsList.appendChild(catHeader);

  const ul = document.createElement("ul");
  categorized[category].forEach(toolName => {
    const li = document.createElement("li");

    // ссылка-инструмент
    const span = document.createElement("span");
    span.textContent = toolName;
    span.classList.add("tool-link");
    span.dataset.name = toolName;
    span.style.cursor = "pointer";
    span.style.color = "#0066cc";
    span.style.textDecoration = "underline";

    // div для деталей
    const details = document.createElement("div");
    details.className = "tool-details hidden";
    details.id = `details-${toolName.replace(/\s/g, "_")}`;

    li.appendChild(span);
    li.appendChild(details);
    ul.appendChild(li);
  });
  toolsList.appendChild(ul);
}

// 🔄 Привязка обработчиков после отрисовки
document.querySelectorAll(".tool-link").forEach(el => {
  el.addEventListener("click", async function () {
    const toolName = this.dataset.name;
    const detailsDiv = document.getElementById(`details-${toolName.replace(/\s/g, "_")}`);

    // Скрыть, если уже открыт
    if (!detailsDiv.classList.contains("hidden")) {
      detailsDiv.classList.add("hidden");
      detailsDiv.innerHTML = "";
      return;
    }

    try {
      const res = await fetch(`http://127.0.0.1:8002/recommendations/tool_info/${encodeURIComponent(toolName)}`);
      const tool = await res.json();

      detailsDiv.innerHTML = `
        <p><strong>Описание:</strong> ${tool.description || "Нет описания"}</p>
        <p><strong>Доступен в РФ:</strong> ${tool.available_in_russia ? "✅ Да" : "❌ Нет"}</p>
        <p><strong>Сайт:</strong> ${tool.site ? `<a href="${tool.site}" target="_blank">${tool.site}</a>` : "Не указан"}</p>
      `;
      detailsDiv.classList.remove("hidden");
    } catch (err) {
      detailsDiv.innerHTML = `<p>❌ Информация не найдена</p>`;
      detailsDiv.classList.remove("hidden");
    }
  });
});
  // 📡 Источники из блоков
  const sourcesList = document.getElementById("sourcesList");
  sourcesList.innerHTML = result.sources.map(s => `<li>${s}</li>`).join("");

  // 📊 Этапы анализа
  const blocksList = document.getElementById("blocksList");
  blocksList.innerHTML = "";
  result.blocks.forEach(b => {
    const li = document.createElement("li");
    li.innerHTML = `<strong>${b.stage}:</strong> ${b.description}`;
    blocksList.appendChild(li);
  });

  document.getElementById("results").classList.remove("hidden");

  // Добавляем обработчики
document.querySelectorAll(".tool-link").forEach(el => {
  el.addEventListener("click", async function () {
    const toolName = this.dataset.name;
    const detailsDiv = document.getElementById(`details-${toolName.replace(/\s/g, "_")}`);

    if (!detailsDiv.classList.contains("hidden")) {
      detailsDiv.classList.add("hidden");
      detailsDiv.innerHTML = "";
      return;
    }

    const res = await fetch(`http://127.0.0.1:8002/tool_info/${encodeURIComponent(toolName)}`);
    const tool = await res.json();

    detailsDiv.innerHTML = `
      <p><strong>Описание:</strong> ${tool.description || "Нет описания"}</p>
      <p><strong>Доступен в РФ:</strong> ${tool.available_in_russia ? "✅ Да" : "❌ Нет"}</p>
      <p><strong>Сайт:</strong> ${tool.site ? `<a href="${tool.site}" target="_blank">${tool.site}</a>` : "Не указан"}</p>
    `;
    detailsDiv.classList.remove("hidden");
  });
});
});

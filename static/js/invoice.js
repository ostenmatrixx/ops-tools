document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("add-item");
  const container = document.getElementById("line-items");

  if (!addBtn || !container) return;

  addBtn.addEventListener("click", () => {
    const row = document.createElement("div");
    row.className = "line-item";
    row.innerHTML = `
      <input type="text" name="item_description" placeholder="Description" required />
      <input type="number" name="item_amount" placeholder="Amount" step="0.01" required />
    `;
    container.appendChild(row);
  });
});

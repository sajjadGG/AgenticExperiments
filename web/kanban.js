
window.addEventListener('load', () => {
    const data = window.openai.toolOutput.structuredContent;
    const kanbanRoot = document.getElementById('kanban-root');

    data.columns.forEach(column => {
        const columnEl = document.createElement('div');
        columnEl.className = 'column';
        columnEl.innerHTML = `<div class="column-title">${column.title}</div>`;

        column.tasks.forEach(task => {
            const cardEl = document.createElement('div');
            cardEl.className = 'card';
            cardEl.innerHTML = `
                <div class="card-title">${task.title}</div>
                <div class="card-assignee">${task.assignee}</div>
            `;
            columnEl.appendChild(cardEl);
        });

        kanbanRoot.appendChild(columnEl);
    });
});

const API_BASE = "/api";

// Tab Switching
document.querySelectorAll('.sidebar li').forEach(li => {
    li.addEventListener('click', () => {
        document.querySelector('.sidebar li.active').classList.remove('active');
        li.classList.add('active');

        const tab = li.getAttribute('data-tab');
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        document.getElementById(`${tab}-tab`).classList.add('active');

        const titles = { chats: "실시간 상담 내역", knowledge: "지식 베이스 관리", agent: "에이전트 상담 테스트" };
        document.getElementById('tab-title').innerText = titles[tab];

        if (tab === 'chats') loadChats();
    });
});

// Load Chats
async function loadChats(category = "전체") {
    const listEl = document.getElementById('chat-list');
    try {
        const res = await fetch(`${API_BASE}/chats?category=${encodeURIComponent(category)}`);
        const chats = await res.json();

        listEl.innerHTML = chats.map(chat => `
            <div class="chat-item" onclick="viewChat('${chat.chatId}')">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px">
                    <h4 style="margin: 0">ID: ${chat.chatId}</h4>
                    <span class="badge" style="background: var(--glass); font-size: 0.7rem; padding: 2px 8px; border-radius: 10px">${chat.category}</span>
                </div>
                <p>User: ${chat.userId}</p>
                <p>${chat.lastMessage}</p>
            </div>
        `).join('');

    } catch (err) {
        listEl.innerHTML = `<div class="error">로드 실패: ${err.message}</div>`;
    }
}

function filterCategory(category) {
    document.querySelectorAll('.category-filter button').forEach(btn => {
        btn.classList.toggle('active', btn.innerText === category || (btn.innerText === '스팸' && category === '스팸함'));
    });
    loadChats(category);
}

async function viewChat(chatId) {
    const detailEl = document.getElementById('chat-detail');
    detailEl.innerHTML = '<div class="loading">불러오는 중...</div>';

    const res = await fetch(`${API_BASE}/chats`);
    const chats = await res.json();
    const chat = chats.find(c => c.chatId === chatId);

    detailEl.innerHTML = `
        <div style="padding: 2rem; border-bottom: 1px solid var(--border)">
            <h3>상담 상세: ${chat.chatId}</h3>
        </div>
        <div style="flex: 1; overflow-y: auto; padding: 2rem; display: flex; flex-direction: column">
            ${chat.messages.map(m => {
        let content = m.content;
        if (m.msg_type === 'image') {
            content = `<img src="${m.media_url}" style="max-width: 100%; border-radius: 10px; margin-top: 5px;" alt="image">`;
        } else if (m.msg_type === 'file') {
            content = `<div class="file-link"><i class="fas fa-file"></i> <a href="${m.media_url}" target="_blank">${m.file_name || '파일 보기'}</a></div>`;
        } else if (m.msg_type === 'composite') {
            content = `
                        <div class="composite-card">
                            ${m.media_url ? `<img src="${m.media_url}" style="width: 100%; border-radius: 8px 8px 0 0">` : ''}
                            <div style="padding: 10px">${m.content.replace(/\n/g, '<br>')}</div>
                        </div>
                    `;
        } else {
            // URL 자동 링크 처리
            content = content.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
        }

        return `
                    <div class="chat-bubble ${m.sender}">
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px">${m.sender} | ${m.timestamp}</div>
                        ${content}
                    </div>
                `;
    }).join('')}
        </div>
    `;
}

// Knowledge Management
async function addManualKnowledge() {
    const q = document.getElementById('kb-q').value;
    const a = document.getElementById('kb-a').value;
    if (!q || !a) return alert("필드를 입력하세요.");

    try {
        const res = await fetch(`${API_BASE}/knowledge/manual`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: q, answer: a })
        });
        if (res.ok) {
            alert("지식이 성공적으로 추가되었습니다.");
            document.getElementById('kb-q').value = "";
            document.getElementById('kb-a').value = "";
        }
    } catch (err) { alert("오류 발생: " + err.message); }
}

async function addUrlKnowledge() {
    const url = document.getElementById('kb-url').value;
    if (!url) return alert("URL을 입력하세요.");

    alert("학습을 시작합니다. 잠시만 기다려주세요...");
    try {
        const res = await fetch(`${API_BASE}/knowledge/url`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });
        if (res.ok) alert("URL 학습이 완료되었습니다.");
    } catch (err) { alert("학습 오류: " + err.message); }
}

// Agent Chat
async function queryAgent() {
    const input = document.getElementById('agent-query');
    const query = input.value;
    if (!query) return;

    const messages = document.getElementById('agent-messages');
    messages.innerHTML += `<div class="msg user">${query}</div>`;
    input.value = "";
    messages.scrollTop = messages.scrollHeight;

    try {
        const res = await fetch(`${API_BASE}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });
        const data = await res.json();
        messages.innerHTML += `<div class="msg bot">${data.answer}</div>`;
        messages.scrollTop = messages.scrollHeight;
    } catch (err) {
        messages.innerHTML += `<div class="msg bot error">에러 발생: ${err.message}</div>`;
    }
}

// Initial Load
loadChats();

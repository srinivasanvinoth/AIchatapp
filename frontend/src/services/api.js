const API_URL =
    import.meta.env.VITE_API_URL ||
    "http://localhost:8000";


function getToken() {
    return localStorage.getItem("token");
}


async function request(path, options = {}) {
    const token = getToken();

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(
        `${API_URL}${path}`,
        {
            ...options,
            headers
        }
    );

    if (!response.ok) {
        const error = await response.json()
            .catch(() => ({
                detail: "Request failed"
            }));

        throw new Error(
            error.detail || "Request failed"
        );
    }

    return response.json();
}


export const api = {

    uploadPdf(file) {
        const token = getToken();
        const formData = new FormData();
        formData.append("file", file);

        return fetch(
            `${API_URL}/api/pdf/upload`,
            {
                method: "POST",
                headers: token
                    ? { Authorization: `Bearer ${token}` }
                    : {},
                body: formData
            }
        ).then(async (response) => {
            if (!response.ok) {
                const error = await response.json()
                    .catch(() => ({
                        detail: "PDF upload failed"
                    }));
                throw new Error(
                    error.detail || "PDF upload failed"
                );
            }

            return response.json();
        });
    },

    askPdf(question) {
        return request(
            "/api/pdf/ask",
            {
                method: "POST",
                body: JSON.stringify({ question })
            }
        );
    },

    signup(data) {
        return request(
            "/api/auth/signup",
            {
                method: "POST",
                body: JSON.stringify(data)
            }
        );
    },

    login(data) {
        return request(
            "/api/auth/login",
            {
                method: "POST",
                body: JSON.stringify(data)
            }
        );
    },

    getMe() {
        return request("/api/users/me");
    },

    getConversations() {
        return request("/api/conversations");
    },

    getConversation(id) {
        return request(`/api/conversations/${id}`);
    },

    createConversation(title) {
        return request(
            "/api/conversations",
            {
                method: "POST",
                body: JSON.stringify({ title })
            }
        );
    },

    sendMessage(conversationId, content) {
        return request(
            `/api/conversations/${conversationId}/messages`,
            {
                method: "POST",
                body: JSON.stringify({
                    content,
                    role: "user"
                })
            }
        );
    },

    sendAssistantMessage(conversationId, content) {
        return request(
            `/api/conversations/${conversationId}/messages`,
            {
                method: "POST",
                body: JSON.stringify({
                    content,
                    role: "assistant"
                })
            }
        );
    },

    renameConversation(conversationId, title) {
        return request(
            `/api/conversations/${conversationId}`,
            {
                method: "PUT",
                body: JSON.stringify({ title })
            }
        );
    },

    deleteConversation(conversationId) {
        return request(
            `/api/conversations/${conversationId}`,
            {
                method: "DELETE"
            }
        );
    }
};

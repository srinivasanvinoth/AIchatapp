import {
    useEffect,
    useRef,
    useState
} from "react";


export default function ChatWindow({
    conversation,
    onSendMessage,
    onUploadPdf,
    pdfStatus
}) {
    const [message, setMessage] = useState("");
    const [uploading, setUploading] = useState(false);
    const bottomRef = useRef(null);
    const fileRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });
    }, [conversation?.messages]);

    async function sendMessage(e) {
        e.preventDefault();

        const value = message.trim();

        if (!value) {
            return;
        }

        setMessage("");
        await onSendMessage(value);
    }

    async function handlePdfChange(e) {
        const file = e.target.files?.[0];

        if (!file) {
            return;
        }

        setUploading(true);

        try {
            await onUploadPdf(file);
        } finally {
            setUploading(false);
            e.target.value = "";
        }
    }

    if (!conversation) {
        return (
            <main className="empty-chat">
                <div>
                    <h1>Welcome to Chat</h1>
                    <p>
                        Create a new conversation to get started.
                    </p>
                </div>
            </main>
        );
    }

    return (
        <main className="chat-window">
            <header className="chat-header pdf-toolbar">
                <div>
                    <h3>{conversation.title}</h3>
                    {pdfStatus && (
                        <div className="pdf-status">
                            {pdfStatus}
                        </div>
                    )}
                </div>

                <div>
                    <input
                        ref={fileRef}
                        type="file"
                        accept="application/pdf,.pdf"
                        style={{ display: "none" }}
                        onChange={handlePdfChange}
                    />

                    <button
                        type="button"
                        className="pdf-button"
                        disabled={uploading}
                        onClick={() =>
                            fileRef.current?.click()
                        }
                    >
                        {uploading
                            ? "Indexing PDF..."
                            : "Upload PDF"}
                    </button>
                </div>
            </header>

            <div className="messages">
                {conversation.messages?.map((item) => (
                    <div
                        key={item.message_id}
                        className={`message-row ${item.role}`}
                    >
                        <div className="message">
                            {item.content}
                        </div>
                    </div>
                ))}

                <div ref={bottomRef} />
            </div>

            <form
                className="message-input-container"
                onSubmit={sendMessage}
            >
                <textarea
                    placeholder="Ask a question about your uploaded PDF..."
                    value={message}
                    onChange={(e) =>
                        setMessage(e.target.value)
                    }
                    onKeyDown={(e) => {
                        if (
                            e.key === "Enter" &&
                            !e.shiftKey
                        ) {
                            e.preventDefault();
                            sendMessage(e);
                        }
                    }}
                />

                <button type="submit">
                    Send
                </button>
            </form>
        </main>
    );
}

export default function Sidebar({
    conversations,
    selectedId,
    onSelect,
    onNewChat,
    onDelete
}) {
    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <h2>Chats</h2>

                <button
                    className="new-chat"
                    onClick={onNewChat}
                >
                    + New Chat
                </button>
            </div>

            <div className="conversation-list">
                {conversations.map((conversation) => (
                    <div
                        key={conversation.conversation_id}
                        className={
                            `conversation-item ${
                                selectedId === conversation.conversation_id
                                    ? "active"
                                    : ""
                            }`
                        }
                    >
                        <button
                            className="conversation-title"
                            onClick={() =>
                                onSelect(conversation.conversation_id)
                            }
                        >
                            {conversation.title}
                        </button>

                        <button
                            className="delete-button"
                            onClick={() =>
                                onDelete(conversation.conversation_id)
                            }
                            title="Delete conversation"
                        >
                            ×
                        </button>
                    </div>
                ))}
            </div>
        </aside>
    );
}

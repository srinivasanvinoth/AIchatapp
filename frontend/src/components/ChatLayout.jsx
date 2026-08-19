import {
    useEffect,
    useState
} from "react";

import Sidebar from "./Sidebar";
import ChatWindow from "./ChatWindow";
import UserProfile from "./UserProfile";

import { api } from "../services/api";


export default function ChatLayout({
    user,
    onLogout
}) {
    const [conversations, setConversations] =
        useState([]);

    const [selectedId, setSelectedId] =
        useState(null);

    const [conversation, setConversation] =
        useState(null);

    const [pdfStatus, setPdfStatus] =
        useState("");

    useEffect(() => {
        loadConversations();
    }, []);

    async function loadConversations() {
        const data = await api.getConversations();
        setConversations(data);
    }

    async function selectConversation(id) {
        setSelectedId(id);

        const data =
            await api.getConversation(id);

        setConversation(data);
    }

    async function newChat() {
        const chat =
            await api.createConversation("New Chat");

        await loadConversations();

        setSelectedId(chat.conversation_id);
        setConversation(chat);
    }

    async function sendMessage(content) {
        if (!selectedId) {
            return;
        }

        await api.sendMessage(
            selectedId,
            content
        );

        try {
            const result = await api.askPdf(content);

            await api.sendAssistantMessage(
                selectedId,
                result.answer
            );
        } catch (error) {
            await api.sendAssistantMessage(
                selectedId,
                `PDF assistant error: ${error.message}`
            );
        }

        const updated =
            await api.getConversation(selectedId);

        setConversation(updated);

        await loadConversations();
    }

    async function uploadPdf(file) {
        setPdfStatus("Uploading and indexing PDF...");

        try {
            const result = await api.uploadPdf(file);

            setPdfStatus(
                `${result.file_name} indexed (${result.pages} pages, ${result.chunks} chunks)`
            );
        } catch (error) {
            setPdfStatus(`PDF upload failed: ${error.message}`);
            throw error;
        }
    }

    async function deleteConversation(id) {
        await api.deleteConversation(id);

        if (selectedId === id) {
            setSelectedId(null);
            setConversation(null);
        }

        await loadConversations();
    }

    return (
        <div className="app-container">
            <Sidebar
                conversations={conversations}
                selectedId={selectedId}
                onSelect={selectConversation}
                onNewChat={newChat}
                onDelete={deleteConversation}
            />

            <section className="main-area">
                <div className="top-bar">
                    <div className="app-title">
                        Chat Application
                    </div>

                    <UserProfile
                        user={user}
                        onLogout={onLogout}
                    />
                </div>

                <ChatWindow
                    conversation={conversation}
                    onSendMessage={sendMessage}
                    onUploadPdf={uploadPdf}
                    pdfStatus={pdfStatus}
                />
            </section>
        </div>
    );
}

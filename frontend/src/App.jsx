import {
    useEffect,
    useState
} from "react";

import Login from "./components/Login";
import Signup from "./components/Signup";
import ChatLayout from "./components/ChatLayout";

import { api } from "./services/api";
import "./styles.css";


export default function App() {
    const [user, setUser] = useState(null);
    const [page, setPage] = useState("login");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token =
            localStorage.getItem("token");

        if (!token) {
            setLoading(false);
            return;
        }

        api.getMe()
            .then(setUser)
            .catch(() => {
                localStorage.removeItem("token");
            })
            .finally(() =>
                setLoading(false)
            );
    }, []);

    async function login(data) {
        const response =
            await api.login(data);

        localStorage.setItem(
            "token",
            response.access_token
        );

        setUser(response.user);
    }

    async function signup(data) {
        const response =
            await api.signup(data);

        localStorage.setItem(
            "token",
            response.access_token
        );

        setUser(response.user);
    }

    function logout() {
        localStorage.removeItem("token");

        setUser(null);
        setPage("login");
    }

    if (loading) {
        return (
            <div className="loading">
                Loading...
            </div>
        );
    }

    if (user) {
        return (
            <ChatLayout
                user={user}
                onLogout={logout}
            />
        );
    }

    if (page === "signup") {
        return (
            <Signup
                onSignup={signup}
                onShowLogin={() =>
                    setPage("login")
                }
            />
        );
    }

    return (
        <Login
            onLogin={login}
            onShowSignup={() =>
                setPage("signup")
            }
        />
    );
}

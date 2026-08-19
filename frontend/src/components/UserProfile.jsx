import { useState } from "react";


export default function UserProfile({
    user,
    onLogout
}) {
    const [open, setOpen] = useState(false);

    const initials =
        `${user.first_name?.[0] || ""}${user.last_name?.[0] || ""}`
            .toUpperCase();

    return (
        <div className="user-profile">
            <button
                className="profile-button"
                onClick={() => setOpen(!open)}
            >
                <div className="avatar">
                    {initials}
                </div>

                <span>
                    {user.first_name}
                </span>
            </button>

            {open && (
                <div className="profile-menu">
                    <strong>
                        {user.first_name} {user.last_name}
                    </strong>

                    <span>
                        @{user.login_id}
                    </span>

                    <span>
                        {user.email}
                    </span>

                    <button onClick={onLogout}>
                        Logout
                    </button>
                </div>
            )}
        </div>
    );
}

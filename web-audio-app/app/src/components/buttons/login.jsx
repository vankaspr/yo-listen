import { LoginForm } from "../views/login";
import { useState } from "react";

export function LoginButton() {
    const [showForm, setShowForm] = useState(false);

    const handleOpen = () => {
        setShowForm(true);
        console.log("login form show!");
    }
    
    return (
        <>
        {!showForm && <button onClick={handleOpen}>Login</button>}
        {showForm && <LoginForm />}
        </>
    )
}
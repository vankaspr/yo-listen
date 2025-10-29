import { useState } from "react";
import { API_ENDPOINTS } from "../api/path";

export function useUser() {
    const [user, setUser] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const getCurrentUser = async (token) => {
        setError(null);
        setLoading(true);

        try {
            const response = await fetch(API_ENDPOINTS.USER.ME, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch user data')
            }

            const userData = await response.json();
            setUser(userData);
            return userData;
        } catch (err) {
            setError(err.message);
            throw err;
        }  finally {
            setLoading(false);
        }
    };

    const logout = async () => {
        try {
            const token = localStorage.getItem('access_token');
            if (token) {
                await fetch(API_ENDPOINTS.AUTH.LOGOUT, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
            }
        } catch (error) {
            console.log('Logout API error:', error)
        } finally {
            localStorage.removeItem('access_token');
            setUser(null);
            setError(null);
        }
    };

    return {
        user,
        loading,
        error,
        getCurrentUser,
        logout,

    };

}
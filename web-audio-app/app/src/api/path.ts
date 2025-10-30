export const API_BASE_URL = 'http://localhost:8000/api';

export const API_ENDPOINTS = {
    AUTH: {
        REGISTER: `${API_BASE_URL}/auth/register`,
        LOGIN: `${API_BASE_URL}/auth/login`,
        VERIFY: `${API_BASE_URL}/auth/verify-email`,
        GITHUB:  `${API_BASE_URL}/auth/github`,
        GITHUB_CALLBACK: `${API_BASE_URL}/auth/github/callback`,
        FORGOT_PASSWORD: `${API_BASE_URL}/auth/forgot-password`,
        RESET_PASSWORD: `${API_BASE_URL}/auth/reset-password`,
        REFRESH: `${API_BASE_URL}/auth/refresh`,
        LOGOUT: `${API_BASE_URL}/auth/logout`,
    },

    USER: {
        ME: `${API_BASE_URL}/user/me`,
        PROFILE: `${API_BASE_URL}/user/me/profile`,
    },

    ADMIN: {
        STATISTIC: `${API_BASE_URL}/admin/statistic/users`,
        DEACTIVATE: `${API_BASE_URL}/admin/deactivate/{user_id}`,
        REACTIVATE: `${API_BASE_URL}/admin/reactivate/{user_id}`,
    }
} as const;
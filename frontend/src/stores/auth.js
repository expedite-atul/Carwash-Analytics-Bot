import { writable } from 'svelte/store';

const storedToken = localStorage.getItem('token');
const storedRole = localStorage.getItem('role');

export const token = writable(storedToken);
export const role = writable(storedRole);
export const user = writable(null);

export const isAuthenticated = writable(!!storedToken);

export function login(newToken, newRole) {
    localStorage.setItem('token', newToken);
    localStorage.setItem('role', newRole);
    token.set(newToken);
    role.set(newRole);
    isAuthenticated.set(true);
}

export async function logout() {
    // 1. Call Backend to Invalidate Token
    const currentToken = localStorage.getItem('token');
    if (currentToken) {
        try {
            // We won't block UI if this fails
            const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
            await fetch(`${API_URL}/auth/logout`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${currentToken}` }
            });
        } catch (e) {
            console.error("Logout API failed", e);
        }
    }

    // 2. Clear Local State
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    token.set(null);
    role.set(null);
    user.set(null);
    isAuthenticated.set(false);
}

<script>
    import { navigate } from "svelte-routing";
    import { login } from "../stores/auth";

    let email = "";
    let password = "";
    let error = "";
    let isLoading = false;

    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

    async function handleLogin() {
        isLoading = true;
        error = "";

        const formData = new FormData();
        formData.append("username", email);
        formData.append("password", password);

        try {
            const res = await fetch(`${API_URL}/auth/login`, {
                method: "POST",
                body: formData,
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || "Login failed");
            }

            const data = await res.json();
            login(data.access_token, data.role);
            navigate("/dashboard");
        } catch (err) {
            error = err.message;
        } finally {
            isLoading = false;
        }
    }
</script>

<div
    class="flex items-center justify-center min-h-screen w-full bg-gray-900 text-white fixed inset-0 z-50"
>
    <div
        class="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-xl shadow-2xl border border-gray-700 mx-4"
    >
        <div class="text-center">
            <h1
                class="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent"
            >
                Carwash Bot
            </h1>
            <p class="mt-2 text-gray-400">Sign in to access analytics</p>
        </div>

        {#if error}
            <div
                class="p-3 text-sm text-red-200 bg-red-900/50 border border-red-800 rounded-lg"
            >
                {error}
            </div>
        {/if}

        <form on:submit|preventDefault={handleLogin} class="space-y-4">
            <div>
                <label
                    for="email"
                    class="block text-sm font-medium text-gray-300">Email</label
                >
                <input
                    id="email"
                    type="email"
                    bind:value={email}
                    required
                    class="w-full mt-1 px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white outline-none transition-all"
                    placeholder="admin@carwash.com"
                />
            </div>

            <div>
                <label
                    for="password"
                    class="block text-sm font-medium text-gray-300"
                    >Password</label
                >
                <input
                    id="password"
                    type="password"
                    bind:value={password}
                    required
                    class="w-full mt-1 px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white outline-none transition-all"
                    placeholder="••••••••"
                />
            </div>

            <button
                type="submit"
                disabled={isLoading}
                class="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 rounded-lg font-semibold shadow-lg transform transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {isLoading ? "Signing in..." : "Sign In"}
            </button>
        </form>
    </div>
</div>

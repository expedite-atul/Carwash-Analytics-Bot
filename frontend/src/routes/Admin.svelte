<script>
    import { onMount } from "svelte";
    import { token } from "../stores/auth";

    let authToken = "";
    token.subscribe((val) => (authToken = val));

    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

    let cacheStats = { hits: 0, misses: 0, hit_ratio: 0, logs: [] };
    let users = [];
    let newUserEmail = "";
    let newUserPassword = "";
    let newUserRole = "employee";
    let isLoading = false;
    let message = "";

    async function loadData() {
        // Load Stats
        const resStats = await fetch(`${API_URL}/admin/stats/cache`, {
            headers: { Authorization: `Bearer ${authToken}` },
        });
        if (resStats.ok) cacheStats = await resStats.json();

        // Load Users
        const resUsers = await fetch(`${API_URL}/admin/users`, {
            headers: { Authorization: `Bearer ${authToken}` },
        });
        if (resUsers.ok) users = await resUsers.json();
    }

    async function addUser() {
        if (!newUserEmail || !newUserPassword) return;
        isLoading = true;
        try {
            const res = await fetch(`${API_URL}/auth/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${authToken}`,
                },
                body: JSON.stringify({
                    email: newUserEmail,
                    hashed_password: newUserPassword, // Backend will hash it
                    role: newUserRole,
                    full_name: "New Staff",
                    is_active: true,
                }),
            });
            if (res.ok) {
                message = "User added!";
                newUserEmail = "";
                newUserPassword = "";
                loadData();
            } else {
                const err = await res.json();
                message = "Error: " + err.detail;
            }
        } catch (e) {
            message = e.message;
        }
        isLoading = false;
    }

    async function deleteUser(id) {
        if (!confirm("Are you sure?")) return;
        await fetch(`${API_URL}/admin/users/${id}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${authToken}` },
        });
        loadData();
    }

    onMount(loadData);
</script>

<div class="p-6 space-y-8 text-white h-full overflow-y-auto">
    <h1 class="text-3xl font-bold">Admin Dashboard</h1>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
            class="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg"
        >
            <h3 class="text-gray-400 text-sm font-semibold uppercase">
                Cache Hits
            </h3>
            <p class="text-4xl font-bold text-green-400 mt-2">
                {cacheStats.hits}
            </p>
        </div>
        <div
            class="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg"
        >
            <h3 class="text-gray-400 text-sm font-semibold uppercase">
                Cache Misses
            </h3>
            <p class="text-4xl font-bold text-red-400 mt-2">
                {cacheStats.misses}
            </p>
        </div>
        <div
            class="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg"
        >
            <h3 class="text-gray-400 text-sm font-semibold uppercase">
                Efficiency
            </h3>
            <p class="text-4xl font-bold text-blue-400 mt-2">
                {cacheStats.hit_ratio * 100}%
            </p>
        </div>
    </div>

    <!-- Cache Logs -->
    <div class="bg-gray-800 p-6 rounded-xl border border-gray-700">
        <h2 class="text-xl font-bold mb-4 border-b border-gray-700 pb-2">
            Recent Cache Activity
        </h2>
        <div class="space-y-2 max-h-[300px] overflow-y-auto">
            {#each cacheStats.logs || [] as log}
                <div
                    class="flex items-center justify-between p-2 rounded bg-gray-700/30 font-mono text-sm"
                >
                    <span class="truncate w-1/2 text-gray-300">{log.key}</span>
                    <div class="flex items-center gap-4">
                        <span
                            class="{log.type === 'HIT'
                                ? 'text-green-400'
                                : 'text-red-400'} font-bold">{log.type}</span
                        >
                        <span class="text-gray-500 text-xs"
                            >{new Date(log.time).toLocaleTimeString()}</span
                        >
                    </div>
                </div>
            {/each}
            {#if !cacheStats.logs || cacheStats.logs.length === 0}
                <p class="text-gray-500 text-sm">No recent cache events.</p>
            {/if}
        </div>
    </div>

    <!-- Employee Management -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Add User Form -->
        <div class="bg-gray-800 p-6 rounded-xl border border-gray-700">
            <h2 class="text-xl font-bold mb-4 border-b border-gray-700 pb-2">
                Add Employee
            </h2>
            {#if message}
                <p
                    class="mb-4 text-sm text-yellow-400 bg-yellow-400/10 p-2 rounded"
                >
                    {message}
                </p>
            {/if}

            <form on:submit|preventDefault={addUser} class="space-y-4">
                <div>
                    <label class="block text-sm text-gray-400 mb-1">Email</label
                    >
                    <input
                        bind:value={newUserEmail}
                        type="email"
                        required
                        class="w-full bg-gray-700 border border-gray-600 rounded p-2 text-white"
                        placeholder="staff@carwash.com"
                    />
                </div>
                <div>
                    <label class="block text-sm text-gray-400 mb-1"
                        >Password</label
                    >
                    <input
                        bind:value={newUserPassword}
                        type="text"
                        required
                        class="w-full bg-gray-700 border border-gray-600 rounded p-2 text-white"
                        placeholder="Secret123"
                    />
                </div>
                <div>
                    <label class="block text-sm text-gray-400 mb-1">Role</label>
                    <select
                        bind:value={newUserRole}
                        class="w-full bg-gray-700 border border-gray-600 rounded p-2 text-white"
                    >
                        <option value="employee">Employee</option>
                        <option value="admin">Admin</option>
                    </select>
                </div>
                <button
                    disabled={isLoading}
                    class="w-full bg-blue-600 hover:bg-blue-500 py-2 rounded font-semibold text-white transition"
                >
                    {isLoading ? "Adding..." : "Create User"}
                </button>
            </form>
        </div>

        <!-- User List -->
        <div class="bg-gray-800 p-6 rounded-xl border border-gray-700">
            <h2 class="text-xl font-bold mb-4 border-b border-gray-700 pb-2">
                Staff Directory
            </h2>
            <div class="space-y-3 max-h-[400px] overflow-y-auto pr-2">
                {#each users as u}
                    <div
                        class="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition"
                    >
                        <div>
                            <p class="font-medium text-white">{u.email}</p>
                            <span
                                class="text-xs uppercase px-2 py-0.5 rounded bg-gray-600 text-gray-300"
                                >{u.role}</span
                            >
                        </div>
                        {#if u.role !== "admin"}
                            <button
                                on:click={() => deleteUser(u.id)}
                                class="text-red-400 hover:text-red-300 text-sm font-semibold bg-red-400/10 px-3 py-1 rounded hover:bg-red-400/20"
                                >Remove</button
                            >
                        {/if}
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>

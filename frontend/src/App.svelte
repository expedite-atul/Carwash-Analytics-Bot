<script>
    import { Router, Route, navigate } from "svelte-routing";
    import { isAuthenticated } from "./stores/auth";
    import Sidebar from "./lib/Sidebar.svelte";
    import ChatInterface from "./lib/ChatInterface.svelte";
    import Login from "./routes/Login.svelte";
    import Admin from "./routes/Admin.svelte";
    import { onMount } from "svelte";

    let isAuth = false;
    isAuthenticated.subscribe((value) => {
        isAuth = value;
        if (!value && window.location.pathname !== "/") {
            navigate("/", { replace: true });
        } else if (value && window.location.pathname === "/") {
            navigate("/dashboard", { replace: true });
        }
    });

    export let url = "";
</script>

<Router {url}>
    <main
        class="flex h-screen bg-gray-900 text-white font-sans selection:bg-blue-500 selection:text-white"
    >
        {#if isAuth}
            <!-- Dashboard Layout -->
            <Route path="/dashboard">
                <div class="flex h-full w-full">
                    <Sidebar />
                    <div
                        class="flex-1 flex flex-col relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900"
                    >
                        <header
                            class="h-16 border-b border-gray-800/50 bg-gray-900/50 backdrop-blur-md flex items-center justify-between px-6 z-10"
                        >
                            <h2
                                class="text-lg font-semibold text-gray-200 tracking-tight"
                            >
                                Chat Interface
                            </h2>
                        </header>
                        <div
                            class="flex-1 overflow-y-auto p-4 sm:p-6 scroll-smooth"
                        >
                            <ChatInterface />
                        </div>
                    </div>
                </div>
            </Route>

            <!-- Admin Layout -->
            <Route path="/admin">
                <div class="flex h-full w-full">
                    <Sidebar />
                    <div
                        class="flex-1 flex flex-col relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900"
                    >
                        <div class="flex-1 overflow-y-auto">
                            <Admin />
                        </div>
                    </div>
                </div>
            </Route>

            <!-- Redirect root -->
            <Route path="/">
                <!-- Logic handled in script -->
            </Route>
        {:else}
            <!-- Login Layout -->
            <Route path="/">
                <Login />
            </Route>
            <Route path="*">
                <Login />
            </Route>
        {/if}
    </main>
</Router>

<style>
    :global(body) {
        margin: 0;
        padding: 0;
        background-color: #111827;
    }
</style>

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
    let chatInterfaceComponent;
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
                        class="flex-1 flex flex-col relative overflow-hidden bg-gray-50 from-gray-50 to-gray-50"
                    >
                        <header
                            class="h-16 border-b border-gray-200 bg-white/80 backdrop-blur-md flex items-center justify-between px-6 z-10 sticky top-0"
                        >
                            <h2
                                class="text-lg font-bold text-gray-900 tracking-tight"
                            >
                                Chat Interface
                            </h2>
                            <button
                                on:click={() =>
                                    chatInterfaceComponent.clearChat()}
                                class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                                title="Clear Chat History"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="18"
                                    height="18"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    ><polyline points="3 6 5 6 21 6"
                                    ></polyline><path
                                        d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                                    ></path><line
                                        x1="10"
                                        y1="11"
                                        x2="10"
                                        y2="17"
                                    ></line><line
                                        x1="14"
                                        y1="11"
                                        x2="14"
                                        y2="17"
                                    ></line></svg
                                >
                            </button>
                        </header>
                        <div
                            class="flex-1 overflow-y-auto p-4 sm:p-6 scroll-smooth"
                        >
                            <ChatInterface bind:this={chatInterfaceComponent} />
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

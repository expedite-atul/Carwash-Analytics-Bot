<script>
    import Sidebar from "./lib/Sidebar.svelte";
    import ChatInterface from "./lib/ChatInterface.svelte";
</script>

<div class="flex h-screen w-screen overflow-hidden bg-background">
    <!-- Sidebar -->
    <aside class="w-64 flex-shrink-0 border-r border-gray-200 bg-sidebar">
        <Sidebar />
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col h-full relative">
        <!-- Header -->
        <header
            class="h-16 border-b border-gray-200 bg-surface flex items-center px-6 justify-between"
        >
            <h1 class="text-xl font-semibold text-text">Carwash Analytics</h1>
            <div class="flex items-center gap-4">
                <button
                    class="p-2 text-muted hover:text-primary transition-colors"
                >
                    <span class="sr-only">Notifications</span>
                    🔔
                </button>
                <div
                    class="h-8 w-8 rounded-full bg-primary text-white flex items-center justify-center text-sm font-bold"
                >
                    JD
                </div>
            </div>
        </header>

        <!-- Content Area (Chat) -->
        <div class="flex-1 overflow-hidden p-6">
            <ChatInterface />
        </div>
    </main>
</div>

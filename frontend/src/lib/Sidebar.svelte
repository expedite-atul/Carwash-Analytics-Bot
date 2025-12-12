<script>
  import { navigate, useLocation } from "svelte-routing";
  import { logout, role } from "../stores/auth";

  let userRole = "";
  role.subscribe((val) => (userRole = val));

  const location = useLocation();
  $: activePath = $location.pathname;

  function handleLogout() {
    logout();
    navigate("/");
  }

  function handleNav(path) {
    navigate(path);
  }
</script>

<div
  class="h-full flex flex-col py-6 bg-gray-900 border-r border-gray-800 w-64"
>
  <!-- Logo Area -->
  <div class="px-6 mb-8 flex items-center gap-3">
    <div
      class="h-10 w-10 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center text-white font-bold shadow-lg shadow-blue-900/20"
    >
      CW
    </div>
    <span
      class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-100 to-gray-400"
      >CarwashBot</span
    >
  </div>

  <!-- Navigation -->
  <nav class="flex-1 px-4 space-y-2">
    <!-- Chat (Default) -->
    <button
      on:click={() => handleNav("/dashboard")}
      class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 {activePath ===
      '/dashboard'
        ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20 shadow-sm'
        : 'text-gray-400 hover:bg-gray-800 hover:text-white'}"
    >
      <span class="text-lg">✨</span>
      AI Analytics
    </button>

    <!-- Admin Link (Only for Admin) -->
    {#if userRole === "admin"}
      <button
        on:click={() => handleNav("/admin")}
        class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 {activePath ===
        '/admin'
          ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20 shadow-sm'
          : 'text-gray-400 hover:bg-gray-800 hover:text-white'}"
      >
        <span class="text-lg">🛡️</span>
        Admin Panel
      </button>
    {/if}
  </nav>

  <!-- User Section (Bottom) -->
  <div class="mt-auto px-6 space-y-4">
    <div
      class="p-4 bg-gray-800/50 rounded-xl border border-gray-700/50 shadow-sm"
    >
      <div class="flex items-center gap-3 mb-3">
        <div
          class="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400 text-xs font-bold"
        >
          {userRole === "admin" ? "AD" : "US"}
        </div>
        <div>
          <p class="text-sm font-medium text-gray-200 capitalize">{userRole}</p>
          <p class="text-xs text-gray-500">Pro Plan</p>
        </div>
      </div>

      <button
        on:click={handleLogout}
        class="w-full py-2 text-xs font-semibold text-red-400 bg-red-400/10 hover:bg-red-400/20 rounded-lg transition-colors border border-red-400/20"
      >
        Sign Out
      </button>
    </div>
  </div>
</div>

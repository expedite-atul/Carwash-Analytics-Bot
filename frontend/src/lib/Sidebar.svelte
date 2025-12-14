<script>
  import { navigate, useLocation } from "svelte-routing";
  import { logout, role } from "../stores/auth";
  import IconLogo from "./IconLogo.svelte";

  let userRole = "";
  role.subscribe((val) => (userRole = val));

  const location = useLocation();
  $: activePath = $location.pathname;

  let isCollapsed = false;

  function toggleSidebar() {
    isCollapsed = !isCollapsed;
  }

  function handleLogout() {
    logout();
    navigate("/");
  }

  function handleNav(path) {
    navigate(path);
  }
</script>

<div
  class="h-full flex flex-col pb-6 bg-gray-900 border-r border-gray-800 transition-all duration-300 relative {isCollapsed
    ? 'w-20'
    : 'w-64'}"
>
  <!-- Collapse Toggle -->
  <button
    on:click={toggleSidebar}
    class="absolute -right-3 top-9 bg-gray-800 border border-gray-700 text-gray-400 hover:text-white rounded-full p-1 shadow-lg z-50 transform transition-transform duration-300 hover:scale-110"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="transform transition-transform {isCollapsed ? 'rotate-180' : ''}"
      ><polyline points="15 18 9 12 15 6"></polyline></svg
    >
  </button>

  <!-- Logo Area -->
  <div
    class="px-6 h-16 flex items-center gap-3 overflow-hidden mb-2 border-b border-gray-800/50"
  >
    <div
      class="shrink-0 h-8 w-8 flex items-center justify-center transition-all duration-300 {isCollapsed
        ? 'mx-auto'
        : ''}"
    >
      <div class="w-8 h-8 drop-shadow-[0_0_10px_rgba(100,255,218,0.3)]">
        <IconLogo />
      </div>
    </div>
    <span
      class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-100 to-gray-400 whitespace-nowrap transition-opacity duration-200 {isCollapsed
        ? 'opacity-0 w-0'
        : 'opacity-100'}"
    >
      Query Sense Bot
    </span>
  </div>

  <!-- Navigation -->
  <nav class="flex-1 px-4 space-y-2">
    <!-- Chat (Default) -->
    <button
      on:click={() => handleNav("/dashboard")}
      class="w-full flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-medium transition-all duration-200 {isCollapsed
        ? 'justify-center'
        : ''} {activePath === '/dashboard'
        ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20 shadow-sm'
        : 'text-gray-400 hover:bg-gray-800 hover:text-white'}"
      title={isCollapsed ? "AI Analytics" : ""}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="shrink-0"
        ><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
        ></path></svg
      >
      {#if !isCollapsed}
        <span class="text-sm whitespace-nowrap">AI Analytics</span>
      {/if}
    </button>

    <!-- Admin Link (Only for Admin) -->
    {#if userRole === "admin"}
      <button
        on:click={() => handleNav("/admin")}
        class="w-full flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-medium transition-all duration-200 {isCollapsed
          ? 'justify-center'
          : ''} {activePath === '/admin'
          ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20 shadow-sm'
          : 'text-gray-400 hover:bg-gray-800 hover:text-white'}"
        title={isCollapsed ? "Admin Panel" : ""}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="shrink-0"
          ><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg
        >
        {#if !isCollapsed}
          <span class="text-sm whitespace-nowrap">Admin Panel</span>
        {/if}
      </button>
    {/if}
  </nav>

  <!-- User Section (Bottom) -->
  <div class="mt-auto px-4 space-y-4">
    <div
      class="p-2 transition-all duration-300 {isCollapsed
        ? 'bg-transparent border-0'
        : 'bg-gray-800/50 rounded-xl border border-gray-700/50 shadow-sm p-4'}"
    >
      <div
        class="flex items-center gap-3 {isCollapsed
          ? 'justify-center'
          : 'mb-3'}"
      >
        <div
          class="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400 text-xs font-bold shrink-0"
        >
          {userRole === "admin" ? "AD" : "US"}
        </div>
        {#if !isCollapsed}
          <div class="overflow-hidden">
            <p class="text-sm font-medium text-gray-200 capitalize truncate">
              {userRole}
            </p>
            <p class="text-[10px] text-gray-500 uppercase tracking-wider">
              Pro Plan
            </p>
          </div>
        {/if}
      </div>

      {#if !isCollapsed}
        <button
          on:click={handleLogout}
          class="w-full py-2 text-xs font-semibold text-red-400 bg-red-400/10 hover:bg-red-400/20 rounded-lg transition-colors border border-red-400/20"
        >
          Sign Out
        </button>
      {/if}
    </div>
  </div>
</div>

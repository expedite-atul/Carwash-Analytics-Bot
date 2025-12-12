<script>
  let active = "chat";

  const menuItems = [
    { id: "home", icon: "🏠", label: "Home" },
    { id: "chat", icon: "✨", label: "AI Analytics", active: true },
    { id: "reports", icon: "📊", label: "Reports" },
    { id: "customer", icon: "👥", label: "Customers" },
    { id: "settings", icon: "⚙️", label: "Settings" },
  ];
</script>

<div class="h-full flex flex-col py-6 bg-sidebar">
  <!-- Logo Area -->
  <div class="px-6 mb-8 flex items-center gap-2">
    <div
      class="h-8 w-8 bg-black rounded-lg flex items-center justify-center text-white font-bold"
    >
      C
    </div>
    <span class="text-lg font-bold text-text">CarwashBot</span>
  </div>

  <!-- Navigation -->
  <nav class="flex-1 px-4 space-y-1">
    {#each menuItems as item}
      <button
        class="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200
        {item.id === active
          ? 'bg-primary/10 text-primary'
          : 'text-muted hover:bg-gray-100 hover:text-text'}"
      >
        <span class="text-lg">{item.icon}</span>
        {item.label}
      </button>
    {/each}
  </nav>

  <!-- User Section (Bottom) -->
  <div class="mt-auto px-6">
    <div class="p-4 bg-white rounded-xl border border-gray-200 shadow-sm">
      <p class="text-xs font-semibold text-muted mb-1">CREDITS</p>
      <div class="w-full bg-gray-100 h-2 rounded-full mb-2">
        <div class="bg-primary h-2 rounded-full" style="width: 75%"></div>
      </div>
      <div class="flex justify-between text-xs text-text">
        <span>750 used</span>
        <span>1000 total</span>
      </div>
    </div>
  </div>
</div>

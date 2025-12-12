<script>
  import SuggestionChips from "./SuggestionChips.svelte";
  import MessageBubble from "./MessageBubble.svelte";

  let messages = [
    {
      role: "model",
      content:
        "Hello! I am your Carwash Analytics Assistant. Ask me a question or pick a quick action.",
    },
  ];
  let input = "";
  let isLoading = false;

  async function sendMessage(text = input) {
    if (!text || !text.trim()) return;

    // Optimistic UI
    messages = [...messages, { role: "user", content: text }];
    input = "";
    isLoading = true;

    try {
      // Step 1: Get the Plan (SQL)
      const res = await fetch("http://localhost:8000/chat/plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();

      if (data.status === "success") {
        messages = [
          ...messages,
          {
            role: "model",
            content: data.explanation,
            type: "plan",
            sql: data.sql,
          },
        ];
      } else {
        messages = [
          ...messages,
          { role: "model", content: "Error: " + data.message },
        ];
      }
    } catch (e) {
      console.error(e);
      messages = [
        ...messages,
        { role: "model", content: "Network Error: " + e.message },
      ];
    } finally {
      isLoading = false;
    }
  }

  async function confirmExecution(sql) {
    isLoading = true;
    try {
      const res = await fetch("http://localhost:8000/chat/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sql: sql }),
      });
      const result = await res.json();

      if (result.status === "success") {
        // result.data contains { type: 'kpi'|'table', data: {...} }
        // We inject the SQL back into the message for transparency
        const newMsg = {
          role: "model",
          type: result.type,
          data: result.data,
          sql: result.data.sql, // Ensure SQL is passed for the bubble footer
        };
        messages = [...messages, newMsg];
      } else {
        messages = [
          ...messages,
          { role: "model", content: "Execution Error: " + result.message },
        ];
      }
    } catch (e) {
      messages = [
        ...messages,
        { role: "model", content: "Network Error: " + e.message },
      ];
    } finally {
      isLoading = false;
    }
  }

  function handleSelect(event) {
    sendMessage(event.detail);
  }
</script>

<div
  class="flex flex-col h-full bg-surface/50 rounded-2xl overflow-hidden relative"
>
  <!-- Chat Area -->
  <div class="flex-1 overflow-y-auto p-6 scroll-smooth">
    {#each messages as msg}
      <div class="relative group">
        <MessageBubble message={msg} />

        {#if msg.type === "plan"}
          <div class="absolute bottom-6 left-5">
            <button
              on:click={() => confirmExecution(msg.sql)}
              class="ml-2 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg shadow-lg hover:bg-indigo-700 transition-all transform hover:scale-105 flex items-center gap-2"
            >
              <span>🚀 Proceed</span>
            </button>
          </div>
        {/if}
      </div>
    {/each}

    {#if isLoading}
      <div class="flex justify-start mb-6">
        <div class="bg-white rounded-2xl p-4 flex gap-1 items-center shadow-sm">
          <div
            class="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce"
          ></div>
          <div
            class="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce delay-75"
          ></div>
          <div
            class="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce delay-150"
          ></div>
        </div>
      </div>
    {/if}
  </div>

  <!-- Input Area -->
  <div class="p-4 bg-white border-t border-gray-100">
    <!-- Suggestion Chips -->
    {#if messages.length < 2 && !isLoading}
      <div class="mb-4">
        <SuggestionChips on:select={handleSelect} />
      </div>
    {/if}

    <form
      on:submit|preventDefault={() => sendMessage(input)}
      class="flex gap-2 bg-gray-50 rounded-2xl p-2 border border-gray-200 focus-within:ring-2 focus-within:ring-primary/20 transition-all shadow-inner"
    >
      <input
        type="text"
        bind:value={input}
        placeholder="Ask a question about your data..."
        class="flex-1 bg-transparent border-none focus:outline-none px-4 py-2 text-sm text-text placeholder-muted"
      />
      <button
        type="submit"
        disabled={!input.trim() || isLoading}
        class="p-3 bg-primary text-white rounded-xl hover:bg-indigo-600 disabled:opacity-50 transition-colors shadow-sm"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"
          ><line x1="22" y1="2" x2="11" y2="13"></line><polygon
            points="22 2 15 22 11 13 2 9 22 2"
          ></polygon></svg
        >
      </button>
    </form>
    <div class="text-center mt-3">
      <p
        class="text-[10px] items-center justify-center text-muted/60 uppercase tracking-widest font-semibold flex gap-1"
      >
        <span>Powered by Gemini 2.5</span>
      </p>
    </div>
  </div>
</div>

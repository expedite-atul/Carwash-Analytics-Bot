<script>
    import { createEventDispatcher } from "svelte";
    import { slide } from "svelte/transition";
    import ChartRenderer from "./ChartRenderer.svelte";

    export let message; // { role: 'user' | 'model', content, type, data, sql }

    const dispatch = createEventDispatcher();
    let showSql = false;
</script>

<div
    class="flex {message.role === 'user'
        ? 'justify-end'
        : 'justify-start'} mb-6"
>
    <div class="max-w-[85%]">
        <!-- User Message -->
        {#if message.role === "user"}
            <div
                class="bg-primary text-white rounded-2xl rounded-tr-sm px-5 py-3 shadow-sm"
            >
                <p class="text-sm">{message.content}</p>
            </div>

            <!-- Model Message -->
        {:else}
            <div
                class="bg-white border border-gray-100 rounded-2xl rounded-tl-sm shadow-sm overflow-hidden text-text"
            >
                <!-- 1. KPI Mode -->
                {#if message.type === "kpi"}
                    <div class="p-6 text-center min-w-[200px]">
                        <p
                            class="text-xs font-semibold text-muted uppercase tracking-wider mb-1"
                        >
                            {message.data.label}
                        </p>
                        <p class="text-4xl font-bold text-primary">
                            {message.data.value.toLocaleString()}
                        </p>
                    </div>

                    <!-- 2. Chart Mode -->
                {:else if message.type === "chart"}
                    <div class="p-4 w-full h-[300px]">
                        <p
                            class="text-xs font-semibold text-muted mb-2 text-center uppercase tracking-wider"
                        >
                            Visualization
                        </p>
                        <ChartRenderer
                            data={message.data}
                            type={message.chartType}
                        />
                    </div>

                    <!-- 3. Table Mode -->
                {:else if message.type === "table"}
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm text-left">
                            <thead
                                class="bg-gray-50 text-xs text-muted uppercase font-semibold"
                            >
                                <tr>
                                    {#each message.data.columns as col}
                                        <th class="px-4 py-3">{col}</th>
                                    {/each}
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-100">
                                {#each message.data.rows as row}
                                    <tr class="hover:bg-gray-50/50">
                                        {#each message.data.columns as col}
                                            <td
                                                class="px-4 py-3 font-medium text-slate-700"
                                                >{row[col]}</td
                                            >
                                        {/each}
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>

                    <!-- 3. Plan/Confirmation Mode -->
                {:else if message.type === "plan"}
                    <div class="p-5">
                        <p class="text-sm mb-4 leading-relaxed">
                            {message.content}
                        </p>
                        <div
                            class="bg-amber-50 border border-amber-100 rounded-lg p-3 mb-4"
                        >
                            <p
                                class="text-xs font-mono text-amber-800 break-all"
                            >
                                {message.sql}
                            </p>
                        </div>

                        <!-- Button In-Flow -->
                        <button
                            on:click={() => dispatch("proceed", message.sql)}
                            class="w-full py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg shadow-sm hover:bg-indigo-700 transition-all flex items-center justify-center gap-2"
                        >
                            <span>Proceed</span>
                        </button>
                    </div>

                    <!-- 4. Default Text -->
                {:else}
                    <div class="p-5">
                        <p class="text-sm leading-relaxed whitespace-pre-wrap">
                            {message.content}
                        </p>
                    </div>
                {/if}

                <!-- SQL Footer (Collapsible) -->
                {#if message.sql && message.type !== "plan"}
                    <div class="bg-gray-50 px-4 py-2 border-t border-gray-100">
                        <button
                            on:click={() => (showSql = !showSql)}
                            class="text-xs text-muted flex items-center gap-1 hover:text-primary transition-colors w-full"
                        >
                            <span>{showSql ? "" : ""} Calculation Logic</span>
                        </button>
                        {#if showSql}
                            <div
                                transition:slide
                                class="mt-2 text-xs font-mono text-slate-500 bg-gray-100 p-2 rounded selectable"
                            >
                                {message.sql}
                            </div>
                        {/if}
                    </div>
                {/if}

                <!-- Feedback Actions -->
                {#if message.role === "model" && message.type !== "plan" && message.sql}
                    <div
                        class="flex justify-end p-2 px-4 border-t border-gray-50"
                    >
                        <button
                            on:click={() =>
                                dispatch("feedback", { sql: message.sql })}
                            class="text-xs flex items-center gap-1 text-gray-400 hover:text-green-600 transition-colors"
                            title="Help me learn! Mark this as a good answer."
                        >
                            Great Answer
                        </button>
                    </div>
                {/if}
            </div>
        {/if}
    </div>
</div>

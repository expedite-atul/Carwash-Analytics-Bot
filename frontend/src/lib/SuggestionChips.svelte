<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export const suggestions = [
        {
            label: "Monthly Revenue",
            query: "What is the total revenue this month?",
        },
        {
            label: "Active Customers",
            query: "How many active customers do we have?",
        },
        { label: "Churn Rate", query: "Calculate the customer churn rate." },
        {
            label: "Top Packages",
            query: "What are the most popular wash packages?",
        },
    ];
</script>

<div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
    {#each suggestions as chip}
        <button
            on:click={() => dispatch("select", chip.query)}
            class="flex-shrink-0 px-4 py-2 bg-blue-50 text-blue-700 text-sm font-medium rounded-full hover:bg-blue-100 transition-colors border border-blue-100/50 shadow-sm"
        >
            {chip.label}
        </button>
    {/each}
</div>

<style>
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
    .scrollbar-hide {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
</style>

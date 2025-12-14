<script>
    import { createEventDispatcher } from "svelte";
    import { fade, scale } from "svelte/transition";

    export let title = "Are you sure?";
    export let message = "This action cannot be undone.";
    export let confirmText = "Confirm";
    export let cancelText = "Cancel";

    const dispatch = createEventDispatcher();

    function onConfirm() {
        dispatch("confirm");
    }

    function onCancel() {
        dispatch("cancel");
    }
</script>

<div
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/60 backdrop-blur-sm"
    transition:fade={{ duration: 200 }}
>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="absolute inset-0" on:click={onCancel}></div>

    <div
        class="bg-white rounded-2xl shadow-xl w-full max-w-sm relative overflow-hidden"
        transition:scale={{ duration: 200, start: 0.95 }}
    >
        <div class="p-6 text-center">
            <div
                class="w-12 h-12 rounded-full bg-red-100 text-red-500 mx-auto flex items-center justify-center mb-4"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    ><path d="M3 6h18"></path><path
                        d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"
                    ></path><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"
                    ></path><line x1="10" y1="11" x2="10" y2="17"></line><line
                        x1="14"
                        y1="11"
                        x2="14"
                        y2="17"
                    ></line></svg
                >
            </div>

            <h3 class="text-lg font-bold text-gray-900 mb-2">{title}</h3>
            <p class="text-sm text-gray-500 mb-6">{message}</p>

            <div class="flex gap-3 justify-center">
                <button
                    on:click={onCancel}
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                >
                    {cancelText}
                </button>
                <button
                    on:click={onConfirm}
                    class="px-4 py-2 text-sm font-medium text-white bg-red-500 hover:bg-red-600 rounded-lg shadow-sm shadow-red-500/30 transition-all hover:shadow-red-500/50"
                >
                    {confirmText}
                </button>
            </div>
        </div>
    </div>
</div>

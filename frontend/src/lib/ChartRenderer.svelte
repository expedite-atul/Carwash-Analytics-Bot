<script>
    import { Bar, Line } from "svelte-chartjs";
    import {
        Chart as ChartJS,
        Title,
        Tooltip,
        Legend,
        BarElement,
        LineElement,
        PointElement,
        CategoryScale,
        LinearScale,
    } from "chart.js";

    ChartJS.register(
        Title,
        Tooltip,
        Legend,
        BarElement,
        LineElement,
        PointElement,
        CategoryScale,
        LinearScale,
    );

    export let data; // { labels: [], datasets: [] }
    export let type = "bar";

    let chartData;
    let chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                mode: "index",
                intersect: false,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: "rgba(255, 255, 255, 0.1)",
                },
                ticks: { color: "#ccc" },
            },
            x: {
                grid: { display: false },
                ticks: { color: "#ccc" },
            },
        },
    };

    $: {
        if (data) {
            // Add styling to datasets
            const coloredDatasets = data.datasets.map((ds) => ({
                ...ds,
                backgroundColor:
                    type === "line"
                        ? "rgba(99, 102, 241, 0.2)"
                        : "rgba(99, 102, 241, 0.8)",
                borderColor: "rgba(99, 102, 241, 1)",
                borderWidth: 2,
                pointBackgroundColor: "rgba(99, 102, 241, 1)",
                fill: type === "line", // Fill area under line
                tension: 0.4, // Smooth curve
                borderRadius: 4,
                hoverBackgroundColor: "rgba(99, 102, 241, 1)",
            }));
            chartData = {
                labels: data.labels,
                datasets: coloredDatasets,
            };
        }
    }
</script>

<div class="h-64 w-full bg-gray-900/50 p-4 rounded-lg border border-gray-700">
    {#if chartData}
        {#if type === "line"}
            <Line data={chartData} options={chartOptions} />
        {:else}
            <Bar data={chartData} options={chartOptions} />
        {/if}
    {/if}
</div>

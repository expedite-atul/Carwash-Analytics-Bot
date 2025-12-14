<script>
    import { onMount, afterUpdate, onDestroy } from "svelte";
    import Chart from "chart.js/auto";

    export let type = "bar"; // bar, line, pie, doughnut
    export let data = {
        labels: [],
        datasets: [],
    };
    export let options = {};

    let canvas;
    let chartInstance;

    function createChart() {
        if (chartInstance) chartInstance.destroy();
        if (!canvas) return;

        chartInstance = new Chart(canvas, {
            type,
            data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            color: "#4b5563", // text-gray-600
                            font: {
                                family: "'Inter', sans-serif",
                                size: 11,
                            },
                            usePointStyle: true,
                            padding: 20,
                        },
                    },
                    tooltip: {
                        backgroundColor: "rgba(255, 255, 255, 0.95)",
                        titleColor: "#111827",
                        bodyColor: "#4b5563",
                        borderColor: "#e5e7eb",
                        borderWidth: 1,
                        padding: 10,
                        cornerRadius: 8,
                        displayColors: true,
                        boxPadding: 4,
                    },
                },
                scales:
                    type !== "pie" && type !== "doughnut"
                        ? {
                              y: {
                                  beginAtZero: true,
                                  grid: {
                                      color: "#f3f4f6", // gray-100
                                      drawBorder: false,
                                  },
                                  ticks: {
                                      color: "#6b7280", // gray-500
                                      font: {
                                          size: 10,
                                      },
                                      padding: 10,
                                  },
                                  border: {
                                      display: false,
                                  },
                              },
                              x: {
                                  grid: {
                                      display: false,
                                  },
                                  ticks: {
                                      color: "#6b7280", // gray-500
                                      font: {
                                          size: 10,
                                      },
                                  },
                                  border: {
                                      display: false,
                                  },
                              },
                          }
                        : {
                              x: { display: false },
                              y: { display: false },
                          },
                elements: {
                    line: {
                        tension: 0.3,
                    },
                    bar: {
                        borderRadius: 4,
                    },
                    arc: {
                        borderWidth: 2,
                        borderColor: "#ffffff",
                    },
                },
                ...options,
            },
        });
    }

    onMount(() => {
        createChart();
    });

    afterUpdate(() => {
        createChart();
    });

    onDestroy(() => {
        if (chartInstance) chartInstance.destroy();
    });
</script>

<div class="w-full h-72 relative">
    <canvas bind:this={canvas}></canvas>
</div>

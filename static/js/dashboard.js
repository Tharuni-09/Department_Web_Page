console.log("ERP Dashboard Loaded");

window.addEventListener("DOMContentLoaded", function () {

    // ================= OVERVIEW CHART =================
    const overview = document.getElementById('overviewChart');

    if (overview) {
        new Chart(overview, {
            type: 'bar',
            data: {
                labels: ["Faculty", "Students", "Papers", "Outreach"],
                datasets: [{
                    label: "Total Count",
                    data: [
                        dashboardData.faculty,
                        dashboardData.students,
                        dashboardData.papers,
                        dashboardData.outreach
                    ],
                    backgroundColor: [
                        '#1565C0',
                        '#4CAF50',
                        '#FF9800',
                        '#9C27B0'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });
    }

    // ================= PAPERS CHART =================
    const ctx = document.getElementById('papersChart');

    if (ctx && Array.isArray(papersData)) {

        const labels = papersData.map(p => p.status || "Unknown");
        const values = papersData.map(p => p.count || 0);

        if (labels.length > 0) {
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: [
                            '#4CAF50',
                            '#FFC107',
                            '#F44336',
                            '#2196F3'
                        ]
                    }]
                }
            });
        }
    }

});
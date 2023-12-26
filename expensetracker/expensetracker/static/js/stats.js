const renderChart = (crm_data, labels) => {
  const ctx = document.getElementById("myChart");

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "My First Dataset",
          data: crm_data,
          backgroundColor: [
            "rgb(255, 0, 0)",
            "rgb(54, 162, 235)",
            "rgb(255, 205, 86)",
            "rgb(20, 200, 86)",
          ],
          hoverOffset: 5,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Expenses per category",
      },
      maintainAspectRatio: false,
    },
  });
};

const getChartData = () => {
  fetch("/expenses_category_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log(results, "results");
      const category_data = results.expense_category_data;

      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];

      renderChart(data, labels);
    });
};
document.onload = getChartData();

// {
//     labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
//     datasets: [
//       {
//         label: "# of Votes",
//         data: [12, 19, 3, 5, 2, 3],
//         borderWidth: 1,
//       },
//     ],
//   }

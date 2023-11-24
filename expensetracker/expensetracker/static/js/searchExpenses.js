const searchField = document.querySelector("#searchField");
const appTable = document.querySelector(".app-table");
const NoRes = document.querySelector(".no-res");
const Tbody = document.querySelector(".table-body");

const tableOutputTrue = document.querySelector(".table-output-true");

const paginationContainer = document.querySelector(".pagination-container");

NoRes.style.display = "none";
tableOutputTrue.style.display = "none";

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    Tbody.innerHTML = "";
    fetch("/search_expenses", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        NoRes.style.display = "block";
        appTable.style.display = "none";
        if (data.length === 0) {
          console.log(data.length, "none");
          tableOutputTrue.style.display = "none";
          NoRes.innerHTML = "No results found";
        } else {
          if (data.length >= 1) {
            console.log(data, "something");
            NoRes.style.display = "none";
            tableOutputTrue.style.display = "block";

            data.forEach((item) => {
              Tbody.innerHTML += `
                    <tr>
                    
                    <td>${item.amount}</td>
                    <td>${item.category}</td>
                    <td>${item.desc}</td>
                    <td>${item.date}</td>
                    
                    
                    </tr>
                    `;
            });
          }
        }
      });
  } else {
    tableOutputTrue.style.display = "none";
    appTable.style.display = "block";
    NoRes.style.display = "none";
    paginationContainer.style.display = "block";
  }
});

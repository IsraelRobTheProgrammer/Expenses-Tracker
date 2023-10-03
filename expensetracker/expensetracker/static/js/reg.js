console.log("register works");

const usernameField = document.querySelector("#usernameField");
const feedbackArea = document.querySelector(".invalid-feedback");

usernameField.addEventListener("keyup", (e) => {
  console.log("It works");

  const usernameVal = e.target.value;
  console.log(usernameVal);

  if (usernameVal.length) {
  }

  fetch("/auth/validate_username", {
    body: JSON.stringify({ username: usernameVal }),
    method: "POST",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.user_err) {
        console.log(data.user_err);
        usernameField.classList.add("is-invalid");

        feedbackArea.style.display = "block";
        feedbackArea.innerHTML = `<p>${data.user_err}</p>`;
      } else {
        feedbackArea.style.display = "none";
      }
    });
});

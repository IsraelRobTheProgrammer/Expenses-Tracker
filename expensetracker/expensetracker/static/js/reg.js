const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailFeedbackArea = document.querySelector(".email_invalid_feedback");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");

const showPswdToggle = document.querySelector(".show-password-toggle");

const userSuccess = document.querySelector(".user-success");

const handleToggle = (e) => {
  if (showPswdToggle.textContent === "Show") {
    console.log("in if");

    showPswdToggle.textContent = "Hide";
    passwordField.setAttribute("type", "text");
  } else {
    console.log("in else");

    showPswdToggle.textContent = "Show";
    passwordField.setAttribute("type", "password");
  }
};

showPswdToggle.addEventListener("click", handleToggle);

emailField.addEventListener("keyup", (e) => {
  console.log("11111");
  const emailVal = e.target.value;

  if (emailVal.length > 0) {
    fetch("/auth/validate_email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_err) {
          console.log(data.email_err);
          emailField.classList.add("is-invalid");

          emailFeedbackArea.style.display = "block";
          emailFeedbackArea.innerHTML = `<p>${data.email_err}</p>`;
        } else {
          emailFeedbackArea.style.display = "none";
        }
      });
  }
});

usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
  // console.log(usernameVal);
  userSuccess.textContent = `Checking ${usernameVal}`;
  userSuccess.style.display = "block";

  usernameField.classList.remove("is-invalid");
  feedBackArea.style.display = "none";

  if (usernameVal.length > 0) {
    fetch("/auth/validate_username", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if (data.user_err) {
          console.log(data.user_err);
          userSuccess.style.display = "none";
          usernameField.classList.add("is-invalid");

          feedBackArea.style.display = "block";
          feedBackArea.innerHTML = `<p>${data.user_err}</p>`;
        } else {
          if (!data.user_err) {
            usernameField.classList.remove("is-invalid");
          }
          // feedbackArea.style.display = "none";
        }
      });
  }
});

// usernameField.addEventListener("keyup", (e) => {
//   const usernameVal = e.target.value;

//   usernameSuccessOutput.style.display = "block";

//   usernameSuccessOutput.textContent = `Checking  ${usernameVal}`;

//   usernameField.classList.remove("is-invalid");
//   feedBackArea.style.display = "none";

//   if (usernameVal.length > 0) {
//     fetch("/authentication/validate-username", {
//       body: JSON.stringify({ username: usernameVal }),
//       method: "POST",
//     })
//       .then((res) => res.json())
//       .then((data) => {
//         usernameSuccessOutput.style.display = "none";
//         if (data.username_error) {
//           usernameField.classList.add("is-invalid");
//           feedBackArea.style.display = "block";
//           feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
//           submitBtn.disabled = true;
//         } else {
//           submitBtn.removeAttribute("disabled");
//         }
//       });
//   }
// });

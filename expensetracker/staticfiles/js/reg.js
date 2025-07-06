const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailFeedbackArea = document.querySelector(".email_invalid_feedback");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const passwordField2 = document.querySelector("#passwordField2");

const submitBtn = document.querySelector("#submitBtn");
const showPswdToggle = document.querySelector(".show-password-toggle");

const userSuccess = document.querySelector(".user-success");

const handleToggle = () => {
  if (showPswdToggle.textContent === "Show") {
    showPswdToggle.textContent = "Hide";
    passwordField.setAttribute("type", "text");
    passwordField2.setAttribute("type", "text");
  } else {
    showPswdToggle.textContent = "Show";
    passwordField.setAttribute("type", "password");
    passwordField2.setAttribute("type", "password");
  }
};

showPswdToggle.addEventListener("click", handleToggle);

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  if (emailVal.length > 0) {
    fetch("/auth/validate_email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_err) {
          submitBtn.disabled = true;

          emailField.classList.add("is-invalid");
          emailFeedbackArea.style.display = "block";
          emailFeedbackArea.innerHTML = `<p>${data.email_err}</p>`;
        } else {
          submitBtn.removeAttribute("disabled");
          emailFeedbackArea.style.display = "none";
        }
      });
  }
});

usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
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
        if (data.user_err) {
          console.log(data.user_err);
          userSuccess.style.display = "none";
          usernameField.classList.add("is-invalid");

          submitBtn.disabled = true;
          feedBackArea.style.display = "block";
          feedBackArea.innerHTML = `<p>${data.user_err}</p>`;
        } else {
          usernameField.classList.remove("is-invalid");
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});

function configureRegisterLink() {
  const nextPage = new URLSearchParams(window.location.search).get("next");
  const registerLink = document.getElementById("register-link");

  if (nextPage) {
    registerLink.setAttribute(
      "href",
      registerLink.getAttribute("href") + "?next=" + nextPage
    );
  }
}

function redirectToNextPage() {
  const nextPage = new URLSearchParams(window.location.search).get("next");

  if (nextPage) {
    window.location.href = nextPage;
  } else {
    window.location.href = "/";
  }
}

/**
 *
 * @param {Response} response
 */
async function raiseForBadRequest(response) {
  try {
    content = await response.json();
    error_detail = content.detail;
  } catch (error) {
    error_detail = response.statusText;
  }

  throw new Error(error_detail);
}

/**
 *
 * @param {String} body
 */
async function submitForm(body) {
  const fetchParams = {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: body,
    method: "POST",
  };
  const response = await fetch("/api/token", fetchParams);

  if (!response.ok) {
    await raiseForBadRequest(response);
  }

  const data = await response.json();
  localStorage.setItem("token", data.token);

  redirectToNextPage();
}

/**
 * @param {FormData} formData
 */
async function tryToSubmit(formData) {
  const urlSearchParams = new URLSearchParams();
  Array.from(formData.entries()).forEach((entry) => {
    urlSearchParams.append(entry[0], entry[1]);
  });

  try {
    await submitForm(urlSearchParams.toString());
  } catch (error) {
    console.log(error);
    document.getElementById("form-error").innerText = error;
  }
}

function configureForm() {
  const form = document.getElementById("login-form");
  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const formData = new FormData(form);
    await tryToSubmit(formData);
  });
}

try {
  configureRegisterLink();
  configureForm();
} catch (error) {
  console.error(error);
}

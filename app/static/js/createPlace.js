function checkAuthorization() {
  if (!localStorage.getItem("token")) {
    window.location.href = "/login?next=/create-place";
  }
}

/**
 *
 * @param {Response} response
 */
async function raiseForBadRequest(response) {
  if (response.status === 403) {
    window.location.href = "/login";
  }

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
      Authorization: "Bearer " + localStorage.getItem("token"),
    },
    body: body,
    method: "POST",
  };
  const response = await fetch("/api/places", fetchParams);

  if (!response.ok) {
    await raiseForBadRequest(response);
  }

  window.location.href = "/";
}

/**
 * @param {FormData} formData
 */
async function tryToSubmit(formData) {
  try {
    await submitForm(formData);
  } catch (error) {
    console.log(error);
    document.getElementById("form-error").innerText = error;
  }
}

function configureForm() {
  const form = document.getElementById("place-form");
  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const formData = new FormData(form);
    await tryToSubmit(formData);
  });
}

try {
  checkAuthorization();
  configureForm();
} catch (error) {
  console.error(error);
}

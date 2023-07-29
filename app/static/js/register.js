/**
 * 
 * @param {Response} response 
 */
async function raiseForBadRequest(response){
  try {
    content = await response.json();
    error_detail = content.detail;
  } catch(error){
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
      "Content-Type": "application/json",
    },
    body: body,
    method: "POST",
  };
  const response = await fetch("/api/users/", fetchParams);

  if (!response.ok) {
    await raiseForBadRequest(response);
  }

  window.location.href = "/login";
}

/**
 * @param {FormData} formData
 */
async function tryToSubmit(formData) {
  const formDataObject = {};
  formData.forEach((value, key) => {
    formDataObject[key] = value;
  });
  try {
    await submitForm(JSON.stringify(formDataObject));
  } catch (error) {
    console.log(error);
    document.getElementById("form-error").innerText = error;
  }
}

function configureForm() {
  const form = document.getElementById("register-form");
  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const formData = new FormData(form);
    await tryToSubmit(formData);
  });
}

try {
  configureForm();
} catch (error) {
  console.error(error);
}
